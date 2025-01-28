"use client";

import { useState } from "react";
import { Paper } from "@/lib/types";
import { PaperCard } from "@/components/papers/paper-card";
import { SearchBar } from "@/components/search/search-bar";
import { searchPapers } from "@/lib/api";
import { Credits } from "@/components/credits";
import { BookOpen, Github, Globe } from "lucide-react";
import Image from "next/image";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {

    setLoading(true);
    setError("");

    try {
      const response = await searchPapers(searchQuery);

      if (response.error) {
        setError(response.error);
      } else {
        setPapers(response.papers || []);
      }
    } catch (e) {
      setError("An error occurred while processing your request.");
    }

    setLoading(false);
  };
  const credits = [
    {
      name: "Abdul Rehman",
      role: "Creator",
      github: "festerduck",
    },
    {
      name: "Muhammad Huzaifa",
      role: "Creator",
      github: "ghost-huzaifa"
    }
  ];

  return (
    <main className="min-h-screen bg-background">
      <div className="relative bg-primary overflow-hidden">
        <div className="absolute inset-0">
          <Image
            src="/placeholder.svg?height=400&width=800"
            alt="Abstract background"
            layout="fill"
            objectFit="cover"
            className="opacity-10"
          />
        </div>
        <div className="relative container mx-auto px-4 py-16 sm:py-24">
          <div className="text-center">
            <h1 className="text-2xl font-regular  sm:text-5xl md:text-5xl">
              <span className="block text-white font-bold">Research Paper</span>
              <span className="block text-primary-foreground font-mono">Search Engine</span>
            </h1>
            <p className="mt-3 max-w-xl mx-auto text-base text-primary-foreground sm:text-lg md:mt-5 md:text-xl">
              Discover cutting-edge research papers with ease. Enter prompt to start your academic journey.
            </p>
            <div className="mt-10 max-w-5xl mx-auto">
              <SearchBar
                searchQuery={searchQuery}
                onSearchChange={setSearchQuery}
                onSearch={handleSearch}
                loading={loading}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        {error && (
          <div className="text-destructive text-center mb-8">{error}</div>
        )}

        {papers.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold mb-4">Search Results</h2>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {papers.map((paper) => (
                <PaperCard key={paper.id} paper={paper} />
              ))}
            </div>
          </div>
        )}

        {papers.length === 0 && !loading && !error && (
          <div className="text-center text-muted-foreground">
            <BookOpen className="mx-auto h-12 w-12 mb-4" />
            <p>No papers found. Try searching for some keywords.</p>
          </div>
        )}


      </div>
    </main>
  );
}