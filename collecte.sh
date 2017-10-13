#!/usr/bin/env zsh

# Au préalable, je vous conseil de séparer vos séries en trois dossiers. Pour ce
# faire, allez dans le dossier qui contient tout le data et entrez les commandes
# suivantes:
#
# mkdir ../serie1 ../serie2 ../serie3
# cp $(ls | grep "testset_[0-9]\+_[0-9].txt") ../serie1
# cp $(ls | grep "testset_[0-9]\+_1[0-9].txt") ../serie2
# cp $(ls | grep "testset_[0-9]\+_2[0-9].txt") ../serie3
#
# Vous pouvez par après vous inspirer de ce script pour évaluer toutes les
# séries avec tous les algorithmes.

for algo in {"conv","strassen","strassenSeuil"}; do
    # Pour chaque fichier de série.
    for serie in {6..10}; do
        # Pour chaque exemplaire dans une série.
        # for ex in $(ls $serie); do
        for i in {1..4}; do
            for j in $(seq $((i + 1)) 5); do
                # On receuille le temps d'exécution dans t.
                t=$(source ./tp.sh -a $algo -e ./testset${serie}/ex_${serie}.${i} ./testset${serie}/ex_${serie}.${j} -t)
                # On évalue la taille de l'exemplaire.
                n=$(cat ./testset${serie}/ex_${serie}.${i} | wc -l)
                # Si jamais on mesure un temps, on l'insère dans le bon fichier.
                if [ t != "" ]; then
                    echo $((n-1)),$t >> ./resultat_${serie}_${algo}.csv   
                fi
            done
        done
    done
done