# ODMTP  (TPF Server)

## Requirements
- **Python 3.12**

## How to Launch ODMTP

### 1. Setup Environment Variables

Copy the example `.env` file to create your own configuration:
```bash
cp .env.example .env
```

Edit the `.env` file to set up your environment variables:
- `SECRET_KEY` – Your Django secret key.
- `DEBUG` – Set to `False` for production or `True` for development.
- `HOST` – The host address to bind to (e.g., `127.0.0.1` for local use or `0.0.0.0` to expose externally).
- `PORT` – The port for the Django server (default: `8000`).
- `BEACON_API_URL` – URL for the Beacon API endpoint (e.g., `http://127.0.0.1:5050/api/g_variants`).

### 2. Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Launch the Django Web Server

Start the development server:
```bash
python manage.py runserver
```

The TPF server will be available at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

### Using Docker

Alternatively, you can run ODMTP with Docker.

1. At the root of the project directory, execute:
   ```bash
   docker compose up -d
   ```

2. Docker will:
   - Build the required containers.
   - Launch ODMTP automatically.

3. **Important Notes**:
   - Ensure the Docker network specified in the `docker-compose.yaml` file matches the Beacon's network.
   - If Beacon is running on a different network or location, set the network mode to `host` and update the environment variables in the `docker-compose.yaml` file accordingly.

The TPF server will run at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Comunica Web Client

For querying with the [Comunica web client](http://query.linkeddatafragments.org/), set your data source to:
```
http://127.0.0.1:8000/beacon/query
```

---
You can extend odmtp for other APIs by creating a new package that will use the same structure as the beacon one.
---

## About

This project is an improved fork of [odmtp-tpf](https://github.com/benj-moreau/odmtp-tpf), developed by Benjamin MOREAU ([@benj-moreau](https://github.com/benj-moreau)).