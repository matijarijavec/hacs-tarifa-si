# Tarifa SI

A custom Home Assistant integration that fetches tariff information from [tarifa.si](https://www.tarifa.si/).

## Installation via HACS

1. In Home Assistant, navigate to **HACS > Integrations**.
2. Click on the three dots in the top right corner and choose **Custom repositories**.
3. Add this repository URL: `https://github.com/matijarijavec/hass-tarifa-si`.
4. Choose **Integration** as the category.
5. After adding the repository, find **Tarifa SI** in HACS and install it.

## Configuration

Add the following to your `configuration.yaml` file:

```yaml
sensor:
  - platform: tarifa_si
    scan_interval: 60  # Update every 60 seconds (change this value as needed)