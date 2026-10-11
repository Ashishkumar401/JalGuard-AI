
import { useState } from 'react';
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
  useMap,
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const areas = [
  {
    name: 'Sinhagad Road',
    position: [18.463, 73.807],
    risk: 'High',
    color: '#f97316',
    reason: 'Illustrative low-lying and heavy-rain scenario. Verify with official data.',
  },
  {
    name: 'Warje',
    position: [18.482, 73.802],
    risk: 'Moderate',
    color: '#eab308',
    reason: 'Scenario-based risk indicator; not a live flood forecast.',
  },
  {
    name: 'Kothrud',
    position: [18.507, 73.807],
    risk: 'Low',
    color: '#16a34a',
    reason: 'Baseline demonstration zone; actual risk can change with local conditions.',
  },
  {
    name: 'Deccan',
    position: [18.516, 73.841],
    risk: 'High',
    color: '#f97316',
    reason: 'Illustrative scenario only. Check current official warnings.',
  },
  {
    name: 'Yerawada',
    position: [18.551, 73.879],
    risk: 'Moderate',
    color: '#eab308',
    reason: 'Scenario-based indicator; requires rainfall and drainage validation.',
  },
  {
    name: 'Hadapsar',
    position: [18.508, 73.926],
    risk: 'Low',
    color: '#16a34a',
    reason: 'Baseline demonstration zone; not a prediction for the real area.',
  },
];

function MapResize() {
  const map = useMap();

  setTimeout(() => map.invalidateSize(), 100);

  return null;
}

export default function PuneFloodMap() {
  const [selected, setSelected] = useState('All');
  const [rainScenario, setRainScenario] = useState('Normal');

  const scenarioRisk = (risk) => {
    if (rainScenario === 'Heavy') {
      if (risk === 'Low') return 'Moderate';
      if (risk === 'Moderate') return 'High';
      return 'Very high';
    }

    if (rainScenario === 'Extreme') {
      return 'Very high';
    }

    return risk;
  };

  const colors = {
    Low: '#16a34a',
    Moderate: '#eab308',
    High: '#f97316',
    'Very high': '#dc2626',
  };

  const filteredAreas =
    selected === 'All'
      ? areas
      : areas.filter((area) => scenarioRisk(area.risk) === selected);

  return (
    <section className="panel large-panel">
      <div className="panel-title">
        <div>
          <h2>Pune Flood Risk Map</h2>
          <p>
            Explore illustrative area risk zones under different rainfall
            scenarios.
          </p>
        </div>
        <span className="panel-tag">SIMULATION</span>
      </div>

      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', margin: '18px 0' }}>
        <label>
          Rainfall scenario{' '}
          <select
            value={rainScenario}
            onChange={(event) => setRainScenario(event.target.value)}
          >
            <option value="Normal">Normal</option>
            <option value="Heavy">Heavy rain</option>
            <option value="Extreme">Extreme rain</option>
          </select>
        </label>

        <label>
          Filter zones{' '}
          <select
            value={selected}
            onChange={(event) => setSelected(event.target.value)}
          >
            <option>All</option>
            <option>Low</option>
            <option>Moderate</option>
            <option>High</option>
            <option>Very high</option>
          </select>
        </label>
      </div>

      <div
        style={{
          height: 440,
          width: '100%',
          borderRadius: 14,
          overflow: 'hidden',
        }}
      >
        <MapContainer
          center={[18.5204, 73.8567]}
          zoom={11}
          style={{ height: '100%', width: '100%' }}
          scrollWheelZoom
        >
          <MapResize />
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {filteredAreas.map((area) => {
            const risk = scenarioRisk(area.risk);

            return (
              <CircleMarker
                key={area.name}
                center={area.position}
                radius={20}
                pathOptions={{
                  color: colors[risk],
                  fillColor: colors[risk],
                  fillOpacity: 0.55,
                  weight: 2,
                }}
              >
                <Popup>
                  <strong>{area.name}</strong>
                  <br />
                  Scenario risk: <strong>{risk}</strong>
                  <br />
                  {area.reason}
                  <br />
                  <small>Simulated indicator — not an official forecast.</small>
                </Popup>
              </CircleMarker>
            );
          })}
        </MapContainer>
      </div>

      <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', marginTop: 16 }}>
        {Object.entries(colors).map(([risk, color]) => (
          <span key={risk} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <span
              style={{
                display: 'inline-block',
                width: 12,
                height: 12,
                borderRadius: '50%',
                background: color,
              }}
            />
            {risk}
          </span>
        ))}
      </div>

      <div className="notice" style={{ marginTop: 16 }}>
        <span>
          Demo only: locations and risk levels are illustrative, not verified
          flood predictions. Rainfall scenarios change the display using
          simple rules, not a trained flood-prediction model.
        </span>
      </div>
    </section>
  );
}
