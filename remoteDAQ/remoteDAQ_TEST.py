import sys
sys.path.append('..')
from influxdb_client import WriteApi, WriteOptions
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import timedelta
import time
from uuid import uuid3, NAMESPACE_DNS
from socket import gethostname
import random
import reactivex as rx
from reactivex import operators as ops
from Automation.BDaq import *
from Automation.BDaq.InstantDiCtrl import InstantDiCtrl
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed

# def on_exit(db_client: InfluxDBClient, write_api: WriteApi):
#     """
#     Close clients after terminate a script.
#     :param db_client: InfluxDB client
#     :param write_api: WriteApi
#     :return: nothing
#     """
#     write_api.close()
#     db_client.close()

def di_daq(devDesc, startPort, portCount):
   """
   Digital input function
   """
   ret = ErrorCode.Success
   instantDiCtrl = InstantDiCtrl(devDesc)
   ret, data = instantDiCtrl.readAny(startPort, portCount)
   retData = {}
   for i in range(startPort, startPort + portCount):
      retData[i] = data[i-startPort]
   instantDiCtrl.dispose()
   
   if BioFailed(ret):
      enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
      print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
   return retData

def ai_daq(devDesc, startPort, portCount):
   """
   Analog input function
   """
   ret = ErrorCode.Success
   instanceAiObj = InstantAiCtrl(devDesc)
   ret, scaledData = instanceAiObj.readDataF64(startPort, portCount)
   retData = {}
   for i in range(startPort, startPort + portCount):
      retData[i] = round(scaledData[i-startPort], 6)
   time.sleep(1)
   instanceAiObj.dispose()

   if BioFailed(ret):
      enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
      print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
   return retData

def line_protocol(measurement_name, channel, value):
    """
    Create an InfluxDB line protocol
    """
    return '{measurement},nodeID={id},channel={ch} value={value}'.format(measurement=measurement_name,
         id=uuid3(NAMESPACE_DNS, gethostname()),
         ch=channel,
         value=value)

# InfluxDB connection config
bucket = "remote-data-acquisition"
org = "UGM"
token = "PXCJT5naU4g1R04-b9U_MtMBFLYkimD4-QZ0GyswJiBwov7MzOMj_ABppwuxvNXIK2HknQnp_qrVYXLfwY2cww=="
url="http://192.168.117.132:8086"

# Data config
interval = 5
num_of_points = 1

# DAQ config
devDesc = "USB-4704,BID#0"
startPort = 0
inputPortCount = 8
outputPortCount = 2

"""
Data aggregator
"""
data = []
for _ in range(num_of_points):
   for channel, value in ai_daq(devDesc, startPort, inputPortCount).items():
      data.append(line_protocol('analogSensor', channel, value))
# data = rx.interval(period=timedelta(seconds=interval)).pipe(ops.map(lambda t: daq()),
#           ops.map(lambda value: line_protocol(value)))

"""
Send data to InfluxDB
"""
# with InfluxDBClient(url=url, token=token, org=org) as client:
#    with client.write_api(write_options=SYNCHRONOUS) as write_api:
#       write_api.write(bucket=bucket, record='\n'.join(data))


print('\n'.join(data))
# input()
