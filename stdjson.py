# Turns a Python-formatted JSON into a standard-formatted JSON
def standard_json(string):
    return string.replace("'", '"').replace("False", "false").replace("True", "true").replace("None", "null")


print(standard_json("python json string"))
