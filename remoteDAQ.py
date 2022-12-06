import sys
sys.path.append('..')
import logging
from logging.handlers import TimedRotatingFileHandler
from uuid import uuid3, NAMESPACE_DNS
from socket import gethostname
from influxdb_client import WriteOptions
from influxdb_client.client.influxdb_client import InfluxDBClient
from Automation.BDaq import *
from Automation.BDaq.InstantDiCtrl import InstantDiCtrl
from Automation.BDaq.InstantDoCtrl import InstantDoCtrl
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.InstantAoCtrl import InstantAoCtrl
import json
from multiprocessing import Pool
import asyncio
from fastapi import FastAPI, Body, Header
import requests

# InfluxDB connection Config
bucket = 'remote-data-acquisition' # CHANGE THIS
org = 'UGM' # CHANGE THIS
token = 'PXCJT5naU4g1R04-b9U_MtMBFLYkimD4-QZ0GyswJiBwov7MzOMj_ABppwuxvNXIK2HknQnp_qrVYXLfwY2cww=='  # CHANGE THIS
url='http://192.168.117.132:8086' # CHANGE THIS
send_to_db = False

# Data Config
dev_id = str(uuid3(NAMESPACE_DNS, gethostname()))

# DAQ Config
devDesc = 'USB-4704,BID#0' # CHANGE THIS
devFunc = {'funcMode':3, 'ports':[_ for _ in range(0, 8)], 'data':0} # DEFAULT BEHAVIOR
portList = [_ for _ in range(0,8)]

# Log Config
FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')
LOG_FILE = 'remoteDAQ.log'

'''Log Function'''
def get_file_handler():
   '''
   Log File Handler
   '''
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_logger(logger_name):
   '''
   Main Log Handler
   '''
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG)
   logger.addHandler(get_file_handler())
   logger.propagate = False
   return logger

my_logger = get_logger('remoteDAQ')

'''DAQ Function'''
async def di_daq(devDesc, portList, logger=my_logger):
   '''
   Function to Read Digital Input Signal
   '''
   logger.info('### Starting reading digital input data ###')
   measurement_name = 'digitalInput'
   result = []
   try:
      instantDiCtrl = InstantDiCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
   else:
      for i in portList:
         tmp = {}
         _, data = instantDiCtrl.readBit(0, i)
         logger.info('Successfully read digital input port #' + str(i))
         tmp['measurement_name'] = measurement_name
         tmp['port'] = i
         tmp['data'] = data
         result.append(tmp)
      logger.info('### Finished reading digital input data ###')
      instantDiCtrl.dispose()
      return result
   
async def do_daq(devDesc, data, logger=my_logger):
   '''
   Function to Write Digital Output Signal
   '''
   logger.info('### Starting writing digital output data ###')
   try:
      instantDoCtrl = InstantDoCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
   else:
      for i in range(len(data)):
         _ = instantDoCtrl.writeAny(i, 1, [data[i]])
         logger.info('Successfully write digital output port #' + str(i))
      logger.info('### Finished writing digital output data ###')
      instantDoCtrl.dispose()
      return 0

async def doi_daq(devDesc, portList, logger=my_logger):
   '''
   Function to Read Digital Output Signal
   '''
   logger.info('### Starting reading digital output data ###')
   measurement_name = 'digitalOutputValue'
   result = []
   try:
      instantDoCtrl = InstantDoCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
   else:
      for i in portList:
         tmp = {}
         _, data = instantDoCtrl.readBit(0, i)
         logger.info('Successfully read digital output port #' + str(i))
         tmp['measurement_name'] = measurement_name
         tmp['port'] = i
         tmp['data'] = data
         result.append(tmp)
      logger.info('### Finished reading digital output data ###')
      instantDoCtrl.dispose()
      return result

async def ai_daq(devDesc, portList, decimalPrecision=2, logger=my_logger):
   '''
   Function to Read Analog Input Signal
   '''
   logger.info('### Starting reading analog input data ###')
   measurement_name = 'analogInput'
   result = []
   try:
      instanceAiObj = InstantAiCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
   else:
      for i in portList:
         tmp = {}
         _, scaledData = instanceAiObj.readDataF64(i, 1)
         logger.info('Successfully read analog input port #' + str(i))
         tmp['measurement_name'] = measurement_name
         tmp['port'] = i
         tmp['data'] = round(scaledData[0], decimalPrecision)
         result.append(tmp)
      logger.info('### Finished reading analog input data ###')
      instanceAiObj.dispose()
      return result

