#!/usr/bin/python
from time import sleep
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from random import random
import sys 
import json

#import pdb; pdb.set_trace()

WEIGHT = 'w'
TYPE = 'type'
NAME = 'n'

#Edges that represnet adjacency between nodes of the same level
SIMILAR_EDGE = 'pull'
#Edges that represnet contrains between nodes of the diffrent levels
#(i.e. The "feeder forces" mentioned in 3.3 of the paper)
DISSIMILAR_EDGE = 'push'
EDGE_STYLES = dict([(SIMILAR_EDGE, 'solid'), (DISSIMILAR_EDGE, 'dotted')])

#Example usage
def main():
  
  if len(sys.argv) != 2:
    print 'Must give a file name.'
    sys.exit();
  file = sys.argv[1]
  graph_json = json.load(open(file,'r'));
  
  nodes = graph_json['nodes']
  edges = graph_json['edges']
  print nodes
  graph = buildConstraintGraph(nodes, edges)

  #Get colors from paper algorithim  
  print 'Getting Colors...   ',
  hues = getColors(graph)
  colors = hues_to_rgb(hues)
  print 'Done.'  
  
  print 'Writing JSON',
  outfile = open(file.split('.')[0] + '_colors.json','w')
  json.dump(colors, outfile)
  outfile.close()
  print 'Done.'  
  
  displyConstraintGraph(graph, colors)
  
def hues_to_rgb(hues_map, lightness = .5, saturation = .5):
  colors = {}
  for node in hues_map.keys():
    colors[node] = HSL_to_RGB(hues_map[node], lightness, saturation)
  return colors
  
def displyConstraintGraph(graph, colors=None, save_img=False, filename='ConstraintGraph'):
  if not colors:
    colors = getColors(graph)
  #get layout for graph
  pos = nx.spring_layout(graph, scale=2)
  for node, data in graph.nodes_iter(data=True):
    nx.draw_networkx_nodes(graph, pos, nodelist=[node], node_color=colors[node])
    
  #draw the edges
  #nodeDict = dict(graph.nodes(data=True))
  #for start, end, data in graph.edges(data=True):
  #  edge = (start, end)
  #  nx.draw_networkx_edges(graph, pos, edgelist=[edge], style=EDGE_STYLES[data[TYPE]])
    
  #genterate the label map
  labels = {}
  for node, data in graph.nodes_iter(data=True):
    labels[node] = data.get(NAME, node)
  #draw the labels
  nx.draw_networkx_labels(graph, pos, labels)
  if(save_img):
    plt.savefig(filename +'.png')
  plt.show()

def buildConstraintGraph(nodes, edges, **kwargs):
  '''
    nodes is a lists of node ids/names 
      a list of tutples where each it a (id/name, label) pare in that order 
      a list of dictionaries where each has a 'id' and 'label'
    edges is a list of dictionarys with a "start", "end" and "type"
    "type" should be either 'similar' or 'dissimilar'
  '''
  type_key = kwargs.get('type_key', 'type')
  start_key = kwargs.get('start_key', 'start')
  end_key = kwargs.get('end_key', 'end')
  weight_key = kwargs.get('weight_key', 'weight')
  similar = kwargs.get('similar_type', 'similar')
  dissimilar = kwargs.get('dissimilar_type', 'dissimilar')
  id_key = kwargs.get('id_key', 'id')
  label_key = kwargs.get('label_key', id_key)
  
  G=nx.Graph()
  for node in nodes:
    if isinstance(node, (list, tuple)):
      G.add_node(node[0], attr_dict = {NAME: node[1]})
    elif isinstance(node, dict):
      G.add_node(node[id_key], attr_dict = {NAME: node[label_key]})
    else:
      G.add_node(node)
    
  for edge in edges:
    weight = edge.get(weight_key,1) #default to 1 if no weight
    type_string = edge[type_key]
    if type_string == similar:
      type = SIMILAR_EDGE
    elif type_string == dissimilar:
      type = DISSIMILAR_EDGE
    else:
      raise ValueError(type_string + ' is not a valid value for edge type.')
    G.add_edge(edge[start_key], edge[end_key], attr_dict={TYPE: type, WEIGHT: weight})

  return G

def color_distance(hue1, hue2):
  """Return a value between 0 and 1 that repesents the
  distance between the hues on the color circle. This
  distance function is defined in equation 3 of the paper.
  
  Parameters
  ----------
  hue1, hue2 : The angle on the color circle corisponding to a hue value.
    In the range 0 to 1
  
  Returns
  --------
  distance: Float from 0 to 1
    1 corresponds to colors on the opposite sides of the circle
    0 corresponds to the same color
  """
  dif = abs(hue1 - hue2)
  if dif < .5:
    return 2*dif
  else:
    return 1 - 2*dif
    
