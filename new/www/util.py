from flask import render_template

def render_with_header(template_name, **kwargs):
    kwargs['server_names'] = ['creative', 'survival', 'pve']
    kwargs['server_status'] = {
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

    return render_template(template_name, **kwargs)