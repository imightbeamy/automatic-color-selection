import sys
import ColorSelecter as cs
import FilesysGraph as fsg
import json
import itertools as itr

def main():
  
  # Default path is the current directory
  path = "./"
  
  # If given a command line argument for the path, use it
  if len(sys.argv) > 1:
    path = sys.argv[1]
  
  graph = fsg.gen_filesys_graph(path)
  
  nodes = graph['nodes']
  edges = graph['edgesfile']
  keys = {'type_key': 'relation',
          'similar_type': fsg.CHILD_EDGE,
          'dissimilar_type': fsg.NEIGHBOR_EDGE,
          'id_key': 'name',
          'weight_key': 'weightc'}
  keysfiles = {'type_key': 'relation',
          'similar_type': fsg.FILE_TYPE_EDGE,
          'dissimilar_type': fsg.FILE_TYPE_EDGE_NOT,
          'id_key': 'name',
          'weight_key': 'weightc'}          
          
  graph = cs.buildConstraintGraph(nodes, edges, **keysfiles)

  #Get colors from paper algorithim
  hues = cs.hues_to_rgb(cs.getColors(graph))
  colors = dict([node,list_to_color(color)] for node, color in hues.iteritems())

  infovid_json = fsg.gen_infoVis_format(path,path,color_map=colors)
  print json.dumps(infovid_json)
  cs.displyConstraintGraph(graph,colors)
  
def list_to_color(color):
  return '#' + ''.join(['%02x'%(i*255) for i in color])


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
  spreadsheets = [[['XLS', 'XLSX'], 'ODS'], 'CSV', 'TAB']
  documentTypes = [spreadsheets, documents, presentations]

  executableTypes = ['APP', 'EXE', ['CLASS', 'JAR']]
  
  scriptingTypes = ['PL', 'PHP', 'RB', 'PY', 'JS']
  compliedTypes = ['C', 'JAVA', 'CPP']
  codeTypes = [scriptingTypes, compliedTypes]

  folders = ['NONE', 'NULL']

  fileTypes = [[mediaTypes, documentTypes], codeTypes, executableTypes, folders]

  return fileTypes

def listToGraph(lts):
  def isFlat(lst):
    for n in lst:
      if type(n) == list:
        return False
    return True        

  def toGraph(lts, depth):
    if isFlat(lts):
      return [(e,1) for e in itr.combinations(lts)]
    edges = []
    for n in lst:
      if type(n) == list:
        edges.extend(toGraph(n))
    return edges
  return toGraph(lst, 0)

main()
