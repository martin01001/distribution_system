class Truck:
    """
    Truck class to create Trucks objects

    truck_id : id of truck
    t_name : name of truck if empty or none will contains id
    t_capacity : the total weight can truck carry 

    self.route: Truck Route
     
    def set_address_to_truck(): add address must be visited by truck to list of truck addresses
      
    def set_boxes_in_truck(): set boxes must carry by truck
    set_truck_route() : Set the route that the truck must follow
    print_d() : print all details of object
    __str__() : override str method return just id
    
    """
    def __init__(self, truck_id, t_name = None, t_capacity = None):
        
        # set truck id
        self.truck_id = truck_id

        # check for name if exist and assign id instead if not
        if t_name == None or t_name == "":
            self.t_name = truck_id
        else:
            self.t_name = t_name
        
        # the total weight can truck carry 
        self.t_capacity = t_capacity

        self.load_weight = 0
        self.load_value = 0

        self.boxes = list() # boxes that truck carry 

        self.addresses = list() # Contain all addresses must to visit

        self.route = None # Truck Route

    # set truck route
    def set_truck_route(self, route):
        self.route = route


    # add address that must be visited by truck to list of truck addresses
    def set_address_to_truck(self, address):
        if address not in self.addresses:
            self.addresses.append(address)
    
    # set boxes must be in by truck
    def set_boxes_in_truck(self, list_of_boxes):
        for e in list_of_boxes: self.boxes.append(e)
        
    # calculate the weight of load in truck
    def calc_load_weight(self):
        load_weight = 0
        for box in self.boxes:
            load_weight += box.b_weight
        self.load_weight = load_weight

    # print all object details
    def print_d(self, p=True):
        s = f"Truck ID: {self.truck_id} \nName: {self.t_name} \nCapacity: {self.t_capacity} | Load weight: {self.load_weight} | Load Value: {self.load_value} \nRoute: {self.route}"
        if p:
            print(s)
        else:
            return s 

    # make object printable just id
    def __str__(self):
        return f"{self.truck_id}"