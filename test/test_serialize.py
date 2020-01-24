from phpserialize import serialize, unserialize
a2 = {'loginip': '127.0.0.1', 'uid': 96, 'loginfrom': 4, 'logintime': 1317200595}
str = serialize(a2)

print (str)
a1 = unserialize(str)

print()
print (a2)
print()
print (a1)