import random
import json
import datetime
import time
from random import randint
from datetime import timezone
from time import sleep

class ADSBSensor:
    from outages import outages
    offline = False
    healthy = True
    flux_capacitor = 1.21
    status = 'Operating nominally'
    latency = 0
    outage_msg = ''
    outage_cat = ''

    def __init__(self, sid, lat, lon, city=None, state=None, tier=None, off=False, health=True, latency=0, flux_cap=1.21):
        self.id = sid
        self.city = city
        self.state = state
        self.latitude = lat
        self.longitude = lon
        self.tier = tier
        self.set_offline(off)
        self.set_healthy(health)
        self.set_latency(latency)
        self.set_flux_cap(flux_cap)

    def set_healthy(self, health):
        self.healthy = health
        if self.healthy:
            self.status = 'Operating nominally'

    def set_offline(self, sys_state):
        self.offline = sys_state
    
    def set_flux_cap(self, flux_cap_value):
        if flux_cap_value != '':
            self.flux_capacitor = float(flux_cap_value)
        if self.flux_capacitor > 1.32:
            self.set_healthy(False)
            self.set_offline(True)
            self.status = self.flux_msgs[0]['outage.message'].format(self.flux_capacitor)

    def set_random_error(self):
        err_obj = random.choice(self.outages)
        self.outage_cat = err_obj['outage.category']
        self.outage_msg = err_obj['outage.message']
        self.set_healthy(False)
        self.set_offline(True)
        self.set_status("{} Error".format(self.outage_cat).title())

    def set_latency(self, new_latency):
        self.latency = new_latency
    
    def set_status(self, err_str):
        self.status = err_str

    def get_status(self):
        # Artificially add latency
        sleep(self.latency)
        utc_time = time.time()
        timestamp = datetime.datetime.utcfromtimestamp(utc_time).strftime("%Y-%m-%dT%H:%M:%SZ")
        msg = '{{"@timestamp": "{time}", "id": "{id}", "city": "{city}", "state": "{state}", "location": {{"lat": "{lat}", "lon": "{lon}"}}, "tier": "{tier}", "healthy": "{health}", "offline": "{offline}", "flux_capacitor": "{flux}", "status": "{status}", "outage.category": "{err_cat}", "outage.message": "{err_msg}"}}'.format(time=timestamp, \
                id=self.id, city=self.city, state=self.state, lat=self.latitude, \
                lon=self.longitude, tier=self.tier, health=str(self.healthy).lower(), offline=str(self.offline).lower(), \
                flux=self.flux_capacitor, status=self.status, err_cat=self.outage_cat, err_msg=self.outage_msg)
        return msg 
    
    def __str__(self):
        stat = self.id + ' - ' + self.city + ', ' + self.state
        return stat