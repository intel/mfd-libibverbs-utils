# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for storing fixtures, useful for testing."""

from textwrap import dedent

IBV_DEVINFO_OUT = dedent(
    """\
hca_id: mlx5_0
        transport:                      InfiniBand (0)
        fw_ver:                         16.21.2010
        node_guid:                      506b:4b03:00cc:f69e
        sys_image_guid:                 506b:4b03:00cc:f69e
        vendor_id:                      0x02c9
        vendor_part_id:                 4119
        hw_ver:                         0x0
        board_id:                       MT_0000000011
        phys_port_cnt:                  1
                port:   1
                        state:                  PORT_DOWN (1)
                        max_mtu:                4096 (5)
                        active_mtu:             1024 (3)
                        sm_lid:                 0
                        port_lid:               0
                        port_lmc:               0x00
                        link_layer:             Ethernet

hca_id: cxgb4_0
        transport:                      iWARP (1)
        fw_ver:                         1.23.4.0
        node_guid:                      0007:4347:4200:0000
        sys_image_guid:                 0007:4347:4200:0000
        vendor_id:                      0x1425
        vendor_part_id:                 25608
        hw_ver:                         0x0
        board_id:                       1425.6408
        phys_port_cnt:                  2
                port:   1
                        state:                  PORT_DOWN (1)
                        max_mtu:                4096 (5)
                        active_mtu:             1024 (3)
                        sm_lid:                 0
                        port_lid:               0
                        port_lmc:               0x00
                        link_layer:             Ethernet

                port:   2
                        state:                  PORT_DOWN (1)
                        max_mtu:                4096 (5)
                        active_mtu:             1024 (3)
                        sm_lid:                 0
                        port_lid:               0
                        port_lmc:               0x00
                        link_layer:             Ethernet

"""
)

IBV_DEVINFO_SINGLE_DEV_OUT = dedent(
    """\
hca_id: mlx5_0
        transport:                      InfiniBand (0)
        fw_ver:                         16.21.2010
        node_guid:                      506b:4b03:00cc:f69e
        sys_image_guid:                 506b:4b03:00cc:f69e
        vendor_id:                      0x02c9
        vendor_part_id:                 4119
        hw_ver:                         0x0
        board_id:                       MT_0000000011
        phys_port_cnt:                  1
                port:   1
                        state:                  PORT_DOWN (1)
                        max_mtu:                4096 (5)
                        active_mtu:             1024 (3)
                        sm_lid:                 0
                        port_lid:               0
                        port_lmc:               0x00
                        link_layer:             Ethernet

"""
)

IBV_DEVINFO_SINGLE_PORT_ALL_DEV_OUT = dedent(
    """\
hca_id:	mlx5_0
        transport:			InfiniBand (0)
        fw_ver:				16.21.2010
        node_guid:			506b:4b03:00cc:f69e
        sys_image_guid:			506b:4b03:00cc:f69e
        vendor_id:			0x02c9
        vendor_part_id:			4119
        hw_ver:				0x0
        board_id:			MT_0000000011
        phys_port_cnt:			1
                port:	1
                        state:			PORT_DOWN (1)
                        max_mtu:		4096 (5)
                        active_mtu:		1024 (3)
                        sm_lid:			0
                        port_lid:		0
                        port_lmc:		0x00
                        link_layer:		Ethernet

hca_id:	cxgb4_0
        transport:			iWARP (1)
        fw_ver:				1.23.4.0
        node_guid:			0007:4347:4200:0000
        sys_image_guid:			0007:4347:4200:0000
        vendor_id:			0x1425
        vendor_part_id:			25608
        hw_ver:				0x0
        board_id:			1425.6408
        phys_port_cnt:			2
                port:	1
                        state:			PORT_DOWN (1)
                        max_mtu:		4096 (5)
                        active_mtu:		1024 (3)
                        sm_lid:			0
                        port_lid:		0
                        port_lmc:		0x00
                        link_layer:		Ethernet

"""
)

IBV_DEVINFO_BROKEN = dedent(
    """\
hca_id:	mlx5_0
        transport:			InfiniBand (0)
        fw_ver:				16.21.2010
        node_guid:			506b:4b03:00cc:f69e
        vendor_id:			0x02c9
        vendor_part_id:			4119
        some_broken_field:  EXPLODE
        hw_ver:				0x0
        board_id:			MT_0000000011
        phys_port_cnt:			1
                port:	1
                        state:			PORT_DOWN (1)
                        max_mtu:		4096 (5)
                        active_mtu:		1024 (3)
                        sm_lid:			0
                        port_lid:		0
                        port_lmc:		0x00
                        link_layer:		Ethernet

"""
)
