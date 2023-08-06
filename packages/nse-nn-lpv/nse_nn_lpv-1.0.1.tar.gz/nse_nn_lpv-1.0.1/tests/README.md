# Info on what the files contain and do

## Experiments

 * `CNN_pod_check.py` -- main file

## Helpers

 * `check_pod_parts.py` -- module to check the POD (in state and costate)
 * `train_cnnnse_models.py` -- module to do the training of the NN
 * `plot_errs.py` -- script to plot the errors

## Unit Tests

 * `test_units_*.py` 

## Checks and Tests

 * `cd simple-tests-checks/`
 * `test_conv2d.py` -- testing the `torch.nn.Conv2d` function for our data
 * `data_fem_checks.py` -- check with the original FEM data 
 * `deprecated-checks/ldlpv_nn.py` -- a plain deep NN for NSE data
 * `deprecated-checks/ldlpv_pod.py` -- comparison to POD
 * `deprecated-checks/convterm_as_lpv.py` -- test/check: how to encode the convection term as LPV

# Topics in the data

## Shifted data for POD etc.

Shifting the data, by e.g. a mean value or the value at `t=0`, is needed to

 * have zero boundary conditions (otherwise, we can not simply superpose the vectors, e.g., in the computation of the convection matrices)

In `CNN_pod_check` the data is treated like

1. load the actual data vectors `vvecs`
1. define the shift `podshiftvec` and shift the vectors for the POD
1. provide `podshiftvec` to `NSEDataset` to henceforth load shifted vectors
1. use the shifted vectors as targets in the loss functions (no shifting when computing losses!) 
1. in the convection.... we will see
