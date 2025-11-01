import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, AlertCircle } from "lucide-react";
import RiskMeter from "./RiskMeter.jsx";
import { chatAPI } from "../services/api.js";

const ChatWindow = ({ onClose }) => {
  const [messages, setMessages] = useState([
    {
      from: "bot",
      text: "👋 Hi! I'm Coach Carter, your AI fitness assistant. I can help you create workout plans, analyze exercise safety, and provide training advice. What would you like to know?",
    },
  ]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState("in-depth");
  const [loading, setLoading] = useState(false);
  const [connected, setConnected] = useState(false);
  const [userId] = useState(`user_${Math.random().toString(36).substr(2, 9)}`);
  const chatEndRef = useRef(null);

  // Check backend connection on mount
  useEffect(() => {
    const checkConnection = async () => {
      const health = await chatAPI.healthCheck();
      if (health) {
        setConnected(true);
        setMessages(prev => [...prev, {
          from: "bot",
          text: "✅ Connected to Coach Carter backend! Ready to help you with your fitness goals.",
        }]);
      } else {
        setMessages(prev => [...prev, {
          from: "bot",
          text: "❌ Cannot reach Coach Carter backend. Make sure the backend server is running on port 8000!",
        }]);
      }
    };
    checkConnection();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !connected) return;

    // Add user message
    const userMessage = { from: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      // Call real backend
      const response = await chatAPI.sendQuery(input, userId, mode);

      // Add AI response with risk scores and YouTube links
      setMessages((prev) => [
        ...prev,
        {
          from: "bot",
          text: response.response_text,
          riskScores: response.risk_scores,
          youtubeLinks: response.youtube_links,
        },
      ]);
    } catch (error) {
      // Error handling
      setMessages((prev) => [
        ...prev,
        {
          from: "bot",
          text: `❌ Error: ${error.message}. Please try again.`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-[#0b1622]/95 text-white flex flex-col z-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-4 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-blue-700 rounded-full flex items-center justify-center">
            <Bot size={18} />
          </div>
          <div>
            <p className="font-semibold text-white text-lg">CoachCarter</p>
            <p className={`text-xs ${connected ? 'text-green-200' : 'text-red-200'}`}>
              {connected ? '✅ Online' : '❌ Offline'}
            </p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="text-white text-xl hover:opacity-80 transition"
        >
          ✕
        </button>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, i) => (
          <div key={i}>
            {/* Message */}
            <div
              className={`flex ${
                msg.from === "user" ? "justify-end" : "justify-start"
              } mb-2`}
            >
              <div
                className={`px-4 py-2 rounded-2xl max-w-[75%] whitespace-pre-wrap ${
                  msg.from === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-800 text-gray-100"
                }`}
              >
                {msg.from === "bot" && <Bot className="inline mr-2" size={14} />}
                {msg.text}
              </div>
            </div>

            {/* Risk Scores */}
            {msg.riskScores && msg.riskScores.length > 0 && (
              <div className="ml-0 mt-3 mb-4">
                <p className="text-xs text-gray-400 mb-2">🔍 Safety Analysis:</p>
                {msg.riskScores.map((score, idx) => (
                  <RiskMeter
                    key={idx}
                    exercise={score.exercise}
                    risk={score.risk}
                    effectiveness={score.effectiveness}
                  />
                ))}
              </div>
            )}

            {/* YouTube Links */}
            {msg.youtubeLinks && msg.youtubeLinks.length > 0 && (
              <div className="ml-0 mt-3 mb-4">
                <p className="text-xs text-gray-400 mb-2">📺 Tutorial Videos:</p>
                <div className="space-y-2">
                  {msg.youtubeLinks.map((link, idx) => (
                    <a
                      key={idx}
                      href={link.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block text-blue-400 text-sm hover:underline bg-gray-700 p-2 rounded"
                    >
                      ▶️ {link.exercise}
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}

        <div ref={chatEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-700 bg-[#111b27] space-y-3">
        {/* Mode Selector */}
        <div className="flex items-center gap-2">
          <label className="text-xs text-gray-400">Mode:</label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            disabled={loading}
            className="bg-gray-800 text-white text-xs px-2 py-1 rounded border border-gray-600 outline-none"
          >
            <option value="quick-tip">💨 Quick Tip</option>
            <option value="in-depth">📋 In-Depth Plan</option>
          </select>
        </div>

        {/* Input + Send */}
        <div className="flex items-center gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !loading && handleSend()}
            placeholder="Ask about fitness, training, or recovery..."
            disabled={!connected || loading}
            className="flex-1 bg-gray-800 text-sm text-white placeholder-gray-500 outline-none px-3 py-2 rounded border border-gray-600 disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={!connected || loading}
            className="bg-gradient-to-r from-blue-500 to-cyan-500 p-3 rounded-full hover:opacity-90 disabled:opacity-50 transition"
          >
            <Send size={18} />
          </button>
        </div>

        {!connected && (
          <div className="flex items-center gap-2 text-red-400 text-xs">
            <AlertCircle size={14} />
            Backend not connected. Start the server on port 8000.
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatWindow;
