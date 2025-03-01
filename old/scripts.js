// Initialisation de la carte Leaflet
var map = L.map('map').setView([10.7769, 106.7009], 12); // Centré sur Ho Chi Minh City

// Ajouter les tuiles OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Charger les appartements depuis Flask (API)
fetch('/api/apartments')
    .then(response => response.json())
    .then(data => {
        data.forEach(apartment => {
            // Ajouter un marqueur pour chaque appartement
            L.marker([apartment.lat, apartment.lng])
                .addTo(map)
                .bindPopup(`<b>${apartment.title}</b><br>Prix: ${apartment.price}€`);
        });
    })
    .catch(error => console.error("Erreur lors du chargement des données:", error));
