from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt 
import time
import json

# InfluxDB Config
bucket = 'remote-data-acquisition' # CHANGE THIS
org = 'UGM' # CHANGE THIS
token = 'PXCJT5naU4g1R04-b9U_MtMBFLYkimD4-QZ0GyswJiBwov7MzOMj_ABppwuxvNXIK2HknQnp_qrVYXLfwY2cww==' # CHANGE THIS
url='http://192.168.117.132:8086' # CHANGE THIS
measurement = 'analogInput'
range = '-15d'
data_fields = ['nodeID', 'channel', '_value']

# MQTT Config
mqttBroker ='mqtt.eclipseprojects.io' 
topic = 'remoteDAQ/devFunction'

'''
INFLUXDB Function
'''
def get_data_table(bucket, range, measurement, data_fields):
    '''
    Query Data Using Table Structure
    '''
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()
        tables = query_api.query('from(bucket:"'+ bucket +'") |> range(start: '+ range +') |> filter(fn: (r) => r["_measurement"] == "'+ measurement +'")')

        for table in tables:
            for record in table.records:
                for data_field in data_fields:
                    print(record.values[data_field], end=', ')
                print()

def devfunc():
    '''
        Configure DAQ Mode (Digital/Analog, Input/Output)
        > valid 'funcMode' values:
            0 = 'Digital Output Input' -> Read values from Digital Output pins.
            1 = 'Digital Input'
            2 = 'Digital Output'
            3 = 'Analog Input'
            4 = 'Analog Output'
    '''
    func = {'funcMode':1, 'ports':[0,1], 'data':[0.6,0.5]}
    client.publish(topic, json.dumps(func))
    print('Just published ' + str(func) + ' to topic ' + topic)
    time.sleep(1)
    

if __name__ == '__main__':
    client = mqtt.Client('client')
    client.connect(mqttBroker) 
    devfunc()
    # get_data_table(bucket, range, measurement, data_fields)