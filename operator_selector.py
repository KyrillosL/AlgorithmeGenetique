'''
Roulette fixe. On attribut une probabilité qui augmente et qui descend si les opérateurs sont biens ou non.
f(popm) -> op1 -> f (popm+1)
si f(popm+1) est mieux : on récompense(et on dégrade les autres), sinon on dégrade(et on récompense les autres).
'''


import classes as main
import matplotlib.pyplot as plt

import functions as functions
import random
plt.style.use('seaborn-whitegrid')


def basic_operator(population):
    generation = 0
    while population.select_best_agents(1).get(0).score() != 1.0:
        population.croisement(population.select_best_agents(2).get(0), population.select_best_agents(2).get(1))
        #if population.select_best_agents(1).get(0).score() <= 0.75:
        population = functions.mutate(population, size - number_of_agent_to_select)
        population.sort()
        print("Generation: ", str(generation))
        print(population.select_best_agents(1).get(0))
        plt.scatter(generation, population.select_best_agents(1).get(0).score())
        generation += 1
    print("Generation: ", str(generation))

#basic_operator(population)


class Operator:
    def __init__(self, init_prob):
        self.probability = init_prob
        self.score = 0
        self.temporary_bit_to_switch = []


    def __str__(self):
        return  "probability: " +str(self.probability) + " | Score : " + str(self.score)

    def __repr__(self):
        return self.__str__()

    def mutate(self, agent, is_computing=False):
        print("dans le mauvais mutate")
        return "Mutate should be overrided"


    def Compute_Score(self,agent):
        copy_of_agent = agent.__copy__()
        self.mutate(copy_of_agent, True)
        self.score =  copy_of_agent.score()

    def __gt__(self, other):
        return (self.score > other.score)

    # Switch a bit in the string by an index.
    def switch_bit(self,agent, bit_to_flip):
        if (agent.data[bit_to_flip] == '0') :
            agent.data[bit_to_flip]='1'
        else:
            agent.data[bit_to_flip]='0'

# Flip one random bit in the string
class mutation_bit_flip_1_n(Operator):

    def __str__(self):
        return "BitFlip_1_n "+ super().__str__()

    def __repr__(self):
        return self.__str__()


    def mutate(self,agent,is_computing=False):

        #print("Using 1n, previous score: ", agent.score())

        if is_computing:
            bit_to_flip = random.randrange(0, agent.size)
            self.temporary_bit_to_switch.clear()
            self.temporary_bit_to_switch.append(bit_to_flip)

        super().switch_bit(agent, self.temporary_bit_to_switch[0])

        #print("Using 1n, new score: ", agent.score())
        return agent

# Flip 3 random bit in the string
class mutation_bit_flip_3_n(Operator):

    def __str__(self):
        return "BitFlip_3_n "+ super().__str__()

    def __repr__(self):
        return self.__str__()

    def mutate(self, agent,is_computing=False):
        #print("Using 3n, previous score: ", agent.score())
        #only if the length of our data is > 3
        if agent.size > 3:

            if is_computing:
                # We first select 3 random bits to flip
                # eg : >>> random.sample([1, 2, 3, 4, 5],  3)  -> [4, 1, 5]
                number_to_choose_in = []
                for x in range(agent.size):
                    number_to_choose_in.append(x)
                # print("NUMBERS TO CHOOSE IN: ", number_to_choose_in)
                random_numbers = random.sample(number_to_choose_in, 3)
                # print("RANDOM NUMBERS: ", random_numbers)
                # flip the bits
                self.temporary_bit_to_switch.clear()
                self.temporary_bit_to_switch = random_numbers
            for x in self.temporary_bit_to_switch:
                #print("x",x)
                super().switch_bit(agent,x)
            #print("Using 3n, new score: ", agent.score())
            return agent

