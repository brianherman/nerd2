from flask.ext.assets import Environment, Bundle
from webassets.filter import get_filter

def init_assets(application):
    assets = Environment(application)
    assets.config['SASS_BIN'] = "/usr/local/bin/sass"
    assets.load_path = ["assets/"]
    assets.url = "/static"

    css_main = Bundle('sass/app.scss',
                      filters=('scss,cssmin'),
                      depends=('sass/*.scss', 'sass/**/*.scss', 'sass/**/**/*.scss'),
                      output='css/gen/app.%(version)s.css')
    assets.register('css_main', css_main)

    js_base = Bundle('js/vendor/excanvas.js',
                     'js/vendor/jquery-1.11.1.js',
                     'js/vendor/jquery.minecraftskin.js')
    js_main = Bundle(js_base,
                     filters='rjsmin',
                     output='js/gen/app.%(version)s.js')
    assets.register('js_main', js_main)
