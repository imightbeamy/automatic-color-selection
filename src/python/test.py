import itertools as itr
import networkx as nx
import ColorSelecter as cs
import matplotlib.pyplot as plt
import sys
import json


def makeFileTypeContraintGraph():

                #compressed and Uncompressed
  lossless = [['AIFF', 'WAV'], ['FLAC', 'WMA']]
  lossy = ['MP3', 'AAC', 'WMA']
  audioTypes = [lossless, lossy]

  images =  ['GIF', 'JPEG', 'PNG', 'RAW', 'TIFF', 'JNG', 'ICO']
  videos = ['MPEG', 'AVI', 'M4V', 'WMV', 'FLV']
  mediaTypes = [images, videos, audioTypes]
  
  presentations = ['KEY', ['PPT', 'PPTX'], 'ODP']
  documents = [['DOCX', 'DOC'], 'HTML', 'ODT', 'TXT', 'PDF', 'TeX', 'RTF']
  spreadsheets = [[['XLS', 'XLSX'], 'ODS'], ['CSV', 'TAB']]
  documentTypes = [spreadsheets, documents, presentations]

  executableTypes = ['APP', 'EXE', ['CLASS', 'JAR']]
  
  scriptingTypes = ['PL', 'PHP', 'RB', 'PY', 'JS']
  compliedTypes = ['C', 'JAVA', 'CPP']
  codeTypes = [scriptingTypes, compliedTypes]

  folders = ['NONE', 'NULL']

  fileTypes = [[mediaTypes, documentTypes], codeTypes, executableTypes, folders]

  return documents


def isFlat(lst):
  for n in lst:
    if type(n) == list:
      return False
  return True 

def flatten(lst):
  flat = []
  for n in lst:
    if type(n) == list:
      flat.extend(flatten(n))
    else:
      flat.append(n)
  return flat

def listToGraph(thisisalist):
  G = nx.Graph()

  def toGraph(valus, depth):
    if isFlat(valus):
      for e in itr.combinations(valus, 2):
        G.add_edge(e[0],e[1],attr_dict={'weight': 1}) 
      return depth

    edges = []
    max_depth = 0
    for n in valus:
      if type(n) == list:
        inner_depth = toGraph(n, depth+1)
        max_depth = max(max_depth, inner_depth)
    values = flatten(valus)
    for c in itr.combinations(values, 2):
      if (not c[0] in G or not c[1] in G) or (not c[1] in G[c[0]].keys()):
        G.add_edge(c[0],c[1],attr_dict={'weight': 1.0/(max_depth-depth+1)})
      
    return max_depth

  toGraph(thisisalist, 1)
  return G


if __name__ == '__main__':
  
  lst = makeFileTypeContraintGraph()
  G = listToGraph(lst)
  edges = [{'start': s, 'end':e, 'weight': data['weight'], 'type': 'similar'} for s, e, data in G.edges(data=True)]
  nodes =  G.nodes()
  graph = cs.buildConstraintGraph(nodes, edges)
  
  hues = cs.getColors(graph, similarity_weight=1.0,separation_weight=0.0,start_random=True, max_separation=.3)
  colors = cs.hues_to_rgb(hues)
  print 'Done.'    
  print json.dumps(colors)
  cs.displyConstraintGraph(graph, colors)



  sys.exit()



def lol():
  lst = makeFileTypeContraintGraph()
  #[['a1','b2', 'c3'],['d', ['f', 'g']],['h', 'i', 'j', ['k','l','m']]]
  print lst
  G = listToGraph(lst)
  print G.edges(data=True)
  pos = nx.spring_layout(G, scale=2)
  #get layout for graph
  pos = nx.spring_layout(G, scale=2)
  for node, data in G.nodes_iter(data=True):
    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=400)
   
  #draw the edges
  nodeDict = dict(G.nodes(data=True))
  for start, end, data in G.edges(data=True):
    edge = (start, end)
    nx.draw_networkx_edges(G, pos, edgelist=[edge], width=5*data['weight'], edge_color=[[data['weight'], 0,0]])
  #genterate the label map
  labels = {}
  for node, data in G.nodes_iter(data=True):
    labels[node] = node
  #draw the labels
  nx.draw_networkx_labels(G, pos, labels, font_size=8)
  
  plt.show()
 
