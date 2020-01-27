import statistics
import numpy as np

class Final_plotter:

    def __init__(self):

        self.time_array=[]
        self.score_array=[]
        self.all_prob_array=[]
        self.used_op_array=[]


    def add_plot(self, time, score, all_probs, used ):

        self.time_array.append(time)
        self.score_array.append(score)
        self.all_prob_array.append(all_probs)
        self.used_op_array.append(used)

    def add_plot_score_time(self, time, score ):

        self.time_array.append(time)
        self.score_array.append(score)


    def calculate_means(self, number_of_pass):

        '''
        arrays_score = [np.array(x) for x in self.score_array]

        self.final_score = [np.mean(k) for k in zip(*arrays_score)]

        arrays_time = [np.array(x) for x in self.time_array]

        self.final_time = [np.mean(k) for k in zip(*arrays_time)]


        self.final_prob=[]
        for y in self.all_prob_array:
            arrays_prob = [np.array(x) for x in y]
            tmp = [np.mean(k) for k in zip(*arrays_prob)]
            self.final_prob.append(tmp)


        self.final_used=[]
        for y in self.used_op_array:
            arrays_used = [np.array(x) for x in y]
            tmp = [np.mean(k) for k in zip(*arrays_used)]
            self.final_used.append(tmp)
        '''

        self.final_time = max(self.time_array)

        max_size_list = len(max(self.time_array))
        for x in self.score_array:
            x+=[1]*(max_size_list -len(x))
        self.final_score = []
        for i in range(max_size_list):
            local_mean=0
            for j in range(number_of_pass):
                local_mean+= self.score_array[j][i]
            local_mean/=number_of_pass
            self.final_score.append(local_mean)

        for x in self.all_prob_array:
            for y in x:
                y += [y[-1]] * (max_size_list - len(y))
        self.final_prob = []
        for i in range(3):
            tmp = []
            for j in range(max_size_list):
                local_mean = 0
                for k in range(number_of_pass):
                    local_mean += self.all_prob_array[k][i][j]
                local_mean /= number_of_pass
                tmp.append(local_mean)
            self.final_prob.append(tmp)


        for x in self.used_op_array:
            for y in x:
                y+=[y[-1]]*(max_size_list -len(y))
        self.final_used = []
        for i in range(3):
            tmp = []
            for j in range(max_size_list):
                local_mean = 0
                for k in range(number_of_pass):
                    local_mean += self.used_op_array[k][i][j]
                local_mean/=number_of_pass
                tmp.append(local_mean)
            self.final_used.append(tmp)




    def calculate_means_score_time(self, number_of_pass):



        arrays_score = [np.array(x) for x in self.score_array]

        self.final_score = [np.mean(k) for k in zip(*arrays_score)]

        arrays_time = [np.array(x) for x in self.time_array]

        self.final_time = [np.mean(k) for k in zip(*arrays_time)]




        

        '''
        self.final_time = max(self.time_array)

        max_size_list = len(max(self.time_array))


        for x in self.score_array:
            x += [1.0] * (max_size_list - len(x))

        self.final_score = []
        for i in range(max_size_list):
            local_mean = 0
            for j in range(number_of_pass):
                local_mean += self.score_array[j][i]
            local_mean= round(local_mean / number_of_pass,2)
            self.final_score.append(local_mean)

        last_it_moy=0
        for x in self.time_array:
            last_it_moy+= x[-1]
        last_it_moy/=len(self.time_array)
        print("LAS IT MOY", last_it_moy)
        print("TIME ", self.final_time)
        print("SCORE AARAY", self.score_array)
        print("FINAL SCORE AARAY", self.final_score)
        '''









        '''
        self.time_array=[0,50, 100]
        self.score_array=[0,0.8,1]
        self.all_prob_array=[[1,0,0],[0,1,0],[0,0,1]]
        self.used_op=[[1,0,0],[0,1,0],[0,0,1]]
        '''


    def max_value(self, inputlist):
        return max([sublist[-1] for sublist in inputlist])

