# ⚡ Quick Deployment Reference

## 🚀 One-Command Deployment

### **Backend (Railway)**
```bash
cd backend && railway up
```

### **Frontend (Vercel)**
```bash
cd frontend && vercel --prod
```

---

## 🔑 Required Environment Variables

### **Railway (Backend)**
```
NEWS_API_KEY=your_news_api_key
OPENAI_API_KEY=your_openai_api_key
WEAVIATE_URL=your_weaviate_url
WEAVIATE_API_KEY=your_weaviate_api_key
ENVIRONMENT=production
DEBUG=false
```

### **Vercel (Frontend)**
```
NEXT_PUBLIC_API_BASE_URL=https://your-railway-app.railway.app
NEXT_PUBLIC_API_TIMEOUT=30000
```

---

## 🧪 Quick Health Checks

### **Backend**
```bash
curl https://your-railway-app.railway.app/health
```

### **Frontend**
```bash
curl https://your-vercel-app.vercel.app
```

---

## 🛠️ Validation Scripts

### **Windows**
```bash
.\check-deployment.bat
```

### **Linux/Mac**
```bash
./check-deployment.sh
```

---

## 📚 Full Documentation

For detailed instructions, see:
- `DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Error prevention checklist
- `DEPLOYMENT_SEPARATED.md` - Technical details

---

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Railway "No start command" | Set Root Directory to `backend/` |
| Vercel build fails | Check `next.config.js` |
| CORS errors | Update CORS in `backend/main.py` |
| API connection fails | Check `NEXT_PUBLIC_API_BASE_URL` |

---

**Need help?** Check the full `DEPLOYMENT_GUIDE.md` for detailed instructions! 🚀
