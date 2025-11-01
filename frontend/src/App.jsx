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
        <button
          onClick={() => setIsChatOpen(true)}
          className="bg-gradient-to-r from-blue-500 to-cyan-500 px-5 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition"
        >
          Chat Now
        </button>
      </header>

      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center text-center px-10 py-32 max-w-7xl mx-auto space-y-8">
        {/* Chat Button */}
        <button
          onClick={() => setIsChatOpen(true)}
          className="bg-gradient-to-r from-blue-500 to-cyan-400 p-14 rounded-full shadow-2xl text-7xl hover:scale-110 transition-transform duration-300 cursor-pointer"
        >
          💬
        </button>

        {/* Main Heading */}
        <h1 className="text-5xl font-extrabold leading-tight">
          Meet{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">
            CoachCarter
          </span>
        </h1>

        {/* Subheading */}
        <p className="text-gray-600 text-lg max-w-2xl">
          Your AI fitness coach powered by cutting-edge machine learning. Get personalized workout plans, safety analysis, and video tutorials tailored to your sport and goals. 💪
        </p>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl mt-12">
          {/* Feature 1 */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
            <div className="text-4xl mb-3">🎯</div>
            <h3 className="text-xl font-semibold mb-2">Personalized Plans</h3>
            <p className="text-gray-600 text-sm">
              Custom training programs based on your sport, age, weight, goals, and fitness level.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
            <div className="text-4xl mb-3">🛡️</div>
            <h3 className="text-xl font-semibold mb-2">Safety First</h3>
            <p className="text-gray-600 text-sm">
              Injury-aware exercise recommendations that adapt to your health history.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
            <div className="text-4xl mb-3">📺</div>
            <h3 className="text-xl font-semibold mb-2">Video Tutorials</h3>
            <p className="text-gray-600 text-sm">
              YouTube tutorial links for every exercise with proper form guidance.
            </p>
          </div>
        </div>

        {/* CTA Button */}
        <button
          onClick={() => setIsChatOpen(true)}
          className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition mt-8"
        >
          Start Your Journey →
        </button>
      </section>

      {/* Sports Supported Section */}
      <section className="bg-white py-16 px-10">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">
            Supported Sports & Beyond
          </h2>
          <p className="text-gray-600 text-center mb-8">
            We support 17 professional sports including football, cricket, basketball, and more. Plus, any custom sport you want!
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div className="p-4 bg-gray-50 rounded-lg">⚽ Football</div>
            <div className="p-4 bg-gray-50 rounded-lg">🏏 Cricket</div>
            <div className="p-4 bg-gray-50 rounded-lg">🏀 Basketball</div>
            <div className="p-4 bg-gray-50 rounded-lg">🎾 Tennis</div>
            <div className="p-4 bg-gray-50 rounded-lg">🏊 Swimming</div>
            <div className="p-4 bg-gray-50 rounded-lg">🥊 Boxing</div>
            <div className="p-4 bg-gray-50 rounded-lg">🏃 Athletics</div>
            <div className="p-4 bg-gray-50 rounded-lg">+ 10 More</div>
          </div>
        </div>
      </section>

      {/* Chatbot Modal */}
      {isChatOpen && <ChatWindow onClose={() => setIsChatOpen(false)} />}
    </div>
  );
};

export default App;
