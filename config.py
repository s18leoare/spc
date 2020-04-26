from os import environ


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY') or 'youll-never-guess-it'
