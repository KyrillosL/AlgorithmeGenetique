import operator_selector as op_sel
import classes
import matplotlib.pyplot as plt


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


        plt.figure(1)
        score_genereal = plt.subplot(2, 2, 1)
        probabilites = plt.subplot(2, 2, 2)

        iteration = 0

        temp_score = 0
        lo = op_sel.adaptive_pursuit(self.population, 0.05, 0.95, 0.05)
        while self.population.select_best_agents(1).get(0).score() != 1.0:

            print(self.population.select_best_agents(1).get(0).score())
            if iteration == 0:
                temp_score = self.population.select_best_agents(1).get(0).score()

            if temp_score > self.population.select_best_agents(1).get(0).score():
                print("ERROR")
            '''
            plt.subplot(2, 2, 1)
            plt.ylim([0, 1])
            plt.ylabel('Score')
            plt.xlabel('Generation')
            plt.scatter(iteration, self.population.select_best_agents(1).get(0).score(), c='black', s=10)
            # print(population.select_best_agents(1).get(0).score())
            plt.subplot(2, 2, 2)
            plt.ylim([0, 1])
            plt.ylabel('Prob. 1_n')
            plt.xlabel('Generation')
            plt.scatter(iteration, lo.list_operators[0].probability, c='blue', s=10)
            plt.subplot(2, 2, 3)
            plt.ylim([0, 1])
            plt.ylabel('Prob. 3_n')
            plt.xlabel('Generation')
            plt.scatter(iteration, lo.list_operators[1].probability, c='red', s=10)
            plt.subplot(2, 2, 4)
            plt.ylim([0, 1])
            plt.ylabel('Prob. 5_n')
            plt.xlabel('Generation')
            plt.scatter(iteration, lo.list_operators[2].probability, c='green', s=10)
            '''
            temp_score = self.population.select_best_agents(1).get(0).score()

            iteration += 1

            #plt.pause(0.00001)  # Note this correction



        # print(population.select_best_agents(1).get(0))

        #plt.show()
        print("NOMBRE ITERATION ", iteration)
        print("fin")







