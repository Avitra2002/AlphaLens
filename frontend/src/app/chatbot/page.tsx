'use client'
import { useState } from 'react'

export default function ChatbotPage() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState<string | null>(null)

  const handleAsk = () => {
    // Simulated response
    setResponse("Emerging markets in 2025 are expected to face moderate inflation...");
  }

  return (
    <section className="space-y-6">
      <h1 className="text-3xl font-bold">🤖 Chat with AlphaLens</h1>
      <p className="text-gray-600">Ask about investment outlook, sectors, or firms.</p>

      <div className="bg-white p-6 rounded-xl shadow space-y-4">
        <input
          type="text"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-3 border rounded"
        />
        <button
          onClick={handleAsk}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Ask
        </button>

        {response && (
          <div className="p-4 bg-gray-100 rounded text-sm">
            <b>Response:</b> {response}
          </div>
        )}
      </div>
    </section>
  )
}
