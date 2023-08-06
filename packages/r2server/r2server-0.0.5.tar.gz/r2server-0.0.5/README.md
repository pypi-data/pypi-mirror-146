## About
r2server python sdk makes it easier for you to work with your r2server server using the python programming language. The SDK uses an object-oriented design and tries to look like r2server API.

## Installation 

#### with pip3

```sh
pip install r2server
```

#### from repo

```sh
make install
make doc # for generate documentation
```

## Quick start

```python
import r2server.api

# init api
network = r2server.api()

# get all observations of METEOR-M2
obs = network.observation(33591)

# print all filtred observations ids
for ob in obs:
    print("Observation " + str(ob.id) + " by " + ob.name)

```