# Perturbation J3-bis — SAR RGPD Art. 15

Livrables intégrés :

- Endpoint `GET /api/accounts/me/export/?format=json|csv`.
- Modèle `DataRequest` pour l'audit trail SAR.
- Bouton frontend `Profil > Exporter mes données JSON / CSV`.
- Pages légales complétées : mentions légales, confidentialité, CGU, cookies.
- `docs/legal/politique-retention.md`.
- `docs/legal/reponse-hugo-petit.md`.
- Tests `backend/accounts/test_rgpd_export.py`.

Décision : l'export est strictement filtré par `request.user`. Les fichiers exportés ne sont pas persistés : seul leur SHA-256 est conservé dans l'audit trail.
