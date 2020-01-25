class Final_plotter:

    def __init__(self):

        self.time_array=[]
        self.score_array=[]
        self.all_prob_array=[]
        self.used_op=[]


    def add_plot(self, time, score, all_probs, used ):

        self.time_array.append(time)
        self.score_array.append(score)
        self.all_prob_array.append(all_probs)
        self.used_op.append(used)

    def calculate_means(self):
        self.final_time = []

        max_time= max(max(s) for s in zip(*self.time_array))
        print(max_time)
        '''
        self.time_array=[0,50, 100]
        self.score_array=[0,0.8,1]
        self.all_prob_array=[[1,0,0],[0,1,0],[0,0,1]]
        self.used_op=[[1,0,0],[0,1,0],[0,0,1]]
        '''




