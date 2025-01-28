import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Loader2 } from 'lucide-react';

interface SearchBarProps {
  searchQuery: string;
  onSearchChange: (value: string) => void;
  onSearch: () => void;
  loading: boolean;
}

export function SearchBar({
  searchQuery,
  onSearchChange,
  onSearch,
  loading
}: SearchBarProps) {
  return (
    <div className="flex gap-2 w-full">
      <div className="relative flex-1 w-full">
        <Input
          placeholder="Prompt me..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && onSearch()}
          className="pl-16 py-5 h-full text-2xl bg-white/10 text-white placeholder:text-white/70 border-white/20 w-full"
        />
        <Search className="absolute left-6 top-1/2 transform -translate-y-1/2 text-white/60 h-full w-7" />
      </div>
      <Button onClick={onSearch} disabled={loading} className="bg-white text-primary hover:bg-white/90 py-5 px-8 text-xl h-full">
        {loading ? (
          <Loader2 className="mr-2 h-6 w-6 animate-spin" />
        ) : (
          <Search className="mr-2 h-6 w-6" />
        )}
        Search
      </Button>
    </div>
  );
}

