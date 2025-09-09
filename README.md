# Multi-Agent AI System

A sophisticated multi-agent AI system built with FastAPI, LangGraph, Next.js, and Weaviate Cloud. This system features 7 specialized agents working in coordination to provide intelligent responses to user queries.

## 🎯 System Overview

The Multi-Agent AI System consists of:

- **Decision Agent**: Routes queries to appropriate specialist agents
- **Research Agent**: RAG with document retrieval using Weaviate
- **News Agent**: Fetches live news data via NewsAPI
- **Sentiment Analysis Agent**: Analyzes text sentiment
- **Summarizer Agent**: Condenses outputs into insights
- **Frontend Agent**: Formats results for the UI
- **Documentation Agent**: Auto-updates system documentation

## 🏗️ Architecture

- **Backend**: FastAPI + LangGraph + LangChain
- **Frontend**: Next.js 14 + TypeScript + TailwindCSS
- **Vector Database**: Weaviate Cloud
- **Deployment**: Docker + Docker Compose
- **AI Models**: OpenAI GPT-4

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- API Keys: OpenAI, NewsAPI, Weaviate Cloud

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai-agents-FULl
```

### 2. Environment Configuration

#### Backend Environment
```bash
cd backend
cp env.example .env
# Edit .env with your API keys
```

#### Frontend Environment
```bash
cd frontend
cp env.local.example .env.local
# Edit .env.local with your configuration
```

### 3. Development Setup

#### Option A: Docker (Recommended)
```bash
# Development with hot reload
docker-compose -f docker-compose.dev.yml up --build

# Production
docker-compose up --build
```

#### Option B: Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
ai-agents-FULl/
├── backend/                 # FastAPI backend
│   ├── agents/             # Agent implementations
│   ├── prompts/            # Agent prompts
│   ├── schemas/            # Pydantic models
│   ├── utils/              # Utility functions
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   └── lib/           # Utility functions
│   ├── package.json       # Node dependencies
│   └── Dockerfile         # Frontend container
├── docker-compose.yml      # Production setup
├── docker-compose.dev.yml  # Development setup
└── IMPLEMENTATION_ROADMAP.md
```

## 🔧 Configuration

### Required Environment Variables

#### Backend (.env)
```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here

# Weaviate Configuration
WEAVIATE_URL=your_weaviate_cloud_url_here
WEAVIATE_API_KEY=your_weaviate_api_key_here

# Application Settings
ENVIRONMENT=development
DEBUG=true
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 API Endpoints

### Core Endpoints
- `POST /query` - Process user queries
- `GET /agents/status` - Get agent status
- `GET /health` - Health check
- `GET /config` - System configuration

### Documentation
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

## 🚀 Deployment

### Production Deployment

1. **Backend**: Deploy to Render, Railway, or AWS
2. **Frontend**: Deploy to Vercel or Netlify
3. **Database**: Use Weaviate Cloud for vector storage

### Docker Deployment
```bash
# Build and run production containers
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📈 Development Roadmap

See [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) for detailed development phases and milestones.

### Current Status: Phase 1 Complete ✅
- ✅ Project structure created
- ✅ FastAPI backend setup
- ✅ Next.js frontend setup
- ✅ Docker configuration
- ✅ Environment configuration

### Next Steps: Phase 2
- 🔄 Implement core agents (Research, News, Sentiment)
- 🔄 Set up Weaviate integration
- 🔄 Basic LangGraph orchestration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions and support:
- Check the [documentation](IMPLEMENTATION_ROADMAP.md)
- Open an issue on GitHub
- Review the API documentation at `/docs`

---

**Built with ❤️ using modern AI technologies**
