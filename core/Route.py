import numpy as np
class Route:
    """
    Route class to create Routes objects
    self.trk = truck
    self.addresses_count : the number of address must pass on
    self.route : Route is 1D array indexes are the arrange and values are addresses
    self.main_address : the main address to start from and end in
    self.total_time : the total time of route
    self.fitness : fitness value for the route
    
    set_addresses_to_route : return truck addresses that the route must contain
    shuffle_route_addresses : shuffle route addresses in route
    set_full_route :  add main address to first and last of route attribute
    is_valid_route : return true if route is valid or false if not
    get_total_time : get the total time of route
    swap_two_addresses_in_route : swap between two addresses in route based on two integer number
    print_route : print all details of route
    __str__ : override on str() to make route printable
    __eq__() : override equal operation
    __hash__ : make route hashable
    """

    def __init__(self, truck):
        self.trk = truck
        self.addresses_count = len(truck.addresses)
        self.route = np.array(self.set_addresses_to_route())
        self.main_address = None
        self.total_time = 0
        self.fitness = None



    # assign the addresses that the truck must visit
    def set_addresses_to_route(self):
        return [ e for e in self.trk.addresses ]

    # shuffle Route addresses
    def shuffle_route_addresses(self):
        np.random.shuffle(self.route[1:-1])
        
    # add start point and destination to route
    def set_full_route(self):
        if self.route[0] != self.route[-1] or self.addresses_count == 1:
            if self.main_address != None:
                self.route = np.concatenate(([self.main_address], self.route, [self.main_address]))

    
    
    # check if the route Valid route
    def is_valid_route(self):

        if self.route[0] != self.main_address and self.route[-1] != self.main_address:
            return False

        if len(self.route) < (self.addresses_count + 2):
            return False

        # check if exist path to neighbor address
        for i in range(1, len(self.route)):
            if not self.route[i - 1].check_time(self.route[i]):
                return False
        
        # check if exist duplicated address
        for i in range(1, len(self.route)):
            for j in range(i + 1, len(self.route)):
                if self.route[i] == self.route[j]:
                    return False
        
        return True


    # return total time to route
    def get_total_time(self):
        self.total_time = sum(self.route[i - 1].time_to[self.route[i].addr_id] for i in range(1, len(self.route)))
        return self.total_time
    
    def swap_two_addresses_in_route(self, i, j):
        if i == j:
            return True
        else:
            self.route[i], self.route[j] = self.route[j], self.route[i]
            if self.is_valid_route():
                return True
        return False


    # print all object details
    def print_route(self, p=True):
        rt = " ".join(str(a) for a in self.route)
        s = f"Truck: {self.trk}\nRoute: {rt}"
        if p:
            print(s)
        else:
            return s

    # make object printable just id
    def __str__(self):
        rt = " -> ".join(f"{self.route[i - 1]} ({self.route[i - 1].time_to[self.route[i].addr_id]})" for i in range(1, len(self.route)))
        return rt + f" -> {self.route[-1]}"
    
    # override equal operation
    def __eq__(self, __value: object) -> bool: 
        if __value != None :
            if self.trk.truck_id != __value.trk.truck_id:
                return False
        else:
            return False

        return np.array_equal(self.route[1:-1], __value.route[1:-1])
    
    def __hash__(self):
        return hash((self.trk, str(self)))