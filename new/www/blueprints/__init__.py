from www.blueprints import standalone, wiki, server, api

blueprint_packages = [
    standalone,
    wiki,
    server
]

blueprints = [p.blueprint for p in blueprint_packages]
