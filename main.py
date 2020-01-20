import algorithme_genetique as ag



parametres_algo = {
"nombre_agents_par_population":20,
"taille_agent":1000
}

"test"
ag = ag.Algorithme_genetique(parametres_algo)

#0 = best
#1 = roulette fixe
#2 = roulette adaptive
#3= adaptive poursuit
#4=ucb
ag.solve(4, True)

print(ag)