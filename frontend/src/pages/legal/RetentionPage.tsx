import LegalScaffold, { type LegalSection } from './LegalScaffold';

// Reprend fidèlement docs/legal/politique-retention.md (livrable J3-bis RGPD).
const SECTIONS: LegalSection[] = [
  {
    title: 'Durées de conservation',
    content: (
      <ul className="text-sm text-slate-600 list-disc pl-5 space-y-1">
        <li>
          <span className="font-medium">Compte utilisateur</span> : conservé tant que le compte
          est actif.
        </li>
        <li>
          <span className="font-medium">Cours uploadés / textes extraits</span> : conservés tant
          que les quiz associés existent ou jusqu&apos;à suppression du compte.
        </li>
        <li>
          <span className="font-medium">Quiz, réponses et scores</span> : conservés tant que le
          compte est actif pour fournir l&apos;historique et le suivi de progression.
        </li>
        <li>
          <span className="font-medium">Logs d&apos;audit SAR / demandes RGPD</span> : conservés
          12 mois pour démontrer le traitement des demandes.
        </li>
        <li>
          <span className="font-medium">Signalements de contenu</span> : catégorie prévue pour J4 ;
          conservation cible 3 ans maximum si un modèle de signalement est ajouté.
        </li>
      </ul>
    ),
  },
  {
    title: 'Motifs légaux',
    content: (
      <>
        <p className="text-sm text-slate-600 mb-2">
          Chaque traitement repose sur une base légale de l&apos;
          <span className="font-medium">article 6 du RGPD</span> :
        </p>
        <ul className="text-sm text-slate-600 list-disc pl-5 space-y-1">
          <li>
            <span className="font-medium">Exécution du service (Art. 6-1-b)</span> : création de
            compte, génération de quiz, historique de révision.
          </li>
          <li>
            <span className="font-medium">Consentement (Art. 6-1-a)</span> : cookies non essentiels
            et communications optionnelles, révocable à tout moment.
          </li>
          <li>
            <span className="font-medium">Intérêt légitime (Art. 6-1-f)</span> : sécurité
            applicative, audit, prévention des abus.
          </li>
          <li>
            <span className="font-medium">Obligation légale (Art. 6-1-c)</span> : réponse aux
            demandes d&apos;accès, de portabilité ou de suppression RGPD.
          </li>
        </ul>
      </>
    ),
  },
  {
    title: 'Suppression et droit à l’oubli',
    content: (
      <>
        <p className="text-sm text-slate-600 mb-2">
          Deux mécanismes assurent la suppression des données :
        </p>
        <ul className="text-sm text-slate-600 list-disc pl-5 space-y-1">
          <li>
            <span className="font-medium">Suppression manuelle (SAR Art. 17)</span> :
            l&apos;utilisateur peut supprimer son compte depuis la page Profil. Cette action
            supprime le compte, le profil et les quiz liés par cascade. L&apos;équipe vérifie
            qu&apos;aucune obligation légale ne justifie une conservation temporaire de certaines
            preuves d&apos;audit.
          </li>
          <li>
            <span className="font-medium">Purge automatique (cron)</span> : une tâche planifiée
            purge automatiquement les logs d&apos;audit{' '}
            <code className="text-xs bg-slate-100 px-1 py-0.5 rounded">DataRequest</code> au-delà de
            leur durée de conservation (12 mois) et les catégories arrivées à échéance, sans
            intervention manuelle.
          </li>
        </ul>
        <p className="text-sm text-slate-600 mt-2">
          Les exports RGPD sont générés à la demande et ne sont pas conservés comme fichier
          permanent ; seul le hash est enregistré dans{' '}
          <code className="text-xs bg-slate-100 px-1 py-0.5 rounded">DataRequest</code>.
        </p>
      </>
    ),
  },
];

export default function RetentionPage() {
  return (
    <LegalScaffold
      title="Politique de rétention des données"
      intro="Durées de conservation, motifs légaux et modalités de suppression des données personnelles d'EduTutor IA."
      sections={SECTIONS}
    />
  );
}
