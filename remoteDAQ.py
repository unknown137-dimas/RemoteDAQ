
from uuid import uuid3, NAMESPACE_DNS
from socket import gethostname
from influxdb_client.client.influxdb_client import InfluxDBClient
from datetime import datetime
import remoteDAQ_Logger
from remoteDAQ_USB import ai_daq, di_daq, doi_daq
import asyncio


# InfluxDB Client Config
url='http://192.168.117.132:8086' # CHANGE THIS
token = 'PXCJT5naU4g1R04-b9U_MtMBFLYkimD4-QZ0GyswJiBwov7MzOMj_ABppwuxvNXIK2HknQnp_qrVYXLfwY2cww=='  # CHANGE THIS
bucket = 'remote-data-acquisition' # CHANGE THIS
org = 'UGM' # CHANGE THIS
send_to_db = False

# DAQ Config
devDesc = 'USB-4704,BID#0' # CHANGE THIS
portList = [_ for _ in range(0,8)]

#Logger Config
my_logger = remoteDAQ_Logger.get_logger('RemoteDAQ')

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
      with client.write_api() as write_client:
         logger.info('### Starting Sending input data to DB ###')
         write_client.write(bucket, data)

'''Main Function'''
async def main(devDesc, portList):
   ai_results = await ai_daq(devDesc, portList)
   di_results = await di_daq(devDesc, portList)
   doi_results = await doi_daq(devDesc, portList)
   
   ai_upload = []
   di_upload = []
   doi_upload = []
   for i in portList:
      ai_result = ai_results['data'][i]
      di_result = di_results['data'][i]
      doi_result = doi_results['data'][i]
      
      ai_tmp_upload = line_protocol(
         measurement_name=ai_result['measurement_name'],
         id=dev_id,
         port=ai_result['port'],
         value=ai_result['value']
      )
      di_tmp_upload = line_protocol(
         measurement_name=di_result['measurement_name'],
         id=dev_id,
         port=di_result['port'],
         value=di_result['value']
      )
      doi_tmp_upload = line_protocol(
         measurement_name=doi_result['measurement_name'],
         id=dev_id,
         port=doi_result['port'],
         value=doi_result['value']
      )
      
      ai_upload.append(ai_tmp_upload)
      di_upload.append(di_tmp_upload)
      doi_upload.append(doi_tmp_upload)
   
   send_to_influxdb(data=ai_upload)
   send_to_influxdb(data=di_upload)
   send_to_influxdb(data=doi_upload)

if __name__ == '__main__':
   now = datetime.now()
   while True:
        check = datetime.now()
        diff = check - now
        if diff.total_seconds() > 5:
            asyncio.run(main(devDesc, portList))
            now = check