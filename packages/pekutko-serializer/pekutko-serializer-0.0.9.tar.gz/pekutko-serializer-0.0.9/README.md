# ISP-2022-053504

Serilizer for python complex objects for JSON, TOML and YAML formats.

## Installation
```bash
pip install pekutko_serializer
```
## Usage
You can uses it in two modes:

### 1) As library
```python
from pekutko_serizlier import JsonSerializer

def my_func(a,b):
    return a+b

ser = JsonSerializer()
# return json string from dumps method
my_json_str = ser.dumps(my_func)
# load python obj from json string
func = ser.loads(my_json_str)

print(func(42, 15)) # 57 
```

### 2) As python module
Run in console/termianal:
```bash
python3 -m pekutko_serizlier --source "data.json" --to "data.toml"
```
Command above will convert python object json representation from data.json file to same object represantation in toml format and write it in data.toml file.
### Run converter module from config:
```bash
python3 -m pekutko_serizlier --conf "config.ini"
```
config.ini:
```ini
[DEFAULT]
source_file = "data.toml"
to_file = "data.yaml"
```