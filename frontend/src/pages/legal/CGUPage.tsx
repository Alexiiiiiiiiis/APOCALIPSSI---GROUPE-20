import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Objet du service',
    content: (
      <p className="text-sm text-slate-600">
        EduTutor IA permet à un utilisateur authentifié d&apos;importer un cours, de générer un
        quiz de révision, de répondre aux questions et de suivre ses résultats.
      </p>
    ),
  },
  {
    title: 'Compte utilisateur',
    content: (
      <p className="text-sm text-slate-600">
        L&apos;email sert d&apos;identifiant. L&apos;utilisateur doit fournir des informations exactes,
        conserver son mot de passe confidentiel et signaler tout usage non autorisé.
      </p>
    ),
  },
  {
    title: 'Comportements interdits',
    content: (
      <p className="text-sm text-slate-600">
        Sont interdits : tentative d&apos;accès au compte d&apos;autrui, injection de prompt,
        contournement de sécurité, dépôt de contenus illicites ou extraction massive de données.
      </p>
    ),
  },
  {
    title: 'Contenu généré par IA',
    content: (
      <p className="text-sm text-slate-600">
        Les quiz sont générés automatiquement à partir du cours fourni. Ils peuvent contenir des
        erreurs et doivent être vérifiés avant tout usage académique ou professionnel.
      </p>
    ),
  },
  {
    title: 'Responsabilité',
    content: (
      <p className="text-sm text-slate-600">
        EduTutor IA est un projet pédagogique fourni sans garantie de disponibilité permanente.
        L&apos;équipe n&apos;est pas responsable d&apos;un usage abusif ou d&apos;une mauvaise interprétation des
        résultats générés.
      </p>
    ),
  },
];

export default function CGUPage() {
  return (
    <LegalScaffold
      title="Conditions Générales d'Utilisation"
      intro="Les règles d'utilisation du service EduTutor IA."
      sections={SECTIONS}
    />
  );
}
