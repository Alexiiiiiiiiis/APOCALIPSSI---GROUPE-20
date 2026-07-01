import type { ReactNode } from 'react';

export const REGLEMENTATION_URL = 'https://mohamedelafrit.com/teaching/Reglementation_des_Donnees';

export type LegalSection = {
  title: string;
  hint?: string;
  content?: ReactNode;
};

type Props = {
  title: string;
  intro: string;
  sections: LegalSection[];
  children?: ReactNode;
};

export default function LegalScaffold({ title, intro, sections, children }: Props) {
  const completed = sections.every((section) => section.content);

  return (
    <article className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">{title}</h1>
      <p className="text-slate-600 mb-6">{intro}</p>

      <div
        className={`mb-8 p-4 border-l-4 rounded text-sm ${
          completed
            ? 'bg-emerald-50 border-emerald-400 text-emerald-900'
            : 'bg-amber-50 border-amber-400 text-amber-900'
        }`}
      >
        <p className="font-semibold mb-1">
          {completed ? '✅ Page complétée pour le MVP' : '📝 Page à compléter par votre équipe'}
        </p>
        <p>
          Document pédagogique APOCAL&apos;IPSSI 2026. Pour le cadre théorique, consultez{' '}
          <a
            href={REGLEMENTATION_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-700 underline hover:no-underline font-medium"
          >
            le cours « Réglementation des données »
          </a>
          .
        </p>
      </div>

      <div className="space-y-6">
        {sections.map((section, i) => (
          <section key={section.title}>
            <h2 className="text-lg font-semibold text-slate-900 mb-1">
              {i + 1}. {section.title}
            </h2>
            {section.content ?? (
              <p className="text-sm text-slate-500 italic">À compléter — {section.hint}</p>
            )}
          </section>
        ))}
      </div>

      {children}

      <p className="text-xs text-slate-400 mt-10 pt-4 border-t border-slate-200">
        Dernière mise à jour : 01/07/2026. Document rédigé dans le cadre pédagogique
        APOCAL&apos;IPSSI 2026.
      </p>
    </article>
  );
}
