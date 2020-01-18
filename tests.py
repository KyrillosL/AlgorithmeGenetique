import classes as main


size = 8
population = main.Population(size)
print("INIT:")
print(population.select_best_agents(1).get(0))
print("****************************************************")

print("Mutation")
print("1 bit")
population.select_best_agents(1).get(0).mutation_bit_flip_1_n()
print("\tTest 1", population.select_best_agents(1).get(0))
population.select_best_agents(1).get(0).mutation_bit_flip_1_n()
print("\tTest 2",population.select_best_agents(1).get(0))
print("")

print("3 bits ")
population.select_best_agents(1).get(0).mutation_bit_flip_3_n()
print("\tTest 1",population.select_best_agents(1).get(0))
population.select_best_agents(1).get(0).mutation_bit_flip_3_n()
print("\tTest 2",population.select_best_agents(1).get(0))
print("")

print("5 bits")
population.select_best_agents(1).get(0).mutation_bit_flip_5_n()
print("\tTest 1",population.select_best_agents(1).get(0))
population.select_best_agents(1).get(0).mutation_bit_flip_5_n()
print("\tTest 2",population.select_best_agents(1).get(0))
print("")

print("bit flip")
population.select_best_agents(1).get(0).mutation_bit()
print("\tTest 1",population.select_best_agents(1).get(0))
population.select_best_agents(1).get(0).mutation_bit()
print("\tTest 2",population.select_best_agents(1).get(0))
print("****************************************************")

print("Selection - Population Initiale: ")
population = main.Population(size)
print(population)

print("Selection - 2 Best agents : ")
new_population = population.select_best_agents(2)
print(new_population)

print("Selection - 4 Best agents : ")
new_population = population.select_best_agents(4)
print(new_population)


print("Selection - 2 Random agents : ")
new_population = population.select_random_agents(2)
print(new_population)

print("Selection - 4 Random agents : ")
new_population = population.select_random_agents(4)
print(new_population)


print("Selection - 2 Tournament agents : ")
new_population = population.select_tournament_agents(2, 10)
print(new_population)

print("Selection - 4 Tournament agents : ")
new_population = population.select_tournament_agents(4, 10)
print(new_population)

print("****************************************************")

print("Croisement : avant")
new_population = population
print(population.get(0))
print(population.get(1))
new_population.croisement(new_population.get(0),new_population.get(1))
print("Croisement : apres")
print(population.get(0))
print(population.get(1))






