'''
Roulette fixe. On attribut une probabilité qui augmente et qui descend si les opérateurs sont biens ou non.
f(popm) -> op1 -> f (popm+1)
si f(popm+1) est mieux : on récompense(et on dégrade les autres), sinon on dégrade(et on récompense les autres).
'''
import operator_gen as op

import classes as main
import matplotlib.pyplot as plt

import functions as functions
import random
plt.style.use('seaborn-whitegrid')
import numpy as np
import math
import operator



class Operator_Selector():
    def __init__(self,population):



        self.population = population
        self.nb_operateurs = 3
        self.list_operators = [op.mutation_1_flip(1 / self.nb_operateurs), op.mutation_3_flip(1 / self.nb_operateurs),
                               op.mutation_5_flip(1 / self.nb_operateurs)]




class roulette_fixe(Operator_Selector): #NOT REALLY A FIX
    def apply(self):
        id_selected_operator = random.randrange(0,len(self.list_operators))

        self.list_operators[id_selected_operator].compute_Score(self.population.select_best_agents(1).get(0))
        op = self.list_operators[id_selected_operator]
        print("SCORE OP", op)

        if op.score >self.population.select_best_agents(1).get(0).score():
            new_agent = op.mutate(self.population.select_best_agents(1).get(0))
            self.population.select_best_agents(1).set(0, new_agent)


class best_operator(Operator_Selector):
    def apply(self):
        for x in self.list_operators:
            x.compute_Score(self.population.select_best_agents(1).get(0))
        best_operator = max(self.list_operators)

        if best_operator.score >self.population.select_best_agents(1).get(0).score():
            new_agent = best_operator.mutate(self.population.select_best_agents(1).get(0))
            self.population.select_best_agents(1).set(0, new_agent)


class roulette_adaptive(Operator_Selector):

    def __init__(self, pmin=0.2):
        Operator_Selector.__init__()
        self.pmin = pmin

    def apply(self):

        #We compute the score at the iteration +1
        for op in self.list_operators:
            op.compute_Score(self.population.select_best_agents(1).get(0))

        #We sum all the scores
        sum_score_all_op =0
        for s in self.list_operators:
            sum_score_all_op+= s.score

        for op in self.list_operators:
            op.probability= self.pmin+ (1-self.pmin)*( op.score / sum_score_all_op )

        list_prob= []
        for op in self.list_operators:
            print(op.probability)
            list_prob.append(round(op.probability,1))


        chosen_op = np.random.choice(self.list_operators,1, [x.probability for x in self.list_operators ])[0]

        print("CHOSEN OP", chosen_op)

        if chosen_op.score > self.population.select_best_agents(1).get(0).score():
            new_agent = chosen_op.mutate(self.population.select_best_agents(1).get(0))
            self.population.select_best_agents(1).set(0, new_agent)

class adaptive_pursuit(Operator_Selector):

    def __init__(self, pmin=0.2, pmax=0.8, beta=0.5):
        Operator_Selector.__init__()
        self.beta=beta
        self.pmin = pmin
        self.pmax = pmax


    def apply(self):

        # We compute the score at the iteration +1
        for op in self.list_operators:
            op.compute_Score(self.population.select_best_agents(1).get(0))
            #print(op)



        best_operator = max(self.list_operators)


        #On augmente le meilleur
        best_operator.probability+= self.beta*(self.pmax - best_operator.probability)

        #On baisse les autres :
        for op in self.list_operators:
            if op != best_operator:

                op.probability += self.beta * (self.pmin - op.probability)


        chosen_op = np.random.choice(self.list_operators, 1, [x.probability for x in self.list_operators])[0]

        #print("CHOSEN OP", chosen_op)

        #input()

        if chosen_op.score > self.population.select_best_agents(1).get(0).score():
            new_agent = chosen_op.mutate(self.population.select_best_agents(1).get(0))
            self.population.select_best_agents(1).set(0, new_agent)


class upper_confidence_bound(Operator_Selector): #𝐴𝑡≐𝑎𝑟𝑔𝑚𝑎𝑥𝑎[𝑄𝑡(𝑎)+𝑐𝑙𝑛𝑡𝑁𝑡(𝑎)‾‾‾‾‾√]

    def __init__(self, population):
        Operator_Selector.__init__(self,population)
        self.nb_used =0 # UCB
        self.average_reward = 0
        self.exploration=0.5

        self.iteration=0

        for op in self.list_operators:
            op.compute_Score(self.population.select_best_agents(1).get(0))
            op.average_rewards = op.score
            op.times_used=1



    def apply(self):

        self.iteration += 1
        dict_score_ucb={}
        for op in self.list_operators:
            op.compute_Score(self.population.select_best_agents(1).get(0))
            dict_score_ucb[op] = op.average_rewards + self.exploration * math.sqrt(math.log(self.iteration) / op.times_used)
            op.average_rewards= op.average_rewards+op.score/op.times_used

        #print(dict_score_ucb)
        best_operator= max(dict_score_ucb.items(), key=operator.itemgetter(1))[0]



        #best_operator= self.list_operators[0]
        for score_ucb in dict_score_ucb:
            print(score_ucb, dict_score_ucb[score_ucb])

        print(best_operator)

        input()

        if best_operator.score >self.population.select_best_agents(1).get(0).score():
            new_agent = best_operator.mutate(self.population.select_best_agents(1).get(0))
            self.population.select_best_agents(1).set(0, new_agent)
            best_operator.probability=1
            best_operator.times_used += 1


            # On baisse les autres :
            for op in self.list_operators:
                if op != best_operator:
                    op.probability =0



        #input()


        #operator_to_use = max(    )
















'''OLD

class roulette_fixe(Operator_Selector): #NOT REALLY A FIX
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
        return self.list_operators


class roulette_adaptative(Operator_Selector):

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
        return self.list_operators


class poursuite_adaptative(Operator_Selector):

    def roule(self):
'''


