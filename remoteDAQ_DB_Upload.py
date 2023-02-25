
from os import getenv
from dotenv import load_dotenv
from uuid import uuid3, NAMESPACE_DNS
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS
import remoteDAQ_Logger
from remoteDAQ_USB import ai_daq, di_daq, doi_daq

'''Load Variables'''
load_dotenv()

'''InfluxDB Client Config'''
url = str(getenv('DB_IP'))
token = str(getenv('DB_TOKEN'))
org = str(getenv('DB_ORG'))
bucket = str(getenv('DB_BUCKET'))

'''Logger Config'''
my_logger = remoteDAQ_Logger.get_logger('RemoteDAQ_DB_Upload')

'''Node Config'''
node_hostname = str(getenv('NODE_HOSTNAME'))
node_id = str(getenv('ZT_ID'))
      
'''Create an InfluxDB Line Protocol Format'''
def line_protocol(measurement_name, node_hostname, node_id, port, value):
   return '{measurement_name},node={node_hostname},nodeID={node_id},port={port} value={value}'.format(
         measurement_name,
         node_hostname,
         node_id,
         port,
         value
      )

'''InfluxDB Callback'''
class db_callback():
   '''Success Callback'''
   def success(self, conf, data):
        my_logger.info('### Successfully Sending Data to DB ###')
   '''Error Callback'''
   def error(self, conf, data, exception: InfluxDBError):
        my_logger.error(f'### Error occurs, Error message: {exception} ###')
   '''Retry Callback'''
   def retry(self, conf, data, exception: InfluxDBError):
        my_logger.error(f'### Retryable error occurs, Error message: {exception} ###')
callback = db_callback()

'''Send Data to InfluxDB'''
def send_to_influxdb(
   url=url,
   token=token,
   org=org,
   bucket=bucket,
   data=[]
   ):
   with InfluxDBClient(url, token, org=org) as client:
      with client.write_api(success_callback=callback.success,
                            error_callback=callback.error,
                            retry_callback=callback.retry) as write_client:
         write_client.write(bucket, org, data)

'''Main Function'''
async def main(devDesc, portList):
   daq_results = [
         await ai_daq(devDesc, portList),
         await di_daq(devDesc, portList),
         await doi_daq(devDesc, portList)
         ]
   measurement_name = ['analogInput', 'digitalInput', 'digitalOutputValue']
   
   upload = []
   for r in range(len(daq_results)):
      if daq_results[r]['success']:
         for i in portList:
            result = daq_results[r]['data'][i]
            tmp_upload = line_protocol(
               measurement_name=measurement_name[r],
               node_hostname=node_hostname,
               node_id=node_id,
               port=result['port'],
               value=result['value']
            )
            upload.append(tmp_upload)
   my_logger.info('### Sending Data to DB ###')
   send_to_influxdb(data=upload)