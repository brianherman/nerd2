from blueprints import standalone, wiki, server, player, modreq, usage

blueprint_packages = [
    standalone,
    wiki,
    server,
    player,
    modreq,
    usage
]

blueprints = [p.blueprint for p in blueprint_packages]
