from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import diary, user, entry, exercise
import json
import logging
import sys

description = """
Exercise Diary is the one stop place to store and catalog excersizes and progress.
"""

app = FastAPI(
    title="Exercise Diary",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Andrew Ji, Alexander Jung, Dennis Phun, Jack Colt",
        "email": "aeji@calpoly.edu, ajung04@calpoly.edu, dphun@calpoly.edu, jcolt@calpoly.edu",
    },
)

app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(diary.router)
app.include_router(entry.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the Exercise Diary."}
