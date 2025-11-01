import React from "react";

const ChatMessage = ({ sender, text }) => {
  const isBot = sender === "bot";
  return (
    <div className={`flex ${isBot ? "justify-start" : "justify-end"} mb-3`}>
      <div
        className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm ${
          isBot
            ? "bg-gray-800 text-gray-100 rounded-bl-none"
            : "bg-blue-600 text-white rounded-br-none"
        }`}
      >
        {text}
      </div>
    </div>
  );
};

export default ChatMessage;
