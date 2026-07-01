# Perturbation J3 — Prompt injection

Livrables intégrés :

- `docs/perturbations/j3/adversarial-prompts.md` : jeu de tests adversariaux documenté.
- `docs/perturbations/j3/note-securite.md` : diagnostic, stratégie, limites.
- `backend/llm/services/quiz_prompt.py` : patch architectural system/user, délimiteurs, nettoyage, validation post-LLM.
- `backend/llm/tests/adversarial/test_prompt_injection.py` : tests pytest automatisés exécutés par la CI.

Critère MVP : aucune sauvegarde de quiz si la sortie LLM ne respecte pas exactement le contrat JSON attendu.
