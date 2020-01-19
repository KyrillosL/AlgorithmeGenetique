import operator_selector as op_sel
import classes
import matplotlib.pyplot as plt
import numpy as np


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


    def solve(self):

        #lo = op_sel.upper_confidence_bound(self.population, 0.1, 0.9, 0.05)
        #lo = op_sel.upper_confidence_bound(self.population)
        #lo = op_sel.best_operator(self.population)
        #lo = op_sel.roulette_adaptive(self.population)
        #lo = op_sel.roulette_fixe(self.population)
        lo = op_sel.adaptive_pursuit(self.population)
        nb_op = len(lo.list_operators)


        fig = plt.figure(figsize=(20, 10))
        #SCORE PLOT
        plt_score= fig.add_subplot(3, 2, 1)
        plt_score.set_ylim([0, 1.1])
        plt_score.set_ylabel('Score')
        plt_score.set_xlabel('Generation')
        line_score, = plt_score.plot([], lw=2, c='black')

        list_plt_prob=[]
        list_line_plt=[]

        for i in range(nb_op):
            plt_probs =fig.add_subplot(3, 2, i+2)

            plt_probs.set_xlabel('Generation')


            if i==0:
                line, = plt_probs.plot([], lw=1, c='red')
                plt_probs.set_ylabel('flip 1_n')
            if i == 1:
                line, = plt_probs.plot([], lw=1, c='green')
                plt_probs.set_ylabel('flip 3_n')
            if i == 2:
                line, = plt_probs.plot([], lw=1, c='blue')
                plt_probs.set_ylabel('flip 5_n')
            list_line_plt.append(line)
            list_plt_prob.append(plt_probs )


        '''
        #PROBS PLOT
        plt_probs= fig.add_subplot(2, 1, 2)
        plt_probs.set_ylim([0, 1.1])
        plt_probs.set_ylabel('Prob')
        plt_probs.set_xlabel('Generation')
        line_op_1, = plt_probs.plot([], lw=3, c='red')
        line_op_2, = plt_probs.plot([], lw=3, c='green')
        line_op_3, = plt_probs.plot([], lw=3, c='blue')
        '''


        fig.canvas.draw()
        score_bg = fig.canvas.copy_from_bbox(plt_score.bbox)
        #probs_bg = fig.canvas.copy_from_bbox(plt_probs.bbox)
        list_op_bg=[]
        list_list_data_prob=[]
        for i in range(nb_op):
            list_op_bg.append(fig.canvas.copy_from_bbox(list_plt_prob[i].bbox))
            list_data_prob =[]
            list_data_prob.append(0)
            list_list_data_prob.append(list_data_prob)




        time=[]
        time.append(0)

        data_score=[]
        data_score.append(0)

        data_probs_op_1=[]
        data_probs_op_1.append(0)
        data_probs_op_2=[]
        data_probs_op_2.append(0)
        data_probs_op_3=[]
        data_probs_op_3.append(0)


        plt.show(block=False)



        iteration = 0

        temp_score = 0


        while self.population.select_best_agents(1).get(0).score() != 1.0 :
            lo.apply()
            time.append(iteration)

            #SCORE
            xmin_score, xmax_score, ymin_score, ymax_score = [min(time) / 1.05, max(time) * 1.1, 0, 1.1]
            plt_score.axis([xmin_score, xmax_score, ymin_score, ymax_score])
            data_score.append(self.population.select_best_agents(1).get(0).score())
            line_score.set_data(time,data_score )
            fig.canvas.restore_region(score_bg)
            plt_score.draw_artist(line_score)
            fig.canvas.blit(plt_score.bbox)



            for i in range(nb_op):
                list_list_data_prob[i].append(lo.list_operators[i].probability)
                xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(time) / 1.05, max(time) * 1.1, 0,max(list_list_data_prob[i])*1.1]
                list_plt_prob[i].axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])
                list_line_plt[i].set_data(time, list_list_data_prob[i] )
                fig.canvas.restore_region( list_op_bg[i] )
                list_plt_prob[i].draw_artist(list_line_plt[i])
                fig.canvas.blit( list_plt_prob[i].bbox)

            '''
            #PROBS
            data_probs_op_1.append(lo.list_operators[0].probability)
            data_probs_op_2.append(lo.list_operators[1].probability)
            data_probs_op_3.append(lo.list_operators[2].probability)
            xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(time) / 1.05, max(time) * 1.1, 0, max(x.probability for x in lo.list_operators)]
            plt_probs.axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])

            line_op_1.set_data(time,data_probs_op_1 )
            line_op_2.set_data(time, data_probs_op_2)
            line_op_3.set_data(time, data_probs_op_3)
            fig.canvas.restore_region(probs_bg)
            plt_probs.draw_artist(line_op_1)
            plt_probs.draw_artist(line_op_2)
            plt_probs.draw_artist(line_op_3)
            fig.canvas.blit(plt_probs.bbox)
            '''

            fig.canvas.flush_events()


            print(self.population.select_best_agents(1).get(0).score())
            if iteration == 0:
                temp_score = self.population.select_best_agents(1).get(0).score()

            if temp_score > self.population.select_best_agents(1).get(0).score():
                print("ERROR")

            '''
            plt.subplot(3, 2, 1)
            plt.ylim([0, 1])
            plt.ylabel('Score')
            plt.xlabel('Generation')
            plt.scatter(iteration, self.population.select_best_agents(1).get(0).score(), c='black', s=10)
            plt.subplot(3,2, 2)
            plt.ylim([0, 1])
            plt.ylabel('Prob. 1_n')
            plt.xlabel('Generation')
            plt.scatter(iteration, lo.list_operators[0].probability, c=[lo.list_operators[0].color], s=10)
            plt.subplot(3, 2, 3)
            plt.ylim([0, 1])
            plt.ylabel('Prob. 3_n')
            plt.xlabel('Generation')
            plt.scatter(iteration, lo.list_operators[1].probability, c=[lo.list_operators[1].color], s=10)
            plt.subplot(3, 2, 4)
            plt.ylim([0, 1])
            plt.ylabel('Prob. 5_n')
            plt.xlabel('Generation')
            plt.scatter(iteration, lo.list_operators[2].probability, c=[lo.list_operators[2].color], s=10)

            plt.subplot(3, 2, 5)

            plt.ylabel('Used Operator')
            plt.xlabel('Generation')
            #
            plt.scatter(iteration, 0.5, c=[lo.used_operator.color], s=10)


            plt.subplot(3, 2, 6)
            plt.ylabel('Used Operator')
            plt.xlabel('Generation')
            for x in lo.list_operators:
                plt.scatter(iteration, x.probability, c=[x.color], s=10)
            '''



            temp_score = self.population.select_best_agents(1).get(0).score()

            iteration += 1

            #plt.pause(0.0000001)  # Note this correction


        # print(population.select_best_agents(1).get(0))


        plt.show()
        print("NOMBRE ITERATION ", iteration)
        print("fin")







