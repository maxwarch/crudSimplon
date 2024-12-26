import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()


async def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv('API_USERNAME')
    correct_password = os.getenv('API_PASSWORD')  # **NE JAMAIS** mettre un mot de passe en dur en production !

    if credentials.username == correct_username and credentials.password == correct_password:
        return credentials.username
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
