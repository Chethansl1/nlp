import React, { useState, useEffect } from 'react';
import Fuse from 'fuse.js';

const News = () => {
  const [news, setNews] = useState([]);
  const [filteredNews, setFilteredNews] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);

  // Sample news data - in real app this would come from API
  useEffect(() => {
    const sampleNews = [
      {
        id: 'news-001',
        date: '2025-11-05',
        title: 'Teenager loses ₹1.2 lakh on betting app; family files complaint',
        summary: 'A student reportedly accrued large losses over 3 months on a popular betting platform...',
        source: 'The Indian Express',
        url: 'https://indianexpress.com/...',
        tags: ['loss', 'youth']
      },
      {
        id: 'news-002',
        date: '2025-11-03',
        title: 'Man ends life after losing ₹5 lakh in online betting',
        summary: 'Tragic incident highlights the dangers of unregulated betting platforms...',
        source: 'NDTV',
        url: 'https://ndtv.com/...',
        tags: ['death', 'loss']
      }
    ];
    setNews(sampleNews);
    setFilteredNews(sampleNews);
  }, []);

  // Search functionality
  useEffect(() => {
    if (!searchQuery) {
      setFilteredNews(news);
      return;
    }

    const fuse = new Fuse(news, {
      keys: ['title', 'summary', 'tags'],
      threshold: 0.3
    });

    const results = fuse.search(searchQuery);
    setFilteredNews(results.map(result => result.item));
  }, [searchQuery, news]);

  const allTags = ['death', 'loss', 'regulation', 'youth', 'fraud'];

  const toggleTag = (tag) => {
    setSelectedTags(prev =>
      prev.includes(tag)
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const importantCases = filteredNews.filter(item =>
    item.tags.includes('death') || item.tags.includes('suicide')
  );

  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-text mb-8 text-center">Latest News</h1>

        {/* Search and Filters */}
        <div className="bg-white p-6 rounded-2xl shadow-lg mb-8">
          <div className="flex flex-col md:flex-row gap-4 mb-4">
            <input
              type="text"
              placeholder="Search news..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div className="flex flex-wrap gap-2">
            {allTags.map(tag => (
              <button
                key={tag}
                onClick={() => toggleTag(tag)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  selectedTags.includes(tag)
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-text hover:bg-gray-200'
                }`}
              >
                {tag}
              </button>
            ))}
          </div>
        </div>

        {/* Important Cases */}
        {importantCases.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-accent mb-4">⚠️ Important Cases</h2>
            <div className="bg-red-50 border border-red-200 p-4 rounded-2xl">
              <p className="text-red-800 mb-4">
                <strong>Content Warning:</strong> This section contains reports of gambling-related harm and loss of life.
                If you or someone you know is struggling, please contact mental health helplines.
              </p>
              {importantCases.map(item => (
                <div key={item.id} className="bg-white p-4 rounded-xl mb-4 shadow-sm">
                  <h3 className="font-semibold text-text mb-2">{item.title}</h3>
                  <p className="text-text/70 text-sm mb-2">{item.summary}</p>
                  <div className="flex justify-between items-center text-xs text-text/60">
                    <span>{item.source} • {item.date}</span>
                    <a href={item.url} className="text-primary hover:underline">Read more</a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* News Feed */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredNews.map(item => (
            <div key={item.id} className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="flex flex-wrap gap-2 mb-3">
                {item.tags.map(tag => (
                  <span
                    key={tag}
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      tag === 'death' ? 'bg-red-100 text-red-800' :
                      tag === 'loss' ? 'bg-orange-100 text-orange-800' :
                      'bg-blue-100 text-blue-800'
                    }`}
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <h3 className="font-semibold text-text mb-3">{item.title}</h3>
              <p className="text-text/70 text-sm mb-4">{item.summary}</p>
              <div className="flex justify-between items-center text-xs text-text/60">
                <span>{item.source} • {item.date}</span>
                <button className="text-primary hover:underline">Read more</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default News;