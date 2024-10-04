"""Platform for the tarifa_si sensor integration."""
from homeassistant.components.sensor import SensorEntity
from datetime import timedelta
import requests
import logging

_LOGGER = logging.getLogger(__name__)

# Set the update interval (every 2 minutes)
SCAN_INTERVAL = timedelta(minutes=2)

URL = "https://www.tarifa.si/api/tarifa/trenutna"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    # Get the scan interval from the configuration, default to SCAN_INTERVAL
    scan_interval = config.get("scan_interval", SCAN_INTERVAL)

    # Create the tariff sensor
    data = TarifaSiData()
    add_entities([TarifaSiSensor(data, scan_interval)], True)


class TarifaSiData:
    """Class for handling the data fetching from the API."""

    def __init__(self):
        """Initialize the data object."""
        self.data = None

    def update(self):
        """Fetch the data from the API."""
        try:
            # Attempt to fetch data from the API
            response = requests.get(URL, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses

            # Check if the response is empty
            if response.content:
                self.data = response.json()
            else:
                _LOGGER.warning(f"Received empty response from {URL}")
                # Do not update the data if the response is empty
                return

        except requests.exceptions.Timeout:
            # Handle timeout error
            _LOGGER.error(f"Timeout error when fetching data from {URL}")
            return
        except requests.exceptions.RequestException as e:
            # Handle all other requests-related errors
            _LOGGER.error(f"Failed to fetch data from {URL}: {e}")
            return
        except ValueError as e:
            # Handle JSON decode errors (e.g., malformed JSON)
            _LOGGER.error(f"Failed to parse JSON from {URL}: {e}")
            return


class TarifaSiSensor(SensorEntity):
    """Representation of the tarifa_si sensor."""

    def __init__(self, data, scan_interval):
        """Initialize the sensor."""
        self._data = data
        self._state = None
        self._attributes = {}
        self._scan_interval = scan_interval  # Store the scan interval

    @property
    def scan_interval(self):
        """Return the scan interval for this sensor."""
        return self._scan_interval

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

    def update(self):
        """Fetch new state data for the sensor."""
        self._data.update()

        # Only update state and attributes if data was successfully fetched
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
