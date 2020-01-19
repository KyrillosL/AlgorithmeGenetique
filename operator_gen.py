import random
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

        self.times_used=0

        self.average_rewards = 0


    def __str__(self):
        return  "probability: " +str(self.probability) + " | Score : " + str(self.score)

    def __repr__(self):
        return self.__str__()

    def mutate(self, agent, is_computing=False):
        print("dans le mauvais mutate")
        return "Mutate should be overrided"


    def compute_Score(self, agent):
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
class mutation_1_flip(Operator):

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
class mutation_3_flip(Operator):

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

class mutation_5_flip(Operator):

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

class mutation_bit_flip(Operator):
    def mutate(self, agent):
        for x in range(self.size):
            if random.random() < (1/self.size):
                Operator.switch_bit(agent,x)