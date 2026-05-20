#linear regression
from sklearn.linear_model import LinearRegression              #y=mx+c straight line formula 
import numpy as np                                             #pattern
#training data                                                      x                   y           increase
X = np.array([[1], [2], [3], [4]])                               #1->2                  40->60      +20
y = np.array([40,60,70,80])                                      #2->3                  60->70      +10
#creating the model                                              #3->4                  70->80      +10
model = LinearRegression()                                      #avg increase =+15 per x
#training the model                                             #m=15
model.fit(X, y)                                                 #so the result was 95                       
#making predictions
result = model.predict([[5]])
print("Predicted value for input 5:", result)   
