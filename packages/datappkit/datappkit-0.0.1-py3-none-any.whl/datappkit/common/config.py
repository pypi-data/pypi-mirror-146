import os


def debug():
    return os.getenv('DATAPP_KIT_DEBUG', 'off') == 'on'


JWT = ""
