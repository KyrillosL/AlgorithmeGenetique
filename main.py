import algorithme_genetique as ag



parametres_algo = {
"nombre_agents_par_population":20,
"taille_agent":100 #MAX 10 000 pour un temps raisonable < 1 min
}

"test"
ag = ag.Algorithme_genetique(parametres_algo)

#0 = best OK MARCHE BIEN
#1 = roulette fixe OK RESULTAT ATTENDU
#2 = roulette adaptive NON
#3= adaptive poursuit OK MARCHE BIEN
#4=ucb JOUER SUR LA FENETRE DE REWARD !!!!! DANS LE RAPPORT
#5=Exp3 NE MARHCE QU'AVEC LES NON DEGRADNATS
ag.solve(0, realtime_plot=True, refresh_rate=100, realtime_counter=True, keep_degrading=True)

print(ag)