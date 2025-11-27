import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from supabaseAuth import get_token

def getArtistStats (uuid: str):
    load_dotenv()

    token:str = get_token()
    #COMPROBAR QUE ES ARTISTA Y QUE EXISTE
    url = f"{os.getenv("USUARIOS_SERVICE_BASE_URL")}/users/{uuid}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"  # Opcional, pero buena práctica
    }
    try:
        response = requests.get(url,headers=headers, timeout=5)
        response.raise_for_status()  # Lanza excepción si status >= 400
        data =  response.json()

        if data.get("role") != 'artist':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,  # Es igual a 400
                detail="El UUID proporcionado no es válido para el cálculo de estadísticas."
            )

    except requests.exceptions.RequestException as e:
        print(f"Error al llamar al microservicio de usuarios: {e}")
        return None

    #TOTAL SEGUIDORES
    url = f"{os.getenv("CONTENIDOS_SERVICE_BASE_URL")}/artists/{uuid}"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Lanza excepción si status >= 400
        data = response.json()

        # TOTAL SEGUIDORES
        nFollowers = len(data.get("followers",[]))

        #TOTAL REPRODUCCIONES
        #print(nFollowers)

    except requests.exceptions.RequestException as e:
        print(f"Error al llamar al microservicio de contenidos: {e}")
        return None

    #TOTAL INGRESOS Y PRODUCTOS VENDIDOS
    url = f"{os.getenv("COMPRAS_SERVICE_BASE_URL")}/orders"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Lanza excepción si status >= 400
        data = response.json()

        earn = 0
        totalPlays = 0

        totalCds = 0
        totalVinyls = 0
        totalCassettes = 0
        totalDigitals = 0

        totalSongs = 0
        totalAlbums = 0
        totalMerch = 0
        for order in data:
            items = order.get("items",[])

            for product in items:
                productUuid = product.get("uuid")
                type = product.get("type")
                priceItem = product.get("price")
                quantity = product.get("quantity")
                format = product.get("format")
                plays = product.get("plays")

                if type == "song":
                    urlType = f"{os.getenv("CONTENIDOS_SERVICE_BASE_URL")}/songs/{productUuid}"
                elif type == "album":
                    urlType = f"{os.getenv("CONTENIDOS_SERVICE_BASE_URL")}/albums/{productUuid}"
                elif type == "merch":
                    urlType = f"{os.getenv("CONTENIDOS_SERVICE_BASE_URL")}/products/{productUuid}"

                responseType = requests.get(urlType, headers=headers, timeout=5)
                responseData = responseType.json()
                authorUuid = responseData.get("author").get("uuid")

                if uuid == authorUuid:
                    earn = earn + (priceItem * quantity)
                    totalPlays = totalPlays + plays

                    if type == "song": totalSongs += 1
                    if type == "album": totalAlbums += 1
                    if type == "merch": totalMerch += 1
                    if format == "cd": totalCds += 1
                    if format == "vinyl": totalVinyls += 1
                    if format == "cassette": totalCassettes += 1
                    if format == "digital": totalDigitals += 1

        print(earn)
        print(totalSongs)
        print(totalAlbums)
        print(totalMerch)
        print(totalCds)
        print(totalVinyls)
        print(totalCassettes)
        print(totalDigitals)
    except requests.exceptions.RequestException as e:
        print(f"Error al llamar al microservicio de contenidos: {e}")
        return None


