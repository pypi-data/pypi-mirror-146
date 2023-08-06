import os


def debug():
    return os.getenv('DATAPP_KIT_DEBUG', 'off') == 'on'


def set_authorization(jwt):
    os.environ['DATAPP_KIT_AUTHORIZATION'] = jwt


def authorization():
    return os.getenv('DATAPP_KIT_AUTHORIZATION', '')
