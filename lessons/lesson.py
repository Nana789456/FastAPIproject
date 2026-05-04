d1 = {
    '1':4,
    '2':2,
    '3':1,
    '4':0,
}

def get_value(key):
    return d1[key]

def get_key(key):
    return key


print(d1.get('1'))


result = max(d1)
print(d1[result])
# print(type(result), max(d1, key=get_value))
print(type(result), max(d1, key=d1.get))
