
class Address:
    """
    Address class to create addresses objects

    addr_id : id of address
    a_name : name of address if empty or none will contain id
    time_to : dictionary contain time between object and other objects

    set_time_to_other_addresses() : input: dictionary like {addr_id, required time}
    and fill time_to dictionary
    check_time() : return True if there is path between addresses else False
    print_d() : print all details of object
    __str__() : override str method return just id
    __eq__() : Compare two addresses based on address id
    
    """

    def __init__(self, addr_id, a_name=None):
        '''
        Initialize method
        '''

        # set address id
        self.addr_id = addr_id
        
        # check for name if exist and assign id instead if not
        if a_name == None or a_name == "":
            self.a_name = addr_id
        else:    
            self.a_name = a_name

        # create dictionary for time, and set time between the address and itself 0 
        self.time_to = {self.addr_id: 0.0} 
        
    # assign time between object and other addresses objects
    def set_time_to_other_addresses(self, list_of_addresses): 
        for address_id, time_to in list_of_addresses.items():
            self.time_to[address_id] = float(time_to)

    # check time between two addresses
    def check_time(self, address) -> bool:
        if  address.addr_id not in self.time_to.keys():
            return False
        elif self.time_to[address.addr_id] == 0.0:
            return False
        else:
            return True
        

    # print all object details
    def print_d(self, p=True) -> str:
        s = f"ID: {self.addr_id} Name {self.a_name}\ntime_to {self.time_to}"
        if p:
            print(s)
        else : 
            return s 

    # search on address in addresses list
    def what_the_index_in(self, addresses):
        m = len(addresses)
        if m == 0:
            return -1
        i = 0
        for i in range(m):
            if addresses[i] == self:
                return i
        if i == m-1:
            return -1


    # make object printable just id
    def __str__(self) -> str:
        return f"{self.addr_id}"

    # override compare
    def __eq__(self, __value: object) -> bool:
        if __value != None:
            return self.addr_id == __value.addr_id
        return False