import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, AlertCircle, Plus } from "lucide-react";
import RiskMeter from "./RiskMeter.jsx";
import { chatAPI } from "../services/api.js";
import axios from "axios";

// Sport display names
const sportDisplayNames = {
  'football': '⚽ Football (Soccer)',
  'cricket': '🏏 Cricket',
  'basketball': '🏀 Basketball',
  'field_hockey': '🏑 Field Hockey',
  'tennis': '🎾 Tennis',
  'volleyball': '🏐 Volleyball',
  'table_tennis': '🏓 Table Tennis (Ping Pong)',
  'baseball': '⚾ Baseball',
  'rugby': '🏈 Rugby (Union & League)',
  'golf': '⛳ Golf',
  'motorsports': '🏎️ Formula 1 / Motorsports',
  'boxing': '🥊 Boxing',
  'athletics': '🏃 Athletics (Track & Field)',
  'badminton': '🏸 Badminton',
  'swimming': '🏊 Swimming',
  'mma': '🥋 Mixed Martial Arts (MMA)',
  'gymnastics': '🤸 Gymnastics'
};

const SPORTS = Object.keys(sportDisplayNames);

const GOALS = [
  'strength', 'endurance', 'speed', 'agility', 'flexibility',
  'power', 'muscle_gain', 'fat_loss', 'injury_recovery'
];

const CHAT_STAGES = {
  GREETING: 'greeting',
  NAME: 'name',
  AGE: 'age',
  GENDER: 'gender',
  HEIGHT: 'height',
  WEIGHT: 'weight',
  HEALTH: 'health',
  SPORT: 'sport',
  CUSTOM_SPORT: 'custom_sport',
  EXPERIENCE: 'experience',
  DURATION: 'duration',
  GOALS: 'goals',
  CONFIRM: 'confirm',
  GENERATING: 'generating',
  CHAT: 'chat'
};

