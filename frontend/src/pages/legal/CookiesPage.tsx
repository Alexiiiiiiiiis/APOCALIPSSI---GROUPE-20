import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Cookies et stockage utilisés',
    content: (
      <p className="text-sm text-slate-600">
        Le MVP utilise le localStorage du navigateur pour conserver le token d&apos;authentification
        et la préférence de thème. Aucun cookie publicitaire ou traceur marketing n&apos;est utilisé.
      </p>
    ),
  },
  {
    title: 'Finalité',
    content: (
      <p className="text-sm text-slate-600">
        Ces stockages sont strictement nécessaires : maintenir la session, appeler l&apos;API de
        manière authentifiée et conserver l&apos;apparence choisie par l&apos;utilisateur.
      </p>
    ),
  },
  {
    title: 'Durée de conservation',
    content: (
      <p className="text-sm text-slate-600">
        Le token reste stocké jusqu&apos;à la déconnexion ou suppression manuelle du stockage local.
        La préférence de thème reste conservée jusqu&apos;à modification ou suppression navigateur.
      </p>
    ),
  },
  {
    title: 'Gestion',
    content: (
      <p className="text-sm text-slate-600">
        L&apos;utilisateur peut effacer ces données depuis les paramètres de son navigateur. La
        suppression du token provoque une déconnexion du service.
      </p>
    ),
  },
];

export default function CookiesPage() {
  return (
    <LegalScaffold
      title="Politique de gestion des cookies"
      intro="Stockages techniques utilisés par EduTutor IA."
      sections={SECTIONS}
    />
  );
}
