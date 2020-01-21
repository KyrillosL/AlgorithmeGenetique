import operator_selector as op_sel
#import operator_selector_ALL_ALGO as op_sel
import sys
import time

import classes
import matplotlib
matplotlib.use('tkAgg')

import matplotlib.pyplot as plt
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


    def solve(self, m, realtime_plot=True, realtime_counter=True):

        start = time.time()

        # method = op_sel.upper_confidence_bound(self.population, 0.1, 0.9, 0.05)
        if m==0:
            self.method = op_sel.best_operator_oracle(self.population)
        elif m==1:
            self.method = op_sel.roulette_fixe(self.population)
        elif m == 2:
            self.method = op_sel.roulette_adaptive(self.population)
        elif m == 3:
            self.method = op_sel.adaptive_pursuit(self.population)
        elif m == 4:
            self.method = op_sel.upper_confidence_bound(self.population)
            #self.method = op_sel.upper_confidence_bound(self.population.select_best_agents(1).get(0))
        #else:
        #    method = op_sel.upper_confidence_bound(self.population)


        self.init_plot(m)

        self.iteration = 0

        temp_score = 0


        while self.population.select_best_agents(1).get(0).score() != 1.0 :


            '''
            #self.population.croisement(self.population.select_best_agents(2).get(0), self.population.select_best_agents(2).get(1))
            list_removed = self.population.remove_worst_agents()
            new_agent = self.method.apply(self.population.select_best_agents(2).get(0))
            new_agent.id = list_removed[0]
            self.population.add_an_agent(new_agent, new_agent.id)
            new_agent2 = self.method.apply(self.population.select_best_agents(2).get(1))
            new_agent2.id=list_removed[1]
            self.population.add_an_agent(new_agent2, new_agent2.id)
            '''
            self.method.apply()

            self.score = self.population.select_best_agents(1).get(0).score()







            self.time.append(self.iteration)
            self.data_score.append(self.score)
            for i in range(self.nb_op):
                self.list_list_data_prob[i].append(self.method.list_operators[i].probability)
                self.list_used_op[i].append(self.method.list_operators[i].times_used)



            if realtime_counter:
                end = time.time()
                sys.stdout.write('\rScore : %.2f Iteration : %i Time %.2f' % (self.score, self.iteration, end - start))
                sys.stdout.flush()


            if realtime_plot and self.iteration % 1000 == 0:
                self.update_plot()



            #if temp_score > self.population.select_best_agents(1).get(0).score():
            #    print("ERROR")

            temp_score = self.population.select_best_agents(1).get(0).score()


            #self.population.ad
            self.iteration += 1


        #SHOW THE GRAPH AT THE END AND STAY IT
        end = time.time()
        sys.stdout.write('\rScore : %.2f Iteration : %i Time %.2f' % (self.score, self.iteration, end - start))
        sys.stdout.flush()

        self.update_plot()
        plt.ioff()
        plt.show()

        print("NOMBRE ITERATION ", self.iteration)
        print("fin")


    def init_plot(self, m):


        self.nb_op = len(self.method.list_operators)




        self.fig = plt.figure(figsize=(20, 10))


        if m==0:
            self.fig.suptitle('Method : Oracle (Best Operator) | INFO : no probalities in this method ', fontsize=14, fontweight='bold')
        elif m==1:
            self.fig.suptitle('Method : Uniform (Fixed wheel probabilities) | INFO : all probs = 0.33. Only keeping the improving operator ', fontsize=14, fontweight='bold')
        elif m == 2:
            self.fig.suptitle('Method : Adaptive wheel  | INFO : Only keeping the improving operator  ', fontsize=14, fontweight='bold')
        elif m == 3:
            self.fig.suptitle('Method : Adaptive pursuit  | INFO : Only keeping the improving operator', fontsize=14, fontweight='bold')
        elif m == 4:
            self.fig.suptitle('Method :UCB  | INFO : Rewards displayed. Only keeping the improving operator', fontsize=14, fontweight='bold')


        gs = gridspec.GridSpec(3, 3)  # 2 rows, 3 columns

        line_width= 2

        plt.ion()
        #SCORE PLOT
        self.plt_score= self.fig.add_subplot(gs[0,0])
        self.plt_score.set_ylim([0, 1.1])
        self.plt_score.set_ylabel('Score')
        self.plt_score.set_xlabel('Generation')
        self.line_score, = self.plt_score.plot([], lw=line_width, c='black')
        self.txt_score = self.plt_score.text(1, 1, "", fontsize=20,color='red')


        #ALL PROBS PLOT
        self.all_probs= self.fig.add_subplot(gs[0,1:])
        self.all_probs.set_ylabel('All probs')
        self.all_probs.set_xlabel('Generation')


        #USED_OP PLOT
        self.plt_used_op= self.fig.add_subplot(gs[2,:])
        self.plt_used_op.set_ylim([0, 1])
        self.plt_used_op.set_ylabel('Used Op')
        self.plt_used_op.set_xlabel('Generation')



        # PROBS PLOT
        self.list_plt_prob=[]
        self.list_line_plt=[]
        self.list_line_plt__all_probs = []
        self.list_line_used_op = []
        for i in range(self.nb_op):

            plt_probs = self.fig.add_subplot(gs[1,i])
            plt_probs.set_xlabel('Generation')
            if i==0:
                if m==3:
                    line, = plt_probs.plot([],'o',markersize=2, lw=line_width, c='red')
                    line_all_probs, = self.all_probs.plot([],'o',markersize=2, lw=line_width-0.5, c='red')
                else:
                    line, = plt_probs.plot([],  lw=line_width, c='red')
                    line_all_probs, = self.all_probs.plot([],  lw=line_width - 0.5, c='red')
                line_all_time_used, = self.plt_used_op.plot([], lw=line_width-0.5, c='red')
                plt_probs.set_ylabel('flip 1_n')
            if i == 1:
                if m == 3:
                    line, = plt_probs.plot([],'o',markersize=2,  lw=line_width, c='green')
                    line_all_probs, = self.all_probs.plot([],'o',markersize=2, lw=line_width-0.5, c='green')
                else:
                    line, = plt_probs.plot([],  lw=line_width, c='green')
                    line_all_probs, = self.all_probs.plot([], lw=line_width - 0.5, c='green')
                line_all_time_used, = self.plt_used_op.plot([], lw=line_width - 0.5, c='green')
                plt_probs.set_ylabel('flip 3_n')
            if i == 2:
                if m == 3:
                    line, = plt_probs.plot([],'o',markersize=2, lw=line_width, c='blue')
                    line_all_probs, = self.all_probs.plot([],'o',markersize=2, lw=line_width-0.5, c='blue')
                else:
                    line, = plt_probs.plot([],  lw=line_width, c='blue')
                    line_all_probs, = self.all_probs.plot([],  lw=line_width - 0.5, c='blue')

                line_all_time_used, = self.plt_used_op.plot([], lw=line_width - 0.5, c='blue')
                plt_probs.set_ylabel('flip 5_n')
            self.list_line_plt.append(line)
            self.list_line_plt__all_probs.append(line_all_probs)
            self.list_line_used_op.append(line_all_time_used)
            self.list_plt_prob.append(plt_probs )
            self.list_plt_prob[i].set_ylim([0, 1.1])

        self.fig.canvas.draw()
        self.score_bg = self.fig.canvas.copy_from_bbox(self.plt_score.bbox)
        self.all_probs_bg = self.fig.canvas.copy_from_bbox(self.all_probs.bbox)
        self.plt_used_op_bg = self.fig.canvas.copy_from_bbox(self.plt_used_op.bbox)

        self.list_op_bg=[]
        self.list_list_data_prob=[]
        self.list_used_op = []
        for i in range(self.nb_op):
            self.list_data_used = []
            self.list_data_used.append(0)
            self.list_used_op.append(self.list_data_used)

        for i in range(self.nb_op):
            self.list_op_bg.append(self.fig.canvas.copy_from_bbox(self.list_plt_prob[i].bbox))
            self.list_data_prob =[]
            self.list_data_prob.append(0)

            self.list_list_data_prob.append(self.list_data_prob)

        self.time=[]
        self.time.append(0)

        self.data_score=[]
        self.data_score.append(0)

        plt.show(block=False)


    def update_plot(self):

            # SCORE
            xmin_score, xmax_score, ymin_score, ymax_score = [min(self.time) / 1.05, max(self.time) * 1.01, 0, 1.1]
            self.plt_score.axis([xmin_score, xmax_score, ymin_score, ymax_score])
            self.plt_score.set_xlim([0, self.iteration])
            self.line_score.set_data(self.time, self.data_score)
            self.txt_score.set_text("Score " + str(self.score))
            self.fig.canvas.restore_region(self.score_bg)
            # plt_score.draw_artist(line_score)
            # plt_score.draw_artist(txt_score)
            self.fig.canvas.blit(self.plt_score.bbox)

            for i in range(self.nb_op):
                xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(self.time) / 1.05, max(self.time) * 1.01, 0,
                                                                  max(max(s) for s in zip(*self.list_list_data_prob)) * 1.1]
                self.list_plt_prob[i].axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])

                self.list_line_plt[i].set_data(self.time, self.list_list_data_prob[i])
                self.list_line_plt__all_probs[i].set_data(self.time, self.list_list_data_prob[i])
                self.fig.canvas.restore_region(self.list_op_bg[i])
                #self.list_plt_prob[i].draw_artist(self.list_line_plt[i])
                self.fig.canvas.blit(self.list_plt_prob[i].bbox)

            # ALL PROBS
            xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(self.time) / 1.05, max(self.time) * 1.01, 0,
                                                              max(max(s) for s in zip(*self.list_list_data_prob)) * 1.1]
            self.all_probs.axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])

            self.fig.canvas.restore_region(self.all_probs_bg)
            #for i in range(self.nb_op):
            # print(list_line_plt[i])
                #self.all_probs.draw_artist(self.list_line_plt__all_probs[i])
            self.fig.canvas.blit(self.all_probs.bbox)

            # Used_OP

            xmin_score, xmax_score, ymin_score, ymax_score = [min(self.time) / 1.05, max(self.time) * 1.01, 0, max(
                max(s) for s in zip(*self.list_used_op)) * 1.1]
            self.plt_used_op.axis([xmin_score, xmax_score, ymin_score, ymax_score])
            self.plt_used_op.set_xlim([0, self.iteration])
            self.fig.canvas.restore_region(self.plt_used_op_bg)
            for i in range(self.nb_op):
                self.list_line_used_op[i].set_data(self.time, self.list_used_op[i])
                #self.plt_used_op.draw_artist(self.list_line_used_op[i])

            self.fig.canvas.blit(self.plt_used_op.bbox)
            self.fig.canvas.flush_events()







