import React, { useState, useRef, useEffect } from "react";
import { Send, Bot } from "lucide-react";
import RiskMeter from "./RiskMeter.jsx";

// Helper to convert text-based risk levels → numbers
const interpretRiskFromText = (text) => {
  const lower = text.toLowerCase();
  if (lower.includes("low")) return 2;
  if (lower.includes("moderate") || lower.includes("medium")) return 5;
  if (lower.includes("high")) return 8;
  if (lower.includes("critical") || lower.includes("severe")) return 10;
  return null; // default if no keyword found
};

const ChatWindow = ({ onClose }) => {
  const [messages, setMessages] = useState([
    {
      from: "bot",
      text: "Hi! I'm Coach Carter, your fitness assistant. I can help with workouts, nutrition, and training advice. What would you like to know?",
    },
  ]);
  const [input, setInput] = useState("");
  const [riskScore, setRiskScore] = useState(null); // 🧠 risk state
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = { from: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // ✨ Simulated AI reply (replace with real backend call later)
    setTimeout(() => {
      let botReply = "";
      let newRisk = null;

      // Basic logic to simulate context detection
      if (input.toLowerCase().includes("injury")) {
        botReply =
          "It sounds like you’ve experienced an injury. That’s a *high risk* situation — focus on recovery and mobility before intense workouts.";
        newRisk = 8;
      } else if (input.toLowerCase().includes("tired")) {
        botReply =
          "You might be moderately fatigued. Let’s take a rest day or light session — your risk is *medium* right now.";
        newRisk = 5;
      } else if (
        input.toLowerCase().includes("ready") ||
        input.toLowerCase().includes("start")
      ) {
        botReply =
          "Awesome! You’re in a *low risk* zone — let’s begin with a warm-up and good hydration.";
        newRisk = 2;
      } else if (input.toLowerCase().includes("pain")) {
        botReply =
          "Pain isn’t something to push through. This could be a *critical risk* situation — consult a physiotherapist before continuing.";
        newRisk = 10;
      } else {
        botReply =
          "Got it! I’ll prepare a personalized plan. Your current risk level seems *moderate*. Tell me your main goal — strength, endurance, or flexibility?";
        newRisk = 5;
      }

      // Push bot reply to chat
      setMessages((prev) => [...prev, { from: "bot", text: botReply }]);

      // Detect risk level (from text OR pre-set numeric value)
      const interpretedRisk = interpretRiskFromText(botReply) ?? newRisk;
      setRiskScore(interpretedRisk);
    }, 1000);
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
            <p className="text-xs text-green-200">Online now</p>
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
      <div className="flex-1 overflow-y-auto p-6 space-y-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.from === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-[75%] ${
                msg.from === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-800 text-gray-100"
              }`}
            >
              {msg.from === "bot" && <Bot className="inline mr-2" size={14} />}
              {msg.text}
            </div>
          </div>
        ))}

        {/* 🧩 Risk Meter */}
        {riskScore !== null && (
          <div className="mt-6">
            <RiskMeter label="Workout Risk Level" score={riskScore} />
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-700 flex items-center bg-[#111b27]">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask about fitness, training, or recovery..."
          className="flex-1 bg-transparent text-sm text-white placeholder-gray-400 outline-none"
        />
        <button
          onClick={handleSend}
          className="ml-3 bg-gradient-to-r from-blue-500 to-cyan-500 p-3 rounded-full hover:opacity-90"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
