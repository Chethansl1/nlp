import React from 'react';

const Model = () => {
  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-text mb-8 text-center">Model Analysis</h1>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">Random Forest Model Summary</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="font-semibold text-text mb-2">Model Parameters</h3>
              <ul className="text-text/70 space-y-1">
                <li>• n_estimators: 100</li>
                <li>• max_depth: 10</li>
                <li>• min_samples_split: 5</li>
                <li>• random_state: 42</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-text mb-2">Performance Metrics</h3>
              <ul className="text-text/70 space-y-1">
                <li>• Accuracy: 87.3%</li>
                <li>• Precision: 85.1%</li>
                <li>• Recall: 82.4%</li>
                <li>• F1-Score: 83.7%</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-semibold text-text mb-6">Fairness Check Tool</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-text font-medium mb-2">Home Team Odds</label>
              <input
                type="number"
                step="0.01"
                placeholder="2.10"
                className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label className="block text-text font-medium mb-2">Away Team Odds</label>
              <input
                type="number"
                step="0.01"
                placeholder="3.40"
                className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          <button className="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:bg-primary/90 transition-colors mb-6">
            Calculate Fair Probability
          </button>

          <div className="bg-green-50 p-4 rounded-xl">
            <h3 className="font-semibold text-green-800 mb-2">Results:</h3>
            <ul className="text-green-700 space-y-1">
              <li>• Fair Home Win Probability: 45.2%</li>
              <li>• Fair Away Win Probability: 32.1%</li>
              <li>• Fair Draw Probability: 22.7%</li>
              <li>• Bias Index: +12.4% (unfair odds detected)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Model;