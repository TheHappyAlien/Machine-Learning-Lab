import heapq
import geopy.distance
import math
import csv
import Utils
import time
 
PUBLIC_TRANSPORT_SPEED_KM_H = 20
LINE_CHANGE_COST = 0

def astar_t_backup(graph_dict, start, goal, trip_start_time, coords_heuristic_fn):
    counter = 0
    pq = [(0, start)]
    prev_nodes = {start: None}
    cost_so_far = {start: 0}
    trip_start_time = Utils.minutes_from_midnight(trip_start_time)
    while pq:
        _, current = heapq.heappop(pq)
        curr_cost = cost_so_far[current]
        curr_arrival_time = trip_start_time + curr_cost
        base_days_en_route = 0
        if current == goal:
            break
        
        if curr_arrival_time > 24*60:
            base_days_en_route = int(curr_arrival_time/(24*60))
            curr_arrival_time = curr_arrival_time%(24*60)
            
        prev_line = ''
        if prev_nodes[current]:
            prev_line = prev_nodes[current][1]
            
        for neighbor, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon in graph_dict[current]:
            counter += 1
            days_en_route = base_days_en_route
            
            coords1 = (start_stop_lat, start_stop_lon)
            coords2 = (end_stop_lat, end_stop_lon)
            
            if curr_arrival_time <= start_time:
                # current travel time + time spent waiting for the bus/tram + time spent en route 
                new_cost = curr_cost + (start_time - (curr_arrival_time)) + weight
            else:
                # current travel time + (time till midnight + start_time) + time spent en route
                new_cost = curr_cost + (24*60 - (curr_arrival_time) + start_time) + weight
                days_en_route += 1
            
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + math.floor(coords_heuristic_fn(coords1, coords2))
                # priority = new_cost
                heapq.heappush(pq, (priority, neighbor))
                prev_nodes[neighbor] = (current, line, start_time + days_en_route*24*60, arrival_time + days_en_route*24*60)

    print(f'COUNTER: {counter}')
    return cost_so_far, prev_nodes

def astar_t_old(graph_dict, start, goal, trip_start_time, coords_heuristic_fn):
    goal_info = graph_dict[goal][0]
    coords2 = (goal_info[5], goal_info[6])
    counter = 0
    pq = [(0, start)]
    prev_nodes = {start: None}
    cost_so_far = {start: 0}
    trip_start_time = Utils.minutes_from_midnight(trip_start_time)
    while pq:
        _, current = heapq.heappop(pq)
        curr_cost = cost_so_far[current]
        curr_arrival_time = trip_start_time + curr_cost
        base_days_en_route = 0
        if current == goal:
            break
        
        if curr_arrival_time > 24*60:
            base_days_en_route = int(curr_arrival_time/(24*60))
            curr_arrival_time = curr_arrival_time%(24*60)
            
        prev_line = ''
        if prev_nodes[current]:
            prev_line = prev_nodes[current][1]
            
        for neighbor, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon in graph_dict[current]:
            counter += 1
            days_en_route = base_days_en_route
            
            coords1 = (start_stop_lat, start_stop_lon)

            if curr_arrival_time <= start_time:
                # current travel time + time spent waiting for the bus/tram + time spent en route 
                new_cost = curr_cost + (start_time - (curr_arrival_time)) + weight
            else:
                # current travel time + (time till midnight + start_time) + time spent en route
                new_cost = curr_cost + (24*60 - (curr_arrival_time) + start_time) + weight
                days_en_route += 1
            
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + math.floor(coords_heuristic_fn(coords1, coords2))
                # priority = new_cost
                heapq.heappush(pq, (priority, neighbor))
                prev_nodes[neighbor] = (current, line, start_time + days_en_route*24*60, arrival_time + days_en_route*24*60)

    print(f'COUNTER: {counter}')
    return cost_so_far, prev_nodes

