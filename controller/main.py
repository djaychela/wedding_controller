from fastapi import FastAPI

from . import models
from .database import engine

from .routers import users, songs, gradients, effects, ledfx, state, dancefloor

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(songs.router)
app.include_router(gradients.router)
app.include_router(effects.router)
app.include_router(ledfx.router)
app.include_router(state.router)
app.include_router(dancefloor.router)

