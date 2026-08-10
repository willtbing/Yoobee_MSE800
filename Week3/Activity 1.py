from ucimlrepo import fetch_ucirepo 
  
# fetch dataset 
iris = fetch_ucirepo(id=53) 
  
# data (as pandas dataframes) 
X = iris.data.features 
y = iris.data.targets 

print("The total number of records in the file.")
print(len(X))
print("The total number of different flower available.")
print(y['class'].nunique())
print("The names of all different flowers in the dataset.")
print(y['class'].unique().tolist())