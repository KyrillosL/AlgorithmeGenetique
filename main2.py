'''
5 Flips puis 3 Flips puis 1 flip -> Utiliser la roulette -> Mettre à jour à chaque fois la moyenne. Au départ la même probabilité. Calculer la meilleure amélioration à chaque tout.
Pour l'instant on enlève le croisement

Sous forme de tableau ecart type
voir photo
Faire des courbes lisses en faisant la moyenne des représentations

Garder les mêmes graines aléatoires.

bit flip chaque gene a 1/N chance de changer
1 flip yen a qu'un qui change sur tout le chromosome
'''

#Various import
import random
from copy import copy
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np


class Agent:
    """ An agent has data (a string containing a number of "0") and the length of the string.
    For this problem, the score is the number of 1 in the string.
    We can perform various mutations on the string """

    def __init__(self, data, id):
        self.data = list(data)
        self.size = len(data)
        self.id = id

    def __str__(self):
        return "Agent " + str(self.id) + ", " + ''.join(self.data) + " | Score : " + str(self.score()) + "\n"

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        return (self.score() > other.score())

    def score(self):
        return 1 - ((self.size - self.data.count('1')) / self.size)

    # Swith a bit in the string by an index.
    def switch_bit(self, bit_to_flip):
        if (self.data[bit_to_flip] == '0') :
            self.data[bit_to_flip]='1'
        else:
            self.data[bit_to_flip]='0'

    # Flip one random bit in the string
    def mutation_bit_flip_1_n(self):
        bit_to_flip = random.random.randrange(0, self.size)
        switch_bit(bit_to_flip)

    def mutation_bit_flip_3_n(self):
        for x in range(3):
            self.mutation_bit_flip_1_n()

    def mutation_bit_flip_5_n(self):
        for x in range(5):
            self.mutation_bit_flip_1_n()

    def mutation_bit(self):
        print("mutation")
        for x in range(self.size):
            if random.random() < (1/self.size):
                self.switch_bit(x)




class Population:
    def __init__(self, size):
        self.size = size
        self.agents = []
        for x in range(size):
            l = [random.randrange(0, 2) for y in range(size)]
            self.agents.append(Agent("".join(str(x) for x in l), x))
        self.sort()

    def sort(self):
        self.agents.sort(reverse=True)

    def __str__(self):
        string_to_return = ""
        for agent in  self.agents:
            string_to_return += (agent.__str__())
        return string_to_return

    def __repr__(self):
        return self.__str__()

    def select_best_agents(self,number_of_agent_to_return):
        return self.agents[:number_of_agent_to_return]

    def select_random_agents(self,number_of_agent_to_return):
        return "@TODO"

    def select_tournament_agents(self,number_of_agent_to_return):
        return "@TODO"

    def croisement(self, agent1, agent2):
        #@TODO : ADD ONE POINT TO SLICE
        agent1Temporaire = copy(agent1)
        agent2Temporaire = copy(agent2)

        agent1.data = agent1.data[:int((agent1.size)/2)] #Cut the string at the half
        agent1.data +=  (agent2.data[int((agent2.size)/2):]) #Append the end of the second one

        agent2.data = agent2Temporaire.data[:int((agent2Temporaire.size)/2)]
        agent2.data +=  (agent1Temporaire.data[int((agent1Temporaire.size)/2):])



    def add(self,agents):
        for agent in agents:
            self.agents.insert(0,agent)


def init_string_to_get(size):
    return "1" * size


def mutate(population, number_of_agent):
    new_population = Population(number_of_agent)
    new_population.add(population.select_best_agents(number_of_agent))
    return new_population


size = 8
number_of_agent_to_select = 2

string_to_get = init_string_to_get(size)
print("string to get: " + string_to_get)

population = Population(size)
print("Population initiale")
print(population)

# print(population.select_best_agents(2))
generation = 0

while population.select_best_agents(1)[0].score() != 1.0:
    population.croisement(population.select_best_agents(2)[0], population.select_best_agents(2)[1])
    if population.select_best_agents(1)[0].score() <= 0.75:
        population = mutate(population, size - number_of_agent_to_select)
    population.sort()
    # print("Generation: ", str(generation))
    # print(population.select_best_agents(1)[0])
    plt.scatter(generation, population.select_best_agents(1)[0].score())
    generation += 1

print("Generation: ", str(generation))
print(population.select_best_agents(1)[0])

plt.ylim([0, 1])
plt.ylabel('Score')
plt.xlabel('Generation')
#plt.show()


print(population.select_best_agents(1)[0])
population.select_best_agents(1)[0].mutation_bit()
print(population.select_best_agents(1)[0])

print("fin")
