import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';
import { SearchResponse } from '@/lib/types';

export async function POST(req: Request) {
  try {
    const { keywords } = await req.json();
    
    if (!Array.isArray(keywords) || keywords.length === 0) {
      return NextResponse.json(
        { error: 'Keywords must be provided as an array' },
        { status: 400 }
      );
    }

    const scriptPath = path.join(process.cwd(), 'scripts', 'research_agent.py');

    const response: SearchResponse = await new Promise((resolve) => {
      const pythonProcess = spawn('python3', [scriptPath, ...keywords]);
      let dataString = '';

      pythonProcess.stdout.on('data', (data) => {
        dataString += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
      });

      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          resolve({ error: 'Failed to execute search' });
          return;
        }

        try {
          const results = JSON.parse(dataString);
          resolve(results);
        } catch (e) {
          console.error('Failed to parse Python output:', e);
          resolve({ error: 'Failed to parse results' });
        }
      });
    });

    if (response.error) {
      return NextResponse.json({ error: response.error }, { status: 500 });
    }

    return NextResponse.json(response);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}