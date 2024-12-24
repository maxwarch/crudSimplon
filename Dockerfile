FROM python:3.12-slim-bookworm AS dev

RUN echo "config dev"
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

RUN apt-get update
RUN apt-get install -y \ 
    curl \
    gnupg2 && \
    pip install --upgrade pip

# Installer les dépendances de développement
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# ODBC
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
RUN curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN exit
RUN apt-get update
RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN apt-get update
RUN apt-get install -y unixodbc

COPY . .