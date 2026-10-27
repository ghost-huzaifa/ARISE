import { Paper } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Calendar, FileText, ExternalLink, Sparkles, BookOpen } from 'lucide-react';

interface PaperCardProps {
  paper: Paper;
}

export function PaperCard({ paper }: PaperCardProps) {
  const score = paper.relevance_score ?? 85;
  const scoreVariant = score >= 85 ? "default" : score >= 70 ? "secondary" : "outline";

  return (
    <Card className="flex flex-col hover:shadow-lg transition-shadow duration-300 relative overflow-hidden">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between gap-2 mb-2">
          {paper.source && (
            <Badge variant="outline" className="text-xs font-mono text-muted-foreground flex items-center gap-1">
              <BookOpen className="h-3 w-3" />
              {paper.source}
            </Badge>
          )}
          {paper.relevance_score !== undefined && (
            <Badge variant={scoreVariant} className="text-xs font-semibold flex items-center gap-1">
              <Sparkles className="h-3 w-3" />
              {paper.relevance_score}% Match
            </Badge>
          )}
        </div>

        <CardTitle className="line-clamp-2 text-lg">
          {paper.title}
        </CardTitle>
        <div className="flex flex-wrap gap-1.5 mt-2">
          {paper.authors.slice(0, 3).map((author, idx) => (
            <Badge key={idx} variant="secondary" className="text-xs font-normal">
              {author}
            </Badge>
          ))}
          {paper.authors.length > 3 && (
            <Badge variant="secondary" className="text-xs font-normal">
              +{paper.authors.length - 3} more
            </Badge>
          )}
          {paper.citations !== undefined && paper.citations !== null && (
            <Badge variant="outline" className="text-xs font-normal text-muted-foreground">
              {paper.citations} citations
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col pt-0">
        <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
          {paper.abstract}
        </p>
        <div className="mt-auto flex gap-2 justify-between items-center pt-2 border-t">
          <div className="flex items-center text-xs text-muted-foreground">
            <Calendar className="mr-1 h-3.5 w-3.5" />
            {new Date(paper.published).toLocaleDateString(undefined, { year: 'numeric', month: 'short' })}
          </div>
          <div className="flex gap-2">
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm">
                  <FileText className="mr-1.5 h-3.5 w-3.5" />
                  Abstract
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
                <DialogHeader>
                  <div className="flex items-center gap-2 mb-2">
                    {paper.source && (
                      <Badge variant="outline">{paper.source}</Badge>
                    )}
                    {paper.relevance_score !== undefined && (
                      <Badge variant="default">{paper.relevance_score}% Relevance Score</Badge>
                    )}
                  </div>
                  <DialogTitle className="mb-4 text-left leading-snug">{paper.title}</DialogTitle>
                  <DialogDescription asChild>
                    <div>
                      <div className="flex flex-wrap gap-1.5 mb-3">
                        {paper.authors.map((author, idx) => (
                          <Badge key={idx} variant="secondary">
                            {author}
                          </Badge>
                        ))}
                      </div>
                      <p className="text-xs text-muted-foreground mb-4 flex items-center">
                        <Calendar className="mr-1.5 h-3.5 w-3.5" />
                        Published: {new Date(paper.published).toLocaleDateString()}
                        {paper.citations ? ` • ${paper.citations} total citations recorded` : ""}
                      </p>
                      <div className="p-4 bg-muted/40 rounded-lg text-sm text-foreground leading-relaxed whitespace-pre-wrap">
                        {paper.abstract || "No abstract available."}
                      </div>
                    </div>
                  </DialogDescription>
                </DialogHeader>
              </DialogContent>
            </Dialog>
            {paper.link && (
              <Button
                variant="default"
                size="sm"
                onClick={() => window.open(paper.link, "_blank")}
              >
                <ExternalLink className="mr-1.5 h-3.5 w-3.5" />
                Paper
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
