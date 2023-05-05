from .base import *

DEBUG = False

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'frontend/',
        'STATS_FILE': os.path.join(BASE_DIR, '..', 'frontend', 'webpack-stats-prod.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\\.hot-update.js', '.+\\.map'],
    }
}

# TODO NEEDS TO BE UPDATED
CORS_ALLOWED_ORIGINS = [
    "https://your-production-domain.com",
]
