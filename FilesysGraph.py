#!/usr/bin/python
import sys
import os
import random 

random.seed()

def main():
    # Default path is the current directory
    path = "./"
    
    # If given a command line argument for the path, use it
    if len(sys.argv) > 1:
        path = sys.argv[1]
    
    nodes_edges = nodes_edges_to_json(path)

    infoVis_json = nodes_to_infoVis_format(path, path)
    
    print "Data for Amy:"
    print nodes_edges
    print ""
    print "InfoVis json:"
    print infoVis_json

# Generate the InfoVis formatted data for a path
def nodes_to_infoVis_format(path, root):
    for dirname, dirnames, filenames in os.walk(path):
        
        # Generate a random color
        # (to be replaced by the color algorithm)
        random_color = ""
        for i in range(3):
            random_color += hex(random.randrange(0, 255, 1))[2:]
        while len(random_color) < 6:
            random_color += "0"
        
        # Calculate the level
        level = 0
        level_temp = dirname.replace(root + "/", "")
        level_temp = level_temp.replace(root, "")
        spaces = ""
        if len(level_temp) != 0:
            level = level_temp.count("/") + 1
        out = "\n\t{\"children\": ["
        for dir in dirnames:
            out += nodes_to_infoVis_format(os.path.join(dirname, dir), root)
        if out[-1] == ",":
            out = out[:-1]
        out += "],"
        out += "\n\t\"data\": {\n"
        dirnameshort = dirname.replace(root, "./").replace("//", "/")
        out += "\t\"description\": \"" + dirnameshort + "\", \n"
        out += "\t\"size\": " + str(get_dir_size(dirname)) + ", \n"
        out += "\t\"sizec\": " + str(get_dir_size_including_children(dirname)) + ", \n"
        out += "\t\"typec\": \"" + get_dir_common_count(dirname) + "\", \n"
        out += "\t\"types\": \"" + get_dir_common_size(dirname) + "\", \n"
        out += "\t\"$color\": \"#" + random_color + "\", \n"
        out += "\t\"lvl\": " + str(level) + ""
        out += "},\n"
        out += "\t\"id\": \"" + dirname + "\", "
        out += "\n\t\"name\": \"" + dirnameshort + "\""
        out += "\n\t},"
        for i in range(level):
            spaces += "     "
        out = out.replace("\t", spaces)
        out = out[:-1]
        if path == root:
            out = out[1:]
        return out
    return ""


# Generate the data for the nodes and edges
def nodes_edges_to_json(path):
    nodes = []
    edges = []
    
    # Walk the path and get the directories
    for dirname, dirnames, filenames in os.walk(path):
        
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
        nodes.append([dirnameshort, level, dirsize, dirsizec, dirfilecount, dirfilesize])
        
        # Create parent-child relationships in the edges
        for subdirname in dirnames:
            edges.append([dirnameshort, os.path.join(dirnameshort,subdirname), "child"])
            
            # Create neighbor relationships in the edges
            for neighbor in dirnames:
                
                # Don't create an edge to self
                if neighbor == subdirname:
                    continue
                
                # Make up a neighbor node, sorted (this prevents duplicates)
                temp = sorted([os.path.join(dirnameshort,subdirname),os.path.join(dirnameshort,neighbor)])
                temp.append("neighbor")
            
                # If not in edges, we have a new edge, so add it
                if temp not in edges:
                    edges.append(temp)
    
    # Format the data
    json_out = "{\n"
    json_out += "\t\"nodes\":\n\t["
    for node in nodes:
        json_out += "\n\t\t{ \"name\": \"" + node[0] + "\", "
        json_out += "\"lvl\": " + str(node[1]) + ", "
        json_out += "\"size\": " + str(node[2]) + ", "
        json_out += "\"sizec\": " + str(node[3]) + ", "
        json_out += "\"typecount\": \"" + node[4] + "\", "
        json_out += "\"typesize\": \"" + node[5] + "\" },"
    json_out = json_out[:-1]
    json_out += "\n\t],\n"
    json_out += "\t\"edges\":\n\t["
    for edge in edges:
        json_out += "\n\t\t{ \"start\": \"" + edge[0] + "\", "
        json_out += "\"end\": \"" + edge[1] + "\" },"
        #json_out += "relation: '" + edge[2] + "' },"
    json_out = json_out[:-1]
    json_out += "\n\t]\n}"
    json_out = json_out.replace("\t", "  ")
    return json_out

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
