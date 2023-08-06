# Simples steps for using the PyDaisi SDK

## Preliminary tasks

### Install with PIP:

- `pip install pydaisi`

### (Optional) Set your personal access token:

Create your personal access token

- https://app.daisi.io/settings/personal-access-tokens

Set it in the environment:
```
export DAISI_ACCESS_TOKEN=a1b2c3d4e5f67890abcdef124567890
```
or in a `.env` file:
```
DAISI_ACCESS_TOKEN=a1b2c3d4e5f67890abcdef124567890
```

## Using PyDaisi

```
from pydaisi import Daisi

# instantiate a Daisi object
daisi = Daisi("my-pebble-tutorial")
# call a Daisi function. You can also use position parameters: daisi.median("London")
temp = daisi.median(city="London")
print(f"Median temperature in London was: {temp.value()}")

# call a function but return without waiting for it to complete
temp2 = daisi.dispatch("median","Paris")
# see if it's done
if temp2.get_status() == "FINISHED":
# get the results the same way as the blocking call:
    print("Median: ", {temp2.value()})
```
