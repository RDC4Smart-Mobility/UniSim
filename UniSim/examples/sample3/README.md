# Example 3 -- Multiple Simulator (include Deivide Route) --

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
python sample3.py
```

## How to make extra infomation json file
1. osm => (net.xml, poly.xml)  
2. net.xml -> rou.xml  
  $SUMO_HOME/tools/randomTrips.py -n {input}.net.xml -r {output}.rou.xml -p {interval} --pedestrians  
3. rou.xml -> ext.json  
  ext_info.py -r {input}.rou.xml -e {input}.json -o {output}.ext.json