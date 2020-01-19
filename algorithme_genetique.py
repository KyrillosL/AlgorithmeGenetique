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


        fig = plt.figure()
        plt_score= fig.add_subplot(3, 2, 1)
        plt_score.set_xlim(0,1000)
        plt_score.set_ylim([0, 1.1])
        plt_score.set_ylabel('Score')
        plt_score.set_xlabel('Generation')

        line_score, = plt_score.plot([], lw=3, c='black')


        fig.canvas.draw()
        score_bg = fig.canvas.copy_from_bbox(plt_score.bbox)


        time=[]
        time.append(0)
        data_score=[]
        data_score.append(0)


        plt.show(block=False)



        iteration = 0

        temp_score = 0
        #lo = op_sel.upper_confidence_bound(self.population, 0.1, 0.9, 0.05)
        #lo = op_sel.upper_confidence_bound(self.population)
        #lo = op_sel.best_operator(self.population)
        #lo = op_sel.roulette_adaptive(self.population)
        #lo = op_sel.roulette_fixe(self.population)
        lo = op_sel.adaptive_pursuit(self.population)


        while self.population.select_best_agents(1).get(0).score() != 1.0 :
            lo.apply()

            xmin, xmax, ymin, ymax = [min(time) / 1.05, max(time) * 1.1, 0, 1.1]
            plt_score.axis([xmin, xmax, ymin, ymax])


            time.append(iteration)
            data_score.append(self.population.select_best_agents(1).get(0).score())

            line_score.set_data(time,data_score )

            fig.canvas.restore_region(score_bg)

            plt_score.draw_artist(line_score)


            fig.canvas.blit(plt_score.bbox)

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







