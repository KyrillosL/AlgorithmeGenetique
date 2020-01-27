import algorithme_genetique as ag

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt





parametres_algo = {
"nombre_agents_par_population":10,
"taille_agent":100 #MAX 10 000 pour un temps raisonable < 1 min
}


ag = ag.Algorithme_genetique(parametres_algo)

#0 = Oracle Myope OK MARCHE BIEN
#1 = roulette fixe OK RESULTAT ATTENDU
#2 = roulette adaptive NON
#3= adaptive poursuit OK MARCHE BIEN
#4=ucb JOUER SUR LA FENETRE DE REWARD !!!!! DANS LE RAPPORT
#5=Exp3 NE MARHCE QU'AVEC LES NON DEGRADNATS
#6= BASIC 1 N
#refresh_rate_counter=parametres_algo["taille_agent"]/10

all_score = False

if all_score:
    list_score=[]
    list_time=[]
    for i in range(2):
        time,score = ag.solve(method=i, realtime_plot=False, refresh_rate_plot=1, realtime_counter=True,refresh_rate_counter=1,  keep_degrading=True, one_indiv=False, stop_after=10000, number_of_pass=1, all_score=True)
        list_score.append(score)
        list_time.append(time)
        plt.ioff()
        plt.close()
    print("FIN")
    plt.figure()
    for i in range(len(list_time)):
        plt.plot(list_time[i], list_score[i])

    plt.legend(['oracle', 'uniform', 'adaptive wheel', 'adaptive pursuit', 'ucb', 'exp3', '1Flip'], loc='lower right', fontsize=15)

    #plt.legend(['oracle', 'uniform', 'adaptive wheel', 'adaptive pursuit', 'ucb', 'exp3', '1Flip'], loc='upper left')

    plt.show(block=True)
else:
    ag.solve(method=3, realtime_plot=False, refresh_rate_plot=1, realtime_counter=True,
                           refresh_rate_counter=1, keep_degrading=True, one_indiv=False, stop_after=10000,
                           number_of_pass=20, all_score = False)
