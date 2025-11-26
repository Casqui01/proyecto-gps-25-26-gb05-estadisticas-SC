from artistStats import getArtistStats
from fastapi import FastAPI

app = FastAPI()


@app.get("/artist/{uuid}/stats")
def artistStats(uuid: str):
    return getArtistStats(uuid)


@app.get("/user/{uuid}/stats")
def userStats(uuid: str):
    return getUserStats(uuid)