def astar_t(graph_dict, start, goal, trip_start_time, coords_heuristic_fn):
    goal_info = graph_dict[goal][0]
    coords2 = (goal_info[5], goal_info[6])
    counter = 0
    pq = [(0, start)]
    prev_nodes = {start: None}
    
    distances = {node: float('inf') for node in graph_dict}
    distances[start] = 0
    
    trip_start_time = Utils.minutes_from_midnight(trip_start_time)
    while pq:
        _, current = heapq.heappop(pq)
        curr_cost = distances[current]
        curr_arrival_time = trip_start_time + curr_cost
        base_days_en_route = 0
        if current == goal:
            break
        
        if curr_arrival_time > 24*60:
            base_days_en_route = int(curr_arrival_time/(24*60))
            curr_arrival_time = curr_arrival_time%(24*60)
            
        prev_line = ''
        if prev_nodes[current]:
            prev_line = prev_nodes[current][1]
            
        for neighbor, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon in graph_dict[current]:
            counter += 1
            days_en_route = base_days_en_route
            
            coords1 = (start_stop_lat, start_stop_lon)

            if curr_arrival_time <= start_time:
                # current travel time + time spent waiting for the bus/tram + time spent en route 
                new_cost = curr_cost + (start_time - (curr_arrival_time)) + weight
            else:
                # current travel time + (time till midnight + start_time) + time spent en route
                new_cost = curr_cost + (24*60 - (curr_arrival_time) + start_time) + weight
                days_en_route += 1
            
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                priority = new_cost + math.floor(coords_heuristic_fn(coords1, coords2))
                # priority = new_cost
                heapq.heappush(pq, (priority, neighbor))
                prev_nodes[neighbor] = (current, line, start_time + days_en_route*24*60, arrival_time + days_en_route*24*60)

    print(f'COUNTER: {counter}')
    return distances, prev_nodes


def astar_p(graph_dict, start, goal, trip_start_time, coords_heuristic_fn):
    goal_info = graph_dict[goal][0]
    goal_coords = (goal_info[5], goal_info[6])
    
    start_info = graph_dict[start][0]
    current_coords = (start_info[5], start_info[6])
    
    counter = 0
    
    pq = [(0, start)]
    prev_nodes = {start: None}
    distances = {node: float('inf') for node in graph_dict}
    distances[start] = 0
    
    fScore = {node: float('inf') for node in graph_dict}
    fScore[start] = 0
    
    trip_start_time = Utils.minutes_from_midnight(trip_start_time)
    print("dupa")
    while pq:
        curr_fScore, current = heapq.heappop(pq)
        curr_cost = distances[current]
        curr_arrival_time = trip_start_time + curr_cost
        base_days_en_route = 0
        if current == goal:
            break
        
        if curr_arrival_time > 24*60:
            base_days_en_route = int(curr_arrival_time/(24*60))
            curr_arrival_time = curr_arrival_time%(24*60)
            
        prev_line = ''
        if prev_nodes[current]:
            prev_line = prev_nodes[current][1]
            
        for neighbor, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, _, _ in graph_dict[current]:
            
            if prev_line == line or prev_line == '': line_change_penalty = 0
            else: line_change_penalty = LINE_CHANGE_COST 
                
            counter += 1
            days_en_route = base_days_en_route
            current_coords = (start_stop_lat, start_stop_lon)

            if curr_arrival_time <= start_time:
                # current travel time + time spent waiting for the bus/tram + time spent en route 
                new_cost = curr_cost + (start_time - (curr_arrival_time)) + weight
            else:
                # current travel time + (time till midnight + start_time) + time spent en route
                new_cost = curr_cost + (24*60 - (curr_arrival_time) + start_time) + weight
                days_en_route += 1
            
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                fScore[neighbor] = new_cost + line_change_penalty
                priority = new_cost + math.floor(coords_heuristic_fn(current_coords, goal_coords)) + 0
                # priority = new_cost
                heapq.heappush(pq, (priority, neighbor))
                prev_nodes[neighbor] = (current, line, start_time + days_en_route*24*60, arrival_time + days_en_route*24*60)

    print(f'COUNTER: {counter}')
    return distances, prev_nodes


