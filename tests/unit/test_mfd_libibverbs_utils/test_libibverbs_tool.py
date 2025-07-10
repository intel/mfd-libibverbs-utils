# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for test LibibverbsTool."""

import pytest
from mfd_connect import Connection
from mfd_typing import OSName

from mfd_libibverbs_utils.exceptions import LibibverbsToolNotAvailable
from mfd_libibverbs_utils.libibverbs_tool import LibibverbsTool


class TestLibibverbsTool:
    class_under_test = LibibverbsTool

    @pytest.fixture()
    def conn(self, mocker):
        conn = mocker.create_autospec(Connection)
        conn.get_os_name.return_value = OSName.LINUX
        return conn

    @pytest.fixture()
    def libibverbs_initializable_class(self, mocker):
        tool_class = self.class_under_test
        if hasattr(tool_class, "__abstractmethods__"):
            # Remove abstract methods, if any so the class can be instantiated
            tool_class.__abstractmethods__ = []
        tool_class.tool_executable_name = mocker.sentinel.tool_executable_name
        return tool_class

    @pytest.fixture()
    def libibverbs(self, libibverbs_initializable_class, conn, mocker):
        tool = libibverbs_initializable_class(connection=conn)
        tool._tool_exec = mocker.sentinel.tool_exec
        return tool

    def test_class_cannot_be_initialized(self, conn):
        with pytest.raises(AssertionError):
            _ = self.class_under_test(connection=conn)

    def test__get_tool_exec_in_system_path(self, conn, libibverbs_initializable_class):
        tool = libibverbs_initializable_class.__new__(libibverbs_initializable_class)
        tool._connection = conn
        tool._connection.execute_command.return_value.stdout = "/usr/bin/libibverbs_tool\n"
        assert tool._get_tool_exec(tool_path_dir=None) == "/usr/bin/libibverbs_tool"
        tool._connection.execute_command.assert_called_once()

    def test__get_tool_exec_not_found_in_system_path(self, conn, libibverbs_initializable_class):
        tool = libibverbs_initializable_class.__new__(libibverbs_initializable_class)
        tool._connection = conn
        tool._connection.execute_command.side_effect = LibibverbsToolNotAvailable(returncode=1, cmd="")
        with pytest.raises(LibibverbsToolNotAvailable):
            _ = tool._get_tool_exec(tool_path_dir=None)

        tool._connection.execute_command.assert_called_once()

    def test__get_tool_exec_in_custom_path(self, mocker, conn, libibverbs_initializable_class):
        conn.path.return_value = f"{mocker.sentinel.binary_dir}/{mocker.sentinel.tool_executable_name}"
        tool = libibverbs_initializable_class(connection=conn, absolute_path_to_binary_dir=mocker.sentinel.binary_dir)
        assert tool._tool_exec == f"{mocker.sentinel.binary_dir}/{mocker.sentinel.tool_executable_name}"

    def test_check_if_available(self, libibverbs):
        # There should be no exception raised
        libibverbs._connection.execute_command.return_value.return_code = 0
        libibverbs.check_if_available()

    def test_check_if_available_when_tool_not_found(self, libibverbs):
        libibverbs._connection.execute_command.side_effect = LibibverbsToolNotAvailable(returncode=1, cmd="")
        with pytest.raises(LibibverbsToolNotAvailable):
            libibverbs.check_if_available()

    def test_get_version(self, libibverbs):
        assert libibverbs.get_version() == "N/A"
