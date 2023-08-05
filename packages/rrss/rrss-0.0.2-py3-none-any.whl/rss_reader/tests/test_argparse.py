import argparse
import logging

import pytest

from ..arg_parser import ArgParser


@pytest.fixture
def set_cli_args_options(monkeypatch):
    def mock_parse_args(*args, **kwargs):
        """ Mocks the behaviour cli argument options """

        return argparse.Namespace(source='some source', limit=1, json=True, loglevel=logging.DEBUG)

    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)
    args = ArgParser()
    return args.cli_args


def test_arguments(set_cli_args_options):
    """ Test results of mocked arguments  """

    assert set_cli_args_options.source == 'some source'
    assert set_cli_args_options.limit == 1
    assert set_cli_args_options.json is True
    assert set_cli_args_options.loglevel == logging.DEBUG