def astar_p_bad(graph_dict, start, goal, trip_start_time, coords_heuristic_fn):
    pq = [(0, start, '')]
    prev_nodes = {(start, ''): None}
    # cost_so_far = {(start, ''): 0}
    cost_w_switch = {(start, '') : (0, 0)}
    trip_start_time = Utils.minutes_from_midnight(trip_start_time)
    while pq:
        _, current, prev_line = heapq.heappop(pq)
        curr_cost = cost_w_switch[(current, prev_line)][0]
        base_line_changes = cost_w_switch[(current, prev_line)][1]
        
        curr_arrival_time = trip_start_time + curr_cost
        base_days_en_route = 0
        if current == goal:
            break
        
        if curr_arrival_time > 24*60:
            base_days_en_route = int(curr_arrival_time/(24*60))
            curr_arrival_time = curr_arrival_time%(24*60)
            
        for neighbor, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon in graph_dict[current]:
            
            line_changes = base_line_changes
            days_en_route = base_days_en_route
            
            if prev_line != '' and prev_line != line: 
                line_changes += 1
            
            coords1 = (start_stop_lat, start_stop_lon)
            coords2 = (end_stop_lat, end_stop_lon)
            
            if curr_arrival_time <= start_time:
                # current travel time + time spent waiting for the bus/tram + time spent en route 
                new_cost = curr_cost + (start_time - (curr_arrival_time)) + weight
            else:
                # current travel time + (time till midnight + start_time) + time spent en route
                new_cost = curr_cost + (24*60 - (curr_arrival_time) + start_time) + weight
                days_en_route += 1
            
            if ((neighbor, line), _) not in cost_w_switch or new_cost + line_changes * LINE_CHANGE_COST < cost_w_switch[(neighbor, line)][0] + cost_w_switch[(neighbor, line)][1] * LINE_CHANGE_COST or prev_line == line:
                cost_w_switch[(neighbor, line)] = (new_cost, line_changes)
                priority = new_cost + math.floor(coords_heuristic_fn(coords1, coords2))
                priority += line_changes * LINE_CHANGE_COST
                heapq.heappush(pq, (priority, neighbor, line))
                prev_nodes[(neighbor, line)] = (current, prev_line, start_time + days_en_route*24*60, arrival_time + days_en_route*24*60)
                
            elif prev_line == '':
                priority = new_cost + math.floor(coords_heuristic_fn(coords1, coords2))
                priority += line_changes * LINE_CHANGE_COST
                heapq.heappush(pq, (priority, neighbor, line))
                          
    return cost_w_switch[(current, prev_line)][0], prev_nodes, prev_line

class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.graph_dict = {}
        for start, end, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon in self.edges:
            if start in self.graph_dict:
                self.graph_dict[start].append((end, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon))
            else:
                self.graph_dict[start] = [(end, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon)]
            if end not in self.graph_dict:
                self.graph_dict[end] = []
                
