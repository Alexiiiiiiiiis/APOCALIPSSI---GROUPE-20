#!/usr/bin/env bash
set -euo pipefail

PROMPT='Génère un quiz de 5 questions à choix multiples (QCM) avec 1 bonne réponse et 3 mauvaises réponses à partir d un cours d algorithmie sur les tris et la complexité.'

for model in llama3.1:8b llama3.2:3b phi3:mini; do
  echo "=== $model ==="
  ollama run "$model" "$PROMPT" --verbose || true
  echo

done
