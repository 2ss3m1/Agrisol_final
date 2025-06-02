// websocket.js

// Connexion WebSocket au serveur Django Channels
const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsUrl = `${wsProtocol}://${window.location.host}/ws/sensor-data/`;
const socket = new WebSocket(wsUrl);

const charts = {};

// Fonction pour créer un graphique Chart.js
function createChart(ctx, label) {
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: label,
        data: [],
        borderColor: 'rgba(54, 162, 235, 0.8)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        fill: true,
        tension: 0.3,
        pointRadius: 2,
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: { display: true, title: { display: true, text: 'Temps' } },
        y: { display: true, beginAtZero: true }
      }
    }
  });
}

// Fonction pour traduire le code IA en message clair
function getRecommendationMessage(code) {
  switch (parseInt(code)) {
    case 1: return "💧 Irrigation recommandée : le sol est trop sec ou chaud.";
    case 2: return "💨 Ventilation recommandée : conditions trop humides ou chaudes.";
    case 3: return "⚗️ Correction du pH recommandée : valeur hors plage optimale.";
    case 4: return "💡 Ajustement de la lumière recommandé : intensité non optimale.";
    case 5: return "🫧 Ajustement du CO₂ recommandé : concentration anormale.";
    case 0: return "✅ Aucune action nécessaire : conditions optimales.";
    default: return "ℹ️ Recommandation IA : donnée inconnue.";
  }
}

// Initialisation des graphiques après chargement du DOM
document.addEventListener('DOMContentLoaded', () => {
  charts.humidity = createChart(document.getElementById('chartH').getContext('2d'), 'Humidité');
  charts.ph = createChart(document.getElementById('chartP').getContext('2d'), 'PH');
  charts.co2 = createChart(document.getElementById('chartC').getContext('2d'), 'CO2');
  charts.light = createChart(document.getElementById('chartL').getContext('2d'), 'Lumière');
  charts.temperature = createChart(document.getElementById('chartT').getContext('2d'), 'Température');
  charts.water = createChart(document.getElementById('chartN').getContext('2d'), "Niveau d'eau");

  // Gestion des commandes ventilateur et irrigation via WebSocket
  document.getElementById('fan-on').addEventListener('click', () => {
    socket.send(JSON.stringify({ action: 'fan_on' }));
  });
  document.getElementById('fan-off').addEventListener('click', () => {
    socket.send(JSON.stringify({ action: 'fan_off' }));
  });
  document.getElementById('irrigation-on').addEventListener('click', () => {
    socket.send(JSON.stringify({ action: 'irrigation_on' }));
  });
  document.getElementById('irrigation-off').addEventListener('click', () => {
    socket.send(JSON.stringify({ action: 'irrigation_off' }));
  });
});

// Réception des données via WebSocket et mise à jour des graphiques et statuts
socket.onmessage = function(event) {
  const data = JSON.parse(event.data);
  const sensorData = data.sensor_data || data;
  const timestamp = new Date().toLocaleTimeString();

  if (sensorData.humidity !== undefined) {
      document.querySelector('.metric-card.humidity h2').innerHTML = `${sensorData.humidity} <span>g/m³</span>`;
    }
    if (sensorData.ph !== undefined) {
      document.querySelector('.metric-card.ph h2').textContent = sensorData.ph;
    }
    if (sensorData.co2 !== undefined) {
      document.querySelector('.metric-card.co2 h2').innerHTML = `${sensorData.co2} <span>g/m³</span>`;
    }
    if (sensorData.light !== undefined) {
      document.querySelector('.metric-card.light h2').innerHTML = `${sensorData.light} <span>lux</span>`;
    }
    if (sensorData.temperature !== undefined) {
      document.querySelector('.metric-card.temperature h2').innerHTML = `${sensorData.temperature} <span>°C</span>`;
    }
    if (sensorData.waterLevel !== undefined) {
      document.querySelector('.metric-card.water h2').innerHTML = `${sensorData.waterLevel} <span>Pa</span>`;
    }
    
  // Fonction pour mettre à jour un graphique donné
  function updateChart(chart, value) {
    if (chart) {
      chart.data.labels.push(timestamp);
      chart.data.datasets[0].data.push(parseFloat(value));
      if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
      }
      chart.update();
    }
  }

  // Mise à jour des graphiques si la donnée existe
  if (sensorData.temperature !== undefined) updateChart(charts.temperature, sensorData.temperature);
  if (sensorData.humidity !== undefined) updateChart(charts.humidity, sensorData.humidity);
  if (sensorData.waterLevel !== undefined) updateChart(charts.water, sensorData.waterLevel);
  if (sensorData.ph !== undefined) updateChart(charts.ph, sensorData.ph);
  if (sensorData.co2 !== undefined) updateChart(charts.co2, sensorData.co2);
  if (sensorData.light !== undefined) updateChart(charts.light, sensorData.light);

  // Mise à jour statut ventilateur
  if (data.fan_status !== undefined) {
    const fanOnBtn = document.getElementById('fan-on');
    const fanOffBtn = document.getElementById('fan-off');
    const fanStatus = document.getElementById('fan-status');
    if (data.fan_status) {
      fanStatus.classList.add('active', 'text-success');
      fanStatus.classList.remove('text-danger');
      fanStatus.querySelector('span').textContent = 'Ventilateur actif';
      fanOnBtn.classList.add('btn-active');
      fanOffBtn.classList.remove('btn-active');
    } else {
      fanStatus.classList.remove('active', 'text-success');
      fanStatus.classList.add('text-danger');
      fanStatus.querySelector('span').textContent = 'Ventilateur inactif';
      fanOffBtn.classList.add('btn-active');
      fanOnBtn.classList.remove('btn-active');
    }
  }

  // Mise à jour statut irrigation
  if (data.irrigation_status !== undefined) {
    const irrigationOnBtn = document.getElementById('irrigation-on');
    const irrigationOffBtn = document.getElementById('irrigation-off');
    const irrigationStatus = document.getElementById('irrigation-status');
    if (data.irrigation_status) {
      irrigationStatus.classList.add('active', 'text-success');
      irrigationStatus.classList.remove('text-danger');
      irrigationStatus.querySelector('span').textContent = 'Irrigation active';
      irrigationOnBtn.classList.add('btn-active');
      irrigationOffBtn.classList.remove('btn-active');
    } else {
      irrigationStatus.classList.remove('active', 'text-success');
      irrigationStatus.classList.add('text-danger');
      irrigationStatus.querySelector('span').textContent = 'Irrigation inactive';
      irrigationOffBtn.classList.add('btn-active');
      irrigationOnBtn.classList.remove('btn-active');
    }
  }

  // === Affichage dynamique de la recommandation IA ===
  if (data.recommendations !== undefined) {
    const recElem = document.getElementById('ia-recommendation');
    if (recElem) {
      recElem.textContent = getRecommendationMessage(data.recommendations);
    }
  }
};
