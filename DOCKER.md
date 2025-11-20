# Docker Deployment Guide

This guide explains how to build and run DocuGener using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start the container:**
   ```bash
   docker-compose up -d --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:5100
   - Backend API: http://localhost:5000

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t docugener:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name docugener \
     -p 5000:5000 \
     -p 5100:5100 \
     -v $(pwd)/data/captures:/app/backend/captures \
     -v $(pwd)/data/database:/app/backend \
     docugener:latest
   ```

3. **Access the application:**
   - Frontend: http://localhost:5100
   - Backend API: http://localhost:5000

## Important Notes

### Screenshot Capture Limitations

**Important:** DocuGener is designed as a desktop application that captures screenshots and detects mouse clicks. When running in a Docker container:

- **Screenshot capture will NOT work** in a standard container environment because:
  - Containers don't have direct access to the host's display
  - Mouse click detection requires system-level input access
  - The application needs to interact with the desktop environment

### Use Cases for Containerized Deployment

The Docker container is useful for:
- **Development and testing** of the web interface
- **API testing** and integration
- **Deployment scenarios** where you only need the web interface
- **CI/CD pipelines** for automated testing

### Running with Display Access (Linux)

If you're running on Linux and want to enable screenshot capture, you can:

1. **Install X11 forwarding support:**
   ```bash
   xhost +local:docker
   ```

2. **Run with X11 socket:**
   ```bash
   docker run -d \
     --name docugener \
     -p 5000:5000 \
     -p 5100:5100 \
     -e DISPLAY=$DISPLAY \
     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
     -v $(pwd)/data/captures:/app/backend/captures \
     docugener:latest
   ```

3. **Note:** This still has limitations and may not work perfectly for all screenshot capture scenarios.

### Windows/Mac Considerations

On Windows and macOS, running screenshot capture in Docker is even more challenging due to:
- Different display server architectures
- Security restrictions
- Limited X11 support

**Recommendation:** For full functionality, run DocuGener natively on your operating system rather than in a container.

## Data Persistence

The Docker setup uses volumes to persist:
- **Captures:** Stored in `./data/captures/`
- **Database:** Stored in `./data/database/`

Make sure these directories exist or Docker will create them.

## Environment Variables

You can customize the deployment with environment variables:

```yaml
environment:
  - DISPLAY=:99          # Virtual display
  - PYTHONUNBUFFERED=1   # Python output buffering
  - FLASK_ENV=production # Flask environment
```

## Troubleshooting

### Container won't start
- Check logs: `docker-compose logs`
- Ensure ports 5000 and 5100 are not in use
- Verify Docker has sufficient resources

### Can't access the web interface
- Check if ports are correctly mapped
- Verify firewall settings
- Check container logs for errors

### Screenshot capture not working
- This is expected in containerized environments
- Use native installation for full functionality
- See "Screenshot Capture Limitations" above

## Building for Production

For production deployments, consider:

1. **Multi-stage builds** (already implemented)
2. **Security scanning:**
   ```bash
   docker scan docugener:latest
   ```

3. **Resource limits:**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 2G
   ```

4. **Health checks:**
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:5000/api/status"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```

## Support

For issues related to Docker deployment, please check:
- Container logs
- Volume permissions
- Port conflicts
- System requirements

For full functionality, use the native installation method described in the main README.

