from artistStats import getArtistStats
from roleChecker import RoleChecker
from userStats import getUserStats
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/artists/stats")
def artistStats(current_user: dict = Depends(RoleChecker(["artist"]))):
    return getArtistStats(current_user["user"].id)


@app.get("/users/stats")
def userStats(current_user: dict = Depends(RoleChecker(["user"]))):
    return getUserStats(current_user["user"].id)
