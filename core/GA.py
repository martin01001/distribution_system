from .Route import Route
import random
import numpy as np
import gc
import math

# initialize phase
def generate_chromosome(truck, main_address):
    '''
    Generate one individual
    input : truck instance and main address
    output : route instance
    '''
    # create route instance
    route_chromosome = Route(truck) 
    # set main address to route 
    route_chromosome.main_address = main_address
    # add main address to first and end addresses list in route
    route_chromosome.set_full_route()
    # shuffle addresses - make random chromosome
    route_chromosome.shuffle_route_addresses()
    # check if route is valid if not we still shuffle the route
    # till we get valid route
    while not route_chromosome.is_valid_route():
        route_chromosome.shuffle_route_addresses()
    return route_chromosome



def initialize_population(n, truck, main_address):
    '''
    generate first population
    Input: population size and truck and main address
    output: list of individuals 
    '''
    k_address = len(truck.addresses) # Number of addresses the truck must visit
    max_route_number = math.factorial((k_address -1)) # Calculate maximum routs possible not all of them valid route
    population = [] # The generated population 
    for i in range(n):
        rt = generate_chromosome(truck, main_address)  # Generate individual      
        
        while rt in population and i < max_route_number: # if individual already exist try again
            rt = generate_chromosome(truck, main_address)
        
        if rt not in population: # check after loop if found new individual maybe reach maximum and stop on existing one
            population.append(rt)

    return population
    


def fitness(individual):
    '''
    calculate fitness value for individual
    input: individual
    output: float value in negative
    '''
    total_time = individual.get_total_time()

    return (-1 * float(total_time)) 


def calc_fitness_for_generation(population):
    '''
    calculate fitness values for all population
    input: population
    output: tuple with two elements :
            first one fitness_proportion 
            second one new_fitnesses after covert to positive values with same weight
    '''
    total_fitness_val = 0 # Total fitness value for population
    fitness_values = [] # Negative values for fitnesses
    fitness_proportion = [] # Proportion for each individual based on fitness value

    # calculate fitness value for each individual in population
    for individual in population:
        fitness_value = fitness(individual)
        
        fitness_values.append(fitness_value)
    
    min_value = abs(min(fitness_values)) # Get minimum value and convert to positive
    new_fitnesses = [e + min_value + 1 for e in fitness_values] # Convert fitnesses values to positive
    
    for r in range(len(new_fitnesses)):
        population[r].fitness = new_fitnesses[r]

    # calculate proportion for each individual in population
    total_fitness_val = sum(new_fitnesses) # Get total
    # Calculate proportion for each individual 
    # Scale proportion for best selection
    fitness_proportion = [((x / total_fitness_val)*10) for x in new_fitnesses]
    
    return fitness_proportion, new_fitnesses


def selection(population, fitness_proportion):
    '''
    select individuals from population based on fitness proportion values
    # input : population, fitness proportion for every individual
    # output: list of selected individuals
    '''
    truck = population[0].trk
    main_address = population[0].main_address

    m = len(population) # Get Length of population
    k_top = 1 # Top individual number to keep
    selected_population = []
    
    n_sorted_pop = sorted(population,key= lambda x : x.fitness, reverse=True)
    top_k_individual = n_sorted_pop[:k_top]
    
    # Keep Top k best fitness values
    for i in range(k_top):
        rt_object = Route(truck)
        rt_object.main_address = main_address
        rt_object.route = top_k_individual[i].route.copy()
        rt_object.fitness = top_k_individual[i].fitness
        rt_object.set_full_route()
        selected_population.append(rt_object)


    # Select individuals
    selected_population_h = random.choices(population=population,weights=fitness_proportion,k=m-k_top)
    
    for i in range(m-k_top):
        rt_object = Route(truck)
        rt_object.main_address = main_address
        rt_object.route = selected_population_h[i].route.copy()
        rt_object.fitness = selected_population_h[i].fitness
        rt_object.set_full_route()
        selected_population.append(rt_object)
     

    return selected_population

# Create new child from two parents
def create_child(p1, p2, start, end):
    p1_route_rm = p1.route[1:-1]
    p2_route_rm = p2.route[1:-1]

    child_p1 = [None] * (len(p1.route) - 2)
    child_p1[start:end] = p1_route_rm[start:end]

    p2_route = [item for item in p2_route_rm if item not in child_p1]

    child_p1[end:] = p2_route[:len(child_p1) - end]
    child_p1[:start] = p2_route[len(child_p1) - end:]
    
    # Create new object has the generated route
    child = Route(p1.trk)
    child.route = child_p1
    child.main_address = p1.main_address
    child.set_full_route()

    return child

def crossover(parent_1, parent_2, PC, max_retries=5):

    r = np.random.random() # random value in range ]0-1[
    if r < PC:
        retries = 0
        while retries < max_retries:
            point1 = random.randint(1, len(parent_1.route) - 2)
            point2 = random.randint(1, len(parent_1.route) - 2)
            
            if point1 > point2:
                point1, point2 = point2, point1

            # Generate new children
            child_1 = create_child(parent_1, parent_2, point1, point2)
            child_2 = create_child(parent_2, parent_1, point1, point2)

            # check if children is valid
            if child_1.is_valid_route() and child_2.is_valid_route():
                return child_1, child_2

            retries += 1

    return parent_1, parent_2


