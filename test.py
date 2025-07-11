import json

f = open('test.json')
try:
    json_file = json.load(f)
except json.JSONDecodeError as e:
    print(e.lineno)