async def ao_daq(devDesc, portList, data=[0, 0], logger=my_logger):
   '''
   Function to Write Analog Output Signal
   '''
   logger.info('### Starting writing analog output data ###')
   try:
      instantAoCtrl = InstantAoCtrl(devDesc)
   except ValueError as e:
      logger.error(e)
   else:
      for i in portList:
         _ = instantAoCtrl.writeAny(i, 1, None, [data[i]])
         logger.info('Successfully write analog output port #' + str(i))
      logger.info('### Finished writing analog output data ###')
      instantAoCtrl.dispose()
      return 0
      
'''INFLUXDB Funcion'''
def line_protocol(measurement_name, port, value, id):
   '''
   Create an InfluxDB Dictionary
   '''
   return '{measurement},nodeID={id},port={port} value={val}'.format(measurement=measurement_name,
      id=id,
      port=port,
      val=value)

def send_to_influxdb(url, token, org, bucket, data):
   '''
   Send Data to InfluxDB
   '''
   with InfluxDBClient(url, token, org) as client:
      with client.write_api(write_options=WriteOptions(batch_size=1,
                                                      flush_interval=10_000,
                                                      jitter_interval=2_000,
                                                      retry_interval=1_000,
                                                      max_retries=3,
                                                      max_retry_delay=10_000,
                                                      exponential_base=2)) as write_client:
         
         my_logger.info('### Starting Sending input data to DB ###')
         write_client.write(bucket, data)
         my_logger.info('### Finished Sending input data to DB ###')

# '''DAQ Mode Function'''
# def func_mode(devDesc, devFunc):
#    if devFunc['funcMode'] == 0:
#       return doi_daq(devDesc, devFunc['ports'])
#    elif devFunc['funcMode'] == 1:
#       return di_daq(devDesc, devFunc['ports'])
#    elif devFunc['funcMode'] == 2:
#       do_daq(devDesc, devFunc['ports'], devFunc['data'])
#    elif devFunc['funcMode'] == 3:
#       return ai_daq(devDesc, devFunc['ports'])
#    elif devFunc['funcMode'] == 4:
#       ao_daq(devDesc, devFunc['ports'], devFunc['data'])

'''Multiprocessing Function'''
def smap(f, *arg):
    return f(*arg)

def parallel(proc_list):
   with Pool() as pool:
      x = pool.starmap_async(smap, proc_list)
      print(x.get())
      pool.close()
      pool.join()

async def sub_process_1():
   di = await di_daq(devDesc, portList)
   doi = await doi_daq(devDesc, portList)
   ai = await ai_daq(devDesc, portList)
   return {1:di, 2:doi, 3:ai}

async def main():
   output = await asyncio.gather(sub_process_1())
   # with open('result.txt', 'w') as res:
   #    for out in output:
   #       res.writelines(json.dumps(out))

'''API'''
app = FastAPI()

@app.get('/ping')
async def ping():
    return 'pong!!!'

@app.get('/analog/input')
async def get_analog_input(devDesc: str = Body(embed=True), portList: list = Body(embed=True)):
   result = await ai_daq(devDesc, portList)
   return result

@app.get('/digital/input')
async def get_digital_input(devDesc: str = Body(embed=True), portList: list = Body(embed=True)):
   result = await di_daq(devDesc, portList)
   return result

@app.get('/digital_output/input')
async def get_digital_output_input(devDesc: str = Body(embed=True), portList: list = Body(embed=True)):
   result = await doi_daq(devDesc, portList)
   return result

@app.put('/analog/output')
async def get_analog_output(devDesc: str = Body(embed=True), portList: list = Body(embed=True), data: list = Body(embed=True)):
   result = await ao_daq(devDesc, portList, data)
   return result

@app.put('/digital/output')
async def get_digital_output(devDesc: str = Body(embed=True), data: list = Body(embed=True)):
   result = await do_daq(devDesc, data)
   return result