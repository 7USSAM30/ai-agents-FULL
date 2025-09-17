# 🚨 Deployment Error Prevention Checklist

This checklist addresses all the deployment errors you've encountered and ensures smooth deployment.

## 🚂 Railway Backend Deployment Checklist

### ✅ **1. Start Command Configuration**
- [x] **Procfile**: `web: python start.py`
- [x] **railway.json**: Explicit start command configured
- [x] **start.py**: Production-ready startup script with proper port handling
- [x] **Port Configuration**: Uses `$PORT` environment variable

### ✅ **2. Root Directory Configuration**
- [x] **Railway Dashboard**: Set Root Directory to `backend/`
- [x] **File Structure**: All backend files in correct location
- [x] **Procfile**: Located in backend root directory

### ✅ **3. Environment Variables**
Required environment variables for Railway:
- [ ] `NEWS_API_KEY` - Your NewsAPI key
- [ ] `OPENAI_API_KEY` - Your OpenAI API key  
- [ ] `WEAVIATE_URL` - Your Weaviate Cloud URL
- [ ] `WEAVIATE_API_KEY` - Your Weaviate API key
- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=false`
- [ ] `CACHE_TTL=3600`

### ✅ **4. Python Version**
- [x] **runtime.txt**: `python-3.11.9`
- [x] **Compatibility**: All dependencies compatible with Python 3.11.9

### ✅ **5. Dependencies**
- [x] **requirements.txt**: Pinned versions for stability
- [x] **Production Dependencies**: gunicorn, watchfiles included
- [x] **No Conflicts**: Removed conflicting packages

### ✅ **6. Error Handling**
- [x] **Agent Initialization**: Graceful error handling
- [x] **Caching Agent**: Null checks implemented
- [x] **Orchestrator**: Error handling for initialization
- [x] **Lifespan Events**: Safe startup/shutdown

## 🌐 Vercel Frontend Deployment Checklist

### ✅ **7. Build Configuration**
- [x] **vercel.json**: Proper build configuration
- [x] **next.config.js**: Production optimizations
- [x] **Root Directory**: Set to `frontend/`
- [x] **Build Command**: Auto-detected by Vercel

### ✅ **8. Environment Variables**
Required environment variables for Vercel:
- [ ] `NEXT_PUBLIC_API_BASE_URL` - Your Railway backend URL
- [ ] `NEXT_PUBLIC_API_TIMEOUT=30000`

### ✅ **9. API Configuration**
- [x] **API Client**: Centralized communication
- [x] **Error Handling**: Comprehensive error messages
- [x] **Timeout Handling**: Proper timeout configuration
- [x] **CORS**: Backend configured for Vercel domains

### ✅ **10. Security Headers**
- [x] **X-Frame-Options**: DENY
- [x] **X-Content-Type-Options**: nosniff
- [x] **Referrer-Policy**: origin-when-cross-origin

## 🔧 General Deployment Issues Prevention

### ✅ **11. Import Path Issues**
- [x] **Absolute Imports**: All imports use absolute paths
- [x] **Module Structure**: Proper Python module structure
- [x] **Dependencies**: All required modules in requirements.txt

### ✅ **12. Memory Optimization**
- [x] **Single Worker**: Railway uses 1 worker to avoid memory issues
- [x] **Error Handling**: Graceful degradation on failures
- [x] **Resource Management**: Proper cleanup in lifespan events

### ✅ **13. Startup Optimization**
- [x] **Lazy Loading**: Agents initialized with error handling
- [x] **Health Checks**: `/health` endpoint available
- [x] **Startup Time**: Optimized for Railway's timeout limits

### ✅ **14. Weaviate Connection**
- [x] **Error Handling**: Graceful handling of connection failures
- [x] **Environment Variables**: Proper configuration
- [x] **Fallback**: System works even if Weaviate is unavailable

## 🛠️ Deployment Commands

### Railway Backend Deployment:
```bash
cd backend
railway login
railway init
railway up
```

### Vercel Frontend Deployment:
```bash
cd frontend
vercel login
vercel --prod
```

## 📋 Pre-Deployment Testing

### Local Testing:
```bash
# Test backend locally
cd backend
python start.py

# Test frontend locally
cd frontend
npm run dev
```

### Health Checks:
```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000
```

## 🚨 Common Issues & Solutions

### **Issue**: "No start command was found"
**Solution**: 
- Ensure Root Directory is set to `backend/`
- Verify Procfile exists in backend root
- Check start command in railway.json

### **Issue**: "Module not found"
**Solution**:
- Check requirements.txt has all dependencies
- Verify import paths are correct
- Ensure Python version compatibility

### **Issue**: "CORS errors"
**Solution**:
- Update CORS origins in backend/main.py
- Verify Vercel URL is in allowed origins
- Redeploy backend after CORS changes

### **Issue**: "Environment variables missing"
**Solution**:
- Set all required environment variables in Railway
- Verify variable names match exactly
- Check for typos in variable names

### **Issue**: "Port binding errors"
**Solution**:
- Use `$PORT` environment variable
- Ensure start command includes `--port $PORT`
- Check Railway port configuration

## 🎯 Success Indicators

### Backend Success:
- ✅ Health endpoint responds: `/health`
- ✅ Agents status available: `/agents/status`
- ✅ Query endpoint works: `/query`
- ✅ No import errors in logs
- ✅ All environment variables loaded

### Frontend Success:
- ✅ Build completes without errors
- ✅ API client connects to backend
- ✅ No CORS errors in browser
- ✅ Environment variables loaded
- ✅ All components render correctly

## 📞 Troubleshooting Commands

### Check Railway Logs:
```bash
railway logs
```

### Check Vercel Logs:
```bash
vercel logs
```

### Test API Connection:
```bash
curl -X POST https://your-railway-app.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

---

**Remember**: Always test locally first, then deploy to staging, and finally to production!
