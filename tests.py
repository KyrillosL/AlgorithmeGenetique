import main2 as main

size = 8

#string_to_get = main.init_string_to_get(size)
#print("string to get: " + string_to_get)

population = main.Population(size)
print("INIT:")
print(population.select_best_agents(1)[0])

print("Mutation 1 bit - TEST 1")
population.select_best_agents(1)[0].mutation_bit_flip_1_n()
print(population.select_best_agents(1)[0])
print("Mutation 1 bit - TEST 2")
population.select_best_agents(1)[0].mutation_bit_flip_1_n()
print(population.select_best_agents(1)[0])

print("Mutation 3 bits - TEST 1")
population.select_best_agents(1)[0].mutation_bit_flip_3_n()
print(population.select_best_agents(1)[0])
print("Mutation 3 bits - TEST 2")
population.select_best_agents(1)[0].mutation_bit_flip_3_n()
print(population.select_best_agents(1)[0])





