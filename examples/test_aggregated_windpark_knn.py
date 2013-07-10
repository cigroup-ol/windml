"""
Example: KNN Regression for a park
--------------------------------------------------

This example generates a forecast for a windpark in tehachapi.
The sum of all included mills is used: the measurements of all
mills are summed up and the park is treated like a single mill.
A KNN-regressor is trained with 18 months and tested on 6 months
"""

from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.get_feature_and_label_data_aggregated import get_feature_and_label_data_aggregated
from windml.datasets.park_definitions import park_info

from sklearn import neighbors
import math
import matplotlib.pyplot as plt

name = 'tehachapi'
radius1=3
k_neighbors = 25
feature_window = 3
horizon = 3

my_windpark1 = get_nrel_windpark(park_info[name][0], radius1, 2004, 2005)
X,Y = get_feature_and_label_data_aggregated(my_windpark1,feature_window,horizon)


number = len(my_windpark1.mills)


#knn regression
knn = neighbors.KNeighborsRegressor(k_neighbors, 'uniform')
train_to=int(math.floor(len(X)*0.1))
#test_to=len(X)-1
test_to = train_to+28800
train_step=1


print "knn training"
reg = knn.fit(X[0:train_to:train_step],Y[0:train_to:train_step])
print "knn predicting"
y_ = reg.predict(X[train_to:test_to])
naive = []
times = []
for i in range(0, len(y_)):
    #y_[i] = min(max(0,y_[i]),30*number)
    times.append(i)
    naive.append(Y[i+train_to-horizon])
#  y_[i] = 0.75*y_[i] + 0.25*naive[-1]


sum_err_pred = 0.0
sum_err_naiv = 0.0
for i in range(0, test_to-train_to):
#    print y_[i], Y[i+train_to]
    sum_err_pred+=(y_[i]-Y[i+train_to])**2
    sum_err_naiv+=(naive[i]-Y[i+train_to])**2
print "sum of square err of prediction", sum_err_pred
print "sum of square err of naive approach", sum_err_naiv


plt.grid(True)
plt.xlabel("Timesteps")
plt.ylabel("Corrected Score (MW)")
plt.plot(times, Y[train_to:test_to], 'g-', label='measured')
plt.plot(times, y_, 'b-', label='predicted')
plt.plot(times, naive, 'r-', label='naive')
plt.legend(loc='lower right')
plt.show()

