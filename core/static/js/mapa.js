document.addEventListener("DOMContentLoaded", function () {

    const elemento = document.getElementById("map");

    if (!elemento) return;

    const latitude = parseFloat(elemento.dataset.lat);
    const longitude = parseFloat(elemento.dataset.lng);

    const mapa = L.map("map").setView([latitude, longitude], 15);

  L.tileLayer(
    'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }
).addTo(mapa);

    L.marker([latitude, longitude])
        .addTo(mapa)
        .bindPopup("Local do registro")
        .openPopup();

});