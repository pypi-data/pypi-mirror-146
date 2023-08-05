# FusionSolarPy

A very basic python client for the HuaweiFusionSolar API used to monitor
solar power plants.

This client is currently hard-coded to use the https://region01eu5.fusionsolar.huawei.com end point and has not
been tested on any other end-points.

## Installation

Simply install from pypi using:

```bash
pip install fusion_solar_py
```

## Usage

The basic usage centers around the `FusionSolarClient` class. It currently
only has one method to extract the current power production, the total
power production for the current day, and the total energy ever produced
by the plant.

```python
from fusion_solar_py.client import FusionSolarClient

# log into the API - with proper credentials...
client = FusionSolarClient("my_user", "my_password")

# get the stats
stats = client.get_power_status()

# print all stats
print(f"Current power: {stats.current_power_kw} kW")
print(f"Total power today: {stats.total_power_today_kwh} kWh")
print(f"Total power: {stats.total_power_kwh} kWh")

# log out - just in case
client.log_out()
```

It is additional possible to retrieve the data for specific
plants - in case multiple plants are available through the
account.

```python
from fusion_solar_py.client import FusionSolarClient

# log into the API - with proper credentials...
client = FusionSolarClient("my_user", "my_password")

# get the plant ids
plant_ids = client.get_plant_ids()

print(f"Found {len(plant_ids)} plants")

# get the data for the first plant
plant_data = client.get_plant_stats(plant_ids[0])

# plant_data is a dict that contains the complete
# usage statistics of the current day. There is
# a helper function available to extract some
# most recent measurements
last_values = client.get_last_plant_data(plant_data)

print(f"Last production at {last_values["productPower"]["time"]]}: {last_values["productPower"]["value"]}")

# log out - just in case
client.log_out()
```