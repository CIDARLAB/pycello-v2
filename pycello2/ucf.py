__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


class Gate:

    def __init__(self):
        self.name = ""
        self.promoter = ""

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def promoter(self):
        return self.__promoter

    @promoter.setter
    def promoter(self,promoter):
        self.__promoter = promoter

    @property
    def parts(self):
        return self.__parts

    @parts.setter
    def parts(self,parts):
        self.__parts = parts

    @property
    def equation(self):
        return self.__equation

    @equation.setter
    def equation(self,equation):
        self.__equation = equation

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self,parameters):
        self.__parameters = parameters

    @property
    def variables(self):
        return self.__variables

    @variables.setter
    def variables(self,variables):
        self.__variables = variables

class Part:

    def __init__(self):
        self.name = ""
        self.type = ""
        self.sequence = ""

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self,type):
        self.__type = type

    @property
    def sequence(self):
        return self.__sequence

    @sequence.setter
    def sequence(self,sequence):
        self.__sequence = sequence

class Terminator(Part):
    
    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self,strength):
        self.__strength = strength

class Ribozyme(Part):
    
    @property
    def efficiency(self):
        return self.__efficiency

    @efficiency.setter
    def efficiency(self,efficiency):
        self.__efficiency = efficiency

class UCF:

    def __init__(self,ucf):
        self.parts = []
        self.gates = []
        for coll in ucf:
            if coll['collection'] == 'parts':
                if coll['type'] == 'terminator':
                    part = Terminator()
                elif coll['type'] == 'ribozyme':
                    part = Ribozyme()
                else:
                    part = Part()
                part.name = coll['name']
                part.type = coll['type']
                part.sequence = coll['dnasequence']
                self.parts.append(part)
        for coll in ucf:
            if coll['collection'] == 'terminators':
                terminator = self.part(coll['name'])
                terminator.strength = coll['strength']
            if coll['collection'] == 'ribozymes':
                ribozyme = self.part(coll['name'])
                ribozyme.efficiency = coll['efficiency']
            if coll['collection'] == 'gate_parts':
                gate = Gate()
                gate.name = coll['gate_name']
                gate.promoter = self.part(coll['promoter'])
                parts = []
                for part in coll['expression_cassettes'][0]['cassette_parts']:
                    parts.append(self.part(part))
                gate.parts = parts
                self.gates.append(gate)
            if coll['collection'] == 'input_sensors':
                sensor = Gate()
                sensor.name = coll['name']
                sensor.promoter = self.part(coll['promoter'])
                parts = []
                for part in coll['parts']:
                    parts.append(self.part(part))
                sensor.parts = parts
                self.gates.append(sensor)
            if coll['collection'] == 'output_reporters':
                reporter = Gate()
                reporter.name = coll['name']
                parts = []
                for part in coll['parts']:
                    parts.append(self.part(part))
                reporter.parts = parts
                self.gates.append(reporter)
        for coll in ucf:
            if coll['collection'] == 'response_functions':
                gate = self.gate(coll['gate_name'])
                gate.equation = coll['equation']
                parameters = {}
                for param in coll['parameters']:
                    parameters[param['name']] = param['value']
                gate.parameters = parameters
                variables = []
                for var in coll['variables']:
                    variables.append(var['name'])
                gate.variables = variables
            
    @property
    def parts(self):
        return self.__parts

    @parts.setter
    def parts(self,parts):
        self.__parts = parts

    def part(self,name):
        for part in self.parts:
            if part.name == name:
                return part

    @property
    def gates(self):
        return self.__gates

    @gates.setter
    def gates(self,gates):
        self.__gates = gates

    def gate(self,name):
        for gate in self.gates:
            if gate.name == name:
                return gate
            
