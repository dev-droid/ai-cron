# Docker Compose Quick Start Guide

## Quick Start

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## Configuration

### Environment Variables

Edit `docker-compose.yml` to configure:

1. **Proxy Settings** (for regions like China):
   ```yaml
   environment:
     - AICRON_PROXY=http://host.docker.internal:7890
     - HTTP_PROXY=http://host.docker.internal:7890
     - HTTPS_PROXY=http://host.docker.internal:7890
   ```

2. **API Keys**:
   ```yaml
   environment:
     - GEMINI_API_KEY=your_key_here
     - OPENAI_API_KEY=your_key_here
     - ANTHROPIC_API_KEY=your_key_here
   ```

### Using Local Ollama

**Option 1: Connect to Host Ollama**
```yaml
ai-cron:
  network_mode: host
  # This allows accessing Ollama on host's localhost:11434
```

**Option 2: Run Ollama in Docker**
Uncomment the `ollama` service section in `docker-compose.yml`:
```bash
# Pull Ollama model first
docker-compose exec ollama ollama pull llama3

# Restart ai-cron to detect Ollama
docker-compose restart ai-cron
```

## Accessing the Web UI

After starting, open your browser:
- **URL**: http://localhost:8080

## Troubleshooting

### Check container status
```bash
docker-compose ps
```

### View application logs
```bash
docker-compose logs ai-cron
```

### Restart services
```bash
docker-compose restart
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

## Production Deployment

For production use:

1. **Use environment file**:
   Create `.env` file:
   ```env
   GEMINI_API_KEY=your_key
   OPENAI_API_KEY=your_key
   AICRON_PROXY=http://your-proxy:port
   ```

2. **Update docker-compose.yml**:
   ```yaml
   env_file:
     - .env
   ```

3. **Enable HTTPS** (recommended):
   Add nginx reverse proxy with SSL

## Volume Management

**Persistent data locations**:
- Cron jobs: `cron-data` volume
- Ollama models: `ollama-data` volume (if using Ollama service)

**Backup volumes**:
```bash
docker run --rm -v ai-cron_cron-data:/data -v $(pwd):/backup busybox tar czf /backup/cron-backup.tar.gz /data
```
