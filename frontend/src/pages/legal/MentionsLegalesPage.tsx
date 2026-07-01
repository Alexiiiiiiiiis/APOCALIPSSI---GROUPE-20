import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Éditeur du site',
    content: (
      <p className="text-sm text-slate-600">
        EduTutor IA — projet pédagogique réalisé par l&apos;équipe 20 dans le cadre APOCAL&apos;IPSSI
        2026. Adresse de contact : contact@edututor.local.
      </p>
    ),
  },
  {
    title: 'Directeur de la publication',
    content: (
      <p className="text-sm text-slate-600">
        Responsable pédagogique fictif du MVP : Product Owner APOCAL&apos;IPSSI / Équipe 20.
      </p>
    ),
  },
  {
    title: 'Hébergeur',
    content: (
      <p className="text-sm text-slate-600">
        En environnement de démonstration, l&apos;application est hébergée sur l&apos;infrastructure
        fournie pour le projet. En production cible : serveur VPS européen, reverse proxy HTTPS.
      </p>
    ),
  },
  {
    title: 'Propriété intellectuelle',
    content: (
      <p className="text-sm text-slate-600">
        Le code et les contenus de démonstration sont utilisés dans un cadre pédagogique. Les
        cours importés restent la propriété de leurs titulaires respectifs.
      </p>
    ),
  },
  {
    title: 'Contact',
    content: (
      <p className="text-sm text-slate-600">
        Pour toute question juridique ou relative aux présentes mentions, écrivez à
        contact@edututor.local. Les demandes concernant les données personnelles peuvent être
        adressées au DPO fictif : dpo@edututor.local.
      </p>
    ),
  },
];

export default function MentionsLegalesPage() {
  return (
    <LegalScaffold
      title="Mentions légales"
      intro="Informations légales identifiant l'éditeur et l'hébergement du service."
      sections={SECTIONS}
    />
  );
}
