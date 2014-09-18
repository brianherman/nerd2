from blueprints import standalone, wiki, server, player, modreq

blueprint_packages = [
    standalone,
    wiki,
    server,
    player,
    modreq
]

blueprints = [p.blueprint for p in blueprint_packages]
