from flask import Blueprint, render_template, request, redirect, flash
from models.cache import Cache
from bouncer import MCBouncer
import json
import random
import re

blueprint = Blueprint('standalone', __name__, template_folder='templates')

@blueprint.route('/')
def index():
    return render_template('index.html',
        server_detail = {
            'creative': {
                'address': 'c.nerd.nu',
                'tagline': 'flying enabled, infinite blocks',
                'links': [
                    ('live map', 'http://nerd.nu/maps/creative/live')]},
            'pve': {
                'address': 'p.nerd.nu',
                'tagline': 'survival mode, pvp disabled',
                'links': [
                    ('live map', 'http://nerd.nu/maps/pve/live')
                ]},
            'survival': {
                'address': 's.nerd.nu',
                'tagline': 'survival mode, pvp enabled',
                'links': []
            }
        }
    )

@blueprint.route('/community')
def community():
    ### Forums
    forum_posts = json.loads(Cache.query.filter_by(key='FORUM_POSTS').first().value)

    ### Reddit
    reddit_posts = json.loads(Cache.query.filter_by(key='REDDIT_POSTS').first().value)

    ### Mumble
    mumble_online = Cache.query.filter_by(key='MUMBLE_USERS_CURRENT').first().value
    mumble_max = Cache.query.filter_by(key='MUMBLE_USERS_MAX').first().value

    ### IRC
    irc_online = Cache.query.filter_by(key='IRC_USERS_CURRENT').first().value
    irc_quotes = json.loads(Cache.query.filter_by(key='IRC_QUOTES').first().value)
    irc_quote = random.choice(irc_quotes)

    return render_template('community.html',
        title = 'community',
        forum_posts = forum_posts,
        reddit_posts = reddit_posts,
        mumble_online = mumble_online,
        mumble_max = mumble_max,
        irc_online = irc_online,
        irc_quote = irc_quote
    )

@blueprint.route('/appeal', methods=['GET','POST'])
def appeal():
    mcb = MCBouncer('00459b780f103c14acad1b47f829f235')
    if request.method == 'POST':
        username = request.form['username']
        if re.match('^[0-9A-Za-z_]{1,16}$', username):
            details = mcb.getBans(username, '0', '1000')
            for detail in details['data']:
                if detail['server'] == 'c.nerd.nu':
                    return redirect('https://nerd.nu/forums/index.php?app=forums&module=post&section=post&do=new_post&f=12&title=%s+[%s]' % (detail['username'], detail['issuer']))
            flash('%s is not banned from our servers!' % username)
        else:
            flash('Please enter a valid Minecraft username!')

    return render_template('appeal.html', title='appeal')


@blueprint.route('/staff')
def staff():
    staff_list = json.loads(Cache.query.filter_by(key='STAFF_LIST').first().value)

    return render_template('staff.html', title = 'staff', staff_list = staff_list)
