import operator_selector as op_sel
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


    def solve(self, m, realtime_plot=True):

        # method = op_sel.upper_confidence_bound(self.population, 0.1, 0.9, 0.05)
        if m==0:
            method = op_sel.best_operator_oracle(self.population)
        elif m==1:
            method = op_sel.roulette_fixe(self.population)
        elif m == 2:
            method = op_sel.roulette_adaptive(self.population)
        elif m == 3:
            method = op_sel.adaptive_pursuit(self.population)
        elif m == 4:
            method = op_sel.upper_confidence_bound(self.population)
        #else:
        #    method = op_sel.upper_confidence_bound(self.population)

        nb_op = len(method.list_operators)




        fig = plt.figure(figsize=(20, 10))
        gs = gridspec.GridSpec(3, 3)  # 2 rows, 3 columns

        line_width= 2

        plt.ion()
        #SCORE PLOT
        plt_score= fig.add_subplot(gs[0,0])
        plt_score.set_ylim([0, 1.1])
        plt_score.set_ylabel('Score')
        plt_score.set_xlabel('Generation')
        line_score, = plt_score.plot([], lw=line_width, c='black')
        txt_score = plt_score.text(1, 1, "", fontsize=20,color='red')


        #ALL PROBS PLOT
        all_probs= fig.add_subplot(gs[0,1:])
        all_probs.set_ylabel('All probs')
        all_probs.set_xlabel('Generation')


        #USED_OP PLOT
        plt_used_op= fig.add_subplot(gs[2,:])
        plt_used_op.set_ylim([0, 1])
        plt_used_op.set_ylabel('Used Op')
        plt_used_op.set_xlabel('Generation')



        # PROBS PLOT
        list_plt_prob=[]
        list_line_plt=[]
        list_line_plt__all_probs = []
        list_line_plt_all_times_used = []
        for i in range(nb_op):

            plt_probs =fig.add_subplot(gs[1,i])
            plt_probs.set_xlabel('Generation')
            if i==0:
                line, = plt_probs.plot([], lw=line_width, c='red')
                line_all_probs, = all_probs.plot([], lw=line_width-0.5, c='red')
                line_all_time_used, = plt_used_op.plot([], lw=line_width-0.5, c='red')
                plt_probs.set_ylabel('flip 1_n')
            if i == 1:
                line, = plt_probs.plot([], lw=line_width, c='green')
                line_all_probs, = all_probs.plot([], lw=line_width-0.5, c='green')
                line_all_time_used, = plt_used_op.plot([], lw=line_width - 0.5, c='green')
                plt_probs.set_ylabel('flip 3_n')
            if i == 2:
                line, = plt_probs.plot([], lw=line_width, c='blue')
                line_all_probs, = all_probs.plot([], lw=line_width-0.5, c='blue')
                line_all_time_used, = plt_used_op.plot([], lw=line_width - 0.5, c='green')
                plt_probs.set_ylabel('flip 5_n')
            list_line_plt.append(line)
            list_line_plt__all_probs.append(line_all_probs)
            list_line_plt_all_times_used.append(line_all_time_used)
            list_plt_prob.append(plt_probs )
            list_plt_prob[i].set_ylim([0, 1.1])




        fig.canvas.draw()
        score_bg = fig.canvas.copy_from_bbox(plt_score.bbox)
        all_probs_bg = fig.canvas.copy_from_bbox(all_probs.bbox)
        plt_used_op_bg = fig.canvas.copy_from_bbox(plt_used_op.bbox)

        list_op_bg=[]
        list_list_data_prob=[]
        list_used_op = []
        for i in range(nb_op):
            list_op_bg.append(fig.canvas.copy_from_bbox(list_plt_prob[i].bbox))
            list_data_prob =[]
            list_data_prob.append(0)
            list_list_data_prob.append(list_data_prob)
            list_used_op.append(list_data_prob)



        time=[]
        time.append(0)

        data_score=[]
        data_score.append(0)






        plt.show(block=False)



        iteration = 0

        temp_score = 0


        while self.population.select_best_agents(1).get(0).score() != 1.0 :
            method.apply()
            score = self.population.select_best_agents(1).get(0).score()
            print(score, " it ", iteration)
            time.append(iteration)



            data_score.append(score)


            for i in range(nb_op):
                list_list_data_prob[i].append(method.list_operators[i].probability)
                list_used_op[i].append(method.list_operators[i].times_used)

            if realtime_plot and iteration%1000==0:
                    #SCORE
                    xmin_score, xmax_score, ymin_score, ymax_score = [min(time) / 1.05, max(time) * 1.01, 0, 1.1]
                    plt_score.axis([xmin_score, xmax_score, ymin_score, ymax_score])
                    plt_score.set_xlim([0,iteration])
                    line_score.set_data(time,data_score )
                    txt_score.set_text("Score "+ str(score))
                    fig.canvas.restore_region(score_bg)
                    plt_score.draw_artist(line_score)
                    plt_score.draw_artist(txt_score)
                    fig.canvas.blit(plt_score.bbox)






                    for i in range(nb_op):
                        xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(time) / 1.05, max(time) * 1.01, 0,max( max(s) for s in zip(*list_list_data_prob) )*1.1]
                        list_plt_prob[i].axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])

                        list_line_plt[i].set_data(time, list_list_data_prob[i] )
                        list_line_plt__all_probs[i].set_data(time, list_list_data_prob[i] )
                        fig.canvas.restore_region( list_op_bg[i] )
                        list_plt_prob[i].draw_artist(list_line_plt[i])
                        fig.canvas.blit( list_plt_prob[i].bbox)


                    # ALL PROBS
                    xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(time) / 1.05, max(time) * 1.01, 0,max( max(s) for s in zip(*list_list_data_prob) )*1.1]
                    all_probs.axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])

                    fig.canvas.restore_region(all_probs_bg)
                    for i in range(nb_op):
                        #print(list_line_plt[i])
                        all_probs.draw_artist(list_line_plt__all_probs[i])
                    fig.canvas.blit(all_probs.bbox)



                    # Used_OP

                    xmin_score, xmax_score, ymin_score, ymax_score = [min(time) / 1.05, max(time) * 1.01, 0, max(
                        max(s) for s in zip(*list_line_plt_all_times_used)) * 1.1]
                    plt_used_op.axis([xmin_score, xmax_score, ymin_score, ymax_score])
                    plt_used_op.set_xlim([0, iteration])
                    for i in range(nb_op):
                        list_line_plt_all_times_used[i].set_data(time, list_list_data_prob[i])
                        line_score_used_op.set_data(time, list_line_plt_all_times_used[i])
                    fig.canvas.restore_region(plt_used_op_bg)
                    plt_used_op.draw_artist(line_score_used_op)
                    fig.canvas.blit(plt_used_op.bbox)







                    fig.canvas.flush_events()

            #if temp_score > self.population.select_best_agents(1).get(0).score():
            #    print("ERROR")

            temp_score = self.population.select_best_agents(1).get(0).score()

            iteration += 1







        #SHOW THE GRAPH AT THE END AND STAY IT
        # SCORE
        xmin_score, xmax_score, ymin_score, ymax_score = [min(time) / 1.05, max(time) * 1.01, 0, 1.1]
        plt_score.axis([xmin_score, xmax_score, ymin_score, ymax_score])
        plt_score.set_xlim([0, iteration])

        line_score.set_data(time, data_score)
        txt_score.set_text("Score " + str(score))
        fig.canvas.restore_region(score_bg)
        plt_score.draw_artist(line_score)
        plt_score.draw_artist(txt_score)

        for i in range(nb_op):
            xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(time) / 1.05, max(time) * 1.01, 0,
                                                              max(list_list_data_prob[i]) * 1.1]
            list_plt_prob[i].axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])

            list_line_plt[i].set_data(time, list_list_data_prob[i])
            list_line_plt__all_probs[i].set_data(time, list_list_data_prob[i])
            fig.canvas.restore_region(list_op_bg[i])
            list_plt_prob[i].draw_artist(list_line_plt[i])

        # ALL PROBS
        xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(time) / 1.05, max(time) * 1.01, 0,
                                                          max(max(s) for s in zip(*list_list_data_prob)) * 1.1]
        all_probs.axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])
        fig.canvas.restore_region(all_probs_bg)
        for i in range(nb_op):
            all_probs.draw_artist(list_line_plt__all_probs[i])


        plt.ioff()
        plt.show()
        print("NOMBRE ITERATION ", iteration)
        print("fin")







