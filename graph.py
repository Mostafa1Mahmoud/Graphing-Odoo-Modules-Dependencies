import os
import sys

import networkx as nx
import matplotlib.pyplot as plt
   
  
# Defining a Class
class GraphVisualization:

    def __init__(self) -> None:
        self.visual = []

    def addEdge(self, item):
        self.visual.append(item)
   
    def visualize(self, graph=False, direction='dependency'):
        directed_graph = {}
        for module_name ,module_values in graph.items() if isinstance(graph, dict) else []:
            directed_graph[module_name] = module_values[direction] 
        G = nx.DiGraph(directed_graph if isinstance(graph, dict) else graph if graph else self.visual)
        nx.draw_networkx(G)
        plt.show()

Graph = GraphVisualization()

graph_edges = []
graph = {}

def recursive_dfs(graph, start_node, end_node=False, incoming_list=[], direction='dependency'):
    if end_node and start_node == end_node:
        # print(incoming_list)
        return incoming_list
    graph_edges = []
    for module in graph[start_node][direction]:
        if direction == 'dependent':
            graph_edges += recursive_dfs(graph, module, end_node, incoming_list + [(module, start_node)], direction=direction)
        else:
            graph_edges += recursive_dfs(graph, module, end_node, incoming_list + [(start_node, module)], direction=direction)
    return graph_edges

def dfs(graph, start_node, direction='dependency'):
    stack = []
    stack.append(start_node)
    while stack:
        # print(stack, direction)
        stack_top = stack.pop()
        for module in graph[stack_top][direction]:
            if direction == 'dependent':
                print((module, stack_top, graph[module]['dependency']))
                Graph.addEdge((module, stack_top))
            else:
                print((stack_top, module, graph[module]['dependent']))
                Graph.addEdge((stack_top, module))
            stack.append(module)


if __name__ == '__main__':

    if "--paths" in sys.argv:
        paths_index = sys.argv.index("--paths") + 1
    elif "-p" in sys.argv:
        paths_index = sys.argv.index("-p") + 1
    else:
        paths_index = -1
    
    if "--start" in sys.argv:
        start_index = sys.argv.index("--start") + 1
    elif "-s" in sys.argv:
        start_index = sys.argv.index("-s") + 1
    else:
        start_index = -1
    
    if "--end" in sys.argv:
        end_index = sys.argv.index("--end") + 1
    elif "-e" in sys.argv:
        end_index = sys.argv.index("-e") + 1
    else:
        end_index = -1
    
    if "--direction" in sys.argv:
        direction_index = sys.argv.index("--direction") + 1
    elif "-d" in sys.argv:
        direction_index = sys.argv.index("-d") + 1
    else:
        direction_index = -1

    count__valid_modules = 0
    INDEX_OF_FIRST_ELEMENT = 0
    DPENDPS_KEY = 'depends'
    STARTING_MODULE = sys.argv[start_index] if start_index != -1 else False
    ENDING_MODULE = sys.argv[end_index] if end_index != -1 else False
    DIRECTION = sys.argv[direction_index] if direction_index != -1 else False
    dircetion_value = 'dependent' if DIRECTION and DIRECTION != 'down' else 'dependency'
    project_paths = sys.argv[paths_index].split(',')

    print(project_paths)

    for project_path in project_paths:
        
        try:
            os.chdir(project_path)
        except OSError:
            print(project_path, "Is Not a valid path you may have a typo!")
        else:
            print("Current dir: ", project_path)

        print("Number of expected Modules: ", len(os.listdir()), "Module in the current project")

        for module in os.listdir():
            if module[INDEX_OF_FIRST_ELEMENT] == '.':
                continue
            # print(module,": ")
            try:
                items = os.listdir('./'+module)
            except OSError:
                # print("Not a valid module")
                pass
            else:
                count__valid_modules += 1
                for item in items:
                    if item == '__manifest__.py':
                        # print('\t'+module+'/'+item)
                        if not graph.get(module, False):
                            graph[module] = {'dependency': [], 'dependent': []}
                        with open('./'+module+'/__manifest__.py') as manifest:
                            manifest_content = manifest.read()
                            module_dependencies = eval(manifest_content).get(DPENDPS_KEY)
                            if not module_dependencies:
                                continue
                            for dependency in module_dependencies:
                                graph[module]['dependency'].append(dependency)
                                if not graph.get(dependency, False):
                                    graph[dependency] = {'dependency': [], 'dependent': []}
                                graph[dependency]['dependent'].append(module)
                        
    print("Number of actual Modules: ", count__valid_modules, "Module in all projects")
    if STARTING_MODULE:
        if STARTING_MODULE and graph.get(STARTING_MODULE, False):
            if ENDING_MODULE and graph.get(ENDING_MODULE, False):
                graph_edges = recursive_dfs(graph, STARTING_MODULE, ENDING_MODULE, direction=dircetion_value)
                print(graph_edges)
                Graph.visualize(graph_edges)
            elif ENDING_MODULE:
                print("The name of the ending module is not found in the given directories")
            else:
                dfs(graph, STARTING_MODULE, dircetion_value)
                Graph.visualize()
        else:
            print("The name of the starting module is not found in the given directories")
    else:
        Graph.visualize(graph, direction=dircetion_value)
