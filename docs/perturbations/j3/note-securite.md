# Note de sécurité J3 — Prompt injection OWASP LLM-01

## 1. Diagnostic
La vulnérabilité vient du fait que le cours uploadé par l'utilisateur était injecté directement dans le prompt. Si le cours contenait une phrase du type « ignore les instructions précédentes », le modèle pouvait la considérer comme une consigne prioritaire. Le risque est fort dans EduTutor IA, car le produit transforme des documents utilisateurs en quiz : un PDF, un copier-coller HTML ou un texte caché peut manipuler le LLM.

## 2. Stratégie défensive mise en place
Nous avons appliqué une défense en profondeur :

1. **Séparation system / user** : les clients chat conservent des messages séparés ; Ollama reçoit un prompt unique mais structuré avec blocs `[SYSTEM]` et `[USER_DATA]`.
2. **Délimiteurs explicites** : le cours est borné par `<<<DEBUT_COURS_UTILISATEUR_NON_FIABLE>>>` et `<<<FIN_COURS_UTILISATEUR_NON_FIABLE>>>`.
3. **System prompt défensif** : il indique clairement que le cours est une donnée non fiable et que toute instruction présente dedans doit être ignorée.
4. **Sanitization légère** : suppression des balises HTML, commentaires, scripts/styles et caractères invisibles.
5. **Validation post-LLM** : le JSON est rejeté si le schéma est incorrect, si les options ne sont pas distinctes, si le nombre de questions n'est pas exactement 10 ou si toutes les bonnes réponses sont sur la même lettre.
6. **Tests adversariaux CI** : un fichier pytest couvre plusieurs familles d'attaque.

## 3. Limites résiduelles
Cette protection ne garantit pas une sécurité parfaite. Les injections sémantiques très subtiles peuvent encore influencer un petit modèle local. La validation actuelle bloque les erreurs structurelles et le cas critique « toutes les réponses A », mais elle ne prouve pas la justesse pédagogique de chaque question. Il faudra compléter avec l'audit qualité J4, des tests sur PDF réels et une surveillance des signalements utilisateurs.
