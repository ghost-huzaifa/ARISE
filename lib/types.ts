export interface Paper {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  published: string;
  link: string;
  relevance_score?: number;
  source?: string;
  citations?: number | null;
}

export interface SearchResponse {
  papers?: Paper[];
  total_found?: number;
  error?: string;
}

export interface ResearchTask {
  task_id: string;
  description: string;
  status: string;
  created_at: string;
  completed_at?: string;
  result?: any;
}
