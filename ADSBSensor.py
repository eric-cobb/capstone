import random
from random import randint
from datetime import datetime, time
from time import sleep

offline = False
healthy = True
flux_cap = 1.21
status = 'Operating nominally'
latency = 0
outages = [
    '{"outage.category": "power", "outage.message": "Great Scott! Flux capacitor surge detected (' + str(flux_cap) + 'GigaWatt). Shutting down to avoid going back to 2051."}',
    '{"outage.category": "endurance", "outage.message": "This is hard, and I\'m tired. Going offline."}',
    '{"outage.category": "power", "outage.message": "My battery is low and it\'s getting dark."}',
    '{"outage.category": "software", "outage.message": "Task failed successfully."}',
    '{"outage.category": "software", "outage.message": "There\'s a glitch in the matrix."}',
    '{"outage.category": "power", "outage.message": "Vaccuum tube failure."}',
    '{"outage.category": "power", "outage.message": "Flux capacitor has died of dysentery"}'
]

class ADSBSensor:

    def __init__(self, sid, lat, lon, city=None, state=None, tier=None):
        self.id = sid
        self.city = city
        self.state = state
        self.latitude = lat
        self.longitude = lon
        self.tier = tier

    def startup():
        pass

    def set_healthy(self, health):
        global healthy
        healthy = health

    def set_offline(self, state):
        global offline, flux_cap, status
        offline = state
        flux_cap = 0.0
        if offline:
            status = 'Offline'
    
    def set_flux_cap(self, flux_cap_value):
        global flux_cap, status
        flux_cap = flux_cap_value
        if flux_cap > 1.21:
            set_healthy(False)
            status = outages[0]

    def set_latency(self, new_latency):
        global latency
        latency = new_latency

    def status(self):
        global status
        global outages
        global flux_cap
        global latency
        timestamp = datetime.now()
        msg = '[{"timestamp": "%s", "id": "%s", "city": "%s", "state": "%s", "location": {"latitude": "%s", "longitude": "%s"}, "tier": "%s", "flux_capacitor": "%s", "status": "%s"}]' % (
            timestamp,
            self.id, self.city,
            self.state, self.latitude, 
            self.longitude, self.tier,
            flux_cap, status)
        
        # Artificially add latency
        sleep(latency)
        return msg 

    def __str__():
        pass