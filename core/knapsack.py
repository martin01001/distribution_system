def knapsack(capacity, weights, values, n):
        '''
        Select items to be in truck with max value and less or equal to capacity of truck
        input:  
            the weights of the items
            the values of the items
            the capacity of truck
            the number of the boxes
        output:
            the max value
            the matrix of DP process
        '''
        K = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
        
        for i in range(n + 1):
            for w in range(capacity + 1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif weights[i-1] <= w:
                    K[i][w] = max(values[i-1] + K[i-1][w-weights[i-1]], K[i-1][w])
                else:
                    K[i][w] = K[i-1][w]
        
        return K[n][capacity], K

def get_knapsack_items(K, weights, values, capacity, n):
        '''
        Get the boxes that selected 
        input: 
            the matrix of DP process to select the items
            the weights of the items
            the values of the items
            the capacity of truck
            the number of the boxes
        output:
            list of the indexes of selected items
        '''
        res = K[n][capacity] # the max value in truck
        w = capacity # capacity of truck
        items = [] # selected boxes
        
        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res == K[i-1][w]:
                continue
            else:
                items.append(i-1)
                res -= values[i-1]
                w -= weights[i-1]
        
        return items
  
def fill_the_truck_using_DP(truck, goods_list):
    capacity = truck.t_capacity
    values = [int(e["value"]) for e in goods_list]
    weights = [int(e["weight"]) for e in goods_list]
    n = len(goods_list)
    max_value, DP_matrix = knapsack(capacity, weights, values, n)
    indices_selected_boxes = get_knapsack_items(DP_matrix, weights, values, capacity, n)
    indices_selected_boxes.reverse()

    return indices_selected_boxes, max_value
