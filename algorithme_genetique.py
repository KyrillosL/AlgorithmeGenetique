# import operator_selector as op_sel
import operator_selector_ALL_ALGO as op_sel
import sys
import time

import plot as myplt
import final_plotter as fp

import classes
import matplotlib
matplotlib.use('tkAgg')


import numpy as np
from matplotlib import gridspec


class Algorithme_genetique:
    def __init__(self, parametres):
        self.nombre_agents_par_population = parametres["nombre_agents_par_population"]
        self.taille_agent = parametres["taille_agent"]

        number_of_agent_to_select = 2

        self.string_to_get = self.init_string_to_get(self.nombre_agents_par_population)
        print("string to get: " + self.string_to_get)

        self.population = classes.Population(self.nombre_agents_par_population, self.taille_agent)
        print("Population initiale")
        print(self.population)


    def __str__(self):
        return "Nombre d'agents: " + str(self.nombre_agents_par_population) + ", taille agent: " + str(self.taille_agent)

    def __repr__(self):
        return self.__str__()

    def init_string_to_get(self, size):
        return "1" * size

    def reinit(self):
        self.population = classes.Population(self.nombre_agents_par_population, self.taille_agent)


    def solve(self, method=0, realtime_plot=True, refresh_rate_plot=1000, realtime_counter=True, refresh_rate_counter= 1, keep_degrading=True, one_indiv=False, stop_after=1000, number_of_pass=1):


        # method = op_sel.upper_confidence_bound(self.population, 0.1, 0.9, 0.05)
        if method==0:
            # self.method = op_sel.best_operator_oracle(self.population)
            self.method = op_sel.best_operator_oracle(self.population.select_best_agents(1).get(0))
        elif method==1:
            # self.method = op_sel.roulette_fixe(self.population)
            self.method = op_sel.roulette_fixe(self.population.select_best_agents(1).get(0))
        elif method == 2:
            # self.method = op_sel.roulette_adaptive(self.population)
            self.method = op_sel.roulette_adaptive(self.population.select_best_agents(1).get(0))
        elif method == 3:
            # self.method = op_sel.adaptive_pursuit(self.population)
            self.method = op_sel.adaptive_pursuit(self.population.select_best_agents(1).get(0))
        elif method == 4:
            # self.method = op_sel.upper_confidence_bound(self.population)
            self.method = op_sel.upper_confidence_bound(self.population.select_best_agents(1).get(0))
        elif method == 5:
            # self.method = op_sel.exp3(self.population)
            self.method = op_sel.exp3(self.population.select_best_agents(1).get(0))


        final_plotter = fp.Final_plotter()


        for i in range(number_of_pass):

            start = time.time()
            myplot = myplt.Myplot(method, keep_degrading, 3)

            self.iteration = 0
            self.reinit()




            while self.population.select_best_agents(1).get(0).get_score() != 1 and stop_after>= self.iteration :



                if one_indiv:
                    new_agent = self.method.apply(self.population.select_best_agents(1).get(0), keep_degrading)
                    self.population.get_agents().pop()
                    self.population.get_agents().append(new_agent)

                else:
                    #self.population.croisement(self.population.select_best_agents(2).get(0), self.population.select_best_agents(2).get(1))
                    list_removed = self.population.remove_worst_agents()
                    new_agent = self.method.apply(self.population.select_best_agents(2).get(0), keep_degrading)
                    new_agent.id = list_removed[0]
                    self.population.add_an_agent(new_agent, new_agent.id)

                    new_agent2 = self.method.apply(self.population.select_best_agents(2).get(1),  keep_degrading)
                    new_agent2.id=list_removed[1]
                    self.population.add_an_agent(new_agent2, new_agent2.id)

                myplot.score = self.population.select_best_agents(1).get(0).get_score()


                if self.iteration% refresh_rate_counter==0:
                    myplot.time.append(self.iteration)
                    myplot.data_score.append(myplot.score)
                    for i in range(myplot.nb_op):
                        myplot.list_list_data_prob[i].append(self.method.list_operators[i].probability)
                        myplot.list_used_op[i].append(self.method.list_operators[i].times_used)


                if realtime_counter:
                    end = time.time()
                    sys.stdout.write('\rScore : %.5f Iteration : %i Time %.2f' % (myplot.score, self.iteration, end - start))
                    sys.stdout.flush()

                if realtime_plot and self.iteration % refresh_rate_plot == 0:
                    myplot.update_plot()


                self.iteration += 1

            #SHOW THE GRAPH AT THE END AND STAY IT
            end = time.time()
            sys.stdout.write('\rScore : %.2f Iteration : %i Time %.2f' % (myplot.score, self.iteration, end - start))
            sys.stdout.flush()

            myplot.update_plot()

            myplot.turn_off_interactive_mode()
            final_plotter.add_plot(myplot.time, myplot.data_score, myplot.list_list_data_prob, myplot.list_used_op)
            #




        final_plotter.calculate_means()
        myplot.time = final_plotter.time_array
        myplot.data_score= final_plotter.score_array
        for i in range(myplot.nb_op):
            myplot.list_list_data_prob[i] =  final_plotter.all_prob_array[i]
            myplot.list_used_op[i] = final_plotter.used_op[i]
        myplot.update_plot()
        myplot.show()


