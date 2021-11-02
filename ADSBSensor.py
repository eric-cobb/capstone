import random
from random import randint
from datetime import datetime, time
from time import sleep

offline = False
healthy = True
flux_cap = 1.21
status = 'Operating nominally'
outages = [
    '{"outage.category": "power", "outage.message": "Great Scott! Flux capacitor surge detected (1.22 GigaWatt). Shutting down to avoid going back to 2051."}',
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
        global offline
        offline = state

    def status(self):
        global status
        global outages
        global flux_cap
        timestamp = datetime.now()
        if offline:
            status = 'Offline'
            flux_cap = 0.0
        if not healthy:
            status = random.choice(outages)
        msg = '[{"timestamp": "%s", "id": "%s", "city": "%s", "state": "%s", "location": {"latitude": "%s", "longitude": "%s"}, "tier": "%s", "flux_capacitor": "%s", "status": "%s"}]' % (
            timestamp,
            self.id, self.city,
            self.state, self.latitude, 
            self.longitude, self.tier,
            flux_cap, status)
        # Artificially add latency
        sleep(randint(1,30))
        return msg 

    def __str__():
        pass