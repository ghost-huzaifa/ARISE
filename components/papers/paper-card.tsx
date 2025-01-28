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
import { Calendar, FileText, ExternalLink } from 'lucide-react';

interface PaperCardProps {
  paper: Paper;
}

export function PaperCard({ paper }: PaperCardProps) {
  return (
    <Card className="flex flex-col hover:shadow-lg transition-shadow duration-300">
      <CardHeader>
        <CardTitle className="line-clamp-2 text-lg">
          {paper.title}
        </CardTitle>
        <div className="flex flex-wrap gap-2 mt-2">
          {paper.authors.slice(0, 3).map((author, idx) => (
            <Badge key={idx} variant="secondary" className="text-xs">
              {author}
            </Badge>
          ))}
          {paper.authors.length > 3 && (
            <Badge variant="secondary" className="text-xs">
              +{paper.authors.length - 3} more
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col">
        <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
          {paper.abstract}
        </p>
        <div className="mt-auto flex gap-2 justify-between items-center">
          <div className="flex items-center text-sm text-muted-foreground">
            <Calendar className="mr-1 h-4 w-4" />
            {new Date(paper.published).toLocaleDateString()}
          </div>
          <div className="flex gap-2">
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm">
                  <FileText className="mr-2 h-4 w-4" />
                  Details
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle className="mb-4">{paper.title}</DialogTitle>
                  <DialogDescription>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {paper.authors.map((author, idx) => (
                        <Badge key={idx} variant="secondary">
                          {author}
                        </Badge>
                      ))}
                    </div>
                    <p className="text-sm mb-2 flex items-center">
                      <Calendar className="mr-2 h-4 w-4" />
                      Published: {new Date(paper.published).toLocaleDateString()}
                    </p>
                    <p className="text-sm whitespace-pre-wrap">
                      {paper.abstract}
                    </p>
                  </DialogDescription>
                </DialogHeader>
              </DialogContent>
            </Dialog>
            <Button
              variant="default"
              size="sm"
              onClick={() => window.open(`${paper.link}`)}
            >
              <ExternalLink className="mr-2 h-4 w-4" />
              arXiv
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

