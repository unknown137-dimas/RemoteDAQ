
from os import getenv
from uuid import uuid3, NAMESPACE_DNS
from socket import gethostname
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS
import remoteDAQ_Logger
from remoteDAQ_USB import ai_daq, di_daq, doi_daq

# InfluxDB Client Config
url = str(getenv('INFLUXDB_IP'))
token = str(getenv('INFLUXDB_TOKEN'))
org = str(getenv('INFLUXDB_ORG'))
bucket = str(getenv('INFLUXDB_BUCKET'))

#Logger Config
my_logger = remoteDAQ_Logger.get_logger('RemoteDAQ_DB_Upload')

# Node Config
hostname = str(getenv('HOSTNAME'))
dev_id = str(uuid3(NAMESPACE_DNS, hostname))
      
'''Create an InfluxDB Line Protocol Format'''
def line_protocol(measurement_name, node, id, port, value):
   return '{measurement},node={node},nodeID={id},port={port} value={val}'.format(
         measurement=measurement_name,
         node=node,
         id=id,
         port=port,
         val=value
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
               measurement_name = measurement_name[r],
               node=hostname,
               id=dev_id,
               port=result['port'],
               value=result['value']
            )
            upload.append(tmp_upload)
   my_logger.info('### Sending Data to DB ###')
   send_to_influxdb(data=upload)