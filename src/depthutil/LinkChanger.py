from src.main.Module import Module
from src.utility.Config import Config

class LinkChanger(Module):
    def __init__(self, config):
        Module.__init__(self, config)
        
    def run(self):
        set_params = {}
        sel_objs = {}
        for key in self.config.data.keys():
            # if its not a selector -> to the set parameters dict
            if key != 'selector':
                set_params[key] = self.config.data[key]
            else:
                sel_objs[key] = self.config.data[key]
        # create Config objects
        params_conf = Config(set_params)
        sel_conf = Config(sel_objs)
        materials = sel_conf.get_list("selector")
        # materials = Material.convert_to_materials(materials)

        for material in materials:
            self._change_link(material, params_conf)

        
    def _change_link(self, material, params_conf):
        output_node_name = params_conf.get_string("output_node_name", "ShaderNodeTexCoord")
        output_node_create = params_conf.get_bool("output_node_create", False)        
        output_link_type = params_conf.get_string("output_link_type", "Generated")
        input_node_name = params_conf.get_string("input_node_name", "Image Texture") 
        input_node_create = params_conf.get_bool("input_node_create", False)
        input_node_unlink = params_conf.get_bool("input_node_unlink", False)
        input_link_type = params_conf.get_string("input_link_type", "Vector")

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        if input_node_unlink:
            input_node = nodes.get(input_node_name)
            link = input_node.inputs[input_link_type].links
            for l in link:
                links.remove(l)
		
        else:
            if output_node_create:
                output_node = nodes.new(output_node_name)
            else:
                output_node = nodes.get(output_node_name)

            if input_node_create:
                input_node = nodes.new(input_node_name)
            else:
                input_node = nodes.get(input_node_name)

            links.new(output_node.outputs[output_link_type], input_node.inputs[input_link_type])