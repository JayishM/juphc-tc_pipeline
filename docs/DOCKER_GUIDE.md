# Docker Guide: Tax Calculator Application

This guide provides instructions for building, running, inspecting, and troubleshooting the Docker container for the Tax Calculator application.

---

## 1. Prerequisites

Before getting started, ensure you have the following installed and running on your system:
- **Docker Desktop** (macOS / Windows) or **Docker Engine** (Linux).
  - Verify installation:
    ```bash
    docker --version
    docker compose version
    ```
- **Docker Daemon Running**: Ensure Docker Desktop is active or the service is started (`sudo systemctl status docker`).

---

## 2. Docker Architecture Overview

The Tax Calculator uses a production-ready, lightweight Docker container:
- **Base Image**: `node:18-alpine` (~170MB uncompressed, ~50MB compressed).
- **Security**: Runs under the unprivileged `node` user (UID 1000).
- **Dependencies**: Only production dependencies installed via `npm ci --omit=dev`.
- **Healthcheck**: Built-in container probe querying `http://localhost:3000/health`.
- **Exposed Port**: Configurable via `PORT` environment variable (defaults to `3000`).

---

## 3. Building the Docker Image

From the project root directory (`tax-calculator/`), execute:

```bash
docker build -t tax-calculator:latest .
```

To build with a specific version tag:

```bash
docker build -t tax-calculator:v1 .
```

### Build Arguments and Caching
Docker utilizes layer caching. To perform a clean build without cache:

```bash
docker build --no-cache -t tax-calculator:latest .
```

---

## 4. Listing and Inspecting the Docker Image

Verify that the image is registered in your local Docker engine:

```bash
# List images matching 'tax-calculator'
docker images tax-calculator

# Inspect image metadata, labels, and entrypoint
docker inspect tax-calculator:latest

# View layer history and sizes
docker history tax-calculator:latest
```

---

## 5. Running the Application in a Container

### 5.1 Run in Detached Mode (Background)

```bash
docker run -d \
  --name tax-calculator \
  -p 3000:3000 \
  --restart unless-stopped \
  tax-calculator:latest
```

### 5.2 Command Options Explained
- `-d`: Run container in detached mode (background).
- `--name tax-calculator`: Assigns a readable container name.
- `-p 3000:3000`: Maps port 3000 on the host to port 3000 in the container (`<host_port>:<container_port>`).
- `--restart unless-stopped`: Automatically restarts container if it crashes.

### 5.3 Custom Port Mapping
If host port 3000 is occupied, you can map to another port (e.g. 8080):

```bash
docker run -d \
  --name tax-calculator \
  -p 8080:3000 \
  -e PORT=3000 \
  tax-calculator:latest
```

---

## 6. Accessing and Verifying the Application

### 6.1 Web Browser Access
Open your browser to:
- **Web UI**: [http://localhost:3000](http://localhost:3000) (or `http://localhost:8080` if using custom port)

### 6.2 Health Endpoint Verification
Verify the system status via `curl`:

```bash
curl -i http://localhost:3000/health
```

Expected output:
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{"status":"UP","service":"tax-calculator","version":"1.0.0","uptime":12.3,"timestamp":"..."}
```

### 6.3 API Calculation Test
Verify backend calculation via `curl`:

```bash
curl -X POST http://localhost:3000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"income": 60000, "deductions": 5000}'
```

Expected output:
```json
{"grossIncome":60000,"deductions":5000,"taxableIncome":55000,"tax":6000,"netIncome":54000,"effectiveRate":10}
```

---

## 7. Container Management & Lifecycle

```bash
# View running containers
docker ps

# View container logs
docker logs tax-calculator

# Follow container logs in real time
docker logs -f tax-calculator

# Check container resource usage (CPU/Memory)
docker stats tax-calculator --no-stream

# Stop the container
docker stop tax-calculator

# Start a stopped container
docker start tax-calculator

# Remove the container
docker rm -f tax-calculator
```

---

## 8. Troubleshooting Common Docker Errors

### Issue 1: Port already allocated (`bind: address already in use`)
- **Cause**: Another service or previous container is using port 3000.
- **Solution**:
  ```bash
  # Find what is using port 3000
  lsof -i :3000
  # Or run the container on an alternate port
  docker run -d --name tax-calculator -p 3001:3000 tax-calculator:latest
  ```

### Issue 2: `docker: Cannot connect to the Docker daemon`
- **Cause**: Docker Desktop is not running or current user lacks docker group permissions.
- **Solution**:
  - Launch Docker Desktop from `/Applications/Docker.app` (macOS) or start service on Linux: `sudo systemctl start docker`.
  - On Linux, add your user to the docker group: `sudo usermod -aG docker $USER`.

### Issue 3: Container exits immediately after start
- **Cause**: Application startup script failed or syntax error occurred.
- **Solution**:
  ```bash
  # Check failure logs
  docker logs tax-calculator
  
  # Run container interactively to debug
  docker run -it --rm tax-calculator:latest /bin/sh
  ```

---

## 9. Alternative Nginx Static Container (Reference Lab)

If you are following the static Nginx lab variant from the IBM DevOps curriculum:
```bash
# Build using the static Nginx configuration
docker build -f 02-dockerfile -t tax-calculator:nginx-v1 .

# Run on port 8080
docker run -d -p 8080:80 --name tax-calculator-nginx tax-calculator:nginx-v1
```
Both containerization workflows are fully supported in this repository.
