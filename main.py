import algorithme_genetique as ag



parametres_algo = {
"nombre_agents_par_population":1,
"taille_agent":1000 #MAX 10 000 pour un temps raisonable < 1 min
}

"test"
ag = ag.Algorithme_genetique(parametres_algo)

#0 = Oracle Myope OK MARCHE BIEN
#1 = roulette fixe OK RESULTAT ATTENDU
#2 = roulette adaptive NON
#3= adaptive poursuit OK MARCHE BIEN
#4=ucb JOUER SUR LA FENETRE DE REWARD !!!!! DANS LE RAPPORT
#5=Exp3 NE MARHCE QU'AVEC LES NON DEGRADNATS



ag.solve(method=0, realtime_plot=True, refresh_rate_plot=1000, realtime_counter=True,refresh_rate_counter=parametres_algo["taille_agent"]/10,  keep_degrading=False, one_indiv=True, stop_after=10000)

print(ag)