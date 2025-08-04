'use client';
import { JSX, useState } from 'react';
import { MessageSquare, Send, Trash2, Bot, User, AlertCircle } from 'lucide-react';
import RelationshipGraph from '../../components/RelationshipGraph';

interface Relationship {
  entity1: string;
  entity2: string;
  relationship_type: string;
  confidence: number;
  context: string;
}

interface GraphData {
  relationships: Relationship[];
  summary: string;
}

interface QueryResponse {
  intent: string;
  company: string;
  data: string | GraphData;
  data_type: 'text' | 'graph';
  success: boolean;
  error?: string;
}

interface ChatMessage {
  type: 'user' | 'assistant' | 'error';
  content: string | QueryResponse;
  timestamp: Date;
}

export default function ChatbotPage() {
  const [query, setQuery] = useState<string>('');
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

  const handleAsk = async (): Promise<void> => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    // Add user message to chat history
    const userMessage: ChatMessage = { type: 'user' as const, content: query, timestamp: new Date() };
    setChatHistory(prev => [...prev, userMessage]);

    try {
      const response = await fetch('http://localhost:4000/api/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: QueryResponse = await response.json();
      
      if (!data.success) {
        throw new Error('Query failed - please try again');
      }

      setResponse(data);
      
      // Add assistant response to chat history
      const assistantMessage: ChatMessage = { 
        type: 'assistant' as const, 
        content: data, 
        timestamp: new Date() 
      };
      setChatHistory(prev => [...prev, assistantMessage]);

    } catch (err) {
      console.error('Error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      
      // Add error message to chat history
      const errorChatMessage: ChatMessage = { 
        type: 'error' as const, 
        content: `Error: ${errorMessage}`, 
        timestamp: new Date() 
      };
      setChatHistory(prev => [...prev, errorChatMessage]);
    } finally {
      setLoading(false);
      setQuery(''); // Clear input after sending
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  const clearChat = (): void => {
    setChatHistory([]);
    setResponse(null);
    setError(null);
  };

  const formatText = (text: string): JSX.Element[] => {
    // Simple text formatting - convert **text** to bold and handle line breaks
    return text
      .split('\n')
      .map((line, index) => (
        <div key={index} className="mb-2">
          {line.split(/(\*\*.*?\*\*)/).map((part, partIndex) => {
            if (part.startsWith('**') && part.endsWith('**')) {
              return <strong key={partIndex}>{part.slice(2, -2)}</strong>;
            }
            return part;
          })}
        </div>
      ));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex flex-col">
      {/* Fixed Header - positioned below nav */}
      <div className="bg-white shadow-sm border-b fixed left-0 right-0 z-10" style={{ top: '64px' }}>
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <MessageSquare className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AlphaLens Chat</h1>
                <p className="text-sm text-gray-600">Ask about investment outlook, sectors, or firms</p>
              </div>
            </div>
            {chatHistory.length > 0 && (
              <button
                onClick={clearChat}
                className="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg transition-colors"
              >
                <Trash2 className="w-4 h-4" />
                Clear Chat
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 max-w-7xl mx-auto w-full px-6 flex flex-col" style={{ paddingTop: '164px', paddingBottom: '120px' }}>
        <div className="flex-1 bg-white rounded-xl shadow-sm border overflow-hidden flex flex-col">
          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-6">
            {chatHistory.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <div className="bg-blue-50 p-4 rounded-full mb-4">
                  <Bot className="w-12 h-12 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Welcome to AlphaLens Chat</h3>
                <p className="text-gray-600 mb-6 max-w-md">
                  Start a conversation by asking about company financials, investment risks, or business relationships.
                </p>
                <div className="bg-gray-50 rounded-lg p-4 max-w-md">
                  <p className="text-sm text-gray-700 font-medium mb-2">Try asking:</p>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• "What are the key risks facing Apple Inc.?"</li>
                    <li>• "Show me Apple's business relationships"</li>
                    <li>• "What's the investment outlook for Tesla?"</li>
                  </ul>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {chatHistory.map((message, index) => (
                  <div key={index} className={`flex gap-3 ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                    {/* Avatar */}
                    <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                      message.type === 'user' 
                        ? 'bg-blue-600' 
                        : message.type === 'error'
                        ? 'bg-red-500'
                        : 'bg-gray-600'
                    }`}>
                      {message.type === 'user' ? (
                        <User className="w-4 h-4 text-white" />
                      ) : message.type === 'error' ? (
                        <AlertCircle className="w-4 h-4 text-white" />
                      ) : (
                        <Bot className="w-4 h-4 text-white" />
                      )}
                    </div>

                    {/* Message Content */}
                    <div className={`flex-1 max-w-3xl ${message.type === 'user' ? 'text-right' : 'text-left'}`}>
                      <div className={`inline-block p-4 rounded-xl ${
                        message.type === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : message.type === 'error'
                          ? 'bg-red-50 text-red-800 border border-red-200'
                          : 'bg-gray-50 text-gray-900'
                      }`}>
                        {message.type === 'user' ? (
                          <div className="whitespace-pre-wrap">{message.content as string}</div>
                        ) : message.type === 'error' ? (
                          <div className="flex items-start gap-2">
                            <AlertCircle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                            <div>{message.content as string}</div>
                          </div>
                        ) : (
                          <div>
                            <div className="mb-3 pb-2 border-b border-gray-200">
                              <span className="text-xs font-semibold text-blue-600 bg-blue-100 px-2 py-1 rounded">
                                {(message.content as QueryResponse).intent}
                              </span>
                              <span className="text-xs font-semibold text-gray-600 bg-gray-200 px-2 py-1 rounded ml-2">
                                {(message.content as QueryResponse).company}
                              </span>
                            </div>
                            
                            {(message.content as QueryResponse).data_type === 'text' ? (
                              <div className="text-sm">
                                {formatText((message.content as QueryResponse).data as string)}
                              </div>
                            ) : (message.content as QueryResponse).data_type === 'graph' ? (
                              <div>
                                <div className="mb-4">
                                  <RelationshipGraph data={(message.content as QueryResponse).data as GraphData} />
                                </div>
                                {((message.content as QueryResponse).data as GraphData).summary && (
                                  <div className="text-sm p-3 bg-white rounded-lg border">
                                    <h4 className="font-medium text-gray-900 mb-2">Summary:</h4>
                                    {formatText(((message.content as QueryResponse).data as GraphData).summary)}
                                  </div>
                                )}
                              </div>
                            ) : null}
                          </div>
                        )}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                ))}
                
                {/* Loading indicator */}
                {loading && (
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="inline-block p-4 rounded-xl bg-gray-50">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          <span className="text-sm text-gray-600 ml-2">Thinking...</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

        </div>
      </div>

      {/* Input Section at Bottom */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex gap-3">
            <textarea
              rows={1}
              placeholder="Ask a question about company financials, risks, or relationships..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none bg-white"
              disabled={loading}
              style={{ minHeight: '48px', maxHeight: '120px' }}
              onInput={(e) => {
                const target = e.target as HTMLTextAreaElement;
                target.style.height = 'auto';
                target.style.height = Math.min(target.scrollHeight, 120) + 'px';
              }}
            />
            <button
              onClick={handleAsk}
              disabled={loading || !query.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white px-4 py-3 rounded-lg transition-colors flex items-center gap-2 self-end"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Processing
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  Send
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}