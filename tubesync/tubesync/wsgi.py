import os
from urllib.parse import urljoin
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tubesync.settings')
DJANGO_URL_PREFIX = os.getenv('DJANGO_URL_PREFIX', None)
_application = get_wsgi_application()


def application(environ, start_response):
    script_name = None
    if DJANGO_URL_PREFIX:
        if DJANGO_URL_PREFIX.endswith('/'):
            script_name = DJANGO_URL_PREFIX
        else:
            raise Exception(f'DJANGO_URL_PREFIX must end with a /, '
                            f'got: {DJANGO_URL_PREFIX}')
    if script_name:
        static_url = urljoin(script_name, 'static/')
        environ['SCRIPT_NAME'] = script_name
        path_info = environ['PATH_INFO']
        if path_info.startswith(script_name) and not path_info.startswith(static_url):
            environ['PATH_INFO'] = path_info[len(script_name):]
    return _application(environ, start_response)
