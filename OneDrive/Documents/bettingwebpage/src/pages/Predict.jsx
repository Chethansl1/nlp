import React from 'react';

const Predict = () => {
  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-text mb-8 text-center">Bankroll Simulation</h1>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">Simulation Parameters</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <label className="block text-text font-medium mb-2">Start Bankroll (₹)</label>
              <input
                type="number"
                defaultValue="10000"
                className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label className="block text-text font-medium mb-2">Bet Size (%)</label>
              <input
                type="number"
                defaultValue="5"
                className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label className="block text-text font-medium mb-2">Number of Bets</label>
              <input
                type="number"
                defaultValue="100"
                className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          <button className="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:bg-primary/90 transition-colors">
            Run Simulation
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-green-50 p-8 rounded-2xl border-2 border-green-200">
            <h2 className="text-2xl font-semibold text-green-800 mb-4">Safe State</h2>
            <div className="text-center mb-4">
              <div className="text-4xl font-bold text-green-600 mb-2">₹12,450</div>
              <div className="text-green-700">Current Bankroll</div>
            </div>
            <div className="bg-white p-4 rounded-xl">
              <p className="text-green-800 text-sm">
                ✅ Bankroll growing steadily<br />
                ✅ Within safe betting limits<br />
                ✅ No high-risk patterns detected
              </p>
            </div>
          </div>

          <div className="bg-red-50 p-8 rounded-2xl border-2 border-red-200">
            <h2 className="text-2xl font-semibold text-red-800 mb-4">Critical State</h2>
            <div className="text-center mb-4">
              <div className="text-4xl font-bold text-red-600 mb-2">₹1,230</div>
              <div className="text-red-700">Current Bankroll</div>
            </div>
            <div className="bg-white p-4 rounded-xl">
              <p className="text-red-800 text-sm">
                ⚠️ Bankroll depleted by 88%<br />
                ⚠️ Chasing losses detected<br />
                ⚠️ Immediate intervention needed
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Predict;