#!/usr/bin/python
import sys
import os
from random import randint
import json
import string

CHILD_EDGE = 'child'
NEIGHBOR_EDGE = 'neighbor'

def main():
    # Default path is the current directory
    path = "./"
    
    # If given a command line argument for the path, use it
    if len(sys.argv) > 1:
        path = sys.argv[1]
    
    nodes_edges = gen_filesys_graph(path)

    infoVis_json = gen_infoVis_format(path, path)
    prefix = ''
    if len(sys.argv) > 2:
      prefix = sys.argv[2] + '_'
    colorsel_file = open(prefix + 'colorselection.json', 'w') 
    infoVis_file = open(prefix + 'infoVis.json', 'w') 
    json.dump(nodes_edges, colorsel_file, indent=4)
    json.dump(infoVis_json, infoVis_file, indent=4)
    colorsel_file.close()
    infoVis_file.close()
    
# Generate the InfoVis formatted data for a path
def gen_infoVis_format(path, root, color_map=None, include_hidden=False):
    for dirname, dirnames, filenames in os.walk(path):
      
        # Calculate the level
        dirnameshort = dirname.replace(root + "/", "").replace(root, "")

        level = 0
        if dirnameshort:
            level = dirnameshort.count("/") + 1
            
        if color_map:
          color = color_map['./' + dirnameshort]
          print color
        else:
          #random color
          color = '#' + string.join(['%02x'%randint(0,255) for i in range(3)],'')
          
        children = []
        for dir in dirnames:
            if include_hidden or dir[0] != '.':
              children.append(gen_infoVis_format(os.path.join(dirname, dir), root, color_map=color_map))
        data = {}
        data['description'] = dirnameshort
        data['size'] = data['$angularWidth'] = get_dir_size(dirname)
        data['sizec'] = get_dir_size_including_children(dirname)
        data['typec'] = get_dir_common_count(dirname)
        data['types'] = get_dir_common_size(dirname)
        data['$color'] = color
        data['lvl'] = level
        node = {'data': data, 'id': dirname, 'name': dirnameshort or 'root', 'children': children}
        return node
    return []

def isHiddenPath(path):
    path = os.path.abspath(path).split('/')
    return [dir for dir in path if dir and dir[0]=='.'] != []

# Generate the data for the nodes and edges
def gen_filesys_graph(path, include_hidden=False):
    nodes = []
    edges = []
    
    # Walk the path and get the directories
    for dirname, dirnames, filenames in os.walk(path):
        if include_hidden or not isHiddenPath(dirname):
          
          # Calculate the level
          level = 0
          level_temp = dirname.replace(path + "/", "")
          level_temp = level_temp.replace(path, "")
          if len(level_temp) != 0:
              level = level_temp.count("/") + 1
                  
          # Put each node into the list of nodes, with dir size and 
          # size including children
          dirnameshort = dirname.replace(path, "./").replace("//", "/")
          dirsize = get_dir_size(dirname)
          dirsizec = get_dir_size_including_children(dirname)
          dirfilecount = get_dir_common_count(dirname)
          dirfilesize = get_dir_common_size(dirname)
          nodes.append({'name': dirnameshort,
                        'lvl': level, 
                        'size': dirsize,
                        'sizec': dirsizec,
                        'typecount': dirfilecount,
                        'typesize': dirfilesize})
          
          # Create parent-child relationships in the edges
          for subdirname in dirnames:
              if include_hidden or subdirname[0] != '.':
                  edges.append({'start': dirnameshort, 'end': os.path.join(dirnameshort,subdirname), 'relation':CHILD_EDGE})
                  # Create neighbor relationships in the edges
                  for neighbor in dirnames:
                      
                      # Don't create an edge to self
                      if neighbor != subdirname and (include_hidden or neighbor[0] != '.'):
                        # Make up a neighbor node, sorted (this prevents duplicates)
                        edge_ends = sorted([os.path.join(dirnameshort,subdirname),os.path.join(dirnameshort,neighbor)])
                        neighbor_edge = {'start': edge_ends[0], 'end': edge_ends[1], 'relation':NEIGHBOR_EDGE}
          
                        # If not in edges, we have a new edge, so add it
                        if neighbor_edge not in edges:
                            edges.append(neighbor_edge)

    for edge in edges:
        
        if edge['relation'] == CHILD_EDGE:
            for dirname, dirnames, filenames in os.walk(os.path.join(path, edge['start'][2:])):
                ctotal = 0
                ctotalc = 0
                for dir in dirnames:
                    ctotal += get_dir_size(dirname + "/" + dir)
                    ctotalc += get_dir_size_including_children(dirname + "/" + dir)
                cweight = get_dir_size(os.path.join(path, edge['end'][2:])) / float(ctotal)
                cweightc = get_dir_size_including_children(os.path.join(path, edge['end'][2:])) / float(ctotalc)
                edge['weight'] = cweight
                edge['weightc'] = cweightc
                break

    return {'nodes': nodes, 'edges': edges}


# Get the most common file type (based on size) in a path
def get_dir_common_size(path):
    type = {}
    count = 0
    for dirname, dirnames, filenames in os.walk(path):
        for f in filenames:
            count = count + 1
            extension = os.path.splitext(f)[1]
            fp = os.path.join(dirname, f)
            if extension == "":
                extension = "[none]"
            if extension in type:
                type[extension] = type[extension] + os.path.getsize(fp)
            else:
                type[extension] = os.path.getsize(fp)
        break
    if count > 0:
        return max(type, key=type.get)
    else:
        return "NULL"

# Get the most common file type (based on count) in a path
def get_dir_common_count(path):
    type = {}
    count = 0
    for dirname, dirnames, filenames in os.walk(path):
        for f in filenames:
            count = count + 1
            extension = os.path.splitext(f)[1]
            if extension == "":
                extension = "[none]"
            if extension in type:
                type[extension] = type[extension] + 1
            else:
                type[extension] = 1
        break
    if count > 0:
        return max(type, key=type.get)
    else:
        return "NULL"

# Get the size of a directory and children
def get_dir_size_including_children(path):
    total_size = 0
    for dirname, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirname, f)
            total_size += os.path.getsize(fp)
    return total_size

# Get the size of a directory
def get_dir_size(path):
    total_size = 0
    for dirname, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirname, f)
            total_size += os.path.getsize(fp)
        break
    return total_size

if __name__ == "__main__":
    main()
