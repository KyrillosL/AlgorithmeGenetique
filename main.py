import algorithme_genetique as ag



parametres_algo = {
"nombre_agents_par_population":20,
"taille_agent":10000
}

"test"
ag = ag.Algorithme_genetique(parametres_algo)

#0 = best
#1 = roulette fixe
#2 = roulette adaptive
#3= adaptive poursuit
#4=ucb
#5=Exp3
ag.solve(5, realtime_plot=True, realtime_counter=True)

print(ag)