def mutation(individual, PM):
    '''
    swap between two addresses in rout
    input: individual, Probability of mutation
    output: the same individual or new one after swapping
    '''
    r = np.random.random() # Get random number in ]0,1[
    if r < PM :
        l = len(individual.route) - 2
        # generate random two numbers to swap position
        f = random.randint(1, l)
        s = random.randint(1, l)

        # swap addresses break after make sure the new route is valid route
        i = 5 # Number of trying times
        while not individual.swap_two_addresses_in_route(f,s) and i > 0:
            f = random.randint(1, l)
            s = random.randint(1, l)
            i -= 1
        
        # make new instance to avoid reference issues
        after_mut_individual = Route(individual.trk)
        after_mut_individual.main_address = individual.main_address
        after_mut_individual.route = individual.route.copy()
        return after_mut_individual
    else:
        return individual

def crossover_mutation(selected_population, pc, pm):
    '''
    crossover and mutation for selected population
    input: select population, probability of crossover and probability of mutation
    output: new population
    '''
    N = len(selected_population)
    cross_population = []
    new_population = []
    # crossover
    for i in range(0, N, 2):
        parent_1 = selected_population[i]
        parent_2 = selected_population[i+1]
        child_1, child_2 = crossover(parent_1, parent_2, pc)
        cross_population.append(child_1)
        cross_population.append(child_2)
    
    # mutation
    for j in range(N):
        individual = mutation(cross_population[j], pm)
        new_population.append(individual)
    

    return new_population


def GA_Main_loop(pop_size, max_generations, pc, pm, truck, main_address):
    '''
    Main loop for genetic algorithm
    input:
        Population size, maximum generations counts, probability of crossover, probability of mutation
        truck, main address
    output: Shortest Valid Route the algorithm find after generations counts  

    1- encoding route : 
        [main_address, address_1, address_2, address_4, ... , address_n, main_address]
    2- initialize first population with size = pop_size
    3- fitness calculation
    4- selection based on fitness values
    5- Generate new generation
        a- crossover
        b- mutation
    6- repeat steps 3 4 5 until arrive acceptable solution or to arrive max_generations
    '''
    # initialize first population
    population = initialize_population(pop_size, truck, main_address)
    
    # make population length even by drop last one if length is odd
    if len(population) % 2 != 0:
        population.pop()
 
    best_fitness_overall = float('-inf') # best fitness value of all calculated generations
    best_route_overall = Route(truck) # best individual of all calculated generations
    best_route_overall.main_address = main_address

    max_no_improvement_generations = 300 # Max number of no improvement generations
    no_improvement_generations = 0 # Number of no improvement generations

    # Loop to arrive max_generation or arrive acceptable solution
    for i_gen in range(max_generations):
        
        # Calculate fitness value for all population individuals 
        # fitness_proportion: the proportion for each individual - list
        # population_fitnesses: the fitness value for each individual - list
        fitness_proportion, population_fitnesses = calc_fitness_for_generation(population)
        
        # Get best fitness in population
        best_fitness = max(population_fitnesses)   

        # Check if the best of current generation best than the best overall generation to set instead it
        if best_fitness > best_fitness_overall:
            # Get the best individual which has greatest fitness value in generation
            best_individual_index = population_fitnesses.index(best_fitness)
            best_route_overall.route = population[best_individual_index].route.copy() # Get copy of the best route
            best_route_overall.fitness = best_fitness # Set fitness to route
            best_fitness_overall = best_fitness # change best fitness overall
            no_improvement_generations = 0 # Reset no improvement generations number
        else:
            no_improvement_generations += 1 # if no improvement increase by 1


        # print the beat of generation
        # print(f"\ri_gen = {i_gen:06}  -f = {best_fitness_overall:03} -time {best_route_overall.get_total_time()}", end='')
        
        # Check termination condition
        if no_improvement_generations >= max_no_improvement_generations:
            break

        # generate new population to make next generation
        selected_population = selection(population, fitness_proportion)
        population = crossover_mutation(selected_population, pc, pm)
        
        # Clean up memory after each generation
        gc.collect()

    # print best solution
    # print()
    truck.route = best_route_overall
    truck.route.get_total_time()
    # truck.set_truck_route(best_route_overall)  

# main method
def find_route_using_GA(truck, main_address):
    POP_SIZE = 200 # population size
    MAX_GENERATIONS = 2000 # max generations
    PC = 0.8 # probability for crossover
    PM = 0.2 # probability for mutation
    if len(truck.boxes) > 1:
        # call genetic algorithm main loop
        GA_Main_loop(POP_SIZE, MAX_GENERATIONS, PC, PM, truck, main_address)
    
        