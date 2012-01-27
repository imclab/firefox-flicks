import os
import site

os.environ['CELERY_LOADER'] = 'django'

# Add the app dir to the python path so we can import manage.
wsgidir = os.path.dirname(__file__)
site.addsitedir(os.path.abspath(os.path.join(wsgidir, '../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'flicks.settings'

# manage adds /apps, /lib, and /vendor to the Python path.
import manage

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Uncomment this to figure out what's going on with the mod_wsgi environment.
#def application(env, start_response):
#    start_response('200 OK', [('Content-Type', 'text/plain')])
#    return '\n'.join('%r: %r' % item for item in sorted(env.items()))

# vim: ft=python
