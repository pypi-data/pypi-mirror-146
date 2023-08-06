#!/usr/bin/env python

"""`shadocs` 测试包。"""


import unittest
from click.testing import CliRunner

from shadocs import shadocs
from shadocs import cli


class TestShadocs(unittest.TestCase):
    """ `shadocs` 测试包。"""

    def setUp(self):
        """设置测试 fixtures，(如果有的话)。"""

    def tearDown(self):
        """拆卸测试 fixtures，（如果有的话）。"""

    def test_000_something(self):
        """测试。"""

    def test_command_line_interface(self):
        """测试CLI。"""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'shadocs.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  显示该消息并退出。' in help_result.output
