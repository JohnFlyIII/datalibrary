import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

// Use environment variable for API URL (Docker containers) or empty string for proxy (development)
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('research');
  const [systemInfo, setSystemInfo] = useState(null);
  
  // Search parameters
  const [queryType, setQueryType] = useState('legal_research');
  const [limit, setLimit] = useState(20);
  const [authorityWeight, setAuthorityWeight] = useState(0.9);
  const [recencyWeight, setRecencyWeight] = useState(0.4);

  useEffect(() => {
    // Load system info on component mount
    loadSystemInfo();
  }, []);

  const loadSystemInfo = async () => {
    // Set system info directly since we know what Superlinked supports
    setSystemInfo({
      available_practice_areas: ['personal_injury', 'medical_malpractice', 'civil_law'],
      available_query_types: ['legal_research', 'practice_area', 'authority', 'medical_malpractice', 'recent_developments']
    });
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError(null);

    try {
      let endpoint = `/api/v1/search/${queryType}`;
      let payload = {
        search_query: searchQuery,
        limit: limit
      };

      if (activeTab === 'authority') {
        endpoint = '/api/v1/search/authority';
        payload = {
          search_query: searchQuery,
          authority_weight: 1.5,
          citation_weight: 1.2,
          limit: limit
        };
      } else if (activeTab === 'recent') {
        endpoint = '/api/v1/search/recent_developments';
        payload = {
          search_query: searchQuery,
          recency_weight: 1.5,
          limit: limit
        };
      } else {
        // Add weights for research tab
        payload.content_weight = 1.0;
        payload.title_weight = 0.6;
        payload.summary_weight = 0.7;
        payload.practice_area_weight = 0.8;
        payload.authority_weight = authorityWeight;
        payload.recency_weight = recencyWeight;
        payload.citation_weight = 0.3;
      }

      const response = await axios.post(`${API_BASE_URL}${endpoint}`, payload, {
        headers: { 'Content-Type': 'application/json' }
      });

      setSearchResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'Unknown';
    return new Date(timestamp * 1000).toLocaleDateString();
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return '#059669';
    if (score >= 0.6) return '#d97706';
    return '#dc2626';
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Legal Knowledge System</h1>
        <p>Advanced Legal Research Platform</p>
      </div>

      <div className="search-container">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'research' ? 'active' : ''}`}
            onClick={() => setActiveTab('research')}
          >
            Legal Research
          </button>
          <button 
            className={`tab ${activeTab === 'authority' ? 'active' : ''}`}
            onClick={() => setActiveTab('authority')}
          >
            Authoritative Sources
          </button>
          <button 
            className={`tab ${activeTab === 'recent' ? 'active' : ''}`}
            onClick={() => setActiveTab('recent')}
          >
            Recent Developments
          </button>
        </div>

        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            className="search-input"
            placeholder={
              activeTab === 'research' ? "Enter your legal research query..." :
              activeTab === 'authority' ? "Search authoritative legal sources..." :
              "Find recent legal developments..."
            }
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="search-button" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {activeTab === 'research' && (
          <div className="search-options">
            <div className="option-group">
              <label>Query Type:</label>
              <select value={queryType} onChange={(e) => setQueryType(e.target.value)}>
                <option value="legal_research">Comprehensive Research</option>
                <option value="practice_area">Practice Area Search</option>
                <option value="legal_research">Content Gap Analysis</option>
              </select>
            </div>
            <div className="option-group">
              <label>Results Limit:</label>
              <select value={limit} onChange={(e) => setLimit(parseInt(e.target.value))}>
                <option value={10}>10 Results</option>
                <option value={20}>20 Results</option>
                <option value={50}>50 Results</option>
              </select>
            </div>
            <div className="option-group">
              <label>Authority Weight:</label>
              <select value={authorityWeight} onChange={(e) => setAuthorityWeight(parseFloat(e.target.value))}>
                <option value={0.5}>Low (0.5)</option>
                <option value={0.9}>High (0.9)</option>
                <option value={1.5}>Maximum (1.5)</option>
              </select>
            </div>
            <div className="option-group">
              <label>Recency Weight:</label>
              <select value={recencyWeight} onChange={(e) => setRecencyWeight(parseFloat(e.target.value))}>
                <option value={0.2}>Low (0.2)</option>
                <option value={0.4}>Medium (0.4)</option>
                <option value={1.0}>High (1.0)</option>
              </select>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          Searching legal documents...
        </div>
      )}

      {searchResults && (
        <div className="results-container">
          <div className="results-header">
            <h2>Search Results</h2>
            <p>
              Found {searchResults.entries?.length || 0} documents 
              for "{searchQuery}"
            </p>
          </div>
          
          {searchResults.entries?.length > 0 ? (
            searchResults.entries.map((entry, index) => (
              <div key={index} className="result-item">
                <div className="result-title">
                  {entry.fields?.title || entry.id || 'Untitled Document'}
                </div>
                
                <div className="result-meta">
                  {entry.fields?.practice_area && (
                    <span className="meta-item">Practice Area: {entry.fields.practice_area}</span>
                  )}
                  {entry.fields?.jurisdiction && (
                    <span className="meta-item">Jurisdiction: {entry.fields.jurisdiction}</span>
                  )}
                  {entry.fields?.authority_level && (
                    <span className="meta-item">Authority: {entry.fields.authority_level}</span>
                  )}
                  {entry.fields?.document_type && (
                    <span className="meta-item">Type: {entry.fields.document_type}</span>
                  )}
                  {entry.fields?.publication_date && (
                    <span className="meta-item">Published: {formatDate(entry.fields.publication_date)}</span>
                  )}
                </div>

                {entry.fields?.summary && (
                  <div className="result-summary">
                    {entry.fields.summary}
                  </div>
                )}

                {entry.fields?.content_text && (
                  <div className="result-summary">
                    <strong>Content Preview:</strong> {entry.fields.content_text.substring(0, 300)}...
                  </div>
                )}

                {entry.fields?.author && (
                  <div className="result-summary">
                    <strong>Author:</strong> {entry.fields.author}
                  </div>
                )}

                <div className="result-score">
                  {entry.fields?.authority_score && (
                    <span style={{ color: getScoreColor(entry.fields.authority_score) }}>
                      Authority: {(entry.fields.authority_score * 100).toFixed(1)}%
                    </span>
                  )}
                  {entry.fields?.citation_count && (
                    <span style={{ marginLeft: '1rem' }}>
                      Citations: {entry.fields.citation_count}
                    </span>
                  )}
                </div>

                {entry.fields?.source_url && (
                  <div style={{ marginTop: '0.5rem' }}>
                    <a href={entry.fields.source_url} target="_blank" rel="noopener noreferrer">
                      View Source
                    </a>
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="no-results">
              No documents found for your search query.
            </div>
          )}
        </div>
      )}

      {systemInfo && (
        <div style={{ marginTop: '2rem', padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
          <h3>System Information</h3>
          <p><strong>Available Practice Areas:</strong> {systemInfo.available_practice_areas?.join?.(', ') || 'N/A'}</p>
          <p><strong>Query Types:</strong> {systemInfo.available_query_types?.join?.(', ') || 'N/A'}</p>
        </div>
      )}
    </div>
  );
}

export default App;