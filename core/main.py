from .Route import Route
from .Truck import Truck
from .Address import Address
from .Box import Box
from .knapsack import fill_the_truck_using_DP
from .GA import find_route_using_GA
import json


# Read The Data and initialize all necessary objects

def Read_Addresses(data :dict):
    '''
    Read Addresses Details from dictionary Received from front end
    initialize Address objects
    set time between every pair of addresses
    return list of addresses objects
    '''
    addresses_list = [] # list of object addresses

    addresses_number = int(data["addresses_number"]) # number of addresses

    addresses = data["info"] # access addresses information

    # initialize addresses objects and fill addresses_list
    for e in addresses.keys():
        address_id = data["info"][e]["id"]
        address_name = data["info"][e]["name"]
        c_address = Address(address_id, address_name)
        addresses_list.append(c_address)

    # set time between addresses
    for i in range(addresses_number):
        time_to_list = data["info"][addresses_list[i].addr_id]['time_to']
        addresses_list[i].set_time_to_other_addresses(time_to_list)
    
    return addresses_list

def Read_Goods(data: dict, addresses :list):
    '''
    Read Goods Details from dictionary Received from front end
    initialize Box objects
    return list of Boxes objects
    '''

    goods_list = []
    goods = data["info"] # access goods details

    # initialize boxes objects and fill goods_list
    for e in goods.keys():
        box_id = goods[e]["id"]
        box_name = goods[e]["name"]
        box_weight = int(goods[e]["weight"])
        box_value = float(goods[e]["value"])

        c_box = Box(box_id, box_name, box_weight, box_value)
        # set box destination
        for address in addresses:
            if str(goods[e]["going_to"]) == str(address.addr_id):
                c_box.set_destination(address)
        
        goods_list.append(c_box)

    return goods_list

def Read_Trucks(data :dict):
    '''
    Read Trucks Details from dictionary Received from front end
    initialize Truck objects
    return list of Trucks objects
    '''
    trucks_list = []
    trucks = data["info"] # access goods details

    # initialize Trucks objects and fill trucks_list
    for e in trucks.keys():
        truck_id = trucks[e]["id"]
        truck_name = trucks[e]["name"]
        truck_capacity = int(trucks[e]["capacity"])
        c_truck = Truck(truck_id, truck_name, truck_capacity)
        trucks_list.append(c_truck)

    return trucks_list

def Read_all(data :dict):
    # Call the methods to initial objects

    # Read addresses information and create objects
    addresses = data["details"]["addresses_information"]
    addresses_list = Read_Addresses(addresses)

    # Read Goods information and create objects
    goods = data["details"]["repository_information"]
    goods_list = Read_Goods(goods, addresses_list)

    # Read Trucks information and create objects
    trucks = data["details"]["trucks"]
    trucks_list = Read_Trucks(trucks)

    return addresses_list, goods_list, trucks_list

# call knapsack file to sort the goods on trucks
def sort_goods_on_trucks(trucks, goods):

    # initial an array contains dictionaries of boxes must sorted
    remaining_goods = []
    for i in range(len(goods)):
        box = {
            "index":i,
            "value":goods[i].b_value,
            "weight": goods[i].b_weight
        }
        remaining_goods.append(box)

    # loop on trucks to fill with boxes
    for i in range(len(trucks)):

        # Call Dynamic algorithm to fill truck
        boxes_indices, max_value =  fill_the_truck_using_DP(trucks[i], remaining_goods)

        # add boxes to truck and set truck attribute to box
        for j in boxes_indices:
            for k in range(len(remaining_goods)):
                if j == k :
                    goods[remaining_goods[k]["index"]].set_truck(trucks[i])
                    trucks[i].boxes.append(goods[remaining_goods[k]["index"]])
                    break
        
        # update the list of boxes to remove sorted boxes
        remaining_goods = [e for e in remaining_goods if remaining_goods.index(e) not in boxes_indices]
        
        trucks[i].calc_load_weight()
        trucks[i].load_value = max_value

        # if the boxes finished stop
        if len(remaining_goods) == 0 :
            break

# set address to trucks based on what boxes its carry
def fill_truck_addresses_list(trucks):
    m = len(trucks)
    for i in range(m):
        for box in trucks[i].boxes:
            trucks[i].set_address_to_truck(box.going_to)

# covert solution to dictionary in python
def get_result(trucks, goods_list):
    data = {
        "remaining_goods": dict(),
        "trucks_out": dict(),
        "trucks": dict()
    }
    # Get remaining goods in warehouse
    for box in goods_list:
        if box.truck == None:
            data["remaining_goods"][box.box_id] = {
                "box_name" : box.b_name,
                "box_weight" : box.b_weight,
                "box_value" : box.b_value,
                "box_destination" : box.going_to.addr_id
            }
    
    # Get trucks Details 
    for truck in trucks:
        
        if len(truck.boxes) == 0:
            
            data["trucks_out"][truck.truck_id] = {
                "truck_name": truck.t_name,
                "truck_capacity": truck.t_capacity
            }

        else:
            
            truck_boxes = []
            for box in truck.boxes:
                s = f"{box.box_id} {box.b_name} {box.b_weight} {box.b_value} {box.going_to.addr_id}"
                truck_boxes.append(s)
            
            truck_addresses = []
            for address in truck.addresses:
                s = f"{address.addr_id} {address.a_name}"
                truck_addresses.append(s)

            data["trucks"][truck.truck_id] = {
                "truck_name": truck.t_name,
                "truck_capacity": truck.t_capacity,
                "truck_load_weight": truck.load_weight,
                "truck_load_value": truck.load_value,
                "truck_boxes": truck_boxes,
                "truck_addresses": truck_addresses,
                "Route_Total_time": truck.route.total_time,
                "truck_route": str(truck.route)
            }

    return data

# start the app core to call all algorithms and get result
def start_find_solution(data):
    
    # Read data
    addresses_list, goods_list, trucks_list = Read_all(data)

    # The main address
    warehouse_address = addresses_list[0]

    # sort boxes on trucks
    sort_goods_on_trucks(trucks = trucks_list, goods = goods_list)

    # set all address must visited by trucks to addresses attribute in trucks
    fill_truck_addresses_list(trucks=trucks_list)

    # Call genetic algorithm to find best route to all trucks
    for truck in trucks_list:
        if len(truck.addresses) > 1:
            find_route_using_GA(truck=truck, main_address=warehouse_address)
        # check if there is just one address 
        if len(truck.addresses) == 1:
            rt = Route(truck)
            rt.main_address = warehouse_address
            rt.set_full_route()
            rt.get_total_time()
            truck.route = rt
        
    
    # convert solution to dictionary
    result = get_result(trucks_list, goods_list)
    # convert to json file to send via network
    # result_json = json.dumps(result)
    return result


