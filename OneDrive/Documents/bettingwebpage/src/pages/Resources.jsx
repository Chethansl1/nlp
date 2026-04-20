import React from 'react';

const Resources = () => {
  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-text mb-8 text-center">Suggestions & Resources</h1>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">How to Identify Manipulative Odds</h2>

          <div className="space-y-4">
            <div className="flex items-start">
              <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center mr-4 mt-1">
                <span className="text-white text-sm font-bold">1</span>
              </div>
              <div>
                <h3 className="font-semibold text-text mb-1">Compare Across Platforms</h3>
                <p className="text-text/70 text-sm">
                  Check the same event odds on multiple betting apps. Significant variations indicate manipulation.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center mr-4 mt-1">
                <span className="text-white text-sm font-bold">2</span>
              </div>
              <div>
                <h3 className="font-semibold text-text mb-1">Calculate Fair Probability</h3>
                <p className="text-text/70 text-sm">
                  Fair odds = 1 / (actual probability). Compare with bookmaker odds to find bias.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center mr-4 mt-1">
                <span className="text-white text-sm font-bold">3</span>
              </div>
              <div>
                <h3 className="font-semibold text-text mb-1">Watch for Patterns</h3>
                <p className="text-text/70 text-sm">
                  Consistent bias favoring certain outcomes suggests systematic manipulation.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">Safe Betting Tips</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-green-50 p-4 rounded-xl">
              <h3 className="font-semibold text-green-800 mb-2">Set Strict Limits</h3>
              <ul className="text-green-700 text-sm space-y-1">
                <li>• Daily deposit limit: ₹500</li>
                <li>• Weekly loss limit: ₹2,000</li>
                <li>• Session time limit: 30 minutes</li>
              </ul>
            </div>

            <div className="bg-blue-50 p-4 rounded-xl">
              <h3 className="font-semibold text-blue-800 mb-2">Take Breaks</h3>
              <ul className="text-blue-700 text-sm space-y-1">
                <li>• No betting during work hours</li>
                <li>• Mandatory 24-hour cooling off</li>
                <li>• Track all betting activity</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">Helplines & Support</h2>

          <div className="space-y-4">
            <div className="border border-gray-200 p-4 rounded-xl">
              <h3 className="font-semibold text-text mb-2">Gambling Helpline India</h3>
              <p className="text-text/70 text-sm mb-2">24/7 support for gambling addiction</p>
              <p className="text-primary font-medium">Phone: 1800-XXX-XXXX</p>
            </div>

            <div className="border border-gray-200 p-4 rounded-xl">
              <h3 className="font-semibold text-text mb-2">Mental Health Support</h3>
              <p className="text-text/70 text-sm mb-2">For those affected by gambling-related trauma</p>
              <p className="text-primary font-medium">Phone: 1800-XXX-XXXX</p>
            </div>

            <div className="border border-gray-200 p-4 rounded-xl">
              <h3 className="font-semibold text-text mb-2">Consumer Court</h3>
              <p className="text-text/70 text-sm mb-2">File complaints against unfair betting practices</p>
              <p className="text-primary font-medium">Website: consumercourt.gov.in</p>
            </div>
          </div>
        </div>

        <div className="bg-accent/10 p-8 rounded-2xl border-2 border-accent">
          <h2 className="text-2xl font-semibold text-text mb-4">Policy Recommendations</h2>
          <ul className="text-text/70 space-y-2">
            <li>• <strong>Independent Auditing:</strong> Regular third-party audits of betting algorithms</li>
            <li>• <strong>Transparency Requirements:</strong> Public disclosure of odds-setting methodologies</li>
            <li>• <strong>Consumer Protections:</strong> Mandatory cooling-off periods and loss limits</li>
            <li>• <strong>Education Campaigns:</strong> School and community awareness programs</li>
            <li>• <strong>Regulation Enforcement:</strong> Stricter penalties for manipulative practices</li>
          </ul>

          <button className="mt-6 bg-accent text-white px-6 py-3 rounded-xl font-semibold hover:bg-accent/90 transition-colors">
            Download Policy Brief (PDF)
          </button>
        </div>
      </div>
    </div>
  );
};

export default Resources;