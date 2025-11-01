import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";

const App = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 text-gray-900 font-sans relative overflow-hidden">

      {/* Navbar */}
      <header className="flex justify-between items-center px-10 py-5 bg-gray-900 text-white shadow-lg">
        <div className="flex items-center gap-2 text-xl font-semibold">
          <div className="bg-blue-600 rounded-md p-2">🏋️</div>
          CoachCarter
        </div>
        <button className="bg-gradient-to-r from-blue-500 to-cyan-500 px-5 py-2 rounded-lg text-sm font-medium hover:opacity-90">
          Join Now
        </button>
      </header>

      {/* Hero Section (Chatbot Icon is now functional) */}
      <section className="flex flex-col items-center justify-center text-center px-10 py-32 max-w-7xl mx-auto space-y-8">
        <button
          onClick={() => setIsChatOpen(true)}
          className="bg-gradient-to-r from-blue-500 to-cyan-400 p-14 rounded-full shadow-2xl text-7xl hover:scale-110 transition-transform duration-300"
        >
          💬
        </button>

        <h1 className="text-5xl font-extrabold leading-tight">
          Meet{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">
            CoachCarter
          </span>
        </h1>

        <p className="text-gray-600 text-lg max-w-2xl">
          Hey Champ! Coach Carter’s Ready When You Are 💪.Tap the chat icon above to begin your journey!
        </p>
      </section>

      {/* Fullscreen Chat Window */}
      {isChatOpen && <ChatWindow onClose={() => setIsChatOpen(false)} />}
    </div>
  );
};

export default App;