class mutation_bit_flip_5_n(Operator):

    def __str__(self):
        return "BitFlip_5_n "+ super().__str__()

    def __repr__(self):
        return self.__str__()

    def mutate(self, agent,is_computing=False):
        #print("Using 5n, previous score: ", agent.score())
        #only if the length of our data is > 3
        if agent.size > 5:
            if is_computing:
                #We first select 5 random bits to flip
                #eg : >>> random.sample([1, 2, 3, 4, 5],  3)  -> [4, 1, 5]
                number_to_choose_in = []
                for x in range(agent.size):
                    number_to_choose_in.append( x)
                #print("NUMBERS TO CHOOSE IN: ", number_to_choose_in)
                random_numbers = random.sample(number_to_choose_in, 5)
                #print("RANDOM NUMBERS: ", random_numbers)
                self.temporary_bit_to_switch.clear()
                self.temporary_bit_to_switch= random_numbers
            #flip the bits
            for x in self.temporary_bit_to_switch:
                #print("x", x)
                super().switch_bit(agent,x)
            #print("Using 5n, new score: ", agent.score())
            return agent

class mutation_bit(Operator):
    def mutate(self, agent):
        for x in range(self.size):
            if random.random() < (1/self.size):
                Operator.switch_bit(agent,x)

class Roulette():
    def __init__(self,population, list_operators):
        self.population = population
        self.list_operators = list_operators




class roulette_fixe(Roulette):

    def roule(self):

        # we compute the score
        #print("All scores : ")
        for x in self.list_operators:
            x.Compute_Score(self.population.select_best_agents(1).get(0))
            #print("\t",x)


        best_operator = max(self.list_operators)
        #print(list_operators)
        #print("best operator : ", best_operator)

        #if (best_operator.probability +  1/(nb_operateurs*10)) <1:
        #    best_operator.probability +=  1/(nb_operateurs*10)


        if best_operator.score >self.population.select_best_agents(1).get(0).score():
            new_agent = best_operator.mutate(self.population.select_best_agents(1).get(0))
            self.population.select_best_agents(1).set(0, new_agent)
            #print(best_operator) ICI

            if (best_operator.probability +  1/(self.nb_operateurs*10)) <0.90:
               best_operator.probability +=  1/(self.nb_operateurs*10)

            total_prob=0
            for x in self.list_operators:
               total_prob += x.probability
               if x != best_operator:
                   if (x.probability -  (1/(self.nb_operateurs*10)/2)  ) > 0.1:
                        x.probability-= (1/(self.nb_operateurs*10)/2)

            #print(total_prob)


        #print("original agent score: ", population.select_best_agents(1).get(0).score())
        #print("new agent score: ", new_agent.score())



        #we take the best one and update it's probability


        #print("best operator: ", best_operator)
        #print("new agent",population.select_best_agents(1).get(0) )
        return list_operators


class roulette_adaptative(Roulette):

    def roule(self):
        # we compute the score
        for x in self.list_operators:
            x.Compute_Score(self.population.select_best_agents(1).get(0))
            #print(x)
        #we take the best one and update it's probability

        best_operator = max(self.list_operators)

        new_agent =  best_operator.mutate(self.population.select_best_agents(1).get(0))

        #print("o: ", population.select_best_agents(1).get(0).score())
        #print("n: ", new_agent.score())
        if new_agent.score() > self.population.select_best_agents(1).get(0).score():
            #print("setting new")
            self.population.select_best_agents(1).set(0,new_agent)

            if (best_operator.probability + 1 / (self.nb_operateurs * 10)) < 1:
                best_operator.probability += 1 / (self.nb_operateurs * 10)

            for x in self.list_operators:
                if x != best_operator:
                    if (x.probability - 1 / (self.nb_operateurs * 10)) > 0:
                        x.probability -= 1 / (self.nb_operateurs * 10)

        else:
            print("BAD BAD BAD")


        #print("best operator: ", best_operator)
        #print("new agent",population.select_best_agents(1).get(0) )
        return self.list_operators

