import json

def get_json_from_file(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data