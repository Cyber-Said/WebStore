from .base import *
import socket

DEBUG = True


def _database_host() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    if host != "db":
        return host

    # If Django runs on the host OS, Docker service DNS name "db" is not resolvable.
    try:
        socket.gethostbyname(host)
        return host
    except socket.gaierror:
        return "localhost"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': _database_host(),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}
