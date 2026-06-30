document.addEventListener("DOMContentLoaded", function () {

    if (typeof registros === "undefined" || registros.length === 0)
        return;

    const ehVideo = (url) => /\.(mp4|webm|ogg|mov|m4v|avi)$/i.test(url || "");

    const renderMidiaPopup = (url) => {
        if (!url) return "";

        if (ehVideo(url)) {
            return `
                <video controls preload="metadata" playsinline style="width:100%;border-radius:8px;margin-bottom:8px;">
                    <source src="${url}">
                </video>
            `;
        }

        return `<img src="${url}" style="width:100%;border-radius:8px;margin-bottom:8px;">`;
    };

    const mapa = L.map("map2");

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
        const corBorda = registro.atual ? "#16a34a" : "white";

        const icone = L.divIcon({
            html: ehVideo(registro.foto)
                ? `
                    <div style="
                        width:${tamanho}px;
                        height:${tamanho}px;
                        border-radius:50%;
                        border:4px solid ${corBorda};
                        background:#111;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:white;
                        box-shadow:0 2px 8px rgba(0,0,0,.4);
                        font-size:${tamanho * 0.4}px;
                    ">
                        ▶
                    </div>
                `
                : `
                    <img src="${registro.foto}"
                         style="
                            width:${tamanho}px;
                            height:${tamanho}px;
                            border-radius:50%;
                            border:4px solid ${corBorda};
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
                ${renderMidiaPopup(registro.foto)}
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
