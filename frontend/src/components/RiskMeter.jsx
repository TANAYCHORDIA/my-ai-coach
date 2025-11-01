import React, { useEffect, useState } from 'react';

const RiskMeter = ({ exercise, risk, effectiveness }) => {
  // Smooth animated bars
  const [animatedRisk, setAnimatedRisk] = useState(0);
  const [animatedEffect, setAnimatedEffect] = useState(0);

  useEffect(() => {
    setTimeout(() => setAnimatedRisk(risk), 100);
    setTimeout(() => setAnimatedEffect(effectiveness), 200);
  }, [risk, effectiveness]);

  const getRiskGradient = (value) => {
    if (value >= 7) return 'bg-gradient-to-r from-yellow-400 via-orange-400 to-red-500';
    if (value >= 5) return 'bg-gradient-to-r from-yellow-300 via-yellow-400 to-orange-400';
    return 'bg-gradient-to-r from-green-300 to-green-600';
  };

  const getEffectGradient = (value) => {
    if (value >= 8) return 'bg-gradient-to-r from-green-300 to-green-600';
    if (value >= 5) return 'bg-gradient-to-r from-yellow-300 via-green-300 to-green-500';
    return 'bg-gradient-to-r from-red-500 to-yellow-400';
  };

  return (
    <div className="bg-blue-50/80 backdrop-blur-sm p-4 rounded-2xl mb-3 border border-blue-100/40 shadow-md hover:shadow-lg transition">
      <h4 className="text-sm font-bold mb-3 text-blue-900">{exercise}</h4>
      
      <div className="space-y-3">
        {/* Risk Score */}
        <div>
          <div className="flex justify-between text-xs font-medium mb-1">
            <span className="text-blue-700">⚠️ Risk</span>
            <span className="text-blue-900 font-bold">{animatedRisk}/10</span>
          </div>
          <div className="h-2 bg-gray-300/50 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-700 rounded-full ${getRiskGradient(risk)}`}
              style={{ width: `${animatedRisk * 10}%` }}
            ></div>
          </div>
        </div>

        {/* Effectiveness Score */}
        <div>
          <div className="flex justify-between text-xs font-medium mb-1">
            <span className="text-blue-700">💪 Effectiveness</span>
            <span className="text-blue-900 font-bold">{animatedEffect}/10</span>
          </div>
          <div className="h-2 bg-gray-300/50 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-700 rounded-full ${getEffectGradient(effectiveness)}`}
              style={{ width: `${animatedEffect * 10}%` }}
            ></div>
          </div>
        </div>
      </div>

      <style>
        {`
        @keyframes pop {
          0%,100% { transform: scale(1);}
          40% { transform: scale(1.12);}
          80% { transform: scale(0.97);}
        }
        `}
      </style>
    </div>
  );
};

export default RiskMeter;
