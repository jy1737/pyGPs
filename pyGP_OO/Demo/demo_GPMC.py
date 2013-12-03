from pyGP_OO.Core import *
from pyGP_OO.Valid import valid
import numpy as np
from scipy.io import loadmat


# To have a gerneral idea, 
# you may want to read demo_GPR, demo_kernel and demo_optimization first!
# Here, the focus is on multi-class classification.

print ''
print '-------------------GPMC DEMO----------------------'

# GMPC is NOT real multi-class GP classification
# It works as a one vs. one mult-classification wrapper

# i.e. GPMC trains GPC model for each combinations of two classes
# and uses voting scheme over all results to determine the final class

# It only returns the predictive class with highest rating, 
# but no other property values returned

# Lets see a practical example to classify 10(0~9) hand-writen digits,
# using USPS digits dataset.


#----------------------------------------------------------------------
# Load USPS digits dataset
#----------------------------------------------------------------------
data = loadmat('data_for_demo/usps_resampled.mat')
x = data['train_patterns'].T   # train patterns
y = data['train_labels'].T     # train labels
xs = data['test_patterns'].T   # test patterns
ys = data['test_labels'].T     # test labels   

# To be used in GPMC, we need to change label to integer from 0 to n
# here, class value should be 0,1,...,9.
y = np.argmax(y, axis=1)
y = np.reshape(y, (y.shape[0],1))

ys = np.argmax(ys, axis=1)
ys = np.reshape(ys, (ys.shape[0],1))

# To save some time for demo, 
# lets reduce the number of training and testing patterns
x  = x[:100,:]
y  = y[:100,:]
xs = xs[:20,:]
ys = ys[:20,:]


#----------------------------------------------------------------------
# GPMC example
#----------------------------------------------------------------------

# State model with 10 classes
model = gp.GPMC(10)

# Set data to model
model.setData(x,y)

# Train default GPC model for each binary classification problem, 
# and decide label for test patterns of hand-writen digits
y_predict = model.trainAndPredict(xs)

# Accuracy of recognized digit
acc = valid.ACC(y_predict, ys)
print "Accuracy of recognizing hand-writen digits:", round(acc,2)


#----------------------------------------------------------------------
# A bit more things you can do
#----------------------------------------------------------------------
# Just like we did for GP classification
# You can use specify the setting by:
m = mean.Zero()
k = cov.RBF()
model.setPrior(mean=m,kernel=k)
model.useLaplace()

# Beside trainAndPredict(xs),
# there is also an option to predict without optimization
# model.fitAndPredict(xs)


