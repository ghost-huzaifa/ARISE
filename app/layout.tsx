import { ThemeProvider } from '@/components/theme/theme-provider';
import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ThemeToggle } from '@/components/theme/theme-toggle';
import { Credit, Credits } from '@/components/credits';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SSL Research Agent',
  description: 'Automating Research Material Retrieval and Analysis',
   icons: {
    icon: "/favicon.png",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
      const credits: Credit[] = [
    {
      name: "Abdul Rehman",
      role: "Creator",
      github: "festerduck",
    },
    {
      name: "Muhammad Huzaifa",
      role: "Creator",
      github: "ghost-huzaifa"
    },
     {
      name: "Dr. Asifullah Khan",
      role: "Professor",
      website: "https://scholar.google.com.pk/citations?user=C8uhO88AAAAJ&hl=en"
      
    }
  ];
  return (

    <html lang="en">
      <body className={inter.className}>
         <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
         <div className="min-h-screen bg-background">
            <header className="border-b">
              <div className="container mx-auto px-4 py-3 flex justify-between items-center">
                <div className='flex flex-col items-start justify-between'>

                <h1 className="text-xl font-bold">SSL Research Agent</h1>
                <h4 className='font-mono text-muted-foreground'>Automating Research Material Retrieval and Analysis</h4>
                </div>

               <nav className='flex gap-8 justify-center items-center'>
                 <Credits credits={credits} />
                <ThemeToggle />

               </nav>
                
              </div>
            </header>
            {children}
          </div>
        </ThemeProvider>
        </body>
    </html>
  );
}
