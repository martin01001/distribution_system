
class Box():
    """
    Box class to create boxes objects

    box_id : id of box
    b_name : name of box if empty or none will contain id
    b_weight : box weight
    b_value : box value
    going_to : box destination an if from address objects
    truck : id of truck that contains the box

    set_truck() : input: truck id and set to truck attribute
    set_destination() : input address and set to going_to attribute

    print_d() : print all details of object
    __str__() : override str method return just id
    __eq__() : Compare two boxes based on box id
    
    """

    def __init__(self, box_id, b_name = None, b_weight = None, b_value = None, going_to = None):

        # set box id
        self.box_id = box_id

        # check for name if exist and assign id instead if not
        if b_name == None or b_name == "":
            self.b_name  = box_id
        else:
            self.b_name = b_name

        self.b_weight = b_weight # set box weight
        self.b_value = b_value # set box value
        self.going_to = None # set box destination - this wll be an address object

        self.truck = None # truck object that contains the box

    
    # assign time between object and other addresses objects
    def set_truck(self, truck):
        self.truck = truck

    # set destination for box
    def set_destination(self, address):
        self.going_to = address

    # print all object details
    def print_d(self, p=True):
        s = f"Box ID: {self.box_id} Name {self.b_name} weight {self.b_weight} value {self.b_value} truck id {self.truck} Destination {self.going_to}"
        if p:
            print(s)
        else:
            return s

    # make object printable just id
    def __str__(self):
        return f"{self.box_id}"
    
    # override compare
    def __eq__(self, __value :object) -> bool:
        return self.box_id == __value.box_id
