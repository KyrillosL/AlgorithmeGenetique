'''
Roulette fixe. On attribut une probabilité qui augmente et qui descend si les opérateurs sont biens ou non.
f(popm) -> op1 -> f (popm+1)
si f(popm+1) est mieux : on récompense(et on dégrade les autres), sinon on dégrade(et on récompense les autres).
'''
import operator_gen_ALL_ALGO as op

import classes as main
import matplotlib.pyplot as plt

import functions as functions
import random
from statistics import *
from math import *
plt.style.use('seaborn-whitegrid')
import numpy as np
import math
import operator


class Operator_Selector():
    def __init__(self, agent):
        self.agent = agent
        self.nb_operateurs = 3
        self.list_operators = [op.mutation_1_flip(1 / self.nb_operateurs), op.mutation_3_flip(1 / self.nb_operateurs),
                               op.mutation_5_flip(1 / self.nb_operateurs)]

    def weighted_choice(self):

        weights = []
        for x in self.list_operators:
            weights.append(x.probability)

        assert len(weights) == len(self.list_operators)
        #print(weights)
        assert abs(1. - sum(weights)) < 1e-6

        x = random.random()
        for i, elmt in enumerate(self.list_operators):
            if x <= weights[i]:
                #print("ELMT",i,  elmt)
                return elmt
            x -= weights[i]
            #print("W",weights[i])
            #print("x",x)


class  basic_operator_1_flip(Operator_Selector):
    def apply(self, agent, keep_degrading):
        self.agent=agent
        x = self.list_operators[0]
        x.compute_Score(agent)

        if keep_degrading or x.score > self.agent.get_score():
            new_agent = x.mutate(self.agent)
            x.times_used+=1
            return new_agent
        else:
            return self.agent

class best_operator_oracle(Operator_Selector):

    def __init__(self, agent):
        Operator_Selector.__init__(self, agent)
        for x in self.list_operators:
            x.probability=0


    def apply(self, agent, keep_degrading):
        self.agent = agent
        for x in self.list_operators:
            x.compute_Score(self.agent)
        best_operator = max(self.list_operators)

        if keep_degrading or best_operator.score > self.agent.get_score():
            new_agent = best_operator.mutate(self.agent)

            # self.population.select_best_agents(1).set(0, new_agent)
            best_operator.times_used += 1
            best_operator.probability = 0


            return new_agent
        else:
            return self.agent

class roulette_fixe(Operator_Selector):  # NOT REALLY A FIX
    def apply(self, agent, keep_degrading):
        self.agent = agent
        id_selected_operator = random.randrange(0, len(self.list_operators))

        self.list_operators[id_selected_operator].compute_Score(self.agent)
        op = self.list_operators[id_selected_operator]



        if keep_degrading or op.score > self.agent.get_score():
            new_agent = op.mutate(self.agent)
            # self.population.select_best_agents(1).set(0, new_agent)
            op.times_used += 1

            return new_agent
        else:
            return self.agent

class roulette_adaptive(Operator_Selector):

    def __init__(self, agent, pmin=0.2):
        Operator_Selector.__init__(self, agent)
        self.pmin = pmin


    def apply(self, agent, keep_degrading):
        self.agent = agent

        # We compute the score at the iteration +1
        #for op in self.list_operators:
        #    op.compute_Score(self.agent)

        # We sum all the scores
        sum_score_all_op = 1
        for s in self.list_operators:
            sum_score_all_op += s.score

        for op in self.list_operators:
            op.probability = self.pmin + (1 - len(self.list_operators)*self.pmin) * (op.score / sum_score_all_op)


        list_prob = []
        sum_prob=0
        for op in self.list_operators:
            list_prob.append(round(op.probability, 1))
            sum_prob+=op.probability


        for op in self.list_operators:
           op.probability/= sum_prob

        #chosen_op = np.random.choice(self.list_operators, 1, [x.probability for x in self.list_operators])[0]

        chosen_op = self.weighted_choice()

        chosen_op.compute_Score(self.agent)

        if keep_degrading or chosen_op.score > self.agent.get_score():
            new_agent = chosen_op.mutate(self.agent)
            # self.population.select_best_agents(1).set(0, new_agent)
            chosen_op.times_used += 1


            return new_agent

        else:
            return self.agent
