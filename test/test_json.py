# from phpserialize import serialize, unserialize
import json
a2 = {'loginip': '127.0.0.1', 'uid': 96, 'loginfrom': 4, 'logintime': 1317200595}

str = json.dumps(a2)

print (str)

a1 = json.loads(str)

print()
print (a2)
print()
print (a1)
print (a1['loginip'])
print (a1)