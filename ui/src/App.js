import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('research');
  const [systemInfo, setSystemInfo] = useState(null);
  
  // Search parameters
  const [queryType, setQueryType] = useState('legal_research_query');
  const [limit, setLimit] = useState(20);
  const [authorityWeight, setAuthorityWeight] = useState(0.9);
  const [recencyWeight, setRecencyWeight] = useState(0.4);

  useEffect(() => {
    // Load system info on component mount
    loadSystemInfo();
  }, []);

  const loadSystemInfo = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/system/info`);
      setSystemInfo(response.data);
    } catch (err) {
      console.error('Failed to load system info:', err);
      // Set default system info if API call fails
      setSystemInfo({
        available_practice_areas: ['personal_injury', 'medical_malpractice', 'civil_law'],
        available_query_types: ['legal_research_query', 'practice_area_query', 'authority_query']
      });
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError(null);

    try {
      let endpoint = '/api/v1/search/legal';
      let params = {
        query: searchQuery,
        query_type: queryType,
        limit: limit,
        authority_weight: authorityWeight,
        recency_weight: recencyWeight
      };

      if (activeTab === 'authority') {
        endpoint = '/api/v1/search/authority';
        params = {
          query: searchQuery,
          min_authority_score: 0.8,
          limit: limit
        };
      } else if (activeTab === 'recent') {
        endpoint = '/api/v1/search/recent';
        params = {
          query: searchQuery,
          days_back: 90,
          limit: limit
        };
      }

      const response = await axios.post(`${API_BASE_URL}${endpoint}`, null, {
        params: params
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
                <option value="legal_research_query">Comprehensive Research</option>
                <option value="practice_area_query">Practice Area Search</option>
                <option value="content_gap_query">Content Gap Analysis</option>
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
              Found {searchResults.results?.results?.length || 0} documents 
              {searchResults.query && ` for "${searchResults.query}"`}
            </p>
          </div>
          
          {searchResults.results?.results?.length > 0 ? (
            searchResults.results.results.map((result, index) => (
              <div key={index} className="result-item">
                <div className="result-title">
                  {result.title || result.id || 'Untitled Document'}
                </div>
                
                <div className="result-meta">
                  {result.practice_area && (
                    <span className="meta-item">Practice Area: {result.practice_area}</span>
                  )}
                  {result.jurisdiction && (
                    <span className="meta-item">Jurisdiction: {result.jurisdiction}</span>
                  )}
                  {result.authority_level && (
                    <span className="meta-item">Authority: {result.authority_level}</span>
                  )}
                  {result.document_type && (
                    <span className="meta-item">Type: {result.document_type}</span>
                  )}
                  {result.publication_date && (
                    <span className="meta-item">Published: {formatDate(result.publication_date)}</span>
                  )}
                </div>

                {result.summary && (
                  <div className="result-summary">
                    {result.summary}
                  </div>
                )}

                {result.author && (
                  <div className="result-summary">
                    <strong>Author:</strong> {result.author}
                  </div>
                )}

                {result.citations && result.citations.length > 0 && (
                  <div className="result-summary">
                    <strong>Citations:</strong> {result.citations.join(', ')}
                  </div>
                )}

                {result.keywords && result.keywords.length > 0 && (
                  <div className="result-summary">
                    <strong>Keywords:</strong> {result.keywords.join(', ')}
                  </div>
                )}

                <div className="result-score">
                  {result.similarity_score && (
                    <span style={{ color: getScoreColor(result.similarity_score) }}>
                      Similarity: {(result.similarity_score * 100).toFixed(1)}%
                    </span>
                  )}
                  {result.authority_score && (
                    <span style={{ color: getScoreColor(result.authority_score), marginLeft: '1rem' }}>
                      Authority: {(result.authority_score * 100).toFixed(1)}%
                    </span>
                  )}
                  {result.citation_count && (
                    <span style={{ marginLeft: '1rem' }}>
                      Citations: {result.citation_count}
                    </span>
                  )}
                </div>

                {result.source_url && (
                  <div style={{ marginTop: '0.5rem' }}>
                    <a href={result.source_url} target="_blank" rel="noopener noreferrer">
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