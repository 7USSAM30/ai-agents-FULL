# Multi-Agent AI System - Windows PowerShell Deployment Script
# This script handles deployment to Vercel with cleanup of old projects

Write-Host "🚀 Multi-Agent AI System - Unified Deployment" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Check if Vercel CLI is installed
try {
    $vercelVersion = vercel --version
    Write-Host "✅ Vercel CLI found: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "npm install -g vercel" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in to Vercel
try {
    $user = vercel whoami
    Write-Host "✅ Logged in as: $user" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Not logged in to Vercel. Please login first:" -ForegroundColor Yellow
    vercel login
}

Write-Host "`n📋 Step 1: Checking for old projects..." -ForegroundColor Blue
Write-Host "Current Vercel projects:" -ForegroundColor Cyan
vercel ls

Write-Host "`n📋 Step 2: Environment setup..." -ForegroundColor Blue

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item "env.production.example" ".env"
    Write-Host "⚠️  Please edit .env file with your actual API keys before deploying!" -ForegroundColor Yellow
    Write-Host "Press Enter after you've updated the .env file..." -ForegroundColor Cyan
    Read-Host
}

Write-Host "`n📋 Step 3: Deploying to Vercel..." -ForegroundColor Blue

# Deploy to Vercel
Write-Host "🚀 Deploying unified application to Vercel..." -ForegroundColor Green
Write-Host "This will create a new project or update existing one." -ForegroundColor Cyan

try {
    # Deploy with production flag
    vercel --prod --yes
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
} catch {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 Step 4: Setting up environment variables..." -ForegroundColor Blue

# Read .env file and set variables in Vercel
$envContent = Get-Content ".env"
foreach ($line in $envContent) {
    if ($line -match "^([^=]+)=(.*)$" -and $line -notmatch "^#") {
        $key = $matches[1]
        $value = $matches[2] -replace '^"(.*)"$', '$1' -replace "^'(.*)'$", '$1'
        
        if ($key -and $value -and $value -ne "your_*_here") {
            Write-Host "Setting $key..." -ForegroundColor Cyan
            try {
                vercel env add $key production
            } catch {
                Write-Host "⚠️  Could not set $key (may already exist)" -ForegroundColor Yellow
            }
        }
    }
}

Write-Host "`n🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Your unified Multi-Agent AI System is now deployed!" -ForegroundColor Green
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  ✅ Single unified application" -ForegroundColor Green
Write-Host "  ✅ Next.js frontend with integrated API routes" -ForegroundColor Green
Write-Host "  ✅ All AI agents running in one container" -ForegroundColor Green
Write-Host "  ✅ Optimized for Vercel deployment" -ForegroundColor Green
Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Cyan
Write-Host "  /api/query - Main query processing" -ForegroundColor White
Write-Host "  /api/health - Health check" -ForegroundColor White
Write-Host "  /api/agents/status - Agent status" -ForegroundColor White
Write-Host ""
Write-Host "To get your deployment URL, run: vercel ls" -ForegroundColor Yellow
