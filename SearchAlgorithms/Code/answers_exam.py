from SearchAlgorithm import *
from SubwayMap import *
from utils import *

if __name__=="__main__":
    ROOT_FOLDER = '../CityInformation/Barcelona_City/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)



    ### BELOW HERE YOU CAN CALL ANY FUNCTION THAT yoU HAVE PROGRAMED TO ANSWER THE QUESTIONS OF THE EXAM ###
    ### this code is just for you, you won't have to upload it after the exam ###

    ##act2
    print("ACT2:")
    for station in coord2station([242, 184], map):
        print(map.stations[station])
    print("/n")

    ##act3

    print_list_of_path(remove_cycles([Path([7, 3, 6, 1, 5]), Path([7, 3, 6, 1, 8]), Path([7, 3, 6, 1, 7]), Path([7, 3, 6, 1, 3]), Path([7, 3, 6, 1, 4])]))


    ##act4

    print("/n")
    id1=0
    id2=0
    for id in map.stations.keys():
        print(map.stations[id]['name'])
        if(map.stations[id]['name'] =="Selva de mar"):
            id1=id
            break

    for id in map.stations.keys():
        if (map.stations[id]['name']== "Camp de l'Arpa"):
            id2 = id
            break

    nom1=map.stations[13]['name']
    nom2 = map.stations[8]['name']
    print(id1, id2)
    resultado=breadth_first_search(13,8, map)
    print(resultado.route)

    print("/n")

    ##act5
    p1=Path([3, 4, 5, 6])
    resultado2=calculate_cost([p1], map, 2)
    print_list_of_path_with_cost(resultado2)

##act6
    i=0
    names=["Roda", "Tetuan", "Clot"]
    for id in map.stations.keys():
        if (map.stations[id]['name'] == "Bac de Roda"):
            id4 = id
            break

    for id in map.stations.keys():
        if (map.stations[id]['name'] == "Clot"):
            id5 = id
            break
    for id in map.stations.keys():
        if (map.stations[id]['name'] == "Tetuan"):
            id6 = id
            break

    hola=calculate_heuristics([Path([11, 13])], map, 17, 1);

    print_list_of_path_with_cost(hola)
    ##breadth_first_search()
    #this is an example of how to call some of the functions that you have programed
    ##example_path=uniform_cost_search(9, 3, map, 1)
    #print_list_of_path_with_cost([example_path])

    ##act7
    p2 = Path([16, 15, 14, 13])
    resultado3 = calculate_cost([p2], map, 1)
    print_list_of_path_with_cost(resultado2)

    #act10

    reaultado10=Astar([143, 195],[249, 101],map,1)
    print("ver")

    reaultado10 = Astar([59, 239], [133, 136], map, 3)
    print("ver")


    llistapathsnou=[Path([3,5,1]), Path([3,5,6]), Path([3,5,0]), Path([3,5,2,4])]
    pathog=[Path([3,5,2,1]), Path([3,5,2,6]), Path([3,5,2,0]),Path([3,5,2,7])]
    pathog[0].update_g(8)
    pathog[1].update_g(52)
    pathog[2].update_g(47)
    pathog[3].update_g(33)
    dictcost={"5":57.74, "2":43.73, "1":51.63, "6":6.44, "0":26.43}
    solucio8=remove_redundant_paths(llistapathsnou, pathog, dictcost)
    print_list_of_path_with_cost(solucio8[0])
    print_list_of_path_with_cost(solucio8[1])
    print("jsjdosj")