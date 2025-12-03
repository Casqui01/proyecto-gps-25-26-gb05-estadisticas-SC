from artistStats import get_artist_stats
from roleChecker import RoleChecker
from userStats import getUserStats
from fastapi import FastAPI, Depends
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
app = FastAPI()

EXPIRACION = 600  # segundos (10 minutos)


@app.get("/artists/stats")
def artistStats(current_user: dict = Depends(RoleChecker(["artist"]))):
    key = f"artist_stats:{current_user['user'].id}"

    cached = r.get(key)
    if cached:
        return json.loads(cached)

    stats = getArtistStats(current_user["user"].id)
    r.set(key, json.dumps(stats), ex=EXPIRACION)

    return stats


@app.get("/users/stats")
def userStats(current_user: dict = Depends(RoleChecker(["user"]))):
    key = f"user_stats:{current_user['user'].id}"

    cached = r.get(key)
    if cached:
        return json.loads(cached)

    stats = getUserStats(current_user["user"].id)
    r.set(key, json.dumps(stats), ex=EXPIRACION)

    return stats