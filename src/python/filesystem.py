import sys
import ColorSelecter as cs
import FilesysGraph as fsg
import json

def main():
  
  # Default path is the current directory
  path = "./"
  
  # If given a command line argument for the path, use it
  if len(sys.argv) > 1:
    path = sys.argv[1]
  
  graph = fsg.gen_filesys_graph(path)
  
  nodes = graph['nodes']
  edges = graph['edges']
  keys = {'type_key': 'relation',
          'similar_type': fsg.CHILD_EDGE,
          'dissimilar_type': fsg.NEIGHBOR_EDGE,
          'id_key': 'name'}
          
  graph = cs.buildConstraintGraph(nodes, edges, **keys)

  #Get colors from paper algorithim
  hues = cs.hues_to_rgb(cs.getColors(graph))
  colors = dict([node,list_to_color(color)] for node, color in hues.iteritems())
  
  infovid_json = fsg.gen_infoVis_format(path,path,color_map=colors)
  print json.dumps(infovid_json)

def list_to_color(color):
  return '#' + ''.join(['%02x'%(i*255) for i in color])
  
main()