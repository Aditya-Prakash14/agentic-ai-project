#!/bin/bash
# Job Bot - Quick Start Script
# Starts both backend and frontend servers

set -e

echo "🤖 Job Bot - Startup Script"
echo "=========================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"
echo -e "${GREEN}✓ Node.js found${NC}"
echo ""

if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "📦 Installing backend dependencies..."
pip install -q -r requirements.txt

if [ ! -f "resume.txt" ]; then
    echo -e "${YELLOW}⚠️  resume.txt not found${NC}"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env not found${NC}"
    cp .env.example .env
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install > /dev/null 2>&1 && cd ..
fi

echo ""
echo -e "${GREEN}✓ All dependencies installed${NC}"
echo ""
echo "🚀 Starting Job Bot..."
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo ""

python backend/app.py &
BACKEND_PID=$!

cd frontend && npm run dev &
FRONTEND_PID=$!

cd ..

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
