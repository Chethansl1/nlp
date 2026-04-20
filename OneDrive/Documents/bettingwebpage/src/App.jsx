import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import News from './pages/News';
import Admin from './pages/Admin';
import Demo from './pages/Demo';
import Model from './pages/Model';
import Predict from './pages/Predict';
import Traps from './pages/Traps';
import Resources from './pages/Resources';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/news" element={<News />} />
            <Route path="/admin/load" element={<Admin />} />
            <Route path="/demo/preprocess" element={<Demo />} />
            <Route path="/model" element={<Model />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/traps" element={<Traps />} />
            <Route path="/resources" element={<Resources />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
