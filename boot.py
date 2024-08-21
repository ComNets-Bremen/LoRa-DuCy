#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

from machine import UART
import machine
import os
import ustruct, ubinascii, uhashlib

uart = UART(0, baudrate=115200)
os.dupterm(uart)

# machine.main('main.py')



'''
Implemented of LoPy4/Fipy with 1.18 pycom-micropython version
'''
######### Utility Functions #######################
def get_node_id(hex=False):
    """
    Get node id, which consists of four bytes unsigned int.
    Return as hex, according to parameter.
    """
    node_id = ubinascii.hexlify(uhashlib.sha1(
        machine.unique_id()).digest()).decode("utf-8")[-8:]
    if hex:
        return node_id
    else:
        return int(node_id, 16)

######### Own node's information #####################
if get_node_id() == 718333200:
# if get_node_id() == 235968217:   ### sp2
# if get_node_id() == 3253554266:
    print('I am node Mac1')
elif get_node_id() == 1407508338:
# elif get_node_id() == 1883124616:
    print('I am node Mac2')
elif get_node_id() == 50989579:
    print('I am node Mac3')
