# --- build: aiogram is installed from git, so git is needed only here ---
FROM python:3.12-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- runtime ---
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY --from=build /install /usr/local
WORKDIR /app
# The bot sends the already built widget; src/ and minify.py are not needed in the image
COPY doom_bot.py themes.py ./
COPY widgets/ widgets/
RUN useradd --create-home --uid 1000 bot
USER bot
CMD ["python", "doom_bot.py"]
