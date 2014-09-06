from nerdnu import app, bouncer, modreq as modrequest
from flask import Flask, request, redirect, url_for, g, jsonify, session
from flask import render_template, flash, send_file, abort
import json
import glob
import os
import sys
import re
import requests
try:
   from PIL import Image
except:
   import Image
from urllib import urlopen
from StringIO import StringIO
import sqlite3

mcb = bouncer.MCBouncer(app.config['BOUNCER_KEY'])

addr = {'creative': 'c.nerd.nu', 'survival': 's.nerd.nu', 'pve': 'p.nerd.nu'}
req_dbs = {'creative': 'C_MODREQ_DB', 'survival': 'S_MODREQ_DB', 'pve': 'P_MODREQ_DB'}

def load_json(fname):
    f = open('nerdnu/data/%s' % fname, 'r')
    o = json.load(f)
    f.close()
    return o

def load_html(fname):
    f = open('nerdnu/data/%s' % fname, 'r')
    o = f.read()
    f.close()
    return o

def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

def get_staff():
    out = {}
    for fname in glob.glob(os.path.join(app.config['HOME_DIR'], 'permissions/users/*.txt')):
        with open(fname) as handle:
            out[os.path.basename(fname)[:-4]] = map(lambda a: a.strip(), handle.readlines())

def query_db(query, db='DATABASE', args=(), one=False):
    try:
        g.db = sqlite3.connect(app.config[db])
        cur = g.db.execute(query, args)
    except:
        abort(500)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

default_options = lambda: dict(statuses = load_json('statuses.json'))


#def render_helper(*args, **kwargs):
#    kwargs['statuses'] = query_db('SELECT 
    

@app.route('/')
def index():
    return render_template('index.html', 
        statuses=load_json('statuses.json'), 
        addr = addr,
        taglines = {
            'creative': 'flying enabled, infinite blocks', 
            'survival': 'survival mode, pvp enabled', 
            'pve':      'survival mode, pvp disabled'},
        cartos = dict([(i, 'http://redditpublic.com/carto/%s/current/index.html' % i) for i in ('creative', 'pve')])
    )

#def render_server(data):
#    

@app.route('/<server>/')
def server(server):
    server = server.lower()
    if server not in ['creative', 'survival', 'pve']:
        abort(404)
    statuses = load_json('statuses.json')
    current_rev = load_json('current_rev.json')[server]
 
    
    options = {
        'title': server,
        'statuses': statuses,
        'addr': addr,
        'description': load_html('info-%s.html' % server),
        'status': statuses[server],
        'subreddit': load_json('subreddit.json')[server][:10],
        'github': filter(lambda a: server in a['tags'], load_json('github.json'))[:10],
        'current_rev': current_rev,
        'top_players': load_json('top_players.json')[server][:20]}
    
    if server == 'survival':
        del options['status']['players']
    return render_template('server.html', **options)

@app.route('/appeal/', methods=['GET', 'POST'])
def appeal():
    if request.method == 'POST':
        username = request.form['username']
        if re.match('^[0-9A-Za-z_]{1,16}$', username):
            details = mcb.getBanDetails(username)
            if details['is_banned']:
                return redirect('http://nerd.nu/forum/index.php?p=/post/discussion/4&appeal&username=%s&admin=%s' % (details['user'], details['issuer']))
            else:
                flash('%s is not banned from our servers!' % username)
        else:
            flash('Please enter a valid minecraft username!')
    
    return render_template('appeal.html', title='Appeal a ban', statuses=load_json('statuses.json'))

@app.route('/staff/')
def staff():
    options = {
        'title': 'Staff',
        'statuses': load_json('statuses.json')}
    for fname in glob.glob(os.path.join(app.config['HOME_DIR'], 'permissions/users/*.txt')):
        with open(fname) as handle:
            options[os.path.basename(fname)[:-4]] = map(lambda a: a.strip(), handle.readlines())
    
    return render_template('staff.html', **options)

