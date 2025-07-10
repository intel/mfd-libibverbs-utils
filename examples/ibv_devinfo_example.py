# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for example usage of IBVDevinfo class."""

import logging

from mfd_connect import RPyCConnection

from mfd_libibverbs_utils import IBVDevinfo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("When tool in $PATH")
conn = RPyCConnection(ip="10.10.10.10")

devinfo = IBVDevinfo(connection=conn)

logger.info("Get info for particular ib device and port")
devices = devinfo.get_info(ib_port=2, ib_device="cxgb4_0")
logger.info(devices)

logger.info("When binary of tool is stored in for ex. /opt/")
devinfo = IBVDevinfo(connection=conn, absolute_path_to_binary_dir="/opt/")
logger.info("Get info for all ib devices and ports")
devices = devinfo.get_info()
logger.info(devices)
