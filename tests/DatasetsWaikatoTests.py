# -*- coding: utf-8 -*-
import os
import unittest
from unittest import mock, TestCase

from newzealidar import env_var, datasets_waikato
from . import Base


class DatasetsWaikatoTests(Base, TestCase):
    """Tests the datasets_waikato module."""

    @mock.patch.dict(os.environ, {'DATA_DIR': r'tests/data',
                                  'POSTGRES_PORT': env_var.get_env_variable('POSTGRES_PORT_TEST')})
    def test_datasets(self):
        """
        basic test of datasets_waikato module.
        it will same input dataset information to local database.
        """
        datasets_waikato.run()


if __name__ == '__main__':
    unittest.main()
