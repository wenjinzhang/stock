import requests
import pickle
# r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=c0ab4jn48v6tv7n8k3e0')
# pickle.dump(r.json(), open("data.p", "wb"))

data = pickle.load( open( "data.p", "rb" ))
print(len(data))
for d in data:
    print(d, type(d))
    exit()