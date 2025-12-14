# Customer Insights Dashboard

AI-powered analytics dashboard for SaaS startups to track and analyze customer metrics.

## 🎯 Project Overview

A full-stack application combining:
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React + Tailwind CSS + Recharts
- **AI**: Multi-model routing (Claude, GPT-4, Gemini) for contextual chart analysis
- **Security**: Built-in guardrails against prompt injection and jailbreaking

## 🚀 Features

### Current (Phase 1)
- ✅ RESTful API for customer management
- ✅ Realistic demo data generation
- ✅ Security-first input validation
- ✅ Comprehensive analytics endpoints

### Coming Soon
- 🔄 Interactive dashboard UI
- 🔄 AI chat panel for natural language queries
- 🔄 Real-time metric visualization
- 🔄 Advanced security guardrails

## 🛠 Tech Stack

**Backend:**
- FastAPI (async Python framework)
- SQLAlchemy (ORM)
- Pydantic (data validation)
- SQLite → PostgreSQL (production)

**Frontend (Phase 2):**
- React 18 + Vite
- Tailwind CSS
- Recharts (data visualization)
- Zustand (state management)

**AI Integration (Phase 3):**
- Anthropic Claude (analytical reasoning)
- OpenAI GPT-4 (general queries)
- Google Gemini (cost optimization)
- Custom routing logic

## 📦 Installation

### Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Initialize database with demo data
python seed_data.py

# Run development server
uvicorn app.main:app --reload
```

API will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### Frontend Setup (Coming in Phase 2)
```bash
cd frontend
npm install
npm run dev
```

## 📊 API Endpoints

### Customer Management
- `GET /api/customers` - List customers (with pagination & filters)
- `GET /api/customers/{id}` - Get single customer
- `POST /api/customers` - Create customer
- `PATCH /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Analytics
- `GET /api/customers/stats/summary` - Dashboard summary statistics

### AI Chat (Phase 3)
- `POST /api/chat` - Natural language queries about charts

## 🔒 Security Features

This project implements security-first architecture:

1. **Input Validation Layer**: Pydantic models with custom validators
2. **Injection Detection**: Pattern matching for common attacks
3. **Structured Prompts**: XML boundaries for AI context
4. **Output Validation**: Sanitization before returning to frontend
5. **Security Logging**: Audit trail for suspicious activity

## 🎨 Dashboard Metrics

The dashboard tracks essential SaaS metrics:

- **Customer Acquisition**: New signups, growth rate
- **Retention**: Churn rate, cohort analysis
- **Revenue**: MRR, ARR, customer lifetime value
- **Engagement**: Activity patterns, feature adoption

## 📈 Demo Data

The project includes a data generator that creates realistic customer data:
- 200 customers across 2-year timeline
- Realistic growth curve (slow start → rapid growth → steady state)
- Churn patterns based on plan type and engagement
- Industry distribution and employee counts

## 🧪 Testing
```bash
cd backend
pytest
```

## 📝 Development Log

### Week 1: Backend Foundation
- [x] Project setup and structure
- [x] Database models and schemas
- [x] Demo data generation
- [x] CRUD API endpoints
- [x] Security validation layer
- [x] Basic testing framework

### Week 2: Analytics Engine (In Progress)
- [ ] Time-series aggregation
- [ ] Cohort analysis
- [ ] Churn prediction
- [ ] Revenue forecasting

### Week 3-4: Frontend (Planned)
- [ ] Dashboard layout
- [ ] Chart components
- [ ] Filter system
- [ ] Responsive design

### Week 5-6: AI Integration (Planned)
- [ ] Multi-model router
- [ ] Context serialization
- [ ] Chat interface
- [ ] Streaming responses

## 🤝 Contributing

This is a portfolio project, but feedback is welcome! Open an issue or reach out.

## 📄 License

MIT License - See LICENSE file

---

**Note**: This project is part of my exploration into AI security engineering. It demonstrates full-stack development, AI integration, and security-conscious architecture.
