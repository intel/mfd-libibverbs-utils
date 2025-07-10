# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for test ibv_devinfo."""

import pytest
from mfd_connect import Connection

from mfd_typing import OSName
from mfd_libibverbs_utils import IBVDevinfo
from mfd_libibverbs_utils.exceptions import IBVDevinfoException, ParsingError
from mfd_libibverbs_utils.ibv_devices import IBDevice
from mfd_libibverbs_utils.ibv_devinfo import IBDeviceInfo, IBDevPhysicalPort
from tests.helpers.fixtures import (
    IBV_DEVINFO_OUT,
    IBV_DEVINFO_SINGLE_DEV_OUT,
    IBV_DEVINFO_SINGLE_PORT_ALL_DEV_OUT,
    IBV_DEVINFO_BROKEN,
)


class TestIBVDevinfo:
    @pytest.fixture
    def devinfo(self, mocker):
        mocker.patch(
            "mfd_libibverbs_utils.ibv_devinfo.IBVDevinfo.check_if_available",
            mocker.create_autospec(IBVDevinfo.check_if_available),
        )
        mocker.patch(
            "mfd_libibverbs_utils.ibv_devinfo.IBVDevinfo.get_version",
            mocker.create_autospec(IBVDevinfo.get_version, return_value="0.0.1"),
        )
        mocker.patch(
            "mfd_libibverbs_utils.ibv_devinfo.IBVDevinfo._get_tool_exec_factory",
            mocker.create_autospec(IBVDevinfo._get_tool_exec_factory, return_value="ibv_devinfo"),
        )
        conn = mocker.create_autospec(Connection)
        conn.get_os_name.return_value = OSName.LINUX

        devinfo = IBVDevinfo(connection=conn)
        devinfo._tool_exec = "/usr/bin/ibv_devinfo"
        mocker.stopall()
        return devinfo

    def test_get_info_for_all_devices(self, devinfo):
        expected_result = [
            IBDeviceInfo(
                name="mlx5_0",
                transport="InfiniBand (0)",
                fw_ver="16.21.2010",
                node_guid="506b:4b03:00cc:f69e",
                sys_image_guid="506b:4b03:00cc:f69e",
                vendor_id="0x02c9",
                vendor_part_id="4119",
                hw_ver="0x0",
                board_id="MT_0000000011",
                phys_port_cnt=1,
                physical_ports=[
                    IBDevPhysicalPort(
                        number=1,
                        state="PORT_DOWN (1)",
                        max_mtu=4096,
                        active_mtu=1024,
                        sm_lid=0,
                        port_lid=0,
                        port_lmc="0x00",
                        link_layer="Ethernet",
                    )
                ],
            ),
            IBDeviceInfo(
                name="cxgb4_0",
                transport="iWARP (1)",
                fw_ver="1.23.4.0",
                node_guid="0007:4347:4200:0000",
                sys_image_guid="0007:4347:4200:0000",
                vendor_id="0x1425",
                vendor_part_id="25608",
                hw_ver="0x0",
                board_id="1425.6408",
                phys_port_cnt=2,
                physical_ports=[
                    IBDevPhysicalPort(
                        number=1,
                        state="PORT_DOWN (1)",
                        max_mtu=4096,
                        active_mtu=1024,
                        sm_lid=0,
                        port_lid=0,
                        port_lmc="0x00",
                        link_layer="Ethernet",
                    ),
                    IBDevPhysicalPort(
                        number=2,
                        state="PORT_DOWN (1)",
                        max_mtu=4096,
                        active_mtu=1024,
                        sm_lid=0,
                        port_lid=0,
                        port_lmc="0x00",
                        link_layer="Ethernet",
                    ),
                ],
            ),
        ]
        devinfo._connection.execute_command.return_value.stdout = IBV_DEVINFO_OUT
        assert devinfo.get_info() == expected_result

    @pytest.mark.parametrize("ib_device", [IBDevice(device="mlx5_0", node_guid="506b4b0300ccf69e"), "mlx5_0"])
    def test_get_info_for_single_ib_device(self, devinfo, ib_device):
        expected_result = [
            IBDeviceInfo(
                name="mlx5_0",
                transport="InfiniBand (0)",
                fw_ver="16.21.2010",
                node_guid="506b:4b03:00cc:f69e",
                sys_image_guid="506b:4b03:00cc:f69e",
                vendor_id="0x02c9",
                vendor_part_id="4119",
                hw_ver="0x0",
                board_id="MT_0000000011",
                phys_port_cnt=1,
                physical_ports=[
                    IBDevPhysicalPort(
                        number=1,
                        state="PORT_DOWN (1)",
                        max_mtu=4096,
                        active_mtu=1024,
                        sm_lid=0,
                        port_lid=0,
                        port_lmc="0x00",
                        link_layer="Ethernet",
                    )
                ],
            )
        ]
        devinfo._connection.execute_command.return_value.stdout = IBV_DEVINFO_SINGLE_DEV_OUT
        if isinstance(ib_device, IBDevice):
            ib_dev = ib_device.device
        else:
            ib_dev = ib_device
        cmd = f"{devinfo._tool_exec} -d {ib_dev}"

        assert devinfo.get_info(ib_device=ib_device) == expected_result
        devinfo._connection.execute_command.assert_called_with(
            cmd, custom_exception=IBVDevinfoException, expected_return_codes={0, 255}
        )

    def test_get_info_for_defined_ports_and_all_devices(self, devinfo):
        expected_result = [
            IBDeviceInfo(
                name="mlx5_0",
                transport="InfiniBand (0)",
                fw_ver="16.21.2010",
                node_guid="506b:4b03:00cc:f69e",
                sys_image_guid="506b:4b03:00cc:f69e",
                vendor_id="0x02c9",
                vendor_part_id="4119",
                hw_ver="0x0",
                board_id="MT_0000000011",
                phys_port_cnt=1,
                physical_ports=[
                    IBDevPhysicalPort(
                        number=1,
                        state="PORT_DOWN (1)",
                        max_mtu=4096,
                        active_mtu=1024,
                        sm_lid=0,
                        port_lid=0,
                        port_lmc="0x00",
                        link_layer="Ethernet",
                    )
                ],
            ),
            IBDeviceInfo(
                name="cxgb4_0",
                transport="iWARP (1)",
                fw_ver="1.23.4.0",
                node_guid="0007:4347:4200:0000",
                sys_image_guid="0007:4347:4200:0000",
                vendor_id="0x1425",
                vendor_part_id="25608",
                hw_ver="0x0",
                board_id="1425.6408",
                phys_port_cnt=2,
                physical_ports=[
                    IBDevPhysicalPort(
                        number=1,
                        state="PORT_DOWN (1)",
                        max_mtu=4096,
                        active_mtu=1024,
                        sm_lid=0,
                        port_lid=0,
                        port_lmc="0x00",
                        link_layer="Ethernet",
                    )
                ],
            ),
        ]
        devinfo._connection.execute_command.return_value.stdout = IBV_DEVINFO_SINGLE_PORT_ALL_DEV_OUT
        port_number = 1
        cmd = f"{devinfo._tool_exec} -i {port_number}"

        assert devinfo.get_info(ib_port=port_number) == expected_result
        devinfo._connection.execute_command.assert_called_with(
            cmd, custom_exception=IBVDevinfoException, expected_return_codes={0, 255}
        )

    @pytest.mark.parametrize("ib_device", [IBDevice(device="mlx5_0", node_guid="506b4b0300ccf69e"), "mlx5_0"])
    def test_get_info_for_defined_port_and_defined_device(self, devinfo, ib_device):
        expected_result = [
            IBDeviceInfo(
                name="mlx5_0",
                transport="InfiniBand (0)",
                fw_ver="16.21.2010",
                node_guid="506b:4b03:00cc:f69e",
                sys_image_guid="506b:4b03:00cc:f69e",
                vendor_id="0x02c9",
                vendor_part_id="4119",
                hw_ver="0x0",
                board_id="MT_0000000011",
                phys_port_cnt=1,
                physical_ports=[
                    IBDevPhysicalPort(
                        number=1,
                        state="PORT_DOWN (1)",
                        max_mtu=4096,
                        active_mtu=1024,
                        sm_lid=0,
                        port_lid=0,
                        port_lmc="0x00",
                        link_layer="Ethernet",
                    )
                ],
            )
        ]
        ib_port = 1
        devinfo._connection.execute_command.return_value.stdout = IBV_DEVINFO_SINGLE_DEV_OUT
        if isinstance(ib_device, IBDevice):
            ib_dev = ib_device.device
        else:
            ib_dev = ib_device
        cmd = f"{devinfo._tool_exec} -d {ib_dev} -i {ib_port}"

        assert devinfo.get_info(ib_device=ib_device, ib_port=ib_port) == expected_result
        devinfo._connection.execute_command.assert_called_with(
            cmd, custom_exception=IBVDevinfoException, expected_return_codes={0, 255}
        )

    def test_get_info_when_no_ib_devices(self, devinfo):
        devinfo._connection.execute_command.return_value.return_code = 255
        assert devinfo.get_info() == []

    def test_get_info_when_cmd_fails(self, devinfo):
        devinfo._connection.execute_command.side_effect = IBVDevinfoException(returncode=1, cmd="")
        with pytest.raises(IBVDevinfoException):
            _ = devinfo.get_info()

    def test_get_info_when_parsing_error_ib_device_data(self, devinfo):
        devinfo._connection.execute_command.return_value.stdout = IBV_DEVINFO_BROKEN
        with pytest.raises(ParsingError):
            _ = devinfo.get_info()
