import heapq
import Utils
import csv
import time

def dijkstra(graph_dict, start, end, trip_start_time):
    counter = 0
    distances = {node: float('inf') for node in graph_dict}
    distances[start] = 0
    pq = [(0, start)]
    prev_nodes = {node: None for node in graph_dict}
    trip_start_time = Utils.minutes_from_midnight(trip_start_time)
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        curr_arrival_time = trip_start_time + curr_dist
        base_days_en_route = 0
        
        if curr_arrival_time > 24*60:
            base_days_en_route = int(curr_arrival_time/(24*60))
            curr_arrival_time = curr_arrival_time%(24*60)
            
        if curr_node == end:
            break
        
        if curr_dist > distances[curr_node]:
            continue
        
        for neighbor, line, start_time, arrival_time, weight in graph_dict[curr_node]:
            counter += 1
            days_en_route = base_days_en_route
            if curr_arrival_time <= start_time:
                # current travel time + time spent waiting for the bus/tram + time spent en route 
                new_dist = curr_dist + (start_time - (curr_arrival_time)) + weight
            else:
                # current travel time + (time till midnight + start_time) + time spent en route
                new_dist = curr_dist + (24*60 - (curr_arrival_time) + start_time) + weight
                days_en_route += 1
                
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev_nodes[neighbor] = (curr_node, line, start_time + days_en_route*24*60, arrival_time + days_en_route*24*60)
                heapq.heappush(pq, (new_dist, neighbor))
    print(f'COUNTER: {counter}')
    return distances, prev_nodes

class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.graph_dict = {}
        for start, end, line, start_time, arrival_time, weight in self.edges:
            if start in self.graph_dict:
                self.graph_dict[start].append((end, line, start_time, arrival_time, weight))
            else:
                self.graph_dict[start] = [(end, line, start_time, arrival_time, weight)]
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
            
            edges.append((start, end, line, start_time, arrival_time, weight))
    return edges

def shortest_path(graph_dict, start, goal, trip_start_time):
    calc_start_time = time.time()
    distances, prev_nodes = dijkstra(graph_dict, start, goal, trip_start_time)
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


gg = Graph(edges('connection_graph_fixed.csv'))

shortest_path(gg.graph_dict, 'pl. Bema', 'DWORZEC GŁÓWNY', '12:00:00')
shortest_path(gg.graph_dict, 'Ogród Botaniczny', 'Rynek', '20:00:00')
# shortest_path(gg.graph_dict, 'Białowieska', 'most Grunwaldzki', '12:00:00')
shortest_path(gg.graph_dict, 'Kwiska', 'PL. GRUNWALDZKI', '09:00:00')
# shortest_path(gg.graph_dict, 'Iwiny - rondo', 'Hala Stulecia', '14:07:00')
# shortest_path(gg.graph_dict, 'Krzemieniecka', 'Prusa', '20:07:00')
shortest_path(gg.graph_dict, 'KOSZAROWA (Szpital)', 'Waniliowa', '07:07:00')
shortest_path(gg.graph_dict, 'Ossolineum (Uniwersytecka)', 'Kasprowicza', '23:07:00')
# shortest_path(gg.graph_dict, 'Na Ostatnim Groszu', 'Biegasa', '9:07:00')
# shortest_path(gg.graph_dict, 'Orla', 'pl. Strzegomski (Muzeum Współczesne)', '21:07:00')
shortest_path(gg.graph_dict, 'Damrota', 'GIEŁDOWA (Centrum Hurtu)', '00:12:00')
# shortest_path(gg.graph_dict, 'Łozina - Wrocławska (na wys. nr 18)', 'Chopina', '10:07:00')
# shortest_path(gg.graph_dict, 'Magellana', 'DWORZEC AUTOBUSOWY', '09:00:00')

# print("Shortest distance:", distance)
# print("Shortest path:", path)

# test = {'polskie_znaki_ó': 1}

# print(minutes_from_midnight('20:02:00'))
# print(minutes_from_midnight('25:02:00'))
