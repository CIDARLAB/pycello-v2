import json
import re
from collections.abc import Iterable

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class JSONPropertyEncoder(json.JSONEncoder):

    def dict_to_json(self, o):
        d = o.__dict__
        for key in list(d.keys()).copy():
            val = d.pop(key)
            d[re.sub(r"_\w+__", "", key)] = val
        return d

    def obj_to_json(self, o):
        if isinstance(o, Iterable):
            return [self.obj_to_json(o) for e in o]
        else:
            return self.dict_to_json(o)

    def default(self, o):
        return self.obj_to_json(o)


class Header:

    def __init__(self, obj=None):
        self.collection = "header"
        if obj:
            self.description = obj["description"]
            self.version = obj["version"]
            self.date = obj["date"]
            self.author = obj["author"]
            self.organism = obj["organism"]
            self.genome = obj["genome"]
            self.media = obj["media"]
            self.temperature = obj["temperature"]
            self.growth = obj["growth"]

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        self.__version = version

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author):
        self.__author = author

    @property
    def organism(self):
        return self.__organism

    @organism.setter
    def organism(self, organism):
        self.__organism = organism

    @property
    def genome(self):
        return self.__genome

    @genome.setter
    def genome(self, genome):
        self.__genome = genome

    @property
    def media(self):
        return self.__media

    @media.setter
    def media(self, media):
        self.__media = media

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, temperature):
        self.__temperature = temperature

    @property
    def growth(self):
        return self.__growth

    @growth.setter
    def growth(self, growth):
        self.__growth = growth


class MeasurementStd:

    def __init__(self, obj=None):
        self.collection = "measurement_std"
        if obj:
            self.signal_carrier_units = obj["signal_carrier_units"]
            self.normalization_instructions = obj["normalization_instructions"]
            self.plasmid_description = obj["plasmid_description"]
            if "plasmid_sequence" in obj:
                self.plasmid_sequence = obj["plasmid_sequence"]

    @property
    def signal_carrier_units(self):
        return self.__signal_carrier_units

    @signal_carrier_units.setter
    def signal_carrier_units(self, signal_carrier_units):
        self.__signal_carrier_units = signal_carrier_units

    @property
    def normalization_instructions(self):
        return self.__normalization_instructions

    @normalization_instructions.setter
    def normalization_instructions(self, normalization_instructions):
        self.__normalization_instructions = normalization_instructions

    @property
    def plasmid_description(self):
        return self.__plasmid_description

    @plasmid_description.setter
    def plasmid_description(self, plasmid_description):
        self.__plasmid_description = plasmid_description

    @property
    def plasmid_sequence(self):
        return self.__plasmid_sequence

    @plasmid_sequence.setter
    def plasmid_sequence(self, plasmid_sequence):
        self.__plasmid_sequence = plasmid_sequence


class LogicConstraints:

    def __init__(self, obj=None):
        self.collection = "logic_constraints"
        if obj:
            self.available_gates = obj["available_gates"]

    @property
    def available_gates(self):
        return self.__available_gates

    @available_gates.setter
    def available_gates(self, available_gates):
        self.__available_gates = available_gates


class LogicMotif:

    def __init__(self, obj=None):
        self.collection = "motif_library"
        if obj:
            self.inputs = obj["inputs"]
            self.netlist = obj["netlist"]
            self.outputs = obj["outputs"]

    @property
    def inputs(self):
        return self.__inputs

    @inputs.setter
    def inputs(self, inputs):
        self.__inputs = inputs

    @property
    def netlist(self):
        return self.__netlist

    @netlist.setter
    def netlist(self, netlist):
        self.__netlist = netlist

    @property
    def outputs(self):
        return self.__outputs

    @outputs.setter
    def outputs(self, outputs):
        self.__outputs = outputs


class Parameter:

    def __init__(self, obj=None):
        if obj:
            self.name = obj["name"]
            if "value" in obj:
                self.value = obj["value"]
            if "map" in obj:
                self.map = obj["map"]
            if "description" in obj:
                self.description = obj["description"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, map):
        self.__map = map

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description


class Variable:

    def __init__(self, obj=None):
        if obj:
            self.name = obj["name"]
            self.map = obj["map"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, map):
        self.__map = map


