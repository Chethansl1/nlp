import React from 'react';

const About = () => {
  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-text mb-8 text-center">About This Project</h1>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-4">Our Mission</h2>
          <p className="text-text/70 mb-6">
            To educate users about manipulative practices in online betting platforms and provide tools
            to identify fair odds versus manipulated ones. We focus specifically on the Indian betting market
            where these issues are particularly prevalent.
          </p>

          <h2 className="text-2xl font-semibold text-text mb-4">Methodology</h2>
          <ul className="list-disc list-inside text-text/70 mb-6 space-y-2">
            <li><strong>Data Collection:</strong> Scraping odds from multiple Indian betting platforms</li>
            <li><strong>Fair-odds Model:</strong> Using Random Forest regression trained on historical sports data</li>
            <li><strong>Bias Index:</strong> Calculated as percentage deviation from fair probability</li>
            <li><strong>Simulation:</strong> Monte Carlo analysis of betting strategies</li>
          </ul>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-semibold text-text mb-4">Team & Credits</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-text mb-2">Research Lead</h3>
              <p className="text-text/70">Dr. Analysis Kumar</p>
            </div>
            <div>
              <h3 className="font-semibold text-text mb-2">Data Science</h3>
              <p className="text-text/70">Team Data Insights</p>
            </div>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-text/70 text-sm">
              This project is supported by academic research grants and community donations.
              All analysis is conducted using open-source tools and publicly available data.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;