def getColors(contraint_graph, **kwargs):
  """Return a value between 0 and 1 that repesents the
  distance between the hues on the color circle. This
  distance function is defined in equation 3 of the paper.
  
  Parameters
  ----------
  contraint_graph : A networkx graph representing the color contraints.
    Edges should have a 'type' atitibute in thier attr_dict that is
          either ADJACENCY_EDGE or INTER_LEVEL_EDGE. 
          See also -> ADJACENCY_EDGE and INTER_LEVEL_EDGE definitions.
    Nodes should have should have a 'level' atitibute in thier attr_dict 
          that is greater than 0.
  Returns
  --------
  Color assinments: A dictionary mapping each node to its hue value. 
         Hues are a float in the range 0 to 1.
  """
  start_random = kwargs.get('start_random', True)
  min_velocity = kwargs.get('min_velocity',.001)
  momentum_damper = kwargs.get('momentum_damper',0.5)
  velocity_damper = kwargs.get('velocity_damper',0.9999)
  max_iterations = kwargs.get('max_iterations',10000)
  force_limit = kwargs.get('force_limit',1)
  max_separation = kwargs.get('max_separation',.3)
  separation_weight = kwargs.get('separation_weight',1.0)
  similarity_weight = kwargs.get('similarity_weight',0)
  dissimilarity_weight = kwargs.get('dissimilarity_weight',0)  

  G = contraint_graph
  
  #set initial colors
  colors = {}
  if start_random:
    #Assign each node a random hue
    for node in G.nodes_iter(data=False):
      colors[node] = .5 + .001*random()
  else:
    #Assign the nodes hues that are evenly distibuted
    count = 0
    hue_spacing = 1.0/G.number_of_nodes()
    for node in G.nodes_iter(data=False):
      colors[node] = hue_spacing * count
      count+=1
  
  
      
  node_list = G.nodes(data=True)
  node_data = {}
  forces = {}
  for node, data in node_list:
    node_data[node] = data
    forces[node] = 0
     
  damper_current = 1
  iterations = 0
  while iterations < max_iterations:
    iterations+=1
    damper_current = damper_current*velocity_damper
    
    
    #calculate the spread forces
    for node in G.nodes_iter():
      non_ajs_nodes =  set(node_data.keys()) - set([n for n in G[node] if G[node][n][TYPE] == SIMILAR_EDGE])
      #import pdb; pdb.set_trace()
      #print node, non_ajs_nodes
      for n in non_ajs_nodes:
        #forces[node] = momentum_damper*forces[node]
        forces[node]+=calculateSeparationForce(colors[node], colors[n], max_separation)*separation_weight
    
    #Do the contraint edges 
    for start, end, data in G.edges_iter(data=True):
      type = data[TYPE]
      if type == SIMILAR_EDGE:
        force = calculatePullingForce(colors[start], colors[end])*dissimilarity_weight
      elif type == DISSIMILAR_EDGE:
        force = calculatePushingForce(colors[start], colors[end])*similarity_weight
      forces[start]+=force
      forces[end]+=force
      
    for node in G.nodes_iter():
      colors[node] = apply_force(colors[node], forces[node]*damper_current, force_limit)
#      print colors[node]
      forces[node] = 0

  return colors

#Equation 7
def calculatePushingForce(node_color1, node_color2, weight=1):
  return (1 - color_distance(node_color1, node_color2))**2
  
#Equation 8
#weight would be a list of the feeder patern ratio 
def calculatePullingForce(node_color, incoming_node_color, incoming_node_weight=1):
  return color_distance(node_color, incoming_node_color)*incoming_node_weight
 
#Equation 9
def calculateSeparationForce(node_color1, node_color2, max_separation):
  color_dist = color_distance(node_color1, node_color2)
  if color_dist < max_separation:
    return 1 - (color_dist/max_separation)
  else:
    return 0
  
def apply_force(hue, force, force_limit):
  hue+=force
  while hue >= 1.0:
    hue -= 1.0
  while hue < 0.0:
    hue += 1.0
  return hue

def HSL_to_RGB(hue, sat, lit):
  chroma = (1 - abs(2 * lit - 1)) * sat
  #hue in degrees would be divided by 60 but we're on a 0 to 1 scale
  hue_prime = hue / (1.0/360.0 * 60.0)
  X = chroma * (1 - abs(hue_prime % 2 - 1))
  C = chroma
  rgb = (0,0,0)
  if hue_prime < 1:
    rgb = (C, X, 0)
  elif hue_prime < 2:
    rgb = (X, C, 0)
  elif hue_prime < 3:
    rgb = (0, C, X)
  elif hue_prime < 4:
    rgb = (0, X, C)
  elif hue_prime < 5:
    rgb = (X, 0, C)
  elif hue_prime < 6:
    rgb = (C, 0, X)
  m = lit - .5 * chroma
  return [x + m for x in rgb]
    
def randomColor():
  return [random() for i in range(3)]


if __name__ == '__main__':
    main()