class Device:

    def __init__(self, obj=None):
        if obj:
            self.name = obj["name"]
            self.components = obj["components"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def components(self):
        return self.__components

    @components.setter
    def components(self, components):
        self.__components = components


class Input:

    def __init__(self, obj=None):
        if obj:
            self.name = obj["name"]
            self.part_type = obj["part_type"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def part_type(self):
        return self.__part_type

    @part_type.setter
    def part_type(self, part_type):
        self.__part_type = part_type


class AssignableDevice:

    def __init__(self):
        pass


class Gate(AssignableDevice):

    def __init__(self, obj=None):
        self.collection = "gates"
        if obj:
            self.name = obj["name"]
            self.regulator = obj["regulator"]
            self.group = obj["group"]
            self.gate_type = obj["gate_type"]
            self.system = obj["system"]
            if "color" in obj:
                self.color = obj["color"]
            self.model = obj["model"]
            self.structure = obj["structure"]

    # def __lt__(self, other):
    #     return self.name < other.name

    # def __gt__(self, other):
    #     return self.name > other.name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def regulator(self):
        return self.__regulator

    @regulator.setter
    def regulator(self, regulator):
        self.__regulator = regulator

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group):
        self.__group = group

    @property
    def gate_type(self):
        return self.__gate_type

    @gate_type.setter
    def gate_type(self, gate_type):
        self.__gate_type = gate_type

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, system):
        self.__system = system

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    @property
    def structure(self):
        return self.__structure

    @structure.setter
    def structure(self, structure):
        self.__structure = structure


class InputSensor(AssignableDevice):

    def __init__(self, obj=None):
        self.collection = "input_sensors"
        if obj:
            self.name = obj["name"]
            self.model = obj["model"]
            self.structure = obj["structure"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    @property
    def structure(self):
        return self.__structure

    @structure.setter
    def structure(self, structure):
        self.__structure = structure


class OutputDevice(AssignableDevice):

    def __init__(self, obj=None):
        self.collection = "output_devices"
        if obj:
            self.name = obj["name"]
            self.model = obj["model"]
            self.structure = obj["structure"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    @property
    def structure(self):
        return self.__structure

    @structure.setter
    def structure(self, structure):
        self.__structure = structure


class Model:

    def __init__(self, obj=None):
        self.collection = "models"
        if obj:
            self.name = obj["name"]
            self.functions = obj["functions"]
            self.parameters = obj["parameters"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def functions(self):
        return self.__functions

    @functions.setter
    def functions(self, functions):
        self.__functions = functions

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters):
        self.__parameters = parameters


class Structure:

    def __init__(self, obj=None):
        self.collection = "structures"
        if obj:
            self.name = obj["name"]
            self.inputs = []
            for o in obj["inputs"]:
                self.inputs.append(Input(o))
            self.outputs = obj["outputs"]
            self.devices = []
            for o in obj["devices"]:
                self.devices.append(Device(o))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def inputs(self):
        return self.__inputs

    @inputs.setter
    def inputs(self, inputs):
        self.__inputs = inputs

    @property
    def outputs(self):
        return self.__outputs

    @outputs.setter
    def outputs(self, outputs):
        self.__outputs = outputs

    @property
    def devices(self):
        return self.__devices

    @devices.setter
    def devices(self, devices):
        self.__devices = devices


class Function:

    def __init__(self, obj=None):
        self.collection = "functions"
        if obj:
            self.name = obj["name"]
            if "equation" in obj:
                self.equation = obj["equation"]
            if "table" in obj:
                self.table = obj["table"]
            if "variables" in obj:
                self.variables = obj["variables"]
            if "parameters" in obj:
                self.parameters = obj["parameters"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def equation(self):
        return self.__equation

    @equation.setter
    def equation(self, equation):
        self.__equation = equation

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, table):
        self.__table = table

    @property
    def variables(self):
        return self.__variables

    @variables.setter
    def variables(self, variables):
        self.__variables = variables

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters):
        self.__parameters = parameters


class Part:

    def __init__(self, obj=None):
        self.collection = "parts"
        if obj:
            self.name = obj["name"]
            self.type = obj["type"]
            self.dnasequence = obj["dnasequence"]
            if "parameters" in obj:
                self.parameters = []
                for o in obj["parameters"]:
                    self.parameters.append(Parameter(o))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def dnasequence(self):
        return self.__dnasequence

    @dnasequence.setter
    def dnasequence(self, dnasequence):
        self.__dnasequence = dnasequence

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters):
        self.__parameters = parameters


