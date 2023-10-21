import socket

from .base import *

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
]

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
    "127.0.0.1",
    "10.0.2.2",
]

INSTALLED_APPS += ["debug_toolbar"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "expense_mailbox"
EMAIL_PORT = 1025

SESSION_ENGINE = "django.contrib.sessions.backends.db"
