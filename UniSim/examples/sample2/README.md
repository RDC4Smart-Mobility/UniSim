# Example 2 -- Service (REST) --

Install SUMO - Simulation of Urban Mobility before setup Unisim.


## Setup
Set virtualenv

```
python -m venv venv
source venv/bin/activate
```

Install UniSim

```
pip install -e ../../
```

Install JSON Server
https://github.com/typicode/json-server

## Run
Run with multiple terminal or following commands.

```
json-server -w db.json &
python sample2.py
```