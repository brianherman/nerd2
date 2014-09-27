class Source(object):
    pass


import wiki, mumble, irc, mc_ping, top_players, reddit, forums, staff, modreq

source_packages = [
    wiki,
    mumble,
    irc,
    mc_ping,
    top_players,
    reddit,
    forums,
    staff,
    modreq
]

sources = [p.source for p in source_packages]
