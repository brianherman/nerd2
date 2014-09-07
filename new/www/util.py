from www.app import app

server_names = ['creative', 'survival', 'pve']
server_status = {
    'creative': {
        'numplayers': 9,
        'maxplayers': 150,
        'up': False
    },
    'survival': {
        'numplayers': 27,
        'maxplayers': 150,
        'up': True
    },
    'pve': {
        'numplayers': 166,
        'maxplayers': 200,
        'up': True
    }
}

@app.context_processor
def inject_server():
    return dict(
        server_names=server_names,
        server_status=server_status
    )
