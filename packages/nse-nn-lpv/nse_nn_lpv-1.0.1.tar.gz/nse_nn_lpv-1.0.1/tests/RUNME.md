# Set up and train the CNN

```sh
# cd tests
python3 start-cnn-pod-check.py
```

For the `RE=60` case set

```sh
Re = 60  # Reynolds number
fid_params = [20, 15, 10]
```
in `start-cnn-pod-check.py`.

# Run the LPV simulation

```sh
# cd tests
source start-cnn-lpv-simu.sh
```

This simulates with the `CNN-3` model. For 

* other code sizes (in the paper: `CS=3,5,8`)
* for a FOM or POD simulation
* other `alpha` values

adapt

```sh
LDLPV='CNN'  # can be `POD` or `FOM` too
ALPHA=.5  # alpha parameter
CS=3  # list of code sizes to check
```

accordingly.


## Post processing

If all data is computed as in the paper described, then

```sh
python plot_drag_lift_curves.py
```

will return the plots with drag and lift over time and their phase portraits.

If other parameters were used, the file names have to be updated.

The plots for the `RE=60` simulations, were generated via

```sh
python pdlc_quick_check.py
```
