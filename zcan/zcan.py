
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Aug 24 2022
@author: jaanisar
"""
import obd
#connection = obd.OBD()
connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="9600", fast=False, timeout = 30)
#connection = obd.Async("/dev/ttyUSB0", protocol="6", baudrate="9600", fast=False, timeout = 30)

c = obd.commands.RPM
response = connection.query(c)
print(response.value)
connection.close