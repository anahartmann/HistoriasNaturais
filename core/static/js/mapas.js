document.addEventListener("DOMContentLoaded", function () {

    if (typeof registros === "undefined" || registros.length === 0)
        return;

    // cria o mapa
    const mapa = L.map("map2");

    // tiles
    L.tileLayer(
        "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        {
            attribution: "&copy; OpenStreetMap &copy; CARTO",
            maxZoom: 20
        }
    ).addTo(mapa);



    const marcadores = [];


    registros.forEach(registro => {
        const tamanho = registro.atual ? 70 : 50;

        const icone = L.divIcon({
            html: `
        <img src="${registro.foto}"
             style="
                width:${tamanho}px;
                height:${tamanho}px;
                border-radius:50%;
                border:4px solid ${registro.atual ? "#16a34a" : "white"};
                object-fit:cover;
                box-shadow:0 2px 8px rgba(0,0,0,.4);
             ">
    `,
            className: "",
            iconSize: [tamanho, tamanho],
            iconAnchor: [tamanho / 2, tamanho / 2]
        });

        const marcador = L.marker(
            [registro.latitude, registro.longitude],
            { icon: icone }
        ).addTo(mapa);

        if (registro.atual) {

            marcador.bindPopup(`
                <b>${registro.especie}</b><br>
                ${registro.nome}<br><br>
                <b>Registro atual</b>
            `);

        } else {

            marcador.bindPopup(`
                ${registro.foto ? `<img src="${registro.foto}" style="width:100%;border-radius:8px;margin-bottom:8px;">` : ""}
                <b>${registro.especie}</b><br>
                ${registro.nome}<br><br>
                ${registro.fenomeno}<br>

                <a href="/fauna/${registro.id}/">
                    Ver registro
                </a>
            `);

        }

        

        marcadores.push(marcador);

    });

    const grupo = L.featureGroup(marcadores);

    mapa.fitBounds(grupo.getBounds(), {
        padding: [40, 40]
    });

});