$path = ".\frontend\src\App.jsx"
Copy-Item $path "$path.backup" -Force
$content = Get-Content $path -Raw

if ($content -notmatch 'ML Prediction \(Experimental\)') {
  $state = @"
  const [mlResult, setMlResult] = useState(null);
  const [mlLoading, setMlLoading] = useState(false);
  const [mlError, setMlError] = useState('');

  async function runMlPrediction() {
    setMlLoading(true);
    setMlError('');
    setMlResult(null);
    const readings = {
      "Pressure 1 Out": 5.25,
      "Pressure 2 Out": 1.76,
      "Pressure 3 In": 0.79,
      "Pressure 4 In": 0.94,
      "Water Flow 1": 0.37,
      "Water Flow 2": 0.39,
      "Water Flow 3": 0.32,
      "WaterFlow 4": 0.43,
      "VFD 1": 37.9,
      "VFD 2": 0,
      "VFD 3": 40,
      "VFD 4-1": 0,
      "VFD 4-2": 60,
      "Analog Valve 1": 65.7,
      "Analog Valve 2": 62.6
    };
    readings["Water Flow 4"] = readings["WaterFlow 4"];
    delete readings["WaterFlow 4"];
    try {
      const response = await fetch('/api-ml/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ readings })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(JSON.stringify(data.detail || data));
      setMlResult(data);
    } catch (error) {
      setMlError(error.message || 'Could not reach the ML API');
    } finally {
      setMlLoading(false);
    }
  }

"@
  $content = $content -replace '  const \[rainWeight, setRainWeight\] = useState\(40\);\s*', "  const [rainWeight, setRainWeight] = useState(40);`r`n$state`r`n"
  $panel = @"
        <section className="panel" style={{ margin: '20px 0', padding: '20px' }}>
          <div className="eyebrow">EXPERIMENTAL MODEL</div>
          <h2>ML Prediction (Experimental)</h2>
          <p>Demo sensor readings only — not live Pune water-network data.</p>
          <button className="secondary-button" onClick={runMlPrediction} disabled={mlLoading}>
            {mlLoading ? 'Running prediction...' : 'Run ML Prediction'}
          </button>
          {mlError && <p role="alert">API error: {mlError}</p>}
          {mlResult && (
            <div style={{ marginTop: '12px' }}>
              <h3>{mlResult.interpretation}</h3>
              <p>Event probability: {(mlResult.event_probability * 100).toFixed(1)}%</p>
              <p><strong>Experimental only:</strong> {mlResult.warning}</p>
            </div>
          )}
        </section>

"@
  $content = $content -replace '        \{tab === ''simulator'' && \(', "$panel        {tab === 'simulator' && ("
  Set-Content -Path $path -Value $content -Encoding UTF8
  Write-Host "Added ML prediction panel. Backup: App.jsx.backup"
} else {
  Write-Host "ML panel marker already exists; no changes made."
}
