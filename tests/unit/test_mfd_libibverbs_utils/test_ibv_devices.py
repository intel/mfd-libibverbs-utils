# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for test ibv_devices."""

from textwrap import dedent

import pytest
from mfd_connect import Connection
from mfd_typing import OSName

from mfd_libibverbs_utils import IBVDevices
from mfd_libibverbs_utils.exceptions import IBVDevicesException
from mfd_libibverbs_utils.ibv_devices import IBDevice


class TestIBVDevices:
    @pytest.fixture
    def ibv_dev(self, mocker):
        mocker.patch(
            "mfd_libibverbs_utils.ibv_devices.IBVDevices.check_if_available",
            mocker.create_autospec(IBVDevices.check_if_available),
        )
        mocker.patch(
            "mfd_libibverbs_utils.ibv_devices.IBVDevices.get_version",
            mocker.create_autospec(IBVDevices.get_version, return_value="0.0.1"),
        )
        mocker.patch(
            "mfd_libibverbs_utils.ibv_devices.IBVDevices._get_tool_exec_factory",
            mocker.create_autospec(IBVDevices._get_tool_exec_factory, return_value="ibv_devices"),
        )
        conn = mocker.create_autospec(Connection)
        conn.get_os_name.return_value = OSName.LINUX

        ibvdevice = IBVDevices(connection=conn)
        mocker.stopall()
        return ibvdevice

    def test_list(self, ibv_dev):
        expected_result = [
            IBDevice(device="mlx5_0", node_guid="506b4b0300ccf69e"),
            IBDevice(device="cxgb4_0", node_guid="0007434742000000"),
        ]
        ibv_dev._connection.execute_command.return_value.stdout = dedent(
            """
            device                 node GUID
            ------              ----------------
            mlx5_0              506b4b0300ccf69e
            cxgb4_0             0007434742000000
        """
        )
        ibv_dev._connection.execute_command.return_value.return_code = 0
        assert ibv_dev.get_list() == expected_result

    def test_list_when_no_devices(self, ibv_dev):
        expected_result = []
        ibv_dev._connection.execute_command.return_value.stdout = dedent(
            """
                    device                 node GUID
                    ------              ----------------
                """
        )
        ibv_dev._connection.execute_command.return_value.return_code = 0
        assert ibv_dev.get_list() == expected_result

    def test_list_when_cmd_fails(self, ibv_dev):
        ibv_dev._connection.execute_command.side_effect = IBVDevicesException(cmd="", returncode=1)
        with pytest.raises(IBVDevicesException):
            _ = ibv_dev.get_list()