class TargetDataFile:

    def __init__(self, ucf):
        for coll in ucf:
            if coll['collection'] == 'header':
                self.header = Header(coll)
            elif coll['collection'] == 'measurement_std':
                self.measurement_std = MeasurementStd(coll)
            elif coll['collection'] == 'logic_constraints':
                self.logic_constraints = LogicConstraints(coll)
            elif coll['collection'] == 'motif_library':
                if not hasattr(self, "motif_library"):
                    self.motif_library = []
                self.motif_library.append(LogicMotif(coll))
            elif coll['collection'] == 'gates':
                if not hasattr(self, "gates"):
                    self.gates = []
                self.gates.append(Gate(coll))
            elif coll['collection'] == 'input_sensors':
                if not hasattr(self, "input_sensors"):
                    self.input_sensors = []
                self.input_sensors.append(InputSensor(coll))
            elif coll['collection'] == 'output_devices':
                if not hasattr(self, "output_devices"):
                    self.output_devices = []
                self.output_devices.append(OutputDevice(coll))
            elif coll['collection'] == 'models':
                if not hasattr(self, "models"):
                    self.models = []
                self.models.append(Model(coll))
            elif coll['collection'] == 'structures':
                if not hasattr(self, "structures"):
                    self.structures = []
                self.structures.append(Structure(coll))
            elif coll['collection'] == 'functions':
                if not hasattr(self, "functions"):
                    self.functions = []
                self.functions.append(Function(coll))
            elif coll['collection'] == 'parts':
                if not hasattr(self, "parts"):
                    self.parts = []
                self.parts.append(Part(coll))
            elif coll['collection'] == 'circuit_rules':
                self.circuit_rules = coll
            elif coll['collection'] == 'device_rules':
                self.device_rules = coll
            elif coll['collection'] == 'genetic_locations_rules':
                self.genetic_locations_rules = coll
        for model in self.models:
            for f in list(model.functions.keys()):
                for g in self.functions:
                    if model.functions[f] == g.name:
                        model.functions[f] = g
        for structure in self.structures:
            outputs = []
            for output in structure.outputs:
                for part in self.parts:
                    if output == part.name:
                        outputs.append(part)
            structure.outputs = outputs
            names = []
            for device in structure.devices:
                names.append(device.name)
            for device in structure.devices:
                components = []
                for component in device.components:
                    if not component.startswith("#"):
                        if component not in names:
                            for part in self.parts:
                                if component == part.name:
                                    components.append(part)
                        else:
                            for d in structure.devices:
                                if component == d.name:
                                    components.append(d)
                    else:
                        for i in structure.inputs:
                            if component.lstrip("#") == i.name:
                                components.append(i)
                device.components = components
        devices = []
        if hasattr(self, "gates"):
            devices += self.gates
        if hasattr(self, "input_sensors"):
            devices += self.input_sensors
        if hasattr(self, "output_devices"):
            devices += self.output_devices
        for device in devices:
            for model in self.models:
                if device.model == model.name:
                    device.model = model
            for structure in self.structures:
                if device.structure == structure.name:
                    device.structure = structure

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header):
        self.__header = header

    @property
    def measurement_std(self):
        return self.__measurement_std

    @measurement_std.setter
    def measurement_std(self, measurement_std):
        self.__measurement_std = measurement_std

    @property
    def logic_constraints(self):
        return self.__logic_constraints

    @logic_constraints.setter
    def logic_constraints(self, logic_constraints):
        self.__logic_constraints = logic_constraints

    @property
    def motif_library(self):
        return self.__motif_library

    @motif_library.setter
    def motif_library(self, motif_library):
        self.__motif_library = motif_library

    @property
    def gates(self):
        return self.__gates

    @gates.setter
    def gates(self, gates):
        self.__gates = gates

    @property
    def input_sensors(self):
        return self.__input_sensors

    @input_sensors.setter
    def input_sensors(self, input_sensors):
        self.__input_sensors = input_sensors

    @property
    def output_devices(self):
        return self.__output_devices

    @output_devices.setter
    def output_devices(self, output_devices):
        self.__output_devices = output_devices

    @property
    def models(self):
        return self.__models

    @models.setter
    def models(self, models):
        self.__models = models

    @property
    def structures(self):
        return self.__structures

    @structures.setter
    def structures(self, structures):
        self.__structures = structures

    @property
    def functions(self):
        return self.__functions

    @functions.setter
    def functions(self, functions):
        self.__functions = functions

    @property
    def parts(self):
        return self.__parts

    @parts.setter
    def parts(self, parts):
        self.__parts = parts

    @property
    def circuit_rules(self):
        return self.__circuit_rules

    @circuit_rules.setter
    def circuit_rules(self, circuit_rules):
        self.__circuit_rules = circuit_rules

    @property
    def device_rules(self):
        return self.__device_rules

    @device_rules.setter
    def device_rules(self, device_rules):
        self.__device_rules = device_rules

    @property
    def genetic_locations(self):
        return self.__genetic_locations

    @genetic_locations.setter
    def genetic_locations(self, genetic_locations):
        self.__genetic_locations = genetic_locations
