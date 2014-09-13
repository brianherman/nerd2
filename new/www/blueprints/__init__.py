from blueprints import standalone, wiki, server, player

blueprint_packages = [
    standalone,
    wiki,
    server,
    player
]

blueprints = [p.blueprint for p in blueprint_packages]
