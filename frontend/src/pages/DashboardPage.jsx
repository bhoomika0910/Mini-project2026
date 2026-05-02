import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './DashboardPage.css';

function DashboardPage() {
  const [selectedMonument, setSelectedMonument] = useState('');
  const [monuments, setMonuments] = useState([]);
  const [sensorData, setSensorData] = useState(null);
  const [historyData, setHistoryData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Har 5 second me naya data mangwane ka logic (Polling)
  useEffect(() => {
    const fetchLatestData = async () => {
      try {
        const response = await axios.get('https://mini-project2026-2.onrender.com/latest');
        // Array ko object me convert karna
        const dataByMonument = response.data.reduce((acc, item) => {
          acc[item.monument] = item;
          return acc;
        }, {});

        setSensorData(dataByMonument);
        
        const availableMonuments = Object.keys(dataByMonument);
        setMonuments(availableMonuments);
        
        // Agar koi monument select nahi hai, toh pehla wala auto-select kar lo
        if (availableMonuments.length > 0 && !selectedMonument) {
          setSelectedMonument(availableMonuments[0]);
        }

        setLoading(false);
        setError(null);
      } catch (err) {
        console.error('Error fetching live data:', err);
        setError('Backend se connect nahi ho pa raha hai...');
      }
    };

    fetchLatestData(); // Pehli baar turant run karo
    const intervalId = setInterval(fetchLatestData, 5000); // Phir har 5 sec me run karo
    
    return () => clearInterval(intervalId);
  }, [selectedMonument]);

  // Chart ke liye history data mangwana
  useEffect(() => {
    const fetchHistory = async () => {
      if (!selectedMonument) return;
      try {
        const response = await axios.get(`https://mini-project2026-1.onrender.com/readings/${encodeURIComponent(selectedMonument)}`);
        const formattedHistory = response.data.map(item => ({
          time: new Date(item.timestamp).toLocaleTimeString(),
          temperature: item.temperature,
          humidity: item.humidity,
        })).reverse(); // Purane se naya sort karne ke liye
        
        setHistoryData(formattedHistory);
      } catch (err) {
        console.error('Error fetching history:', err);
      }
    };

    fetchHistory();
    const intervalId = setInterval(fetchHistory, 5000);
    
    return () => clearInterval(intervalId);
  }, [selectedMonument]);

  return (
    <div className="dashboard-page">
      {/* Navbar */}
      <nav className="dashboard-navbar">
        <Link to="/" className="navbar-brand">HeritageAI</Link>
        <h1 className="dashboard-title">Monitoring Dashboard</h1>
        <div className="monument-selector">
          <select
            value={selectedMonument}
            onChange={(e) => setSelectedMonument(e.target.value)}
            className="monument-dropdown"
            disabled={monuments.length === 0}
          >
            <option value="">-- Select Site --</option>
            {monuments.map((monument) => (
              <option key={monument} value={monument}>{monument}</option>
            ))}
          </select>
          <span className="connection-indicator connected">
            🟢 Live Sync On
          </span>
        </div>
      </nav>

      <main className="dashboard-content">
        {/* Anomaly Alert Banner */}
        {sensorData && selectedMonument && sensorData[selectedMonument]?.anomaly === -1 && (
          <div className="alert-banner">
            ⚠️ Anomaly Detected at {selectedMonument}! Immediate attention required.
          </div>
        )}

        {loading && monuments.length === 0 ? (
          <div className="loading-state">
            <div className="loader"></div>
            <p>Waiting for ESP32 Sensor Data...</p>
          </div>
        ) : error && monuments.length === 0 ? (
          <div className="error-state">
            <p>{error}</p>
            <button onClick={() => window.location.reload()} className="btn btn-primary">
              Retry Connection
            </button>
          </div>
        ) : selectedMonument && sensorData?.[selectedMonument] ? (
          <>
            {/* Health Overview Section */}
            <section className="health-overview">
              <div className="shi-card">
                <h2>Site Health Index</h2>
                <div className="shi-value">
                  {sensorData[selectedMonument]?.shi?.toFixed(1)}%
                </div>
                <div className="shi-bar">
                  <div 
                    className="shi-progress" 
                    style={{ width: `${(sensorData[selectedMonument]?.shi ?? 0)}%` }}
                  ></div>
                </div>
              </div>
              <div className="risk-card">
                <h2>Risk Assessment</h2>
                {getRiskBadge(sensorData[selectedMonument]?.risk_level)}
                <p className="last-update">
                  Updated: {new Date(sensorData[selectedMonument]?.timestamp).toLocaleTimeString() || 'pending...'}
                </p>
              </div>
            </section>

            {/* Sensor Cards */}
            <section className="sensors-section">
              <h2 className="section-title">Live Sensor Readings</h2>
              <div className="sensors-grid">
                {['temperature', 'humidity', 'air_pollution', 'vibration', 'crack_width'].map((sensor) => (
                  <div key={sensor} className="sensor-card">
                    <div className="sensor-icon">{getSensorIcon(sensor)}</div>
                    <h3>{formatSensorName(sensor)}</h3>
                    <div className="sensor-value">
                      {typeof sensorData[selectedMonument]?.[sensor] === 'number' 
                        ? sensorData[selectedMonument][sensor].toFixed(2)
                        : 'N/A'}
                      <span className="sensor-unit">{getSensorUnit(sensor)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* History Chart */}
            <section className="chart-section">
              <h2 className="section-title">Temperature & Humidity History (Live)</h2>
              <div className="chart-container">
                {historyData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={historyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#243654" />
                      <XAxis dataKey="time" stroke="#a0a0a0" tick={{ fill: '#a0a0a0' }} />
                      <YAxis stroke="#a0a0a0" tick={{ fill: '#a0a0a0' }} />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1a2942', 
                          border: '1px solid #d4af37',
                          borderRadius: '8px',
                          color: '#fff'
                        }}
                      />
                      <Legend />
                      <Line type="monotone" dataKey="temperature" stroke="#d4af37" strokeWidth={2} dot={{ fill: '#d4af37', strokeWidth: 2 }} name="Temperature (°C)" isAnimationActive={false} />
                      <Line type="monotone" dataKey="humidity" stroke="#4ecdc4" strokeWidth={2} dot={{ fill: '#4ecdc4', strokeWidth: 2 }} name="Humidity (%)" isAnimationActive={false} />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="no-data">Loading chart data...</div>
                )}
              </div>
            </section>
          </>
        ) : (
          <div className="no-data-state">
            <p>Please select a monument to view live data</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>&copy; 2026 HeritageAI. Real-time Heritage Monitoring System.</p>
      </footer>
    </div>
  );
}

const getRiskBadge = (riskLevel) => {
  switch (riskLevel) {
    case 0: return <span className="risk-badge risk-low">Low Risk</span>;
    case 1: return <span className="risk-badge risk-medium">Medium Risk</span>;
    case 2: return <span className="risk-badge risk-high">High Risk</span>;
    default: return <span className="risk-badge">Unknown</span>;
  }
};

const getSensorIcon = (sensor) => {
  const icons = { temperature: '🌡️', humidity: '💧', air_pollution: '🌫️', vibration: '📳', crack_width: '🔍' };
  return icons[sensor] || '📊';
};

const formatSensorName = (sensor) => {
  const names = { temperature: 'Temperature', humidity: 'Humidity', air_pollution: 'Air Pollution', vibration: 'Vibration', crack_width: 'Crack Width' };
  return names[sensor] || sensor;
};

const getSensorUnit = (sensor) => {
  const units = { temperature: '°C', humidity: '%', air_pollution: 'AQI', vibration: 'mm/s', crack_width: 'mm' };
  return units[sensor] || '';
};

export default DashboardPage;