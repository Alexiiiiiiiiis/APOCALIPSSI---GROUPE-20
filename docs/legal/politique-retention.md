# Politique de rétention des données — EduTutor IA

## 1. Durées de conservation
- **Compte utilisateur** : conservé tant que le compte est actif.
- **Cours uploadés / textes extraits** : conservés tant que les quiz associés existent ou jusqu'à suppression du compte.
- **Quiz, réponses et scores** : conservés tant que le compte est actif pour fournir l'historique et le suivi de progression.
- **Logs d'audit SAR / demandes RGPD** : conservés 12 mois pour démontrer le traitement des demandes.
- **Signalements de contenu** : catégorie prévue pour J4 ; conservation cible 3 ans maximum si un modèle de signalement est ajouté.

## 2. Motifs légaux
Chaque traitement repose sur une base légale de l'**article 6 du RGPD** :
- **Exécution du service (Art. 6-1-b)** : création de compte, génération de quiz, historique de révision.
- **Consentement (Art. 6-1-a)** : cookies non essentiels et communications optionnelles, révocable à tout moment.
- **Intérêt légitime (Art. 6-1-f)** : sécurité applicative, audit, prévention des abus.
- **Obligation légale (Art. 6-1-c)** : réponse aux demandes d'accès, de portabilité ou de suppression RGPD.

## 3. Suppression et droit à l'oubli
Deux mécanismes assurent la suppression des données :
- **Suppression manuelle (SAR Art. 17)** : l'utilisateur peut supprimer son compte depuis la page Profil. Cette action supprime le compte, le profil et les quiz liés par cascade. Pour une demande RGPD Art. 17, l'équipe vérifie qu'aucune obligation légale ne justifie une conservation temporaire de certaines preuves d'audit.
- **Purge automatique (cron)** : une tâche planifiée purge automatiquement les logs d'audit `DataRequest` au-delà de leur durée de conservation (12 mois) et les catégories arrivées à échéance, sans intervention manuelle.

Les exports RGPD sont générés à la demande et ne sont pas conservés comme fichier permanent ; seul le hash est enregistré dans `DataRequest`.
