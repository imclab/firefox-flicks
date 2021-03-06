# This file contains settings that apply only while the test suite is running.
# If the setting value is important to your test, mock it instead of using this.

SITE_URL = 'http://test.com'

VIDLY_USER_ID = '1234'
VIDLY_USER_KEY = 'asdf'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

NOTIFY_KEY = 'asdf'

PROD_LANGUAGES = ('en-US', 'fr', 'es', 'de', 'pt-BR')
