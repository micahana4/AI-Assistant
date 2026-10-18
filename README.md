# AI Assistant

A Django web app that helps students with class questions using the Gemini API. It includes a Progressive Web App (PWA) manifest and service worker for installation and basic offline support.

## Features

- Sends student prompts to the Django backend, which calls the Gemini API. The API key stays on the server.
- Uses the `gemini-3.8-flash` model and gives it a classroom-focused system instruction.
- Includes an installable Progressive Web App (PWA) manifest, app icons, and a service worker that caches the app shell.
- Shows online/offline status. Gemini answers need an internet connection.

## Requirements

- Python 3.9 or newer
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)


## Run locally

1. Open the `projectsite` folder and install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

2. Create a `.env` file in `projectsite` with your Gemini API key:

   ```env
   GEMINI_API_KEY=your_api_key
   ```

3. Start the server:

   ```sh
   python manage.py runserver
   ```

4. Visit <http://127.0.0.1:8000>.

The app needs an internet connection to get AI answers. Keep your API key private and out of frontend code and public repositories.

## Install the PWA

Deploy the app to a host that serves it over HTTPS, configure Django's `ALLOWED_HOSTS` for the deployed domain, and configure the host to serve Django static files from `projectsite/static/` at `/static/`.

The PWA resources are:

- Manifest: `/static/manifest.json`
- Service worker: `/service-worker.js` (served at the site root so it can control the app page)
- Icons: `/static/icons/icon-192.png` and `/static/icons/icon-512.png`

Open the HTTPS site in a supported mobile browser and use its **Install app** or **Add to Home screen** option. On Android Chrome, the in-page install button appears when Chrome signals that installation is available. On iPhone, use Safari's **Share → Add to Home Screen**.

## Project structure

```text
projectsite/
├── assistant/                 # Django views and URL routes
├── projectsite/               # Django settings and root URLs
├── static/
│   ├── icons/                  # PWA app icons
│   ├── manifest.json           # PWA metadata
│   └── service-worker.js       # Offline app-shell caching
├── templates/assistant.html    # Chat interface and client-side behavior
├── manage.py
└── requirements.txt
```

## Notes

- Keep `GEMINI_API_KEY` private. Do not put it in browser JavaScript or commit `.env` to source control.
- Gemini free-tier quotas are limited. A `429 RESOURCE_EXHAUSTED` response means the project's current quota or rate limit has been reached; check the active limits in [Google AI Studio](https://aistudio.google.com/rate-limit).
- Before production deployment, set `DEBUG = False` and configure a strong Django `SECRET_KEY` and the correct `ALLOWED_HOSTS` for your domain.