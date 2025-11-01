import React, { useState, useEffect, useRef } from "react";
import RiskMeter from "./RiskMeter";

const ChatWindow = ({ onClose }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [showRisk, setShowRisk] = useState(false);
  const [riskScore, setRiskScore] = useState(0);
  const chatEndRef = useRef(null);

  // Scroll to bottom on new message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (input.trim() === "") return;

    const userMsg = { text: input, from: "user" };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    // --- Dummy AI behavior (replace with your teammate’s logic) ---
    setTimeout(() => {
      if (input.toLowerCase().includes("risk")) {
        // If AI detects a prompt related to "risk"
        setShowRisk(true);
        const randomScore = Math.floor(Math.random() * 10) + 1;
        setRiskScore(randomScore);
        setMessages((prev) => [
          ...prev,
          { text: "Here's your current risk analysis:", from: "bot" },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { text: "Got it! Let's keep going 💪", from: "bot" },
        ]);
      }
    }, 500);
  };

  return (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-95 flex flex-col z-50 text-white p-4">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-gray-700 pb-3">
        <h2 className="text-lg font-bold">CoachCarter AI</h2>
        <button
          onClick={onClose}
          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg"
        >
          ✕
        </button>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[80%] p-3 rounded-xl ${
              msg.from === "user"
                ? "bg-blue-600 self-end ml-auto"
                : "bg-gray-800 text-gray-100"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {/* Show RiskMeter if needed */}
        {showRisk && (
          <div className="mt-4">
            <RiskMeter label="Injury Risk Score" score={riskScore} />
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input Area */}
      <div className="flex p-3 border-t border-gray-700">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your message..."
          className="flex-1 bg-gray-800 p-3 rounded-lg outline-none text-white"
        />
        <button
          onClick={handleSend}
          className="ml-3 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
