FROM python:3.10.6-slim-bullseye

WORKDIR /app

# COPY . .

# CMD ["python", "main.py"]

# RUN apt-get update && apt-get install -y netcat

# RUN pip install --upgrade pip "poetry==1.5.1"
# RUN poetry config virtualenvs.create false --local

# COPY poetry.lock pyproject.toml ./

# RUN poetry install --no-ansi --only main

# COPY . .

# RUN chmod +x ./prestart.sh
# ENTRYPOINT ["./prestart.sh"]
# CMD ["python", "music_events_bot.py"]
