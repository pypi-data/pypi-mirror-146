import json


def dict2json(filename, data):
    """
    filename: str
    data: dict to save
    """
    with open(filename, 'w') as f:
        json.dump(data, f)

def json2dict(filename):
    """
    filename: str
    """
    with open(filename) as f:
        data = json.load(f)
    f.close()
    return data