class adaptive_pursuit(Operator_Selector):

    def __init__(self, population, pmin=0.2, pmax=0.8, beta=0.5):
        Operator_Selector.__init__(self, population)
        self.beta = 0.9
        self.pmin = pmin
        self.pmax = pmax

    def apply(self, agent, keep_degrading):
        self.agent = agent
        # We compute the score at the iteration +1
        #for op in self.list_operators:
        #    op.compute_Score(self.agent)
            # print(op)

        best_operator = max(self.list_operators)


        # On augmente le meilleur
        best_operator.probability += self.beta * (self.pmax - best_operator.probability)

        # On baisse les autres :
        for op in self.list_operators:
            if op != best_operator:
                op.probability += self.beta * (self.pmin - op.probability)


        sum_prob=0
        for op in self.list_operators:
            sum_prob += op.probability
        for op in self.list_operators:
            op.probability/= sum_prob
            #print(op)
        #input()




        #chosen_op = np.random.choice(self.list_operators, 1, [x.probability for x in self.list_operators])[0]
        chosen_op= self.weighted_choice()
        #print("CHOSEN OP", chosen_op)

        # input()
        chosen_op.compute_Score(self.agent)

        if keep_degrading or chosen_op.score > self.agent.get_score():
            new_agent = chosen_op.mutate(self.agent)

            chosen_op.times_used += 1
            return new_agent
        else:
            return self.agent

class upper_confidence_bound(Operator_Selector):  # 𝐴𝑡≐𝑎𝑟𝑔𝑚𝑎𝑥𝑎[𝑄𝑡(𝑎)+𝑐𝑙𝑛𝑡𝑁𝑡(𝑎)‾‾‾‾‾√]

    def __init__(self, agent):
        Operator_Selector.__init__(self, agent)
        self.nb_used = 0  # UCB
        self.average_reward = 0
        self.exploration =1

        self.iteration = 3

        for op in self.list_operators:
            op.compute_Score(self.agent)
            #op.average_rewards = op.score
            op.average_rewards_array.append(op.score)
            op.times_used = 1

    def apply(self,agent, keep_degrading ):


        self.agent=agent

        dict_score_ucb = {}
        #sum_prob=0
        #sum_op = 0
        for op in self.list_operators:
            #sum_op+= op.times_used
            if len(op.average_rewards_array)>5:
                op.average_rewards_array.pop(0)

        #print("SUM OP", sum_op)
        #print("IT", self.iteration)

        for op in self.list_operators:
            #dict_score_ucb[op] = op.average_rewards + self.exploration * math.sqrt(2*math.log(self.iteration) / op.times_used)
            dict_score_ucb[op] = op.average_rewards + self.exploration * math.sqrt(  math.log(self.iteration) / op.times_used)
            op.score = dict_score_ucb[op]
            op.probability = dict_score_ucb[op]


        # print(dict_score_ucb)
        best_operator = max(dict_score_ucb.items(), key=operator.itemgetter(1))[0]
        best_operator.compute_Score(self.agent)

        # best_operator= self.list_operators[0]
        #for score_ucb in dict_score_ucb:
            # print(score_ucb, dict_score_ucb[score_ucb])


        # print("best_operator ", best_operator, " pop ", self.agent.score())
        self.iteration += 1
        if keep_degrading or best_operator.score > self.agent.get_score():
            new_agent = best_operator.mutate(self.agent)
            # self.population.select_best_agents(1).set(0, new_agent)
            # best_operator.probability=1
            best_operator.times_used += 1
            # best_operator.average_rewards = (best_operator.score + (
            #          best_operator.times_used - 1) * best_operator.average_rewards) / best_operator.times_used

            # if len(best_operator.average_rewards_array)>3:
            #       best_operator.average_rewards_array.pop(0)

            '''
            if  len(best_operator.average_rewards_array)>=2 and best_operator.score<=best_operator.average_rewards_array[-1]+0.1:
                best_operator.times_not_rewarded += 1


            else:
                best_operator.times_not_rewarded = 0

            if best_operator.times_not_rewarded >= 15:

                best_operator.average_rewards_array.clear()
                best_operator.average_rewards = 0
                best_operator.times_not_rewarded =0
            else:
            '''
            best_operator.average_rewards_array.append(best_operator.score)
            best_operator.average_rewards = mean(best_operator.average_rewards_array)
            return new_agent
        else:
            #print("NOT USED")
            return self.agent
            '''
            if  len(best_operator.average_rewards_array)>=2 and best_operator.probability<=best_operator.average_rewards_array[-1]:
                best_operator.times_not_rewarded += 1
                print("HERE")

            # else:
            #     best_operator.times_not_rewarded = 0

            if best_operator.times_not_rewarded >= 5:
                best_operator.average_rewards_array.clear()
                best_operator.average_rewards = 0
                best_operator.times_not_rewarded =0
            else:
                best_operator.average_rewards_array.append(best_operator.score)
                best_operator.average_rewards = mean(best_operator.average_rewards_array)
            '''
            #print(best_operator.times_not_rewarded )



            #print(best_operator.average_rewards, ' op ' ,  best_operator,' time used ',best_operator.times_used )
            # input()






