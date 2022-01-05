import random
import datetime
import time
from datetime import timezone
from time import sleep

class ADSBSensor:
    """
    Class representing an ADS-B sensor and its status

    Attributes
    ----------
    offline : bool
        Whether or not the sensor is offline
    healthy : bool
        Whether or not the sensor is healthy
    flux_capacitor : float
        Flux capacitor power expressed in Gigawatts :-P
    status : str
        Status message that will be returned upon calling get_status()
        (default 'Operating nominally')
    latency : int
        The amount of artificial latency that should be added to the
        get_status() response
    outage_msg : str
        The message to be included when there is an outage with the 
        sensor (default '')
    outage_cat : str
        The outage category (e.g. 'Power,' 'Software,' etc) (default '')
    
    Methods
    -------
    set_healthy(health)
        Sets sensor health status to true/false
    set_offline(sys_state)
        Sets sensor offline status to true/false
    set_flux_cap(flux_cap_value)
        Sets the sensor's flux capacitor value
    set_random_error()
        Assign random error to a sensor's outage category/message
    set_latency(new_latency)
        Set the amount of latency that will be used before responding
        to any call to get_status()
    set_status(err_str)
        Set the status message to be returned. This is the 'log' output
        that will be generated when calling get_status()
    get_status()
        Return an NDJSON line representing the sensor's full status
    """

    from outages import outages
    offline = False
    healthy = True
    flux_capacitor = 1.21
    status = 'Operating nominally'
    latency = 0
    outage_msg = ''
    outage_cat = ''

    def __init__(self, sid, lat, lon, city=None, state=None, tier=None, off=False, health=True, latency=0, flux_cap=1.21):
        """
        Parameters
        ----------
        sid : str
            The ADS-B sensor ID
        lat : str
            The sensor's latitude
        lon : str
            The sensor's longitude
        city : str, optional
            The city where the sensor is located
        state : str, optional
            The state where the sensor is located
        tier : str, optional
            Honestly have no idea what this is
        off : bool, optional
            Whether or not the sensor is offline (default false)
        health : bool, optional
            Whether or not the sensor is healthy (default true)
        latency : int, optional
            Latency to add to get_status() calls (default 0)
        flux_cap : float, optional
            The initial flux capacitor value (default 1.21 IYKYK)
        """

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

    def get_status(self):
        """
        Returns the full status message of the sensor's state as an
        NDJSON string
        """

        # Artificially add latency
        sleep(self.latency)
        utc_time = time.time()
        timestamp = datetime.datetime.utcfromtimestamp(utc_time).strftime("%Y-%m-%dT%H:%M:%SZ")
        msg = '{{"@timestamp": "{time}", "id": "{id}", "city": "{city}", "state": "{state}", "location": {{"lat": "{lat}", "lon": "{lon}"}}, "tier": "{tier}", "healthy": "{health}", "offline": "{offline}", "flux_capacitor": "{flux}", "status": "{status}", "outage.category": "{err_cat}", "outage.message": "{err_msg}"}}'.format(time=timestamp, \
                id=self.id, city=self.city, state=self.state, lat=self.latitude, \
                lon=self.longitude, tier=self.tier, health=str(self.healthy).lower(), offline=str(self.offline).lower(), \
                flux=self.flux_capacitor, status=self.status, err_cat=self.outage_cat, err_msg=self.outage_msg)
        return msg

    def set_flux_cap(self, flux_cap_value):
        """
        Sets the value of the flux capacitor. If the value is above
        1.46, set the sensor to 'unhealthy' and 'offline'. If the value
        is below 1.17, set the sensor to 'healthy' and 'online'.

        Parameters
        ----------
        flux_cap_value : float
            The value of the flux capacitor, expressed in Gigawatts
        """

        if flux_cap_value != '':
            self.flux_capacitor = float(flux_cap_value)
        if self.flux_capacitor > 1.46:
            self.set_healthy(False)
            self.set_offline(True)
            # Error state encountered, so set outage category and message
            self.outage_cat = "Power"
            self.outage_msg = "Great Scott! Flux capacitor surge detected (" + str(flux_cap_value) + " GigaWatt). Shutting down to avoid going back to year 2051."
            self.set_status("{} Error".format(self.outage_cat).title())
        # This just sets an explicit status message, since we're not
        # in a normal state but also not in an error state. (In case
        # you haven't guessed by now this is all completely made up!)
        elif self.flux_capacitor < 1.17:
            self.set_healthy(True)
            self.set_offline(False)
            self.set_status("Flux Capacitor Underpowered")

    def set_healthy(self, health):
        """
        Sets the sensor state to either 'online' or 'offline'.

        Parameters
        ----------
        health : bool
            Whether or not the sensor is healthy (True/False)
        """

        self.healthy = health
        if self.healthy:
            self.status = 'Operating nominally'

    def set_latency(self, new_latency):
        """
        Sets the amount of latency to wait before responding to calls
        to get_status()

        Parameters
        ----------
        new_latency : float
            The amount of time to wait before returning a status
        """

        self.latency = new_latency

    def set_offline(self, sys_state):
        """
        Sets the state of the sensor as either 'online' or 'offline'.

        Parameters
        ----------
        sys_state : bool
            Offline or online
        """

        self.offline = sys_state

    def set_random_error(self):
        """
        Grab a random error message from the 'outages' dict and 
        apply it to this object's outage/message 
        """

        err_obj = random.choice(self.outages)
        self.outage_cat = err_obj['outage.category']
        self.outage_msg = err_obj['outage.message']
        # Sensor is unhealthy, so also set health and offline 
        # appropriately, as well as the status message
        self.set_healthy(False)
        self.set_offline(True)
        self.set_status("{} Error".format(self.outage_cat).title())
    
    def set_status(self, err_str):
        """
        Sets the status of the sensor based on the string based in

        Parameters
        ----------
        err_str : str
            The status message that gets returned/written as the 
            sensor's ultimate state
        """

        self.status = err_str 
    
    def __str__(self):
        """
        This does something. I think.
        """
        
        stat = self.id + ' - ' + self.city + ', ' + self.state
        return stat