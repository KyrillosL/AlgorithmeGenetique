import algorithme_genetique as ag



parametres_algo = {
"nombre_agents_par_population":20,
"taille_agent":100
}

ag = ag.Algorithme_genetique(parametres_algo)
ag.solve()

print(ag)