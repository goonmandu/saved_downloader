import json

# Turns a Python-formatted JSON into a standard-formatted JSON
def standard_json(string):
    return string.replace("'", '"').replace("False", "false").replace("True", "true").replace("None", "null")

t = ""
print(standard_json(t))