const ChatWindow = ({ onClose }) => {
  const [messages, setMessages] = useState([
    {
      from: "bot",
      text: "👋 Hey there, champ! I'm Coach Carter, your personal AI fitness coach! Let's set up your profile to create your perfect training program. What's your name?",
    },
  ]);
  
  const [input, setInput] = useState("");
  const [mode, setMode] = useState("in-depth");
  const [loading, setLoading] = useState(false);
  const [connected, setConnected] = useState(false);
  const [userId] = useState(`user_${Math.random().toString(36).substr(2, 9)}`);
  const [chatStage, setChatStage] = useState(CHAT_STAGES.NAME);
  
  const [profile, setProfile] = useState({
    name: '',
    age: '',
    gender: '',
    height_cm: '',
    weight_kg: '',
    injuries: [],
    sport: '',
    experience_years: '',
    duration_weeks: 12,
    goals: [],
    sessions_per_week: 5
  });
  
  const chatEndRef = useRef(null);

  useEffect(() => {
    const checkConnection = async () => {
      const health = await chatAPI.healthCheck();
      setConnected(health !== null);
    };
    checkConnection();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addBotMessage = (text, options = null) => {
    setMessages(prev => [...prev, { from: "bot", text, options }]);
  };

  const handleProfileAnswer = (answer) => {
    let nextStage = chatStage;
    let newProfile = { ...profile };

    switch (chatStage) {
      case CHAT_STAGES.NAME:
        newProfile.name = answer;
        nextStage = CHAT_STAGES.AGE;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage("Nice to meet you, " + answer + "! 🤝 How old are you?");
        break;

      case CHAT_STAGES.AGE:
        const age = parseInt(answer);
        if (isNaN(age) || age < 10 || age > 100) {
          addBotMessage("Please enter a valid age (10-100)");
          return;
        }
        newProfile.age = age;
        nextStage = CHAT_STAGES.GENDER;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage("Got it! Are you male, female, or other?", {
          type: "buttons",
          options: ["Male", "Female", "Other"]
        });
        break;

      case CHAT_STAGES.GENDER:
        newProfile.gender = answer.toLowerCase();
        nextStage = CHAT_STAGES.HEIGHT;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage("Perfect! What's your height in cm? (e.g., 180)");
        break;

      case CHAT_STAGES.HEIGHT:
        const height = parseFloat(answer);
        if (isNaN(height) || height < 100 || height > 250) {
          addBotMessage("Please enter a valid height (100-250 cm)");
          return;
        }
        newProfile.height_cm = height;
        nextStage = CHAT_STAGES.WEIGHT;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage("Great! What's your current weight in kg?");
        break;

      case CHAT_STAGES.WEIGHT:
        const weight = parseFloat(answer);
        if (isNaN(weight) || weight < 30 || weight > 300) {
          addBotMessage("Please enter a valid weight (30-300 kg)");
          return;
        }
        newProfile.weight_kg = weight;
        nextStage = CHAT_STAGES.HEALTH;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage("Any past injuries or health issues? (e.g., 'lower back pain, knee injury' or 'none')");
        break;

      case CHAT_STAGES.HEALTH:
        const injuries = answer.toLowerCase() === 'none' 
          ? [] 
          : answer.split(',').map(s => s.trim()).filter(s => s);
        newProfile.injuries = injuries;
        nextStage = CHAT_STAGES.SPORT;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage("What sport are you training for?", {
          type: "buttons",
          options: [...SPORTS.map(s => sportDisplayNames[s]), "➕ Other Sport"]
        });
        break;

      case CHAT_STAGES.SPORT:
        const isPresetSport = SPORTS.some(s => 
          sportDisplayNames[s].includes(answer) || s === answer.toLowerCase()
        );
        
        if (answer === "➕ Other Sport") {
          nextStage = CHAT_STAGES.CUSTOM_SPORT;
          setMessages(prev => [...prev, { from: "user", text: answer }]);
          addBotMessage("Cool! What sport would you like to train for? (Type any sport)");
        } else if (isPresetSport) {
          const sportKey = Object.keys(sportDisplayNames).find(
            key => sportDisplayNames[key] === answer
          ) || answer.toLowerCase();
          newProfile.sport = sportKey;
          nextStage = CHAT_STAGES.EXPERIENCE;
          setMessages(prev => [...prev, { from: "user", text: answer }]);
          addBotMessage(`Excellent! ${answer} is amazing! 🔥 How many years of experience do you have?`);
        } else {
          addBotMessage("Please select from the options or choose '➕ Other Sport'");
          return;
        }
        break;

      case CHAT_STAGES.CUSTOM_SPORT:
        newProfile.sport = answer.toLowerCase().trim();
        nextStage = CHAT_STAGES.EXPERIENCE;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage(`Nice! ${answer} is a great sport! 🔥 How many years of experience do you have?`);
        break;

      case CHAT_STAGES.EXPERIENCE:
        const exp = parseInt(answer);
        if (isNaN(exp) || exp < 0 || exp > 60) {
          addBotMessage("Please enter a valid experience (0-60 years)");
          return;
        }
        newProfile.experience_years = exp;
        nextStage = CHAT_STAGES.DURATION;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage("How many weeks should your training program be? (1-52 weeks)");
        break;

      case CHAT_STAGES.DURATION:
        const duration = parseInt(answer);
        if (isNaN(duration) || duration < 1 || duration > 52) {
          addBotMessage("Please enter 1-52 weeks");
          return;
        }
        newProfile.duration_weeks = duration;
        nextStage = CHAT_STAGES.GOALS;
        setMessages(prev => [...prev, { from: "user", text: answer }]);
        addBotMessage("Perfect! What are your main training goals? (Select one or more)", {
          type: "buttons",
          options: GOALS.map(g => g.replace('_', ' ').charAt(0).toUpperCase() + g.slice(1))
        });
        break;

      case CHAT_STAGES.GOALS:
        if (profile.goals.length === 0 || !newProfile.goals.includes(answer.toLowerCase().replace(' ', '_'))) {
          const goal = answer.toLowerCase().replace(' ', '_');
          newProfile.goals = [...profile.goals, goal];
          setMessages(prev => [...prev, { from: "user", text: answer }]);
          addBotMessage(`Great choice! Select more goals or click "Done"`, {
            type: "buttons",
            options: [...GOALS.filter(g => !newProfile.goals.includes(g)).map(g => g.replace('_', ' ')), "Done"]
          });
        } else if (answer === "Done") {
          nextStage = CHAT_STAGES.CONFIRM;
          setMessages(prev => [...prev, { from: "user", text: "Done" }]);
          
          const summary = `
📋 YOUR PROFILE SUMMARY:
Name: ${newProfile.name}
Age: ${newProfile.age} years
Gender: ${newProfile.gender}
Height: ${newProfile.height_cm} cm
Weight: ${newProfile.weight_kg} kg
Injuries: ${newProfile.injuries.length > 0 ? newProfile.injuries.join(', ') : 'None'}
Sport: ${newProfile.sport}
Experience: ${newProfile.experience_years} years
Program Duration: ${newProfile.duration_weeks} weeks
Goals: ${newProfile.goals.join(', ')}

Ready to generate your personalized training program?`;
          
          addBotMessage(summary, {
            type: "buttons",
            options: ["Yes, Generate Plan!", "Edit Profile"]
          });
        } else {
          return;
        }
        break;

      case CHAT_STAGES.CONFIRM:
        if (answer === "Yes, Generate Plan!") {
          generateTrainingPlan(newProfile);
          nextStage = CHAT_STAGES.GENERATING;
        } else {
          setChatStage(CHAT_STAGES.NAME);
          setProfile({
            name: '',
            age: '',
            gender: '',
            height_cm: '',
            weight_kg: '',
            injuries: [],
            sport: '',
            experience_years: '',
            duration_weeks: 12,
            goals: [],
            sessions_per_week: 5
          });
          setMessages(prev => [...prev, { from: "user", text: "Edit Profile" }]);
          addBotMessage("Let's start over! What's your name?");
          return;
        }
        break;

      default:
        break;
    }

    setProfile(newProfile);
    setChatStage(nextStage);
    setInput("");
  };

  const generateTrainingPlan = async (completeProfile) => {
    setMessages(prev => [...prev, { from: "user", text: "Yes, Generate Plan!" }]);
    addBotMessage("🚀 Generating your personalized training program... This may take a moment!");
    setLoading(true);

    try {
      const profilePayload = {
        user_id: userId,
        ...completeProfile,
        sessions_per_week: 5,
        available_equipment: [],
        dietary_restrictions: []
      };

      await axios.post('http://127.0.0.1:8000/api/profile/create', profilePayload);

      const query = `Create a detailed ${completeProfile.duration_weeks}-week personalized training program for a ${completeProfile.age}-year-old ${completeProfile.sport} athlete with ${completeProfile.experience_years} years of experience. Goals: ${completeProfile.goals.join(', ')}. ${
        completeProfile.injuries.length > 0 ? `Important - avoid exercises that aggravate: ${completeProfile.injuries.join(', ')}` : ''
      } Include specific exercises, drills, duration and frequency of workouts tailored to ${completeProfile.sport}.`;

      const response = await chatAPI.sendQuery(query, userId, "in-depth");

      setMessages(prev => [...prev, {
        from: "bot",
        text: response.response_text,
        riskScores: response.risk_scores,
        youtubeLinks: response.youtube_links
      }]);

      setChatStage(CHAT_STAGES.CHAT);
      setMode("in-depth");
    } catch (error) {
      addBotMessage(`❌ Error generating plan: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRegularChat = async () => {
    if (!input.trim() || !connected) return;

    setMessages(prev => [...prev, { from: "user", text: input }]);
    setInput("");
    setLoading(true);

    try {
      const response = await chatAPI.sendQuery(input, userId, mode);

      setMessages(prev => [...prev, {
        from: "bot",
        text: response.response_text,
        riskScores: response.risk_scores,
        youtubeLinks: response.youtube_links,
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        from: "bot",
        text: `❌ Error: ${error.message}. Please try again.`,
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = () => {
    if (chatStage === CHAT_STAGES.CHAT) {
      handleRegularChat();
    } else {
      handleProfileAnswer(input);
    }
  };

  const handleButtonClick = (option) => {
    setInput(option);
    handleProfileAnswer(option);
  };

  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-black bg-opacity-40 px-2 py-4">
      {/* Chat Card (GLASSMORPHISM + FUNCTIONAL) */}
      <div className="w-full max-w-2xl rounded-3xl shadow-2xl bg-white/80 backdrop-blur-lg border border-blue-100 flex flex-col space-y-3 relative animate-fadeIn h-[90vh] max-h-[90vh]">
        
        {/* Header - Beautiful */}
        <div className="flex items-center gap-3 px-6 pt-4 pb-3 border-b border-blue-100">
          <span className="relative">
            <span className="emoji-pop inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-tr from-blue-400 to-cyan-300 text-2xl shadow">
              💬
            </span>
            <span className={`absolute right-1 bottom-1 block w-3 h-3 rounded-full border-2 border-white ${connected ? "bg-green-400" : "bg-red-400"}`}></span>
          </span>
          <div>
            <span className="font-bold text-xl bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-500">
              CoachCarter
            </span>
            <div className={`text-xs font-medium ml-1 ${connected ? "text-green-500" : "text-red-400"}`}>
              {connected ? "● Online" : "● Offline"}
            </div>
          </div>
          <button
            onClick={onClose}
            className="ml-auto px-4 py-2 rounded-xl bg-red-100 text-red-700 font-semibold hover:bg-red-200 shadow transition"
          >
            Close
          </button>
        </div>

        {/* Chat Messages - Scrollable */}
        <div className="flex-1 overflow-y-auto px-6 space-y-4 pr-2">
          {messages.map((msg, i) => (
            <div key={i}>
              <div className={`flex ${msg.from === "user" ? "justify-end" : "justify-start"} mb-1`}>
                <div className={`px-4 py-2 rounded-2xl max-w-[80%] whitespace-pre-wrap font-medium shadow animate-fadeIn ${
                  msg.from === "user"
                    ? "bg-gradient-to-r from-blue-200 to-blue-400 text-blue-900"
                    : "bg-white/90 text-blue-900 border border-blue-100"
                }`}>
                  {msg.from === "bot" && <Bot className="inline mr-2 text-blue-400" size={16} />}
                  <span className="inline-block align-middle">{msg.text}</span>
                </div>
              </div>

              {/* Button Options */}
              {msg.options?.type === "buttons" && (
                <div className="flex flex-wrap gap-2 ml-0 mb-4">
                  {msg.options.options.map((opt, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleButtonClick(opt)}
                      disabled={loading}
                      className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-3 py-2 rounded-lg disabled:opacity-50 transition"
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              )}

              {/* Risk Scores */}
              {msg.riskScores && msg.riskScores.length > 0 && (
                <div className="ml-0 mt-3 mb-4">
                  <p className="text-xs text-blue-500 mb-2">🔍 Safety Analysis:</p>
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
                  <p className="text-xs text-blue-500 mb-2">📺 Tutorial Videos:</p>
                  <div className="space-y-2">
                    {msg.youtubeLinks.map((link, idx) => (
                      <a
                        key={idx}
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block text-blue-600 text-sm hover:underline bg-blue-50 p-2 rounded"
                      >
                        ▶ {link.exercise}
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Input Area - Beautiful */}
        <div className="px-6 pb-4 border-t border-blue-100 bg-white/50 space-y-2 rounded-b-3xl">
          {/* Mode Selector */}
          {chatStage === CHAT_STAGES.CHAT && (
            <div className="flex items-center gap-2">
              <label className="text-xs text-gray-600">Mode:</label>
              <select
                value={mode}
                onChange={(e) => setMode(e.target.value)}
                disabled={loading}
                className="bg-blue-50 text-blue-900 text-xs px-2 py-1 rounded border border-blue-200 outline-none"
              >
                <option value="quick-tip">💨 Quick Tip</option>
                <option value="in-depth">📋 In-Depth Plan</option>
              </select>
            </div>
          )}

          {/* Input + Send */}
          <div className="flex items-center gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !loading && handleSend()}
              placeholder={chatStage === CHAT_STAGES.CHAT ? "Ask about your training..." : "Type your answer..."}
              disabled={!connected || loading}
              className="flex-1 bg-blue-50 text-sm text-blue-900 placeholder-blue-300 outline-none px-3 py-2 rounded border border-blue-200 focus:ring-2 focus:ring-cyan-300 disabled:opacity-60 shadow"
            />
            <button
              onClick={handleSend}
              disabled={!connected || loading || !input.trim()}
              className="flying-btn bg-gradient-to-r from-blue-400 to-cyan-400 p-3 rounded-full hover:scale-105 text-white font-bold shadow hover:shadow-xl transition disabled:opacity-50"
            >
              <Send size={18} />
            </button>
          </div>

          {!connected && (
            <div className="flex items-center gap-2 text-red-500 text-xs">
              <AlertCircle size={14} />
              Backend not connected. Start the server on port 8000.
            </div>
          )}
        </div>
      </div>

      {/* Animations */}
      <style>
        {`
        @keyframes pop {
          0%,100% { transform: scale(1);}
          40% { transform: scale(1.13);}
          60% { transform: scale(0.96);}
        }
        .emoji-pop {
          animation: pop 1.8s cubic-bezier(.68,-0.55,.27,1.55) infinite;
        }
        @keyframes fadeIn {
          0% { opacity: 0; transform: translateY(18px) scale(.98);}
          70% { opacity: 1; transform: translateY(0) scale(1);}
          100% { opacity: 1; }
        }
        .animate-fadeIn {
          animation: fadeIn .8s cubic-bezier(.52,.2,.27,.98) both;
        }
        @keyframes fly {
          0% { transform: translateY(0) scale(1);}
          30% { transform: translateY(-10px) scale(1.09);}
          55% { transform: translateY(0) scale(1.02);}
          70% { transform: translateY(8px) scale(1);}
          100% { transform: translateY(0) scale(1);}
        }
        .flying-btn {
          animation: fly 2.1s cubic-bezier(.68,-0.55,.27,1.55) infinite;
          will-change: transform;
        }
        `}
      </style>
    </div>
  );
};

export default ChatWindow;
