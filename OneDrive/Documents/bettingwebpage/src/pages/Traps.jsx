import React from 'react';

const Traps = () => {
  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-text mb-8 text-center">Psychological & Economic Traps</h1>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">Common Dark Patterns</h2>

          <div className="space-y-6">
            <div className="border-l-4 border-accent pl-4">
              <h3 className="font-semibold text-text mb-2">Near-Miss Effect</h3>
              <p className="text-text/70 mb-2">
                Apps highlight "close calls" to create false hope and encourage continued betting.
              </p>
              <div className="bg-red-50 p-3 rounded-lg text-red-800 text-sm">
                <strong>Impact:</strong> Increases dopamine response similar to actual wins.
              </div>
            </div>

            <div className="border-l-4 border-accent pl-4">
              <h3 className="font-semibold text-text mb-2">Loss Recovery Prompts</h3>
              <p className="text-text/70 mb-2">
                "Double or nothing" offers appear immediately after losses.
              </p>
              <div className="bg-red-50 p-3 rounded-lg text-red-800 text-sm">
                <strong>Impact:</strong> Exploits loss aversion bias, leading to larger losses.
              </div>
            </div>

            <div className="border-l-4 border-accent pl-4">
              <h3 className="font-semibold text-text mb-2">Streak Notifications</h3>
              <p className="text-text/70 mb-2">
                Push notifications celebrating "winning streaks" to maintain engagement.
              </p>
              <div className="bg-red-50 p-3 rounded-lg text-red-800 text-sm">
                <strong>Impact:</strong> Creates illusion of control and skill-based success.
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">Economic Realities</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-text mb-2">House Edge</h3>
              <p className="text-text/70 text-sm mb-3">
                Every bet has a built-in mathematical disadvantage for the player.
              </p>
              <div className="bg-blue-50 p-3 rounded-lg">
                <strong className="text-blue-800">Example:</strong> Roulette house edge = 5.26%
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-text mb-2">Expected Value</h3>
              <p className="text-text/70 text-sm mb-3">
                Long-term mathematical expectation of any betting strategy.
              </p>
              <div className="bg-red-50 p-3 rounded-lg">
                <strong className="text-red-800">Reality:</strong> Always negative for players
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-semibold text-text mb-6">Self-Check Quiz</h2>

          <div className="space-y-4">
            <div>
              <p className="font-medium text-text mb-2">1. Do you bet more after a loss to "recover"?</p>
              <div className="flex gap-4">
                <label className="flex items-center">
                  <input type="radio" name="q1" value="yes" className="mr-2" />
                  <span className="text-text/70">Yes</span>
                </label>
                <label className="flex items-center">
                  <input type="radio" name="q1" value="no" className="mr-2" />
                  <span className="text-text/70">No</span>
                </label>
              </div>
            </div>

            <div>
              <p className="font-medium text-text mb-2">2. Do you check betting apps multiple times daily?</p>
              <div className="flex gap-4">
                <label className="flex items-center">
                  <input type="radio" name="q2" value="yes" className="mr-2" />
                  <span className="text-text/70">Yes</span>
                </label>
                <label className="flex items-center">
                  <input type="radio" name="q2" value="no" className="mr-2" />
                  <span className="text-text/70">No</span>
                </label>
              </div>
            </div>

            <div>
              <p className="font-medium text-text mb-2">3. Have you lied about your betting losses?</p>
              <div className="flex gap-4">
                <label className="flex items-center">
                  <input type="radio" name="q3" value="yes" className="mr-2" />
                  <span className="text-text/70">Yes</span>
                </label>
                <label className="flex items-center">
                  <input type="radio" name="q3" value="no" className="mr-2" />
                  <span className="text-text/70">No</span>
                </label>
              </div>
            </div>
          </div>

          <button className="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:bg-primary/90 transition-colors mt-6">
            Calculate Risk Score
          </button>
        </div>
      </div>
    </div>
  );
};

export default Traps;