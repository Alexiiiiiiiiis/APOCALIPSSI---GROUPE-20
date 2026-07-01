# Correction J2 — Changement LLM finalisé

Le runtime Django utilisait déjà `OLLAMA_MODEL=llama3.2:3b` dans `backend/apocal/settings.py` et dans `.env.example`, mais quelques références restaient sur l'ancien modèle `llama3.1:8b` dans les scripts et la documentation.

Corrections appliquées :
- `backend/llm/providers.py` : modèle conseillé Ollama passé à `llama3.2:3b`.
- `Makefile` : `make pull-model` télécharge maintenant `llama3.2:3b`.
- scripts de démarrage Linux/macOS/Windows : fallback modèle passé à `llama3.2:3b`.
- scripts de redeploy : commande affichée corrigée.
- guides et troubleshooting : commandes de test corrigées.

Note : `scripts/benchmark-llm-j2.sh` conserve volontairement `llama3.1:8b`, `llama3.2:3b` et `phi3:mini` car c'est le script de comparaison du benchmark J2.