def edges(fileName):
    edges = []
    with open(fileName, 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        for row in reader:
            line = row[2]
            start_time = Utils.minutes_from_midnight(row[3])
            arrival_time = Utils.minutes_from_midnight(row[4]) 
            weight = arrival_time - start_time
            
            if weight < 0:
                weight += 24*60
            
            start = row[5]
            end = row[6]
            
            start_stop_lat = row[7]
            start_stop_lon = row[8]
            end_stop_lat = row[9]
            end_stop_lon = row[10]
            
            edges.append((start, end, line, start_time, arrival_time, weight, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon))
    return edges

def distance_from_coords(coords1, coords2):
    return geopy.distance.geodesic(coords1, coords2).km

def time_from_distance(distance):
    return distance/PUBLIC_TRANSPORT_SPEED_KM_H * 60
    
def time_from_coords(coords1, coords2):
    return time_from_distance(distance_from_coords(coords1, coords2))

def shortest_path_t(graph_dict, start, goal, trip_start_time, coords_heuristic_fn):
    calc_start_time = time.time()
    distances, prev_nodes = astar_t(graph_dict, start, goal, trip_start_time, coords_heuristic_fn)
    calc_end_time = time.time()
    print(f'time_taken: {round(calc_end_time - calc_start_time, 3)}s')
    path = []
    curr_node = goal
    line = ''
    trip_length = distances[goal]
    start_time = 0
    arrival_time = Utils.minutes_from_midnight(trip_start_time) + trip_length
    while True:
        path.append((curr_node, line, start_time, arrival_time))
        if(prev_nodes[curr_node]):
            curr_node, line, start_time, arrival_time = prev_nodes[curr_node]
        else:
            break
    path.reverse()
    Utils.print_solution(trip_start_time, trip_length, path)

def shortest_path_p(graph_dict, start, goal, trip_start_time, coords_heuristic_fn):
    calc_start_time = time.time()
    trip_length, prev_nodes, prev_line = astar_p(graph_dict, start, goal, trip_start_time, coords_heuristic_fn)
    calc_end_time = time.time()
    print(f'time_taken: {round(calc_end_time - calc_start_time, 3)}s')
    path = []
    line = ''
    curr_node = goal
    start_time = 0
    arrival_time = Utils.minutes_from_midnight(trip_start_time) + trip_length
    while True:
        path.append((curr_node, line, start_time, arrival_time))
        if(prev_nodes[(curr_node, prev_line)]):
            line = prev_line
            curr_node, prev_line, start_time, arrival_time = prev_nodes[(curr_node, line)]

        else:
            break
    path.reverse()
    Utils.print_solution(trip_start_time, trip_length, path)

chosenFun = astar_p
gg = Graph(edges('connection_graph_fixed.csv'))
# gg = Graph(edges('test2.csv'))
# gg = Graph(edges('test3.csv'))
# gg = Graph(edges('test4.csv'))
# shortest_path(gg.graph_dict, 'Hutmen', 'most Grunwaldzki', '12:00:00', time_from_coords) 
shortest_path_t(gg.graph_dict, 'pl. Bema', 'DWORZEC GŁÓWNY', '12:00:00', time_from_coords)
# shortest_path_t(gg.graph_dict, 'Ogród Botaniczny', 'Rynek', '14:38:00', time_from_coords)
# shortest_path_p(gg.graph_dict, 'Iwiny - rondo', 'Hala Stulecia', '14:07:00', time_from_coords)
# shortest_path_t(gg.graph_dict, 'Kwiska', 'PL. GRUNWALDZKI', '09:00:00', time_from_coords)
# shortest_path_p(gg.graph_dict, 'Kwiska', 'PL. GRUNWALDZKI', '09:00:00', time_from_coords)
# shortest_path(gg.graph_dict, 'SĘPOLNO', 




# def manhattan_distance(a, b):
#     return sum([abs(x - y) for x, y in zip(a, b)])


# def euclidean_distance(a, b):
#     return math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)]))


# def towncenter_distance(a, b):
#     return euclidean_distance(a, (0, 0, 0, 0, 0, 0, 0)) + euclidean_distance((0, 0, 0, 0, 0, 0, 0), b)


# def unidimensional_distance(a, b):
#     return max([abs(x - y) for x, y in zip(a, b)])


# def cosine_distance(a, b):
#     dot_product = sum(x * y for x, y in zip(a, b))
#     magnitude_a = math.sqrt(sum(x ** 2 for x in a))
#     magnitude_b = math.sqrt(sum(x ** 2 for x in b))
#     return 1 - (dot_product / (magnitude_a * magnitude_b))


# def chebyshev_distance(a, b):
#     return max(abs(x - y) for x, y in zip(a, b))