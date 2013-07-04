"""
Example: KNN Regression 
--------------------------------------------------

This example generates a forecast for one windmill in Tehachapi.
A KNN-regressor is trained with 18 months and tested on 6 months 

"""
from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.get_feature_and_label_data import get_feature_and_label_data
from sklearn import neighbors
import math
import matplotlib.pyplot as plt
park_indices = {'tehachapi': 4155, 'alfred': 7139}
radius=50
k_neighbors = 50
feature_window = 3 
horizon = 3 

my_windpark = get_nrel_windpark(park_indices['tehachapi'], radius, 2004, 2005)
X,Y = get_feature_and_label_data(my_windpark,feature_window,horizon)

#knn regression
knn = neighbors.KNeighborsRegressor(k_neighbors, 'uniform')
train_to=int(math.floor(len(X)*0.75))
test_to=len(X)-1
train_step=1

print "knn training"
reg = knn.fit(X[0:train_to:train_step],Y[0:train_to:train_step])
print "knn predicting"
y_ = reg.predict(X[train_to:test_to])
naive = []
times = []
for i in range(0, test_to-train_to):
    times.append(i)
    naive.append(Y[i+train_to-horizon])

plt.ylabel("Corrected Score (MW)")
plt.plot(times, Y[train_to:test_to], 'g-')
plt.plot(times, y_, 'b-')
plt.plot(times, naive, 'r-')
plt.show()

sum_err_pred = 0.0
sum_err_naiv = 0.0
for i in range(0, test_to-train_to):
#    print y_[i], Y[i+train_to]
    sum_err_pred+=(y_[i]-Y[i+train_to])**2
    sum_err_naiv+=(naive[i]-Y[i+train_to])**2
print "sum of square err of prediction", sum_err_pred
print "sum of square err of naive approach", sum_err_naiv
