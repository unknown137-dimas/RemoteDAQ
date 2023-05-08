import subprocess
import platform
from PyAccessPoint import pyaccesspoint

access_point = pyaccesspoint.AccessPoint(inet=None,
                                         ip='192.168.1.1',
                                         ssid='Test',
                                         password='test123123')
    
try:
    res = subprocess.check_output('ping -{} 1 google.com'.format('n' if platform.system().lower() == 'windows' else 'c'))
    if res:
        access_point.stop()
except:
    if not access_point.is_running():
        access_point.start()