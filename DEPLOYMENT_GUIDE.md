# 🚀 Multi-Agent AI System - Complete Deployment Guide

This guide covers deploying your Multi-Agent AI System with **separated frontend and backend**:
- **Frontend**: Next.js application → **Vercel**
- **Backend**: FastAPI Python application → **Railway**

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ **Vercel Account** - [Sign up here](https://vercel.com/signup)
- ✅ **Railway Account** - [Sign up here](https://railway.app/signup)
- ✅ **API Keys Ready**:
  - NewsAPI key
  - OpenAI API key
  - Weaviate Cloud credentials (optional)

## 🎯 Quick Start (5 Minutes)

### **Step 1: Deploy Backend to Railway**
```bash
cd backend
railway login
railway init
railway up
```

### **Step 2: Deploy Frontend to Vercel**
```bash
cd frontend
vercel login
vercel --prod
```

### **Step 3: Connect Frontend to Backend**
1. Get your Railway URL from Railway dashboard
2. Set `NEXT_PUBLIC_API_BASE_URL` in Vercel environment variables
3. Redeploy frontend

---

## 🚂 Detailed Backend Deployment (Railway)

### **1. Prepare Railway CLI**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
```

### **2. Deploy Backend**

```bash
# Navigate to backend directory
cd backend

# Initialize Railway project
railway init

# Deploy to Railway
railway up
```

### **3. Configure Environment Variables**

In Railway dashboard, add these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEWS_API_KEY` | Your NewsAPI key | `abc123...` |
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-abc123...` |
| `WEAVIATE_URL` | Weaviate Cloud URL | `https://your-cluster.weaviate.cloud` |
| `WEAVIATE_API_KEY` | Weaviate API key | `abc123...` |
| `ENVIRONMENT` | Environment setting | `production` |
| `DEBUG` | Debug mode | `false` |
| `CACHE_TTL` | Cache time-to-live | `3600` |

### **4. Get Railway URL**

After deployment, Railway will provide a URL like:
```
https://your-app-name-production.up.railway.app
```

**Save this URL** - you'll need it for the frontend configuration.

### **5. Test Backend**

```bash
# Test health endpoint
curl https://your-app-name-production.up.railway.app/health

# Test agents status
curl https://your-app-name-production.up.railway.app/agents/status
```

---

## 🌐 Detailed Frontend Deployment (Vercel)

### **1. Prepare Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login
```

### **2. Configure Environment Variables**

Create `.env.local` file in frontend directory:

```bash
cd frontend
cp .env.local.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=https://your-app-name-production.up.railway.app
NEXT_PUBLIC_API_TIMEOUT=30000
```

### **3. Deploy Frontend**

```bash
# Deploy to Vercel
vercel --prod
```

### **4. Configure Vercel Environment Variables**

In Vercel dashboard, add:

| Variable | Value | Description |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://your-app-name-production.up.railway.app` | Railway backend URL |
| `NEXT_PUBLIC_API_TIMEOUT` | `30000` | API timeout in milliseconds |

### **5. Test Frontend**

Visit your Vercel URL and verify:
- ✅ Page loads without errors
- ✅ Agent status displays correctly
- ✅ Query functionality works

---

## 🔧 Platform-Specific Configuration

### **Railway Configuration**

Your backend is configured with:

- **Start Command**: `python start.py`
- **Port**: Automatically assigned (`$PORT`)
- **Health Check**: `/health`
- **Python Version**: 3.11.9
- **Dependencies**: All pinned in `requirements.txt`

### **Vercel Configuration**

Your frontend is configured with:

- **Framework**: Next.js 14.2.32
- **Build Command**: Auto-detected
- **Output Directory**: `.next`
- **Node Version**: 18.x
- **Environment**: Production optimized

---

## 🚨 Troubleshooting

### **Common Railway Issues**

#### **Issue**: "No start command found"
**Solution**:
- Ensure Root Directory is set to `backend/`
- Verify `Procfile` exists in backend root
- Check `start.py` file exists

#### **Issue**: "Module not found"
**Solution**:
- Verify all dependencies in `requirements.txt`
- Check Python version compatibility
- Ensure all imports use correct paths

#### **Issue**: "Environment variables not working"
**Solution**:
- Double-check variable names in Railway dashboard
- Ensure no extra spaces or quotes
- Redeploy after adding variables

### **Common Vercel Issues**

#### **Issue**: "Build failed"
**Solution**:
- Check `next.config.js` configuration
- Verify all dependencies in `package.json`
- Check TypeScript compilation errors

#### **Issue**: "API connection failed"
**Solution**:
- Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Check Railway backend is running
- Verify CORS configuration

#### **Issue**: "CORS errors"
**Solution**:
- Update CORS origins in backend `main.py`
- Add Vercel domain to allowed origins
- Redeploy backend after CORS changes

---

## 📊 Monitoring & Health Checks

### **Backend Health Checks**

```bash
# Basic health check
curl https://your-railway-app.railway.app/health

# Agents status
curl https://your-railway-app.railway.app/agents/status

# Query test
curl -X POST https://your-railway-app.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### **Frontend Health Checks**

```bash
# Check if frontend loads
curl https://your-vercel-app.vercel.app

# Check API connection
curl https://your-vercel-app.vercel.app/api/health
```

---

## 🔄 Deployment Workflow

### **Development Workflow**

1. **Local Development**:
   ```bash
   # Backend
   cd backend && python start.py
   
   # Frontend
   cd frontend && npm run dev
   ```

2. **Testing**:
   ```bash
   # Run deployment check
   .\check-deployment.bat
   ```

3. **Deploy**:
   ```bash
   # Deploy backend
   cd backend && railway up
   
   # Deploy frontend
   cd frontend && vercel --prod
   ```

### **Production Workflow**

1. **Update Backend**:
   ```bash
   cd backend
   railway up
   ```

2. **Update Frontend**:
   ```bash
   cd frontend
   vercel --prod
   ```

---

## 🎯 Success Checklist

### **Backend Deployment ✅**
- [ ] Railway service is running
- [ ] Health endpoint responds (`/health`)
- [ ] Agents status endpoint works (`/agents/status`)
- [ ] All environment variables set
- [ ] No import errors in logs
- [ ] Query endpoint functional (`/query`)

### **Frontend Deployment ✅**
- [ ] Vercel deployment successful
- [ ] Page loads without errors
- [ ] Agent status displays correctly
- [ ] API client connects to backend
- [ ] No CORS errors
- [ ] Query functionality works

### **Integration ✅**
- [ ] Frontend communicates with backend
- [ ] All API endpoints accessible
- [ ] Error handling works
- [ ] User experience smooth

---

## 🚀 Advanced Configuration

### **Custom Domains**

#### **Railway Custom Domain**:
1. Go to Railway dashboard
2. Select your service
3. Go to Settings → Domains
4. Add your custom domain

#### **Vercel Custom Domain**:
1. Go to Vercel dashboard
2. Select your project
3. Go to Settings → Domains
4. Add your custom domain

### **Environment-Specific Configs**

#### **Staging Environment**:
- Create separate Railway project for staging
- Use different Vercel project for staging
- Set different environment variables

#### **Production Environment**:
- Use main Railway project
- Use main Vercel project
- Set production environment variables

---

## 📞 Support & Resources

### **Platform Documentation**
- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)

### **Project Resources**
- `DEPLOYMENT_CHECKLIST.md` - Error prevention checklist
- `check-deployment.bat` - Windows validation script
- `check-deployment.sh` - Linux/Mac validation script

### **Getting Help**
1. Check the troubleshooting section above
2. Review platform-specific documentation
3. Check deployment logs in Railway/Vercel dashboards
4. Run validation scripts to identify issues

---

## 🎉 Congratulations!

You've successfully deployed your Multi-Agent AI System with separated frontend and backend! 

Your application is now:
- ✅ **Scalable**: Independent scaling of frontend and backend
- ✅ **Reliable**: Platform-specific optimizations
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Production-Ready**: Optimized for performance

**Happy coding!** 🚀
