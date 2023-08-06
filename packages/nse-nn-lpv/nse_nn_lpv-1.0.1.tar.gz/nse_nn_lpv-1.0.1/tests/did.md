## 2021-05-29 08:19:47+02:00

 * `nse_data_matrix.py` + `CNN_AE.py` can be run
 * the CNN is not applied yet
 * need to apply it to the data

## 2021-06-05 07:39:59+02:00

 * `test_conv2d.py` has one step with real data
 * DONE: apply the full chain as in `CNN_AE.py`
   * make it 2D in `CNN_AE.py`

## 2021-06-05 14:07:29+02:00

 * PLAN: Check nonsquare kernels and strides to account for flow direction
 * Q: What about pooling?
   * no particular mention in Lee/Carlberg
 * `CNN_AE` encoder "works"
 * DONE: script it for dynamic setup
   * compute the size of the full connected layers by the formulas here:
   * https://pytorch.org/docs/1.8.1/generated/torch.nn.Conv2d.html#torch.nn.Conv2d

## 2021-06-07 10:46:56+02:00

 * scripted the encoder CNN layers via their channel numbers

## 2021-06-17 07:53:56+02:00

 * now decoding working too
 * TODO: check the reshape -- it should preserve the data order
 * NEXT: train the network
 * NOTE: can only use particular input shapes so that encode/decode returns the same shape

## 2021-06-18 11:06:38+02:00

 * TODO: Improve the architecture 
 * Better loss function
 * TODO: how to include custom loss functions
   * thought of a weighted L2 norm, but this would require an interpolation back into the FEM space
   * Lee/Carlberg use mean squared error too
   * won't touch this at the moment


## 2021-06-23 16:46:40+02:00

 * `#training`
   * Lee/Carlberg have very small dimensions like 65x32
     * training/data:
       * 64 parameter instances x 600 time steps = 38400 data points
       * mini batches of size 20
       * up to 5000 epochs (with early stopping)
     * ADAM with learning rate `1e-4`
     * and He initialization

   * TODO: check smaller dimensions
   * TODO: check more data
   * TODO: check optimizer
   * TODO: test for different architecture (layers, filters, kernels)
   * TODO: scaling of the grid to better account for important regions

 * `visualization`
   * get a picture of the output
   * visualize the feature maps
   * TODO: plot the output

## 2021-06-29 11:43:53+02:00

 * TODO: check [KimCWZ20](https://arxiv.org/pdf/2011.07727.pdf) -- full layers with sparsity masks
 * TODO: scaling! --- remove the mean 
   * have a function that prepares the data
   * comp the mean in the vel data
   * provide centered (and scaled?) pics
 * TODO: scaling! --- check with POD -- can use both?
 * TODO: nonzero boundary conditions

## 2021-07-06 19:33:40+02:00

 * TODO: unit test with reshaping in myloss (stack two vecs -- get double val)

## 2021-07-08 17:37:27+02:00

 * data for the talk -- found a working setup 

## 2021-08-28 08:15:51+02:00

 * min/max functionality is there 
 * DONE: use it for scaling
 * the dicts of data should have a key `'velmaxima'` -- use it!

## 2021-08-30 14:00:54+02:00

 * yes the maxima are there -- I called them `vxmin` etc
 * DONE: pass the `velmaxima` dict from `vlctflddata` to `nse_data_helpers`

## 2021-09-21 09:45:48+02:00

 * started with naming for saving the models later
 * cp. https://pytorch.org/tutorials/beginner/saving_loading_models.html

## 2021-09-22 07:45:23+02:00

 * DONE: started outsourcing the training of the model
 * then saving/loading is more explicit
 * THERE: unit test for the `myloss`
 * TODO: save model and optimizer state
 * DONE: save model

## 2021-10-07 11:00:36+02:00

 * almost done with saving
   * save/load doesn't quite work
   * seems to save the enc as just one linear layer
   * TODO: check where are the conv layers
   * MAYBE: problems with the dynamic definition
   * DONE: now we have a more explicit but more static definition 
 * need for the model use/check
   * function that turns `velvec` into `tensor`
     * the scaling --> `data_parameters`
   * needed anyways later but checking now only in the same file (too much to transfer)
 * IDEA: if only the `code_size` changes, we can reuse the states

## 2021-10-18 19:14:19+02:00

 * undid Sarvin's workaround around the nested layers
 * working: extracting the convlayers for plotting feature maps
 * https://debuggercafe.com/visualizing-filters-and-feature-maps-in-convolutional-neural-networks-using-pytorch/

## 2021-10-20 12:50:03+02:00

 * IDEA: decode with convolutions but without activation -- should be linear too

## 2021-11-24 17:50:52+01:00

 * testing the `convPODLoss` so far it does what it should -- need to sort out the terms
 * DONE: check the convection POD base (for the M-1 norm comp)
 * DONE: tensorize it and make it an `nn.Module`

## 2022-01-06 07:33:27+01:00

 * convection all done 
 * TODO: plan simus
 * CHECK: CNN-decode with or without activation -- may lead to blowups -- use normalizing the data

## 2022-01-06 13:49:27+01:00

 * TODO: saving podvecs independent of datadim 
 * TODO: double cylinder
 * IDEA: cache the state of lowest training error (since the error is not monotone)

## 2022-01-17 11:48:41+01:00

 * CNN performs poorly on the initial values -- have more of them in the training sets
