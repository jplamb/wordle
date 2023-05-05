from .base import *

DEBUG = True

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'frontend/',
        'STATS_FILE': os.path.join(BASE_DIR, '..', 'frontend', 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\\.hot-update.js', '.+\\.map'],
    }
}
WEBPACK_DEV_SERVER_URL = 'http://localhost:8080/'

CORS_ALLOW_ALL_ORIGINS = True

APPLICATION_TOKEN = os.environ.get('APPLICATION_TOKEN')

