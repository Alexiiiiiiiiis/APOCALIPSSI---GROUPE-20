import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Responsable du traitement',
    content: (
      <p className="text-sm text-slate-600">
        Le responsable du traitement est l&apos;équipe 20 du projet pédagogique EduTutor IA,
        dans le cadre APOCAL&apos;IPSSI 2026. Contact DPO fictif : dpo@edututor.local.
      </p>
    ),
  },
  {
    title: 'Données personnelles collectées',
    content: (
      <p className="text-sm text-slate-600">
        Compte utilisateur : email, prénom, nom, date d&apos;inscription, état de validation
        email. Données pédagogiques : cours importés, textes extraits de PDF, quiz générés,
        réponses sélectionnées, scores, historique et demandes RGPD.
      </p>
    ),
  },
  {
    title: 'Finalités et bases légales',
    content: (
      <p className="text-sm text-slate-600">
        Les données servent à créer le compte, générer des quiz, afficher les scores, conserver
        l&apos;historique, sécuriser le service et répondre aux demandes légales. Bases légales :
        exécution du service demandé, intérêt légitime de sécurité, obligation légale RGPD.
      </p>
    ),
  },
  {
    title: 'Durée de conservation',
    content: (
      <p className="text-sm text-slate-600">
        Le compte et les quiz sont conservés tant que le compte reste actif. Les demandes RGPD
        et preuves associées sont conservées 12 mois. Les données sont supprimées en cas de
        suppression du compte, sauf obligations légales temporaires.
      </p>
    ),
  },
  {
    title: 'Destinataires et transferts',
    content: (
      <p className="text-sm text-slate-600">
        Les données sont accessibles uniquement aux utilisateurs authentifiés et à l&apos;équipe
        d&apos;administration du projet. Le fournisseur LLM retenu pour le MVP est Ollama local :
        les cours ne quittent pas le serveur applicatif.
      </p>
    ),
  },
  {
    title: 'Vos droits',
    content: (
      <p className="text-sm text-slate-600">
        Vous pouvez demander l&apos;accès, la rectification, la suppression, la limitation et la
        portabilité de vos données. Un export JSON/CSV est disponible depuis la page Profil.
        Vous pouvez contacter dpo@edututor.local ou saisir la CNIL.
      </p>
    ),
  },
];

export default function ConfidentialitePage() {
  return (
    <LegalScaffold
      title="Politique de confidentialité"
      intro="Comment EduTutor IA collecte, utilise, exporte et protège les données personnelles."
      sections={SECTIONS}
    />
  );
}
