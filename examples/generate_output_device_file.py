import json
import pycello.target_data as td

objects = [
    {"name": "YFP", "dnasequence": "AGCTGTCACCGGATGTGCTTTCCGGTCTGATGAGTCCGTGAGGACGAAACAGCCTCTACAAATAATTTTGTTTAATACTAGAGAAAGAGGAGAAATACTAGATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACAGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCTTCGGCTACGGCCTGCAATGCTTCGCCCGCTACCCCGACCACATGAAGCTGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCAATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTTAGCTACCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAAGCTCATGTATGTGTCTACGCGAGATTCTCGCCCGAGAACTTCTGCAAGGCACTGCTCTTGGCT"},
]

obj = []

for o in objects:
    d = td.OutputDevice()
    d.name = o["name"] + "_reporter"
    d.model = o["name"] + "_reporter_model"
    d.structure = o["name"] + "_reporter_structure"
    obj.append(d)
    m = td.Model()
    m.name = d.model
    m.functions = {
        "response_function": "linear_response",
        "input_composition": "linear_input_composition"
    }
    unit_conversion = td.Parameter()
    unit_conversion.name = "unit_conversion"
    unit_conversion.value = 1.0
    unit_conversion.description = "Unit conversion"
    m.parameters = [unit_conversion]
    obj.append(m)
    s = td.Structure()
    s.name = d.structure
    s.inputs = [
        {
            "name": "in1",
            "part_type": "promoter"
        },
        {
            "name": "in2",
            "part_type": "promoter"
        }
    ]
    s.devices = [
        {
            "name": "YFP_reporter",
            "components": [
                "#in2",
                "#in1",
                d.name + "_cassette"
            ]
        }
    ]
    obj.append(s)
    p = td.Part()
    p.name = d.name + "_cassette"
    p.type = "cassette"
    p.dnasequence = o["dnasequence"]
    obj.append(p)

f = td.Function()
f.name = "linear_response"
f.equation = "c * x"
x = td.Variable()
x.name = "x"
x.map = "#//model/functions/input_composition"
f.variables = [x]
c = td.Parameter()
c.name = "c"
c.map = "#//model/parameters/unit_conversion"
f.parameters = [c]
obj.append(f)

print(json.dumps(obj, cls=td.JSONPropertyEncoder, indent=4))
