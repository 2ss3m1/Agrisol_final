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
  const timestamp = new Date().toLocaleTimeString();

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
  if (data.temperature !== undefined) updateChart(charts.temperature, data.temperature);
  if (data.humidity !== undefined) updateChart(charts.humidity, data.humidity);
  if (data.waterLevel !== undefined) updateChart(charts.water, data.waterLevel);
  if (data.ph !== undefined) updateChart(charts.ph, data.ph);
  if (data.co2 !== undefined) updateChart(charts.co2, data.co2);
  if (data.light !== undefined) updateChart(charts.light, data.light);

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
};
