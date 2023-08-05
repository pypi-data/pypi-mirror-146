import os

import dotenv


class DotEnv(dict):
    def __init__(self, default=None, dotenv_filename=None):
        dict.__init__(default or {})

        dotenv.load_dotenv(dotenv_filename)

    def __getattr__(self, key):
        if key.isupper() and not key.startswith('_'):
            return os.getenv(key)

        return self.__dict__.get(key)

    def __getitem__(self, key):
        if key.isupper() and not key.startswith('_'):
            return os.getenv(key)

        return dict.__getitem__(self, key)

    def get(self, key, default=None):
        if key.isupper() and not key.startswith('_'):
            return os.getenv(key, default)

        return dict.get(self, key, default)
