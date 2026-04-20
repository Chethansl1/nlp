import React from 'react';
import { motion } from 'framer-motion';

const Home = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-6xl font-bold text-text mb-6"
          >
            Unveiling the Bias
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-text/80 mb-8 max-w-2xl mx-auto"
          >
            How Betting Apps Can Mislead
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <button className="bg-primary text-white px-8 py-3 rounded-2xl font-semibold hover:bg-primary/90 transition-colors">
              Check Fairness Demo
            </button>
            <button className="bg-accent text-white px-8 py-3 rounded-2xl font-semibold hover:bg-accent/90 transition-colors">
              Latest News
            </button>
          </motion.div>
        </div>
      </section>

      {/* Stats Strip */}
      <section className="py-12 bg-white/50 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
              <h3 className="text-2xl font-bold text-primary mb-2">1,247</h3>
              <p className="text-text/70">Total Events Analyzed</p>
            </div>
            <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
              <h3 className="text-2xl font-bold text-primary mb-2">12.4%</h3>
              <p className="text-text/70">Avg Bias Index</p>
            </div>
            <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
              <h3 className="text-2xl font-bold text-accent mb-2">23.7%</h3>
              <p className="text-text/70">Simulated Loss Rate</p>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-text mb-12">How This Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl font-bold">1</span>
              </div>
              <h3 className="text-xl font-semibold text-text mb-2">Data Collection</h3>
              <p className="text-text/70">Gather betting odds from multiple sources</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl font-bold">2</span>
              </div>
              <h3 className="text-xl font-semibold text-text mb-2">Audit Analysis</h3>
              <p className="text-text/70">Compare against fair probability models</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl font-bold">3</span>
              </div>
              <h3 className="text-xl font-semibold text-text mb-2">Awareness</h3>
              <p className="text-text/70">Educate users about manipulation tactics</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;