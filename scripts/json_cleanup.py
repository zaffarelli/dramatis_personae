import json

#  exec(open('scripts/json_cleanup.py').read())

filename = './scripts/toto.json'
filename_out = './scripts/new_toto.json'
sorted_out_data = []

with open(filename, "r") as f:
    data = json.load(f)
    for elem in data:
        if elem["program"] == "BREMEN":
            sorted_out_data.append(elem)
    f.close()
print(sorted_out_data, len(sorted_out_data))
if len(sorted_out_data) > 0:
    with open(filename_out, "w") as f_o:
        json.dump(sorted_out_data, f_o)
        f_o.close()