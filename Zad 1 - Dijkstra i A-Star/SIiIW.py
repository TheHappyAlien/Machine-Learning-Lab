import csv

def file_converter(filename, encoding):
    stop_dictionary = {}
    stop_transform_dict = {} 

    with open(filename, 'r', encoding=encoding) as file:
        reader = csv.reader(file)
        header = next(reader)
        
        for row in reader:
            start_stop = row[5]
            end_stop = row[6]
            start_stop_lat = row[7]
            start_stop_lon = row[8]
            end_stop_lat = row[9]
            end_stop_lon = row[10]
             
            if start_stop in stop_dictionary:
                stop_dictionary[start_stop][0].add(start_stop_lon)
                stop_dictionary[start_stop][1].add(start_stop_lat)
            else:
                stop_dictionary[start_stop] = (set(start_stop_lon), set(start_stop_lat))
           
            if end_stop in stop_dictionary:
                stop_dictionary[end_stop][0].add(end_stop_lon)
                stop_dictionary[end_stop][1].add(end_stop_lat)
            else:
                stop_dictionary[end_stop] = (set(end_stop_lon), set(end_stop_lat)) 
        
        for elem in stop_dictionary:
            longitute_set = stop_dictionary[elem][0]
            longitudes_to_remove = set()
            latitude_set = stop_dictionary[elem][1]
            latitude_to_remove = set()
            for stop_lon in longitute_set:
                   if len(stop_lon) < 6:
                      longitudes_to_remove.add(stop_lon)
            for to_remove in longitudes_to_remove:
                longitute_set.remove(to_remove)
            
            for stop_lat in latitude_set:
                if len(stop_lat) < 6:
                    latitude_to_remove.add(stop_lat)
            for to_remove in latitude_to_remove:
                latitude_set.remove(to_remove) 

        for elem in stop_dictionary:
            longitute_set = stop_dictionary[elem][0]
            avg_lon = avg_from_set(longitute_set)
            latitude_set = stop_dictionary[elem][1]
            avg_lat = avg_from_set(latitude_set)
            for stop_lon in longitute_set:
                stop_transform_dict[stop_lon] = avg_lon
            for stop_lat in latitude_set:
                stop_transform_dict[stop_lat] = avg_lat
        
        print(stop_dictionary['Renoma'])
        print(avg_from_set(stop_dictionary['Renoma'][0]))
        
    with open("connection_graph_fixed.csv", 'w', encoding=encoding) as output_file:
        with open(filename, 'r', encoding=encoding) as input_file:
            reader = csv.reader(input_file)
            header = next(reader)
            
            header_row = ''
            for elem in header:
                header_row += elem + ','
                
            output_file.write(header_row[0:-1] + "\n")
            for row in reader:
                num = row[0]
                company = row[1]
                line = row[2]
                departure_time = row[3]
                arrival_time = row[4]
                start_stop = row[5]
                end_stop = row[6]
                start_stop_lat = row[7]
                start_stop_lon = row[8]
                end_stop_lat = row[9]
                end_stop_lon = row[10]
                
                if stop_transform_dict[start_stop_lat]:
                    start_stop_lat = stop_transform_dict[start_stop_lat]
                else:
                    print("dupa_start_lat")

                if stop_transform_dict[start_stop_lon]:
                    start_stop_lon = stop_transform_dict[start_stop_lon]
                else:
                    print("dupa_start_lon")

                if stop_transform_dict[end_stop_lat]:
                    end_stop_lat = stop_transform_dict[end_stop_lat]
                else:
                    print("dupa_end_lat")

                if stop_transform_dict[end_stop_lon]:
                    end_stop_lon = stop_transform_dict[end_stop_lon]
                else:
                    print("dupa_end_lon")

                output_file.write(f"{num},{company},{line},{departure_time},{arrival_time},{start_stop},{end_stop},{start_stop_lat},{start_stop_lon},{end_stop_lat},{end_stop_lon}\n")

def avg_from_set(set):
    avg = 0
    count = 0.0
    for elem in set:
        avg += float(elem)
        count += 1.0
    return round((avg / count), 8)

if __name__ == "__main__":
    file_converter('connection_graph.csv', 'utf8')