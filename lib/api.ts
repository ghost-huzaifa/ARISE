import { API_BASE_URL } from './config';
import { Paper, SearchResponse } from './types';

export async function searchPapers(prompt: string): Promise<SearchResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch papers');
    }

    return await response.json();
  } catch (error) {
    console.error('Search papers error:', error);
    return { error: error instanceof Error ? error.message : 'An error occurred' };
  }
}