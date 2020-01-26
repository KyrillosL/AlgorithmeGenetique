import matplotlib.pyplot as plt
from matplotlib import gridspec


class Myplot:

    def __init__(self, method=0, keep_degrading=0, nb_op=3, nombre_agents_par_population=100, taille_agent=100, number_of_pass=1):
        self.keep_degrading=keep_degrading
        self.method = method
        self.score = 0
        self.temps_moyen=0
        self.nb_op = nb_op
        self.nombre_agents_par_population = nombre_agents_par_population
        self.taille_agent = taille_agent
        self.fig = plt.figure(figsize=(20, 10))
        self.number_of_pass = number_of_pass

        gs = gridspec.GridSpec(3, 3)  # 2 rows, 3 columns

        line_width = 2

        plt.ion()
        # SCORE PLOT
        self.plt_score = self.fig.add_subplot(gs[0, 0])
        self.plt_score.set_ylim([0, 1.1])
        self.plt_score.set_ylabel('Score')
        self.plt_score.set_xlabel('Generation')
        self.line_score, = self.plt_score.plot([], lw=line_width, c='black')
        self.txt_score = self.plt_score.text(1, 1, "", fontsize=20, color='red')

        # ALL PROBS PLOT
        self.all_probs = self.fig.add_subplot(gs[0, 1:])
        self.all_probs.set_ylabel('All probs')
        self.all_probs.set_xlabel('Generation')

        # USED_OP PLOT
        self.plt_used_op = self.fig.add_subplot(gs[2, :])
        self.plt_used_op.set_ylim([0, 1])
        self.plt_used_op.set_ylabel('Used Operator')
        self.plt_used_op.set_xlabel('Generation')

        self.line_score_used_op, = self.plt_used_op.plot([], lw=line_width, c='black')

        # PROBS PLOT
        self.list_plt_prob = []
        self.list_line_plt = []
        self.list_line_plt__all_probs = []
        self.list_line_used_op = []
        for i in range(self.nb_op):

            plt_probs = self.fig.add_subplot(gs[1, i])
            plt_probs.set_xlabel('Generation')
            if i == 0:
                if method == 3:
                    line, = plt_probs.plot([], 'o', markersize=2, lw=line_width, c='red')
                    line_all_probs, = self.all_probs.plot([], 'o', markersize=2, lw=line_width - 0.5, c='red')
                else:
                    line, = plt_probs.plot([], lw=line_width, c='red')
                    line_all_probs, = self.all_probs.plot([], lw=line_width - 0.5, c='red')
                line_all_time_used, = self.plt_used_op.plot([], lw=line_width - 0.5, c='red')
                plt_probs.set_ylabel('flip 1_n')
            if i == 1:
                if method == 3:
                    line, = plt_probs.plot([], 'o', markersize=2, lw=line_width, c='green')
                    line_all_probs, = self.all_probs.plot([], 'o', markersize=2, lw=line_width - 0.5, c='green')
                else:
                    line, = plt_probs.plot([], lw=line_width, c='green')
                    line_all_probs, = self.all_probs.plot([], lw=line_width - 0.5, c='green')
                line_all_time_used, = self.plt_used_op.plot([], lw=line_width - 0.5, c='green')
                plt_probs.set_ylabel('flip 3_n')
            if i == 2:
                if method == 3:
                    line, = plt_probs.plot([], 'o', markersize=2, lw=line_width, c='blue')
                    line_all_probs, = self.all_probs.plot([], 'o', markersize=2, lw=line_width - 0.5, c='blue')
                else:
                    line, = plt_probs.plot([], lw=line_width, c='blue')
                    line_all_probs, = self.all_probs.plot([], lw=line_width - 0.5, c='blue')

                line_all_time_used, = self.plt_used_op.plot([], lw=line_width - 0.5, c='blue')
                plt_probs.set_ylabel('flip 5_n')
            self.list_line_plt.append(line)
            self.list_line_plt__all_probs.append(line_all_probs)
            self.list_line_used_op.append(line_all_time_used)
            self.list_plt_prob.append(plt_probs)
            self.list_plt_prob[i].set_ylim([0, 1.1])

        self.fig.canvas.draw()
        self.score_bg = self.fig.canvas.copy_from_bbox(self.plt_score.bbox)
        self.all_probs_bg = self.fig.canvas.copy_from_bbox(self.all_probs.bbox)
        self.plt_used_op_bg = self.fig.canvas.copy_from_bbox(self.plt_used_op.bbox)

        self.list_op_bg = []
        self.list_list_data_prob = []
        self.list_used_op = []
        for i in range(self.nb_op):
            self.list_data_used = []
            self.list_data_used.append(0)
            self.list_used_op.append(self.list_data_used)

        for i in range(self.nb_op):
            self.list_op_bg.append(self.fig.canvas.copy_from_bbox(self.list_plt_prob[i].bbox))
            self.list_data_prob = []
            self.list_data_prob.append(0)

            self.list_list_data_prob.append(self.list_data_prob)

        self.time = []
        self.time.append(0)

        self.data_score = []
        self.data_score.append(0)

        # plt.show(block=False)

    def update_plot(self, temps_moyen, itetarion_moyen):

        info = "Taille population  " + str(self.nombre_agents_par_population) + " Taille individu : " + str(self.taille_agent) + "\n" + " Keep degrading : " + str(self.keep_degrading) + "\n" + "Nombre iterations moyennes sur " + str(self.number_of_pass) + " Executions "+ str(itetarion_moyen)+ "\n" + "Temps moyen : " + str(temps_moyen) + "\n"

        if self.method == 0:
            self.fig.suptitle(info + ' Method : Oracle Myope | INFO : no probalities in this method ', fontsize=14,
                              fontweight='bold')
            self.fig
        elif self.method == 1:
            self.fig.suptitle(info +
                'Method : Uniform (Fixed wheel probabilities) | INFO : all probs = 0.33.',
                fontsize=14, fontweight='bold')
        elif self.method == 2:
            self.fig.suptitle(info + 'Method : Adaptive wheel  ', fontsize=14,
                              fontweight='bold')
        elif self.method == 3:
            self.fig.suptitle(info + 'Method : Adaptive pursuit', fontsize=14,
                              fontweight='bold')
        elif self.method == 4:
            self.fig.suptitle(info + 'Method :UCB | INFO : Rewards displayed instead of probabilities', fontsize=14,
                              fontweight='bold')
        elif self.method == 5:
            self.fig.suptitle(info + 'Method :EXP3  ', fontsize=14,
                              fontweight='bold')



        # SCORE
        xmin_score, xmax_score, ymin_score, ymax_score = [min(self.time) / 1.05, max(self.time) * 1.01, 0, 1.1]
        self.plt_score.axis([xmin_score, xmax_score, ymin_score, ymax_score])
        self.plt_score.set_xlim([0, max(self.time)])
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
            # self.list_plt_prob[i].draw_artist(self.list_line_plt[i])
            self.fig.canvas.blit(self.list_plt_prob[i].bbox)

        # ALL PROBS
        xmin_probs, xmax_probs, ymin_probs, ymax_probs = [min(self.time) / 1.05, max(self.time) * 1.01, 0,
                                                          max(max(s) for s in zip(*self.list_list_data_prob)) * 1.1]
        self.all_probs.axis([xmin_probs, xmax_probs, ymin_probs, ymax_probs])

        self.fig.canvas.restore_region(self.all_probs_bg)
        # for i in range(self.nb_op):
        # print(list_line_plt[i])
        # self.all_probs.draw_artist(self.list_line_plt__all_probs[i])
        self.fig.canvas.blit(self.all_probs.bbox)

        # Used_OP

        xmin_score, xmax_score, ymin_score, ymax_score = [min(self.time) / 1.05, max(self.time) * 1.01, 0, max(
            max(s) for s in zip(*self.list_used_op)) * 1.1]
        self.plt_used_op.axis([xmin_score, xmax_score, ymin_score, ymax_score])
        self.plt_used_op.set_xlim([0, max(self.time)])

        # self.line_score_used_op.set_data(self.time,  [i * max(
        #    max(s) for s in zip(*self.list_used_op)) for i in self.data_score])
        self.fig.canvas.restore_region(self.plt_used_op_bg)
        for i in range(self.nb_op):
            self.list_line_used_op[i].set_data(self.time, self.list_used_op[i])
            # self.plt_used_op.draw_artist(self.list_line_used_op[i])

        self.fig.canvas.blit(self.plt_used_op.bbox)
        self.fig.canvas.flush_events()

    def show(self):
        plt.show()

    def turn_off_interactive_mode(self):
        plt.ioff()
