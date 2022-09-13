# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1605947'
__group__ = 'DM.12'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2021 - 2022
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list = []
    for neighbor in map.connections[path.last].keys():
        newPath = copy.deepcopy(path)
        newPath.add_route(neighbor)
        path_list.append(newPath)
    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    path_new = []
    for path in path_list:
        if (len(path.route) == len(set(path.route))):
            path_new.append(path)
    return path_new


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    list_of_path[0:1] = []
    i = len(expand_paths) - 1
    while i >= 0:
        list_of_path.insert(0, expand_paths[i])
        i -= 1
    return list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    paths = [Path(origin_id)]
    while paths[0].last != destination_id and paths != []:
        firstPath = paths[0]
        newPaths = expand(firstPath, map)
        newPaths = remove_cycles(newPaths)
        paths = insert_depth_first_search(newPaths, paths)

    if len(paths) != 0:
        return paths[0]
    else:
        return "No Solution Exists"


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    list_of_path[0:1] = []
    i = 0
    while i < len(expand_paths):
        list_of_path.append(expand_paths[i])
        i += 1
    return list_of_path


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    paths = [Path(origin_id)]
    while paths[0].last != destination_id and paths != []:
        firstPath = paths[0]
        newPaths = expand(firstPath, map)
        newPaths = remove_cycles(newPaths)
        paths = insert_breadth_first_search(newPaths, paths)

    if len(paths) != 0:
        return paths[0]
    else:
        return "No Solution Exists"


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency(number of stops)
                                1 - minimum Time(dictionary of dictionaries)
                                2 - minimum Distance
                                3 - minimum Transfers(transbordo)
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """

    if type_preference == 0:
        for station in expand_paths:
            station.update_g(1)

    elif type_preference == 1:
        for station in expand_paths:
            station.update_g(map.connections[station.last][station.penultimate])

    elif type_preference == 2:
        for station in expand_paths:
            if map.stations[station.last]['line'] == map.stations[station.penultimate]['line']:
                station.update_g(map.velocity[map.stations[station.last]['line']]*map.connections[station.last][station.penultimate])

    elif type_preference == 3:
        for station in expand_paths:
            if map.stations[station.last]['line'] != map.stations[station.penultimate]['line']:
                station.update_g(1)

    return expand_paths

def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    list_of_path[0:1]=[]
    for newP in expand_paths:
        i = 0
        insert = False
        while insert == False and i < len(list_of_path):
            if newP.g < list_of_path[i].g:
                list_of_path.insert(i, newP)
                insert=True
            else:
                i+=1
        if insert==False:
            list_of_path.append(newP)
    return list_of_path




def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    llista=[Path([origin_id])]
    while llista[0].last!=destination_id and len(llista[0].route)!=0:
        c=llista[0]
        e=expand(c,map)
        e=remove_cycles(e)
        calculate_cost(e,map,type_preference)
        llista=insert_cost(e,llista[0:])##pasamos la lista menos el primer path ya que es el que hemos expandido

    if len(llista) != 0:
        return llista[0]
    else:
        return "No existeix Solucio"

def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    if type_preference == 0:
        for station in expand_paths:
            if station.last!=destination_id:
                station.update_h(1)
            else:
                station.h=0

    elif type_preference == 1:
        puntY=[map.stations[destination_id]['x'], map.stations[destination_id]['y']]
        for station in expand_paths:
            if station.last==destination_id:
                station.h=0;
            else:
                puntX=[map.stations[station.last]['x'], map.stations[station.last]['y']]
                ##station.update_h(map.connections[station.last][station.penultimate])
                station.update_h(euclidean_dist(puntX, puntY)/max(map.velocity.values()))

    elif type_preference == 2:
        puntY = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]
        for station in expand_paths:
            if station.last!=destination_id:
                puntX = [map.stations[station.last]['x'], map.stations[station.last]['y']]
                station.update_h(euclidean_dist(puntX, puntY))
            else:
                station.h=0

    elif type_preference == 3:
        for station in expand_paths:
            if station.last==destination_id:
                station.h=0;
            else:
                if map.stations[station.last]['line'] != map.stations[station.penultimate]['line']:
                    station.update_h(1)

    return expand_paths



def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """
    for path in expand_paths:
        if path.last in visited_stations_cost:
            if path.g<visited_stations_cost[path.last]:
                visited_stations_cost[path.last]=path.g
                ##eliminamos paths que tengan camino a este nodo
                i=0
                while i < len(list_of_path):
                    if path.last in list_of_path[i].route:
                        list_of_path[i:i+1]=[]
                    else:
                        i+=1
            else:
                expand_paths.remove(path)
    return expand_paths, list_of_path, visited_stations_cost

def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    list_of_path[0:1] = []
    for newP in expand_paths:
        i = 0
        insert = False
        while insert == False and i < len(list_of_path):
            if newP.f < list_of_path[i].f:
                list_of_path.insert(i, newP)
                insert = True
            else:
                i += 1
        if insert == False:
            list_of_path.append(newP)
    return list_of_path


def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """
    possible_origins = []
    puntos = [map.stations[1]['x'], map.stations[1]['y']]
    min = euclidean_dist(coord, puntos)
    stations = map.stations.keys()
    for key in stations:
        puntos = [map.stations[key]['x'], map.stations[key]['y']]
        dist = euclidean_dist(coord, puntos)
        if dist < min:
            possible_origins = [key]
            min = dist
        else:
            if dist == min and key not in possible_origins:
                possible_origins.append(key)
    return possible_origins

def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    origin_id = coord2station(origin_coor,map)[0]
    dest_id = coord2station(dest_coor,map)[0]
    llista = [Path([origin_id])]
    visitedDict={}
    while llista[0].last != dest_id and llista:
        c = llista[0]
        e = expand(c, map)
        e = remove_cycles(e)
        calculate_cost(e, map, type_preference)
        calculate_heuristics(e, map, dest_id, type_preference)
        e, llista, visitedDict = remove_redundant_paths(e, llista, visitedDict)
        update_f(e)
        llista = insert_cost_f(e, llista[0:])  ##pasamos la lista menos el primer path ya que es el que hemos expandido

    if len(llista) != 0:
        return llista[0]
    else:
        return "No existeix Solucio"