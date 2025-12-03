import os
import requests
from dotenv import load_dotenv
from supabaseAuth import gestor_token
from fastapi import HTTPException, status

def getUserStats (uuid: str):
    load_dotenv()

    token: str = gestor_token.get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # TOTAL GASTADO
    url = f"{os.getenv("COMPRAS_SERVICE_BASE_URL")}/orders"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        totalGastado = 0
        for order in data:
            orderStatus = order.get("status")
            if orderStatus != 'cancelled' and orderStatus != 'pending_payment':
                orderUserUuid = order.get("userUuid")
                if orderUserUuid == uuid:
                    total_price = order.get("totalPrice")
                    totalGastado += total_price
                    # print(totalGastado)

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # MINUTOS ESCUCHADOS TOTALES
    url = f"{os.getenv("CONTENIDOS_SERVICE_BASE_URL")}/users/{uuid}/library"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        totalEscuchado = 0
        for product in data:
            productType = product.get("type")
            if productType == 'Song':
                item = product.get("item")
                duration = item.get("duration")
                plays = item.get("plays")
                totalEscuchado += duration * plays
                # print(totalEscuchado)
            elif productType == 'Album':
                item = product.get("item")
                songs = item.get("songs", [])
                for song in songs:
                    duration = song.get("duration")
                    plays = song.get("plays")
                    totalEscuchado += duration * plays
                    # print(totalEscuchado)

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # TOP 5 CANCIONES MÁS ESCUCHADAS
    url = f"{os.getenv("CONTENIDOS_SERVICE_BASE_URL")}/users/{uuid}/library"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        duracionTotal = 0
        cancionesMasEscuchadas = []
        for product in data:
            productType = product.get("type")
            if productType == 'Song':
                item = product.get("item")
                duration = item.get("duration")
                plays = item.get("plays")
                duracionTotal += duration * plays
                cancion = (item, duracionTotal)
                cancionesMasEscuchadas.append(cancion)
            elif productType == 'Album':
                item = product.get("item")
                songs = item.get("songs", [])
                for song in songs:
                    duration = song.get("duration")
                    plays = song.get("plays")
                    duracionTotal += duration * plays
                    cancion = (song, duracionTotal)
                    cancionesMasEscuchadas.append(cancion)
        cancionesMasEscuchadas.sort(key=lambda x: x[1], reverse=True)
        cancionesMasEscuchadas = cancionesMasEscuchadas[:5]

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    #TOP 5 ARTISTAS MÁS ESCUCHADOS
    url = f"{os.getenv("CONTENIDOS_SERVICE_BASE_URL")}/users/{uuid}/library"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        duracionTotal = 0
        artistasMasEscuchados = []
        for product in data:
            productType = product.get("type")
            if productType == 'Song':
                item = product.get("item")
                duration = item.get("duration")
                plays = item.get("plays")
                duracionTotal += duration * plays
                artist = item.get("author")
                if not any(c[0] == artist for c in artistasMasEscuchados):
                    artista = (artist, duracionTotal)
                    artistasMasEscuchados.append(artista)
                else:
                    for i, (artistX, tiempo_total) in enumerate(artistasMasEscuchados):
                        if artistX == artist:
                            artistasMasEscuchados[i] = (artistX, tiempo_total + duracionTotal)
                            break
            elif productType == 'Album':
                item = product.get("item")
                songs = item.get("songs", [])
                for song in songs:
                    duration = song.get("duration")
                    plays = song.get("plays")
                    duracionTotal += duration * plays
                    artist = item.get("author")
                    artista = (artist, duracionTotal)
                    if not any(c[0] == artist for c in artistasMasEscuchados):
                        artista = (artist, duracionTotal)
                        artistasMasEscuchados.append(artista)
                    else:
                        for i, (artistX, tiempo_total) in enumerate(artistasMasEscuchados):
                            if artistX == artist:
                                artistasMasEscuchados[i] = (artistX, tiempo_total + duracionTotal)
                                break
        artistasMasEscuchados.sort(key=lambda x: x[1], reverse=True)
        artistasMasEscuchados = artistasMasEscuchados[:5]

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return {
        "totalGastado": totalGastado,
        "totalEscuchado": totalEscuchado,
        "cancionesMasEscuchadas": cancionesMasEscuchadas,
        "artistasMasEscuchados": artistasMasEscuchados,
    }