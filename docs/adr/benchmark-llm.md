Benchmark des modèles LLM Locaux (Perturbation J2) 

1. Protocole de test 

Environnement cible : Serveur d'inférence local (Ollama). 

Document source : Extrait de cours d'Algorithmie (définition, tris, complexité temporelle). 

Requête (Prompt) : "Génère un quiz de 5 questions à choix multiples (QCM) avec 1 bonne réponse et 3 mauvaises réponses." 

Méthodologie : Exécution avec le flag --verbose pour capturer la total duration exacte. 

2. Résultats des mesures réelles 

Modèle évalué 

Latence Totale 

Vitesse de génération 

Qualité (sur 5) 

Remarques sur l'output 

Llama 3.1 (8B) (Actuel) 

55.37 s 

17.43 tokens/s 

3.5 / 5 

Formatage instable : n'a généré que 2 choix de réponses au lieu de 4 sur les dernières questions. 

Llama 3.2 (3B) (Option 1) 

8.21 s 

71.28 tokens/s 

4.8 / 5 

Excellent formatage (A, B, C, D), respect strict de la consigne et des distracteurs. 

Phi-3 Mini (3.8B) (Option 2) 

48.50 s 

65.28 tokens/s 

2.0 / 5 

Hallucinations techniques (erreur sur O(n log n)), format illisible intégrant les balises "Bonne réponse" dans les choix. 

3. Conclusion de l'équipe 

Les données parlent d'elles-mêmes. Le modèle de base (Llama 3.1 8B) est beaucoup trop lent (55 secondes) pour notre cas d'usage interactif. L'alternative Llama 3.2 3B a produit le meilleur résultat qualitatif tout en générant le quiz en à peine 8.2 secondes. Le choix technique est donc évident et documenté dans l'ADR-001. 

