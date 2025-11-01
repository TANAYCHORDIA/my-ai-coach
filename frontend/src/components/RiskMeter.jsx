import React from 'react';

const RiskMeter = ({ exercise, risk, effectiveness }) => {
  const getRiskColor = (value) => {
    if (value >= 7) return 'bg-red-600';
    if (value >= 5) return 'bg-yellow-500';
    return 'bg-green-600';
  };

  const getEffectColor = (value) => {
    if (value >= 8) return 'bg-green-600';
    if (value >= 5) return 'bg-yellow-500';
    return 'bg-red-600';
  };

  return (
    <div className="bg-gray-700 p-4 rounded-lg mb-3 border border-gray-600">
      <h4 className="text-sm font-semibold mb-3 text-white">{exercise}</h4>
      
      <div className="space-y-2">
        {/* Risk Score */}
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-gray-300">⚠️ Risk</span>
            <span className="text-gray-200">{risk}/10</span>
          </div>
          <div className="h-2 bg-gray-600 rounded-full overflow-hidden">
            <div 
              className={`h-full ${getRiskColor(risk)} transition-all duration-300`}
              style={{ width: `${risk * 10}%` }}
            ></div>
          </div>
        </div>

        {/* Effectiveness Score */}
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-gray-300">💪 Effectiveness</span>
            <span className="text-gray-200">{effectiveness}/10</span>
          </div>
          <div className="h-2 bg-gray-600 rounded-full overflow-hidden">
            <div 
              className={`h-full ${getEffectColor(effectiveness)} transition-all duration-300`}
              style={{ width: `${effectiveness * 10}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskMeter;
