import random
from random import randint
from datetime import datetime, time
from time import sleep

offline = False
healthy = True
flux_capacitor = 1.21
status = 'Operating nominally'
latency = 0
outages = [
    '{"outage.category": "power", "outage.message": "Great Scott! Flux capacitor surge detected (' + str(flux_capacitor) + 'GigaWatt). Shutting down to avoid going back to 2051."}',
    '{"outage.category": "endurance", "outage.message": "This is hard, and I\'m tired. Going offline."}',
    '{"outage.category": "power", "outage.message": "My battery is low and it\'s getting dark."}',
    '{"outage.category": "software", "outage.message": "Task failed successfully."}',
    '{"outage.category": "software", "outage.message": "There\'s a glitch in the matrix."}',
    '{"outage.category": "power", "outage.message": "Vaccuum tube failure."}',
    '{"outage.category": "power", "outage.message": "Flux capacitor has died of dysentery"}'
]

class ADSBSensor:

    def __init__(self, sid, lat, lon, city=None, state=None, tier=None, off=False, health=True, flux_cap=1.21):
        self.id = sid
        self.city = city
        self.state = state
        self.latitude = lat
        self.longitude = lon
        self.tier = tier
        self.offline = self.set_offline(off)
        self.healthy = self.set_healthy(health)
        self.flux_capacitor = self.set_flux_cap(flux_cap)

    def startup():
        pass

    def set_healthy(self, health):
        self.healthy = health
        if healthy:
            self.status = 'Operating nominally'

    def set_offline(self, state):
        self.offline = state
        self.flux_capacitor = 0.0
        if offline:
            self.status = 'Offline'
    
    def set_flux_cap(self, flux_cap_value):
        self.flux_capacitor = flux_cap_value
        if flux_capacitor > 1.21:
            set_healthy(False)
            self.status = outages[0]

    def set_latency(self, new_latency):
        self.latency = new_latency

    def status(self):
        timestamp = datetime.now()
        msg = '[{"timestamp": "%s", "id": "%s", "city": "%s", "state": "%s", "location": {"latitude": "%s", "longitude": "%s"}, "tier": "%s", "healthy": "%s", "offline": "%s", "flux_capacitor": "%s", "status": "%s"}]' % (
            timestamp,
            self.id, self.city,
            self.state, self.latitude, 
            self.longitude, self.tier,
            self.healthy, self.offline,
            self.flux_capacitor, self.status)
        
        # Artificially add latency
        sleep(latency)
        return msg 

    def __str__():
        pass