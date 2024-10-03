"""Platform for the tarifa_si sensor integration."""
from homeassistant.components.sensor import SensorEntity
from datetime import timedelta
import requests
import logging

_LOGGER = logging.getLogger(__name__)

# Set the update interval (every 1 minute)
SCAN_INTERVAL = timedelta(minutes=1)

URL = "https://www.tarifa.si/api/tarifa/trenutna"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # Create the tariff sensor
    data = TarifaSiData()
    add_entities([TarifaSiSensor(data)], True)


class TarifaSiData:
    """Class for handling the data fetching from the API."""

    def __init__(self):
        """Initialize the data object."""
        self.data = None

    def update(self):
        """Fetch the data from the API."""
        try:
            response = requests.get(URL)
            response.raise_for_status()  # Raise an error for bad responses
            self.data = response.json()
        except Exception as e:
            _LOGGER.error(f"Failed to fetch data from {URL}: {e}")
            self.data = None


class TarifaSiSensor(SensorEntity):
    """Representation of the tarifa_si sensor."""

    def __init__(self, data):
        """Initialize the sensor."""
        self._data = data
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Tarifa SI Sensor"

    @property
    def state(self):
        """Return the state of the sensor (tariff value)."""
        return self._state

    @property
    def icon(self):
        """Return the icon for the sensor."""
        return "mdi:home-lightning-bolt-outline"

    @property
    def extra_state_attributes(self):
        """Return the other key/values as attributes."""
        return self._attributes

    @property
    def unique_id(self):
        """Return a unique identifier for this sensor."""
        return "tarifa_si_sensor"

    @property
    def scan_interval(self):
        """Return the scan interval for this sensor."""
        return SCAN_INTERVAL

    def update(self):
        """Fetch new state data for the sensor."""
        self._data.update()
        if self._data.data is not None:
            # Set the main state as the 'tariff' value
            self._state = self._data.data.get("tariff")
            
            # Set other key/values as attributes
            self._attributes = {
                "season": self._data.data.get("season"),
                "start_hour": self._data.data.get("start_hour"),
                "started_before_hours": self._data.data.get("started_before_hours"),
                "start_day_difference": self._data.data.get("start_day_difference"),
                "end_hour": self._data.data.get("end_hour"),
                "end_day_difference": self._data.data.get("end_day_difference"),
                "ends_in_hours": self._data.data.get("ends_in_hours")
            }
