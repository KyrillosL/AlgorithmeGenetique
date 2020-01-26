import algorithme_genetique as ag



parametres_algo = {
"nombre_agents_par_population":20,
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
#refresh_rate_counter=parametres_algo["taille_agent"]/10


ag.solve(method=1, realtime_plot=False, refresh_rate_plot=1, realtime_counter=True,refresh_rate_counter=1,  keep_degrading=True, one_indiv=False, stop_after=100000, number_of_pass=20)

print(ag)