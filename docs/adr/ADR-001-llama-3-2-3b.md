# ADR-001 — Bascule vers Llama 3.2 3B pour réduire la latence

Date : 30/06/2026  
Statut : Accepté

## Contexte
Le benchmark J2 montre que Llama 3.1 8B génère 5 questions en 55,37 s, au-dessus de l'exigence sponsor de 15 s. Llama 3.2 3B produit le quiz en 8,21 s avec un meilleur respect du format QCM.

## Options
- A : conserver Llama 3.1 8B — 55,37 s.
- B : passer à Llama 3.2 3B — 8,21 s.
- C : passer à Phi-3 Mini — 48,50 s, hallucinations observées.

## Décision
Adopter Llama 3.2 3B pour le MVP local Ollama.

## Conséquences
- Positif : latence divisée par environ 7, conforme à l'objectif d'interactivité.
- Négatif : modèle plus petit, à surveiller sur documents longs.
- Suivi : conserver les tests de qualité J4 et limiter le contexte source à 8000 caractères.
