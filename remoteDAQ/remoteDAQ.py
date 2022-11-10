import sys
sys.path.append('..')
import logging
from logging.handlers import TimedRotatingFileHandler
import time
from uuid import uuid3, NAMESPACE_DNS
import reactivex as rx
from reactivex import operators as ops
from socket import gethostname
from influxdb_client import WriteOptions
from influxdb_client.client.influxdb_client import InfluxDBClient
from Automation.BDaq import *
from Automation.BDaq.InstantDiCtrl import InstantDiCtrl
from Automation.BDaq.InstantDoCtrl import InstantDoCtrl
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.InstantAoCtrl import InstantAoCtrl

# InfluxDB connection config
bucket = 'remote-data-acquisition'
org = 'UGM'
token = 'PXCJT5naU4g1R04-b9U_MtMBFLYkimD4-QZ0GyswJiBwov7MzOMj_ABppwuxvNXIK2HknQnp_qrVYXLfwY2cww=='
url='http://192.168.117.132:8086'

# Data config
interval = 2
num_of_points = 10

# DAQ config
devDesc = 'USB-4704,BID#0'
startPort = 0
endPort = 7

# Log config
FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')

LOG_FILE = 'remoteDAQ.log'

'''
Log Function
'''
def get_console_handler():
   '''
   Console Output Handler
   '''
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

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
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger

my_logger = get_logger('remoteDAQ')

'''
DAQ Function
'''
def di_daq(devDesc, portList):
   '''
   Function to Read Digital Input
   '''
   my_logger.info('### Starting reading digital input channel data ###')
   measurement_name = 'digitalInput'
   try:
      instantDiCtrl = InstantDiCtrl(devDesc)
   except ValueError as e:
      my_logger.error(e)
   else:
      for i in portList:
         _, data = instantDiCtrl.readBit(0, i)
         my_logger.info('Successfully read digital input channel #' + str(i))
         yield measurement_name, i, data
      my_logger.info('### Finished reading digital input channel data ###')
      instantDiCtrl.dispose()
   
def do_daq(devDesc, portList, data):
   '''
   Function to Write Digital Output
   '''
   my_logger.info('### Starting writing digital output channel data ###')
   try:
      instantDoCtrl = InstantDoCtrl(devDesc)
   except ValueError as e:
      my_logger.error(e)
   else:
      for i in portList:
         _ = instantDoCtrl.writeBit(0, i, data)
         my_logger.info('Successfully write digital output channel #' + str(i))
      my_logger.info('### Finished writing digital output channel data ###')
      instantDoCtrl.dispose()

def dov_daq(devDesc, portList):
   '''
   Function to Read Digital Output Value
   '''
   my_logger.info('### Starting reading digital output channel data ###')
   measurement_name = 'digitalOutputValue'
   try:
      instantDoCtrl = InstantDoCtrl(devDesc)
   except ValueError as e:
      my_logger.error(e)
   else:
      for i in portList:
         _, data = instantDoCtrl.readBit(0, i)
         my_logger.info('Successfully read digital output channel #' + str(i))
         yield measurement_name, i, data
      my_logger.info('### Finished reading digital output channel data ###')
      instantDoCtrl.dispose()

def ai_daq(devDesc, portList, decimalPrecision=2):
   '''
   Function to Read Analog Signal
   '''
   my_logger.info('### Starting reading analog channel data ###')
   measurement_name = 'analogInput'
   try:
      instanceAiObj = InstantAiCtrl(devDesc)
   except ValueError as e:
      my_logger.error(e)
   else:
      for i in portList:
         _, scaledData = instanceAiObj.readDataF64(i, 1)
         my_logger.info('Successfully read analog channel #' + str(i))
         yield measurement_name, i, round(scaledData[0], decimalPrecision)
      my_logger.info('### Finished reading analog channel data ###')
      instanceAiObj.dispose()

def ao_daq(devDesc, portList, data=[0, 0]):
   '''
   Function to Output Analog Signal
   '''
   my_logger.info('### Starting writing data to analog channel ###')
   try:
      instantAoCtrl = InstantAoCtrl(devDesc)
   except ValueError as e:
      my_logger.error(e)
   else:
      for i in portList:
         _ = instantAoCtrl.writeAny(i, 1, None, [data[i]])
         my_logger.info('Successfully write analog output channel #' + str(i))
      my_logger.info('### Finished writing data to analog channel ###')
      instantAoCtrl.dispose()
      
def line_protocol(measurement_name, channel, value):
   '''
   Create an InfluxDB Dictionary
   '''
   return '{measurement},nodeID={id},channel={ch} value={val}'.format(measurement=measurement_name,
      id=uuid3(NAMESPACE_DNS, gethostname()),
      ch=channel,
      val=value)

def send_to_influxdb(data, num_of_points):
   '''
   # Send Data to InfluxDB
   # '''
   with InfluxDBClient(url=url, token=token, org=org) as client:
      with client.write_api(write_options=WriteOptions(batch_size=1,
                                                      flush_interval=10_000,
                                                      jitter_interval=2_000,
                                                      retry_interval=1_000,
                                                      max_retries=3,
                                                      max_retry_delay=10_000,
                                                      exponential_base=2)) as write_client:
         
         '''
         Prepare Batches from Generator
         '''
         def write_batch(batch):
            '''
            Synchronous Write
            '''
            my_logger.info('### Starting Sending input data to DB ###')
            write_client.write(bucket=bucket, record=batch)
            my_logger.info('### Finished Sending input data to DB ###')

         batches = rx.from_iterable(data).pipe(ops.buffer_with_count(num_of_points*(len(data))))
         
         '''
         Write Batches
         '''
         batches.subscribe(on_next=lambda batch: write_batch(batch),
                           on_error=lambda ex: print(f'Unexpected error: {ex}'),
                           on_completed=lambda: print('Import finished!'))


if __name__ == '__main__':
   send_to_db = False
   input = False
   if input:
      for _ in range(num_of_points):
         input_data = [line_protocol(measurement_name=name, channel=channel, value=value) for name, channel, value in di_daq(devDesc=devDesc, portList=[i for i in range(6,8)])]
         if input_data and send_to_db:
            send_to_influxdb(input_data, num_of_points)
            time.sleep(1)
         else:
            my_logger.info(input_data)
            time.sleep(1)
   else:
      output_data = do_daq(devDesc=devDesc, portList=[4,5], data=1)