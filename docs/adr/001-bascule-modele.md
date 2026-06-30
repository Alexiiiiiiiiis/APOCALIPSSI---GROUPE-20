ADR-001 : Bascule vers Llama 3.2 3B pour réduire la latence 

Date : 30 juin 2026 Statut : Accepté 

1. Contexte 

Lors du bêta-test étudiant de notre version de développement, un retour critique a été remonté : la génération d'un quiz de 10 questions prenait près d'une minute, poussant l'utilisateur à l'abandon. Pour vérifier ce comportement, nous avons benchmarqué notre modèle actuel (Llama 3.1). Les logs révèlent une latence réelle de 55.37 secondes pour générer 5 questions, ce qui ne respecte pas le critère d'acceptation du sponsor (≤ 15 secondes). 

2. Options envisagées 

Option A : Conserver Llama 3.1 (8B) (Latence testée : 55.37s). 

Option B : Remplacer le modèle par Llama 3.2 (3B) (Latence testée : 8.21s). 

Option C : Remplacer le modèle par Phi-3 Mini (3.8B) (Latence testée : 48.50s). 

3. Décision retenue 

Nous avons décidé d'adopter l'Option B (Llama 3.2 3B). 

Justification du trade-off : Contrairement à nos craintes initiales, passer sur un modèle plus léger n'a pas dégradé la qualité de la génération dans notre cas précis, bien au contraire. Llama 3.2 a divisé le temps de réponse par près de 7 (passant de 55s à 8.2s) tout en respectant bien mieux le formatage QCM demandé (4 choix clairs) que le modèle 8B. Phi-3 a été écarté en raison de ses hallucinations techniques et de son temps d'évaluation du prompt beaucoup trop long (34s). 

4. Conséquences 

Positives : L'expérience utilisateur est sauvée (génération en ~8 secondes). Le produit respecte officiellement l'exigence d'instantanéité du sponsor. L'empreinte mémoire sur le serveur est drastiquement réduite. 

Négatives : Aucune régression qualitative identifiée sur ce test précis. 

À surveiller : Llama 3.2 reste un "petit" modèle (3 milliards de paramètres). Nous devrons vérifier s'il maintient ce niveau de performance et de qualité sur des PDF beaucoup plus longs et complexes (ex: 300 pages) où le contexte pourrait saturer sa mémoire. 

 