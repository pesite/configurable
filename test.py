#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
from Configurable.Configurable import Configurable


class SubConfigurable(Configurable):
    prop = 'test'

    def config_dependent(self):
        return self._config.get('test')


class TestConfigurable(unittest.TestCase):
    def test_configurable_is_singleton(self):
        configured = Configurable()
        configured2 = Configurable()

        self.assertIs(configured, configured2)

    def test_configurable_updates_config(self):
        config = {'a': 5}
        configured = Configurable(config)
        self.assertIs(configured.get_config(), config)
        config = {'b': 5}
        configured2 = Configurable(config)
        self.assertIs(configured2.get_config(), config)

        self.assertEqual(configured.get_config(), {'b': 5})
        configured.set_config({'a': 7})
        self.assertEqual(configured2.get_config(), {'a': 7})

    def test_configurable_keeps_config_non_null(self):
        config = {'a': 5}
        configured = Configurable(config)
        self.assertIs(configured.get_config(), config)
        configured2 = Configurable()
        self.assertIs(configured2.get_config(), config)

    def test_subclassed_configurable_is_different_singleton(self):
        configured = Configurable()
        sub_configured = SubConfigurable()
        sub_configured2 = SubConfigurable()

        self.assertIs(sub_configured, sub_configured2)
        self.assertIsNot(sub_configured, configured)

    def test_subclassed_configurable_keeps_own_properties(self):
        sub_configured = SubConfigurable()
        sub_configured.prop = 'notest'

        self.assertEqual(sub_configured.prop, 'test')

    def test_subclassed_configurable_updates_config(self):
        config = {'a': 5}
        configured = SubConfigurable(config)
        self.assertIs(configured.get_config(), config)
        config = {'b': 5}
        configured2 = SubConfigurable(config)
        self.assertIs(configured2.get_config(), config)

        self.assertEqual(configured.get_config(), {'b': 5})
        configured.set_config({'a': 7})
        self.assertEqual(configured2.get_config(), {'a': 7})

    def test_subclassed_configurable_allows_config_dependent_methods(self):
        config = {'test': 17}
        configured = SubConfigurable(config)

        self.assertEqual(configured.config_dependent(), 17)
        config['test'] = 19
        self.assertEqual(configured.config_dependent(), 19)
        configured.get_config()['test'] = 21
        self.assertEqual(configured.config_dependent(), 21)


if __name__ == '__main__':
    unittest.main()
