import time
import Utils


    
def minutes_from_midnight(time):
    time_split = time.split(':')
    hours = int(time_split[0])
    minutes = int(time_split[1])
    if(hours >= 24):
        hours -= 24
    
    return hours*60+minutes

def to_time(minutes_from_midnight):
    minutes = minutes_from_midnight%60
    hours = int((minutes_from_midnight - minutes)/60)
    
    minutes = str(minutes)
    hours = str(hours)
    
    if len(minutes) < 2:
        minutes = '0' + minutes
        
    if len(hours) < 2:
        hours = '0' + hours
        
    return f"{hours}:{minutes}:00"

def print_solution(start_time, distance, path: list):
    print(f'time: {to_time(distance)}')
    print(f"start time: {start_time}")
    start_stop, curr_line, route_start_time, route_end_time = path[0]
    end_stop, next_line, _, _ = path[1]
    merged_route = []
    route_len = 1
    for i in range(1, len(path)):
        if curr_line != next_line:
            merged_route.append((start_stop, end_stop, route_start_time, route_end_time, curr_line))
            if next_line != '':
                start_stop, curr_line, route_start_time, route_end_time = path[i]
                end_stop, next_line, _, _ = path[i + 1]
            else:
                end_stop, _, _, route_end_time = path[i]
                

            route_len = 1
        else:
            route_len += 1
            _, _, _, route_end_time = path[i]
            end_stop, next_line, _, _ = path[i + 1]
    
    for start_stop, end_stop, start_start_time, end_arrival_time, line_num in merged_route:
        print(f'in: {start_stop} [{to_time(int(start_start_time%(24*60)))}]| line: {line_num}')
        print(f'out: {end_stop} [{to_time(int(end_arrival_time%(24*60)))}]| line: {line_num}')
    
    for i in range(0, 3):
        print("-")

