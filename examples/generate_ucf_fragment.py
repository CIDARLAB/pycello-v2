import json
import pycello.target_data as td

sensors = [
    {"name": "Ara",   "promoter": "PBadmc", "ymin": 0.04, "ymax": 3.33, "dnasequence": "AACGATCGTTGGCTGTAGCATTTTTATCCATAAGATTAGCGGATCCTACCTGACGCTTTTTATCGCAACTCTCTATATTTTTCTCCATACCCG"},
    {"name": "IPTG",  "promoter": "PTac",   "ymin": 0.02, "ymax": 4.20, "dnasequence": ""},
    {"name": "aTc",   "promoter": "PTet",   "ymin": 0.02, "ymax": 5.41, "dnasequence": "AACGATCGTTGGCTGTCCCTATCAGTGATAGAGATTGACATCCCTATCAGTGATAGATATAATGAGCAC"},
    {"name": "Cuma",  "promoter": "PCymRC", "ymin": 0.19, "ymax": 2.39, "dnasequence": "TTCCGATGTAGGAGTAACAAACAGACAATCTGGTCTGTTTGTATTATGGAAAATTTTTCTGTATAATAGATTC"},
    {"name": "Van",   "promoter": "PVanCC", "ymin": 0.02, "ymax": 3.79, "dnasequence": ""},
    {"name": "OHC14", "promoter": "PCin",   "ymin": 0.01, "ymax": 4.38, "dnasequence": "TGGTAGCACAAAAGTCCCTTTGTGCGTCCAAACGGACGCACGGCGCTCTAAAGCGGGTCGCGATCTTTCAGATTCGCTCCTCGCGCTTTCAGTCTTTGTTTTGGCGCATGTCGTTATCGCAAAACCGCTGCACACTTTTGCGCGACATGCTCTGATCCCCCTCATCTGGGGGGGCCTATCTGAGGGAATTTCCGATCCGGCTCGCCTGAACCATTCTGCT"},
    {"name": "Nar",   "promoter": "PTtg",   "ymin": 0.01, "ymax": 0.22, "dnasequence": "TACGCTGCCACGTGTCACCCAGCAGTATTTACAAACAACCATGAATGTAAGTATATTCCTTAGCAA"}
]

obj = []

for sensor in sensors:
    i = td.InputSensor()
    i.name = sensor["name"] + "_sensor"
    i.model = sensor["name"] + "_sensor_model"
    i.structure = sensor["name"] + "_sensor_structure"
    obj.append(i)
    m = td.Model()
    m.name = i.model
    m.functions = {"response_function": "sensor_response"}
    ymax = td.Parameter()
    ymax.name = "ymax"
    ymax.value = sensor["ymax"]
    ymax.description = "Maximal transcription"
    ymin = td.Parameter()
    ymin.name = "ymin"
    ymin.value = sensor["ymin"]
    ymin.description = "Minimal transcription"
    m.parameters = [ymax, ymin]
    obj.append(m)
    s = td.Structure()
    s.name = i.structure
    s.outputs = [sensor["promoter"]]
    obj.append(s)
    p = td.Part()
    p.name = sensor["promoter"]
    p.type = "promoter"
    p.dnasequence = sensor["dnasequence"]
    obj.append(p)

f = td.Function()
f.name = "sensor_response"
f.equation = "$STATE * (ymax - ymin) + ymin"
ymax = td.Parameter()
ymax.name = "ymax"
ymax.map = "#//model/parameters/ymax"
ymin = td.Parameter()
ymin.name = "ymin"
ymin.map = "#//model/parameters/ymin"
f.parameters = [ymax, ymin]
obj.append(f)

print(json.dumps(obj, cls=td.JSONPropertyEncoder, indent=4))
