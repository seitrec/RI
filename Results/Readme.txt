Les mesures de pertinences de notre moteur de recherche se font à l'aide du script measures.

En fonction du type de pondération choisie (standard, tfidf, tfidfnormalisé), on y calcule pour chaque query test de CACM le score d'average precision et on trace la courbe de Precision - Recall pour l'ensemble des requêtes.

Le dossier Results comporte plusieurs courbe Precision-Recall en fonction de différents changement dans le modèle choisi. On remarque que le tfidf est meilleur que l'implémentation standarde. La normalisation du tfidf ne change pas énormément les résultats, ce qui est surprenant. 

Notre structure de mesure est prête pour tester différentes implémentations. 