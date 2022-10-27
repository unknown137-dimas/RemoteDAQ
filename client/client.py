from influxdb_client import InfluxDBClient

# InfluxDB connection config
bucket = 'remote-data-acquisition'
org = 'UGM'
token = 'PXCJT5naU4g1R04-b9U_MtMBFLYkimD4-QZ0GyswJiBwov7MzOMj_ABppwuxvNXIK2HknQnp_qrVYXLfwY2cww=='
url='http://192.168.117.132:8086'
measurement = 'analogInput'
range = '-15d'
data_fields = ['nodeID', 'channel', '_value']

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

if __name__ == '__main__':
    get_data_table(bucket, range, measurement, data_fields)