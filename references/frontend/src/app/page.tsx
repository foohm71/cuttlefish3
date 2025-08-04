"use client";
import React, { useState, useEffect } from "react";

// Use environment variable for API URL, fallback to localhost for local dev
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type SimilarResult = {
  id: string | number;
  score: number;
  payload: {
    key?: string;
    title?: string;
    description?: string;
    [key: string]: unknown;
  };
};

type SimilarResponse = {
  results: SimilarResult[];
};

type RagResponse = {
  answer: string;
  context: SimilarResult[];
};

export default function Home() {
  const [openaiKey, setOpenaiKey] = useState("");
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<SimilarResponse | RagResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load OpenAI key from localStorage on mount
  useEffect(() => {
    const storedKey = localStorage.getItem("openai_api_key") || "";
    setOpenaiKey(storedKey);
  }, []);

  // Save OpenAI key to localStorage when it changes
  useEffect(() => {
    if (openaiKey) {
      localStorage.setItem("openai_api_key", openaiKey);
    }
  }, [openaiKey]);

  const handleSubmit = async (endpoint: "similar" | "rag") => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, openai_api_key: openaiKey }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Unknown error");
      }
      const data = await res.json();
      setResult(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message || "Request failed");
      } else {
        setError("Request failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-50">
      <div className="w-full max-w-xl bg-white rounded shadow p-6 space-y-6">
        <img
          src="/cuttlefish.svg"
          alt="Cuttlefish logo"
          className="mx-auto mb-4 w-28 h-28 object-contain drop-shadow"
        />
        <h1 className="text-2xl font-bold mb-2">Cuttlefish Bug Similarity Search and RAG</h1>
        <div>
          <label className="block font-medium mb-1">OpenAI API Key</label>
          <input
            type="password"
            className="w-full border rounded px-3 py-2"
            value={openaiKey}
            onChange={e => setOpenaiKey(e.target.value)}
            placeholder="sk-..."
            autoComplete="off"
          />
        </div>
        <div>
          <label className="block font-medium mb-1">Query</label>
          <textarea
            className="w-full border rounded px-3 py-2 min-h-[100px]"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Enter your query here..."
          />
        </div>
        <div className="flex gap-4">
          <button
            className="flex-1 bg-blue-600 text-white rounded px-4 py-2 font-semibold hover:bg-blue-700 disabled:opacity-50"
            onClick={() => handleSubmit("similar")}
            disabled={loading || !openaiKey || !query}
          >
            Similarity
          </button>
          <button
            className="flex-1 bg-green-600 text-white rounded px-4 py-2 font-semibold hover:bg-green-700 disabled:opacity-50"
            onClick={() => handleSubmit("rag")}
            disabled={loading || !openaiKey || !query}
          >
            RAG
          </button>
        </div>
        {loading && <div className="text-center text-gray-500">Loading...</div>}
        {error && <div className="text-center text-red-600">{error}</div>}
        {result && (
          <div className="mt-4">
            <h2 className="font-bold mb-2">Results</h2>
            {"results" in result ? (
              <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-200 rounded">
                  <thead>
                    <tr>
                      <th className="px-3 py-2 border-b">Score</th>
                      <th className="px-3 py-2 border-b">Key</th>
                      <th className="px-3 py-2 border-b">Title</th>
                      <th className="px-3 py-2 border-b">Description</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.results.map((item, idx) => (
                      <tr key={item.id || idx} className="hover:bg-gray-50">
                        <td className="px-3 py-2 border-b text-right">{item.score.toFixed(4)}</td>
                        <td className="px-3 py-2 border-b">{item.payload?.key || item.id}</td>
                        <td className="px-3 py-2 border-b">{item.payload?.title || ""}</td>
                        <td className="px-3 py-2 border-b max-w-xs truncate" title={item.payload?.description as string}>{item.payload?.description || ""}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : "answer" in result && "context" in result ? (
              <>
                <div className="mb-6">
                  <h3 className="font-semibold mb-1">Answer</h3>
                  <div className="bg-green-50 border border-green-200 rounded p-3 text-gray-800 whitespace-pre-line">
                    {result.answer}
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Bugs</h3>
                  <div className="overflow-x-auto">
                    <table className="min-w-full bg-white border border-gray-200 rounded">
                      <thead>
                        <tr>
                          <th className="px-3 py-2 border-b">Key</th>
                          <th className="px-3 py-2 border-b">Title</th>
                          <th className="px-3 py-2 border-b">Description</th>
                        </tr>
                      </thead>
                      <tbody>
                        {result.context.map((item, idx) => (
                          <tr key={item.id || idx} className="hover:bg-gray-50">
                            <td className="px-3 py-2 border-b">{item.payload?.key || item.id}</td>
                            <td className="px-3 py-2 border-b">{item.payload?.title || ""}</td>
                            <td className="px-3 py-2 border-b max-w-xs truncate" title={item.payload?.description as string}>{item.payload?.description || ""}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            ) : (
              <pre className="bg-gray-100 p-2 rounded text-sm overflow-x-auto">
                {JSON.stringify(result, null, 2)}
              </pre>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
