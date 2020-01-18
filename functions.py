import classes as classes


'''
def mutate(population, number_of_agent):
    new_population = classes.Population(number_of_agent)
    new_population.add_agents(population.select_best_agents(number_of_agent).get_agents())
    return new_population
'''

def mutate(agent, operator):
    new_population = classes.Population(number_of_agent)
    new_population.add_agents(population.select_best_agents(number_of_agent).get_agents())
    return new_population