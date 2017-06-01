# -*- coding: utf-8 -*-


class Configurable(object):
    '''
    A container for configuration.
    All subclasses of this are singleton and should only contain a config
    or some fixed class-specific fields.
    '''

    class __Configurable(object):
        '''
        '''
        _config = {}

        def __init__(self, config):
            if config is not None:
                self.set_config(config)

        def __str__(self):
            return repr(self) + repr(self._config)

        def set_config(self, config):
            self._config = config

        def get_config(self):
            return self._config

    __instance = {}
    _rinstances = {}

    def __new__(class_, config=None):
        n = str(class_)
        if not Configurable._rinstances.get(n):
            Configurable._rinstances[n] = object.__new__(class_)
        elif config is not None:
            Configurable._rinstances[n]._config = config
        return Configurable._rinstances[n]

    def __init__(self, config=None):
        if self.__instance.get(0) is None:
            self.__instance[0] = self.__class__.__Configurable(config or {})
        elif config is not None:
            self.__instance[0].set_config(config)

    def __repr__(self):
        return self.__instance[0].__repr__()

    def __getattr__(self, name):
        return getattr(self.__instance[0], name)

    def __setattr__(self, key, value):
        pass
