import csv

class GTFSCSVParser(object):
    def parse_agency_file(self, agency_filename):
        self.agencies = []
        self.agency_id_by_name = {}

        with open(agency_filename, 'r') as fp:
            reader = csv.reader(fp)
            first_row = next(reader)

            agency_id_index = first_row.index('agency_id')
            agency_name_index = first_row.index('agency_name')

            for row in reader:
                agency_id = row[agency_id_index]
                agency_name = row[agency_name_index]

                self.agencies.append({
                    'agency_id': agency_id,
                    'agency_name': agency_name
                })

                self.agency_id_by_name[agency_name] = agency_id


    def get_agencies(self):
        return {'agencies' : self.agencies}

    def get_agency_id_by_name(self, agency_name):
        return self.agency_id_by_name[agency_name]
    
    def parse_routes_file(self, routes_filename):
        self.route_id_by_name = {}

        with open(routes_filename, 'r') as fp:
            reader = csv.reader(fp)
            first_row = next(reader)

            agency_id_index = first_row.index('agency_id')
            route_id_index = first_row.index('route_id')
            route_name_index = first_row.index('route_short_name')

            for row in reader:
                agency_id = row[agency_id_index]

                if agency_id not in self.route_id_by_name:
                    self.route_id_by_name[agency_id] = {}

                route_name = row[route_name_index]
                route_id = row[route_id_index]

                self.route_id_by_name[agency_id][route_name] = route_id

    def get_route_id_by_name(self, agency_id, route_name):
        return self.route_id_by_name[agency_id][route_name]

    def parse_stops_file(self, stops_filename):
        self.stop_ids_by_name = {}

        with open(stops_filename, 'r') as fp:
            reader = csv.reader(fp)
            first_row = next(reader)

            stop_id_index = first_row.index('stop_id')
            stop_name_index = first_row.index('stop_name')

            for row in reader:
                stop_name = row[stop_name_index]

                if stop_name not in self.stop_ids_by_name:
                    self.stop_ids_by_name[stop_name] = []
                
                stop_id = row[stop_id_index]

                if stop_id not in self.stop_ids_by_name[stop_name]:
                    self.stop_ids_by_name[stop_name].append(stop_id)

    def get_stop_ids_by_name(self, stop_name):
        return self.stop_ids_by_name[stop_name]

    def parse_trips_file(self, trips_filename):
        self.trip_ids_by_route_id = {}

        with open(trips_filename, 'r') as fp:
            reader = csv.reader(fp)

            first_row = next(reader)

            route_id_index = first_row.index('route_id')
            trip_id_index = first_row.index('trip_id')

            for row in reader:
                route_id = row[route_id_index]

                if route_id not in self.trip_ids_by_route_id:
                    self.trip_ids_by_route_id[route_id] = []

                trip_id = row[trip_id_index]

                self.trip_ids_by_route_id[route_id].append(trip_id)

    def get_trip_ids_by_route_id(self, route_id):
        return self.trip_ids_by_route_id[route_id]
    
    def parse_trip_shape(self, trip_filename, stops_filename, stop_times_filename, shapes_filename):
        self.shape_id_by_trip_id = {}
        self.shapes = {}

        self.stop_locations = {}
        self.trip_stops = {}

        with open(trip_filename, 'r') as fp:
            reader = csv.reader(fp)
            first_row = next(reader)

            trip_id_index = first_row.index('trip_id')
            shape_id_index = first_row.index('shape_id')

            for row in reader:
                trip_id = row[trip_id_index]
                shape_id = row[shape_id_index]

                if shape_id not in self.shapes:
                    self.shapes[shape_id] = []

                if trip_id not in self.shape_id_by_trip_id:
                    self.shape_id_by_trip_id[trip_id] = shape_id

        with open(stops_filename, 'r') as fp:
            reader = csv.reader(fp)
            first_row = next(reader)

            stop_id_index = first_row.index('stop_id')
            stop_lat_index = first_row.index('stop_lat')
            stop_lon_index = first_row.index('stop_lon')

            for row in reader:
                stop_id = row[stop_id_index]
                stop_lat = row[stop_lat_index]
                stop_lon = row[stop_lon_index]

                if stop_id not in self.stop_locations:
                    self.stop_locations[stop_id] = {}

                self.stop_locations[stop_id]['stop_lat'] = stop_lat
                self.stop_locations[stop_id]['stop_lon'] = stop_lon
        
        with open(stop_times_filename, 'r') as fp:
            reader = csv.reader(fp)
            first_row = next(reader)

            trip_id_index = first_row.index('trip_id')
            stop_id_index = first_row.index('stop_id')
            stop_sequence_index = first_row.index('stop_sequence')
            
            shape_dist_traveled_index = -1 
            if 'shape_dist_traveled' in first_row:
                shape_dist_traveled_index = first_row.index('shape_dist_traveled')

            for row in reader:
                trip_id = row[trip_id_index]

                if trip_id not in self.trip_stops:
                    self.trip_stops[trip_id] = []

                stop = {}

                stop['stop_id'] = row[stop_id_index]
                stop['stop_sequence'] = row[stop_sequence_index]

                if shape_dist_traveled_index != -1:
                    stop['shape_dist_traveled'] = row[shape_dist_traveled_index]
                
                self.trip_stops[trip_id].append(stop)


        with open(shapes_filename, 'r') as fp:
            reader = csv.reader(fp)
            first_row = next(reader)

            shape_id_index = first_row.index('shape_id')
            shape_pt_lat_index = first_row.index('shape_pt_lat')
            shape_pt_lon_index = first_row.index('shape_pt_lon')
            shape_pt_sequence_index = first_row.index('shape_pt_sequence')
            shape_dist_traveled_index = -1 if not 'shape_dist_traveled' in first_row else first_row.index('shape_dist_traveled')

            for row in reader:
                shape_id = row[shape_id_index]

                if shape_id in self.shapes:
                    shape_pt = {}

                    shape_pt['shape_pt_lat'] = row[shape_pt_lat_index]
                    shape_pt['shape_pt_lon'] = row[shape_pt_lon_index]

                    shape_pt['shape_pt_sequence'] = row[shape_pt_sequence_index]

                    if shape_dist_traveled_index != -1:
                        shape_pt['shape_dist_traveled'] = row[shape_dist_traveled_index]
                    
                    self.shapes[shape_id].append(shape_pt)
                    
    def get_first_trip_between_stops(self, first_stop_id, last_stop_id, route_id):
        trip_ids = self.trip_ids_by_route_id[route_id]

        for trip_id in trip_ids:
            stops_for_trip = self.trip_stops[trip_id]

            found_first_stop_id = False
            found_last_stop_id = False

            for stop in stops_for_trip:
                if stop['stop_id'] == first_stop_id:
                    found_first_stop_id = True

                if stop['stop_id'] == last_stop_id:
                    found_last_stop_id = True
                    break

            if found_first_stop_id and found_last_stop_id:
                return trip_id

        return -1

    def find_closest_shape_index(self, stop, shape_for_trip, curr_shape_index):
        valid_shapes = shape_for_trip[curr_shape_index:]
        for index_mod in range(len(valid_shapes)):
            if float(valid_shapes[index_mod]['shape_dist_traveled']) >= float(stop['shape_dist_traveled']):
                return index_mod + curr_shape_index

        return len(shape_for_trip) - 1

    def get_shape_between_stops_by_trip(self, first_stop_id, last_stop_id, trip_id):
        stops_for_trip = self.trip_stops[trip_id]
        #stops_for_trip.sort(lambda a,b: cmp(a['stop_sequence'], b['stop_sequence']))

        shape_id_for_trip = self.shape_id_by_trip_id[trip_id]
        shape_for_trip = self.shapes[shape_id_for_trip]

        using_shape_information = False
        curr_shape_index = 0
        prev_shape_index = 0

        found_first_stop_id = False;

        shape = []

        for stop in stops_for_trip:
            if stop['stop_id'] == first_stop_id:
                found_first_stop_id = True
                if 'shape_dist_traveled' in stop:
                    using_shape_information = True
                    curr_shape_index = self.find_closest_shape_index(stop, shape_for_trip, 0)
                    prev_shape_index = curr_shape_index

            if found_first_stop_id:
                if using_shape_information:
                    curr_shape_index = self.find_closest_shape_index(stop, shape_for_trip, prev_shape_index)
                    while prev_shape_index <= curr_shape_index:
                        curr_shape = shape_for_trip[prev_shape_index]
                        shape.append([curr_shape['shape_pt_lat'], curr_shape['shape_pt_lon']])
                        prev_shape_index += 1

                stop_location = self.stop_locations[stop['stop_id']]
                shape.append([stop_location['stop_lat'], stop_location['stop_lon']])


            if stop['stop_id'] == last_stop_id:
                break

        return {"`shape": shape}

parser = GTFSCSVParser()
parser.parse_agency_file('consolidated/agency.txt')
agency_id = parser.get_agency_id_by_name('Metro Transit')

parser.parse_routes_file('consolidated/routes.txt')
route_id = parser.get_route_id_by_name(agency_id, '1')

parser.parse_trips_file('consolidated/trips.txt')
trip_ids = parser.get_trip_ids_by_route_id(route_id)

parser.parse_stops_file('consolidated/stops.txt')
first_stop_ids = parser.get_stop_ids_by_name('10th Ave W & W Howe St')
print(first_stop_ids)
last_stop_ids = parser.get_stop_ids_by_name('3rd Ave & Union St')
print(last_stop_ids)

parser.parse_trip_shape('consolidated/trips.txt', 'consolidated/stops.txt', 'consolidated/stop_times.txt', 'consolidated/shapes.txt')

for first_stop_id in first_stop_ids:
    for last_stop_id in last_stop_ids:
        trip_id = parser.get_first_trip_between_stops(first_stop_id, last_stop_id, route_id)
        print(trip_id)
        if trip_id != -1:
            print(parser.get_shape_between_stops_by_trip(first_stop_id, last_stop_id, trip_id))
    