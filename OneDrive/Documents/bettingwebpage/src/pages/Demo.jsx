import React from 'react';

const Demo = () => {
  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-text mb-8 text-center">Data Preprocessing Demo</h1>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">Raw Dataset Preview</h2>
          <div className="bg-gray-50 p-4 rounded-xl mb-6">
            <pre className="text-sm text-text/70">
{`Date,Home_Team,Away_Team,Home_Odds,Away_Odds,Draw_Odds
2025-01-15,Mumbai City,ATK Mohun Bagan,2.10,3.40,3.20
2025-01-16,Kerala Blasters,FC Goa,2.80,2.45,3.10
...`}
            </pre>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="text-center">
              <h3 className="font-semibold text-text mb-2">Rows</h3>
              <p className="text-2xl font-bold text-primary">1,247</p>
            </div>
            <div className="text-center">
              <h3 className="font-semibold text-text mb-2">Missing Values</h3>
              <p className="text-2xl font-bold text-accent">23</p>
            </div>
            <div className="text-center">
              <h3 className="font-semibold text-text mb-2">Class Balance</h3>
              <p className="text-2xl font-bold text-primary">67/33</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-semibold text-text mb-6">Preprocessing Options</h2>

          <div className="space-y-4 mb-6">
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" defaultChecked />
              <span className="text-text">Apply SMOTE for class balancing</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" defaultChecked />
              <span className="text-text">Scale numerical features (StandardScaler)</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" defaultChecked />
              <span className="text-text">Encode categorical variables (OneHot)</span>
            </label>
          </div>

          <button className="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:bg-primary/90 transition-colors mb-6">
            Run Preprocessing Demo
          </button>

          <div className="bg-gray-50 p-4 rounded-xl">
            <h3 className="font-semibold text-text mb-2">Processing Results:</h3>
            <ul className="text-sm text-text/70 space-y-1">
              <li>• Features scaled to mean=0, std=1</li>
              <li>• Categorical variables encoded (12 new columns)</li>
              <li>• SMOTE applied: 412 synthetic samples added</li>
              <li>• Final dataset: 1,659 rows × 28 features</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Demo;