class exp3(Operator_Selector):

    def __init__(self, agent, pmin=0.2, pmax=0.8, beta=0.5):
        Operator_Selector.__init__(self, agent)
        self.beta = beta
        self.pmin = pmin
        self.pmax = pmax
        self.exploration = 0.5 #LE POIDS DES POIDS. 0 -> BCP D'IMPORTANCE, 1 = PAS D'IMPORTANCE DES POIDS (LA PROB RESTE A 0.33)

        '''
        #On start le meilleur opérateur avec une prob de 0.9
        for op in self.list_operators:
            op.compute_Score(self.agent)
        best_operator = max(self.list_operators)
        best_operator.weight=0.9
        # On baisse les autres :
        for op in self.list_operators:
            if op != best_operator:
                op.weight =0.05
        '''

    def apply(self, agent, keep_degrading):
        self.agent = agent
        sum_weight = 0

        for op in self.list_operators:
            # sum_op+= op.times_used
            if len(op.average_rewards_array) > 5:
                op.average_rewards_array.pop(0)


        for op in self.list_operators:
            sum_weight+=op.weight
        sum_prob=0
        for op in self.list_operators:
            op.probability = (1-self.exploration) * (op.weight/ sum_weight ) + (self.exploration/len(self.list_operators))
            sum_prob+=op.probability


        for op in self.list_operators:
            op.probability/= sum_prob

        #chosen_op = np.random.choice(self.list_operators, 1, [x.probability for x in self.list_operators])[0]
        chosen_op = self.weighted_choice()

        chosen_op.compute_Score(self.agent)

        if keep_degrading or chosen_op.score > self.agent.get_score():
            chosen_op.times_used += 1
            new_agent = chosen_op.mutate(self.agent)
            new_reward = chosen_op.score / (chosen_op.probability + 0.00)

            #chosen_op.average_rewards = (new_reward + (chosen_op.times_used - 1) * chosen_op.average_rewards) / chosen_op.times_used
            chosen_op.weight += exp(self.exploration * chosen_op.average_rewards / len(self.list_operators))
            chosen_op.average_rewards_array.append(chosen_op.score)
            chosen_op.average_rewards = mean(chosen_op.average_rewards_array)
            return new_agent
        else:
            return self.agent