@app.route('/rules/')
def rules():
    options = {
        'title': 'Rules',
        'body': load_html('rules.html'),
        'statuses': load_json('statuses.json')}
    
    return render_template('wikipage.html', **options)

@app.route('/skin/<username>.png')
def skin(username):
    r = requests.get('http://s3.amazonaws.com/MinecraftSkins/%s.png' % username)
    print r.status_code
    if r.status_code==200:
        return send_file(StringIO(r.content), mimetype='image/png')
    else:
        return send_file('data/char.png', mimetype='image/png')

@app.route('/avatar/<username>-<int:mode>.png')
def avatar(username, mode):
    staticpath = 'nerdnu/static/avatars/%s-%d.png' % (username, mode)
    if not os.path.exists(staticpath):
        size = {1:96, 2:48}.get(mode, 1)
        try:
            im = Image.open(StringIO(urlopen("http://s3.amazonaws.com/MinecraftSkins/" + username + ".png").read()))
        except Exception:
            im = Image.open("nerdnu/static/img/default-skin.png")

        box = (8,8,16,16,)
        region = im.crop(box)
        region = region.resize((size,size), Image.NEAREST)
        region.save(staticpath, 'PNG')
    
    return redirect(url_for('static', filename='avatars/%s-%d.png' % (username, mode)))

@app.route('/player/<username>/')
def player(username):
    m = re.match('^[0-9A-Za-z_]{1,16}$', username)
    if m:
        options = {
            'title': username,
            'statuses': load_json('statuses.json'),
            'username': username,
        }
        return render_template('player.html', **options)
    else:
        abort(404)

@app.route('/modreq/')
def modreq_landing():
    return render_template('modreq_landing.html', title = 'Mod Requests', statuses = load_json('statuses.json'))

@app.route('/modreq/<server>/')
def modreq(server):
    get = lambda k: request.args.get(k, None)

    options = {
        'title': 'Mod Requests',
        'statuses': load_json('statuses.json')}

    #Check server makes sense
    if server.lower() not in ('creative', 'survival', 'pve'):
        redirect(url_for('modreq_landing'))
    
    #Query DB
    db = database.ModreqDB(server)
    args = {}
    
    t = get('status')
    if t in ('all', 'open', 'claimed', 'closed'):
        args['status'] = t
    
    t = get('limit')
    if t:
        try:
            t = int(t)
        except:
            flash('limit param doesn\'t make sense')
            abort(404)
        args['limit'] = t
    
    t = get('sort')
    if t in ('asc', 'desc'):
        args['sort'] = t
    
    
    modreqs = db.getModreqs(**args)
    
    if not modreqs:
        flash('Something went wrong!')
        abort(404)
    
    
    #Format data
    data = []
    statuses = {
        0: 'Closed',
        1: 'Claimed',
        2: 'Open'}
    for row in modreqs:
        row['status'] = statuses[row['status']]
        if server == 'survival':
            del(req['request_location'])
    
    #Return in JSON if needed  
    if get('format') == 'json':
        return jsonify(requests=modreqs, amount=len(modreqs))
    
    #Otherwise render for web
    options['requests'] = modreqs
    options['refresh'] = request.args.get('refresh', 90)
    
    return render_template('modreq.html', **options)

@app.route('/ajax/modreq')
def modreqData():
    server = request.args.get('server', None)
    if server == None or server not in ['creative', 'survival', 'pve']:
        abort(400)
    reqs = query_db('SELECT * from modreq_requests', req_dbs[server])
    modreqs = modrequest.graph(reqs)
    return jsonify(modreqs)
    





@app.route('/signup/')
def signup():
    pass








@app.errorhandler(404)
@app.errorhandler(500)
def error(error):
    #print dir(error)
    options = {
        'title': 'Oh no! %s' % error.message,
        'statuses': load_json('statuses.json'),
        'error': error,
    }
    return render_template('error.html', **options), error.code
