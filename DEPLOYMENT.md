# 🚀 Multi-Agent AI System - Unified Deployment Guide

This guide covers deploying your Multi-Agent AI System as a unified Next.js application to Vercel. Everything runs in one container with Next.js serving both the frontend and API routes.

## 📋 Prerequisites

- Docker installed locally
- Vercel account
- API keys for:
  - NewsAPI
  - OpenAI
  - Weaviate Cloud

## 🐳 Local Testing with Docker

### 1. Prepare Environment Variables

```bash
# Copy the production environment template
cp env.production.example .env

# Edit .env with your actual API keys
nano .env
```

### 2. Build and Run Locally

```bash
# Build the Docker image
docker build -t multi-agent-ai .

# Run the container
docker run -p 3000:3000 -p 8000:8000 --env-file .env multi-agent-ai
```

### 3. Test with Docker Compose

```bash
# Start the application
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🌐 Vercel Deployment

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Configure Environment Variables

```bash
# Set your API keys in Vercel
vercel env add NEWS_API_KEY
vercel env add OPENAI_API_KEY
vercel env add WEAVIATE_URL
vercel env add WEAVIATE_API_KEY

# Set application settings
vercel env add ENVIRONMENT production
vercel env add DEBUG false
vercel env add CACHE_TTL 3600
```

### 4. Deploy to Vercel

```bash
# Deploy using Docker
vercel --prod

# Or deploy with specific configuration
vercel --prod --docker
```

### 5. Alternative: GitHub Integration

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard
4. Enable automatic deployments

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEWS_API_KEY` | NewsAPI key for news fetching | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI processing | Yes |
| `WEAVIATE_URL` | Weaviate Cloud instance URL | Yes |
| `WEAVIATE_API_KEY` | Weaviate Cloud API key | Yes |
| `ENVIRONMENT` | Environment (development/production) | No |
| `DEBUG` | Enable debug mode | No |
| `CACHE_TTL` | Cache time-to-live in seconds | No |

### Port Configuration

- **Frontend**: Port 3000 (Next.js)
- **Backend**: Port 8000 (FastAPI)
- **Health Check**: `/api/health`

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check Docker build logs
   docker build --no-cache -t multi-agent-ai .
   ```

2. **Environment Variables**
   ```bash
   # Verify environment variables are set
   vercel env ls
   ```

3. **Port Conflicts**
   ```bash
   # Check if ports are available
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8000
   ```

4. **API Connection Issues**
   - Verify API keys are correct
   - Check network connectivity
   - Review CORS settings

### Health Checks

```bash
# Check application health
curl http://localhost:3000/api/health

# Check backend directly
curl http://localhost:8000/health

# Check agent status
curl http://localhost:8000/agents/status
```

## 📊 Performance Optimization

### Docker Optimization

- Multi-stage builds reduce image size
- Non-root user for security
- Health checks for monitoring
- Proper signal handling

### Vercel Optimization

- Standalone Next.js build
- API route proxying
- Environment variable optimization
- Region selection (iad1 for US East)

## 🔒 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use Vercel's secure environment variable system
3. **Non-root User**: Container runs as non-root user
4. **CORS**: Properly configured for production domains
5. **Rate Limiting**: Implement rate limiting for API endpoints

## 📈 Monitoring

### Health Endpoints

- `/health` - Basic health check
- `/agents/status` - Agent status monitoring
- `/cache/stats` - Cache performance metrics

### Logs

```bash
# View container logs
docker logs <container_id>

# View Vercel function logs
vercel logs
```

## 🎯 Next Steps

1. Set up monitoring and alerting
2. Configure custom domain
3. Implement CI/CD pipeline
4. Add performance monitoring
5. Set up backup strategies

---

**Need help?** Check the main README.md or open an issue on GitHub.
