from flask import Blueprint, render_template, current_app
from models.cache import Cache
import json
import random

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
        forum_posts = forum_posts,
        reddit_posts = reddit_posts,
        mumble_online = mumble_online,
        mumble_max = mumble_max,
        irc_online = irc_online,
        irc_quote = irc_quote
    )

@blueprint.route('/appeal')
def appeal():
    return None #TODO

@blueprint.route('/staff')
def staff():
    return None #TODO
