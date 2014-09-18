from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.modreq import Modreq

blueprint = Blueprint('modreq', __name__, template_folder='templates')

@blueprint.route('/modreq', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        args = request.form.to_dict()
        server = args.get('server')
        args.pop('server')
        return redirect(url_for('modreq.modreq', server=server, **args))
    return render_template('modreq_landing.html', title='modreq')

@blueprint.route('/<server>/modreq')
def modreq(server):
    get = lambda k :request.args.get(k, None)

    if server.lower() not in ('creative', 'pve'):
        flash('invalid server')
        return redirect(url_for('modreq.landing'))

    modreqs = Modreq.query
    args = {}
    args['server'] = server

    t = get('status')
    if t in ('all', 'open', 'claimed', 'closed'):
        if t == 'all':
            pass
        else:
            args['status'] = t
    elif t:
        flash('invalid status parameter')
        return redirect(url_for('modreq.landing'))

    modreqs = modreqs.filter_by(**args)

    t = get('sort')
    if t in ('asc', 'desc'):
        if t == 'desc':
            modreqs = modreqs.order_by(Modreq.id.desc())
    elif t:
        flash('invalid sort parameter')
        return redirect(url_for('modreq.landing'))

    t = get('limit')
    if t:
        try:
            t = int(t)
        except:
            flash('invalid limit parameter')
            return redirect(url_for('modreq.landing'))
        modreqs = modreqs.limit(t)

    modreqs = modreqs.all()
    refresh = request.args.get('refresh', 90)

    return render_template('modreq.html',
                           title='modreq :: %s' % server,
                           server=server,
                           requests=modreqs,
                           refresh=refresh)
