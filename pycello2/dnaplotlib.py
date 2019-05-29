from . import netlist as pycello2_netlist

__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


def get_cds(component):
    for part_instance in component.parts:
        if part_instance.part.type == 'cds':
            return part_instance


def get_designs(netlist):
    color_map = {'YFP': 'white'}
    dpl_designs = []
    for placement in netlist.placements:
        it = iter(['C' + str(i) for i in range(10)])
        dpl_design = []
        dpl_designs.append(dpl_design)
        for group in placement.groups:
            dpl_group = []
            dpl_design.append(dpl_group)
            seq_len = 0
            for component in group.components:
                for part_instance in component.parts:
                    seq_len += len(part_instance.part.sequence)
                    if part_instance.part.type == 'cds':
                        if part_instance.part.name in color_map:
                            part_instance.color = color_map[part_instance.part.name]
                        else:
                            color = next(it)
                            color_map[part_instance.part.name] = color
                            part_instance.color = color
            start = 0
            for i, component in enumerate(group.components):
                for j, part_instance in enumerate(component.parts):
                    extent = len(part_instance.part.sequence)
                    if part_instance.part.type == 'promoter':
                        upstream = pycello2_netlist.get_upstream_node(part_instance.part, component.node, netlist)
                        color = 'black'
                        if (upstream):
                            upstream_components = pycello2_netlist.get_components(upstream, placement)
                            if (len(upstream_components)):
                                cds = pycello2_netlist.get_cds(upstream_components[0])
                                color = cds.color
                        part = {'type': 'Promoter',
                                'fwd': True,
                                'start': start,
                                'end': start + extent,
                                'opts': {'color': color,
                                         'x_extent': 100}}
                    if part_instance.part.type == 'cds':
                        part = {'type': 'CDS',
                                'fwd': True,
                                'opts': {'color': part_instance.color,
                                         'label': part_instance.part.name,
                                         'label_y_offset': -3,
                                         'arrowhead_height': 0,
                                         'arrowhead_length': 5 + seq_len/100},
                                'start': start,
                                'end': start + extent}
                    if part_instance.part.type == 'terminator':
                        part = {'type': 'Terminator',
                                'fwd': True,
                                'start': start,
                                'end': start + extent,
                                'opts': {'color': 'black', 'x_extent': 2 + seq_len/100}}
                    if part_instance.part.type == 'ribozyme':
                        part = {'type': 'Ribozyme',
                                'fwd': True,
                                'start': start,
                                'end': start + extent,
                                'color': 'black'}
                    if part_instance.part.type == 'rbs':
                        part = {'type': 'RBS',
                                'fwd': True,
                                'start': start,
                                'end': start + extent,
                                'opts': {'color': 'black', 'x_extent': 40}}
                    start += extent + 1
                    dpl_group.append(part)
    return dpl_designs
