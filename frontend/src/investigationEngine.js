
export function investigateWaterRisk({ weather = [], sensors = [] } = {}) {
  const findings = [];

  // Check the latest available weather record.
  const latestWeather = weather.length
    ? weather[weather.length - 1]
    : null;

  if (latestWeather) {
    const temperature =
      latestWeather.apparent_temperature_max_c ??
      latestWeather.temperature_max_c;

    const rainfall = latestWeather.precipitation_mm;

    if (Number.isFinite(temperature)) {
      findings.push({
        type: "weather",
        status: temperature >= 35 ? "attention" : "observed",
        finding: `Apparent or maximum temperature: ${temperature}°C.`,
        evidence: "Open-Meteo weather record",
      });
    }

    if (Number.isFinite(rainfall)) {
      findings.push({
        type: "rainfall",
        status: rainfall < 1 ? "attention" : "observed",
        finding: `Recorded precipitation: ${rainfall} mm.`,
        evidence: "Open-Meteo weather record",
      });
    }
  } else {
    findings.push({
      type: "weather",
      status: "missing",
      finding: "No weather records were provided.",
      evidence: "Weather data required",
    });
  }

  // Flagged sensor records are clues, not proof of a leak.
  const flaggedSensors = sensors.filter((sensor) => {
    const score = Number(sensor.score);
    return Number.isFinite(score) && score >= 80;
  });

  findings.push({
    type: "network",
    status: flaggedSensors.length ? "attention" : "observed",
    finding: `${flaggedSensors.length} sensor records meet the demo score threshold of 80.`,
    evidence: "Sensor score rule; verify against real benchmark labels",
  });

  return {
    title: "Water risk investigation",
    conclusion:
      "These findings are screening signals, not proof of a water shortage or leak.",
    findings,
    recommendedAction:
      flaggedSensors.length > 0
        ? "Review flagged records and verify them against sensor location, time, and benchmark labels."
        : "Collect verified sensor data and continue monitoring weather conditions.",
  };
}
