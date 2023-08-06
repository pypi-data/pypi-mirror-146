# Generate the data

```sh
mkdir cached-data
mkdir train-data
source single-cylinder-tdp-sim.sh
```

The default values are for the `RE=40` case. 

For the `RE=60` case set

```sh
RE=60  # Reynolds number of the problem
NTS=1800  # Number of time steps for the simulation
```

inside `single-cylinder-tdp-sim.sh`
