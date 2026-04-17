import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import numpy as np

print("Starting model training...")

# load dataset
data = pd.read_csv("train.csv")

# features
X = data[['GrLivArea','BedroomAbvGr','FullBath','GarageCars']]
y = data['SalePrice']

# model
model = RandomForestRegressor(n_estimators=100)
model.fit(X,y)

# save model
pickle.dump(model, open("model.pkl","wb"))

# create stats
mean_val = np.mean(y)
std_val = np.std(y)

stats = {
    "mean": float(mean_val),
    "std": float(std_val)
}

# save stats
pickle.dump(stats, open("stats.pkl","wb"))

print("✅ model.pkl created")
print("✅ stats.pkl created")