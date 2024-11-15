### Electricity Block Tariff (SI)

Retrieves and displays real-time electricity block tariff information from [tarifa.si](https://www.tarifa.si/) for Slovenian consumers.

### Installation via HACS

1. In Home Assistant, navigate to **HACS**.
2. Click on the three dots in the top right corner and choose **Custom repositories**.
3. Add this repository URL: `https://github.com/matijarijavec/hacs-tarifa-si`.
4. Choose **Integration** as the category.
5. After adding the repository, find **Electricity Block Tariff (SI)** in HACS and install it.

---

After installing, add the following configuration to your `configuration.yaml` file:
```yaml
sensor:
  - platform: tarifa_si
    name: Electricity Block Tariff (SI)
```