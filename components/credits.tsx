import { Github, Globe } from 'lucide-react';

export interface Credit {
  name: string;
  role: string;
  github?: string;
  website?: string;
}

interface CreditsProps {
  credits: Credit[];
}

export function Credits({ credits }: CreditsProps) {
  return (
    <div className="flex border-border">
        {/* <h2 className="text-2xl font-bold mb-4 text-center">Credits</h2> */}
        <div className="flex  justify-center gap-8">
          {credits.map((credit, index) => (
            <div key={index} className="text-center font-mono">
              <p className="font-bold">{credit.name}</p>
              <p className="text-sm text-muted-foreground">{credit.role}</p>
              <div className="flex  justify-center gap-2 mt-2">
                {credit.github && (
                  <a
                    href={`https://github.com/${credit.github}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:text-primary/80"
                    aria-label={`${credit.name}'s GitHub`}
                  >
                    <Github size={20} />
                  </a>
                )}
                {credit.website && (
                  <a
                    href={credit.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:text-primary/80"
                    aria-label={`${credit.name}'s website`}
                  >
                    <Globe size={20} />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
  );
}

