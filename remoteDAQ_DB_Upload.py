
from os import getenv
from uuid import uuid3, NAMESPACE_DNS
from socket import gethostname
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
import remoteDAQ_Logger
from remoteDAQ_USB import ai_daq, di_daq, doi_daq

# InfluxDB Client Config
url='http://192.168.117.132:8086' # CHANGE THIS
token = str(getenv('INFLUXDB_TOKEN'))  # CHANGE THIS
bucket = 'remote-data-acquisition' # CHANGE THIS
org = 'UGM' # CHANGE THIS

#Logger Config
my_logger = remoteDAQ_Logger.get_logger('RemoteDAQ_DB_Upload')

# Node Config
dev_id = str(uuid3(NAMESPACE_DNS, gethostname()))
      
'''Create an InfluxDB Dictionary'''
def line_protocol(measurement_name, id, port, value):
   return '{measurement},nodeID={id},port={port} value={val}'.format(
         measurement=measurement_name,
         id=id,
         port=port,
         val=value
      )

'''Send Data to InfluxDB'''
def send_to_influxdb(
   url=url,
   token=token,
   org=org,
   bucket=bucket,
   data=[],
   logger=my_logger
   ):
   with InfluxDBClient(url, token, org) as client:
      with client.write_api(write_options=ASYNCHRONOUS) as write_client:
         logger.info('### Starting Sending input data to DB ###')
         write_client.write(bucket, org, data)

'''Main Function'''
async def main(devDesc, portList):
   daq_results = [
         await ai_daq(devDesc, portList),
         await di_daq(devDesc, portList),
         await doi_daq(devDesc, portList)
         ]
   measurement_name = ['analogInput', 'digitalInput', 'digitalOutputValue']
   
   for r in range(len(daq_results)):
      upload = []
      for i in portList:
         result = daq_results[r]['data'][i]
         tmp_upload = line_protocol(
            measurement_name = measurement_name[r],
            id=dev_id,
            port=result['port'],
            value=result['data']
         )
         upload.append(tmp_upload)
      print('Sending Data to DB...')
      send_to_influxdb(data=upload)