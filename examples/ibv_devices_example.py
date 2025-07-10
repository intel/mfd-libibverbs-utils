# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for example usage of IBVDevices class."""

from dataclasses import asdict, astuple

from mfd_connect import RPyCConnection

from mfd_libibverbs_utils import IBVDevices

# When tool in $PATH
conn = RPyCConnection(ip="10.10.10.10")
ibv_dev = IBVDevices(connection=conn)
devices = ibv_dev.get_list()
print(devices)

# When binary of tool is stored in for ex. /opt/
conn = RPyCConnection(ip="10.10.10.11")
ibv_dev = IBVDevices(connection=conn, absolute_path_to_binary_dir="/opt/")
devices = ibv_dev.get_list()
print(devices)

# Take advantage of dataclass features
for dev in devices:
    print("Transform dev object to dictionary.")
    dev_dict = asdict(dev)
    print(dev_dict)
    print("Transform dev object to tuple.")
    dev_tuple = astuple(dev)
    print(dev_tuple)
