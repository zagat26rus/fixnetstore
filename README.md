# FixNet - Premium Smartphone Repair Service

🌟 **A next-generation smartphone repair platform with AI-powered diagnostics and premium user experience**

## 🚀 Live Demo
- **Domain**: [fixnetstore.ru](https://fixnetstore.ru)
- **Admin Panel**: `/admin/login` (Email: `zagat5654@gmail.com`, Password: `admin123`)

## ✨ Features

### 🌍 Bilingual Support
- **Russian** (Primary) 🇷🇺
- **English** (Secondary) 🇺🇸
- Automatic language detection and persistent preferences

### 🎨 Premium Design
- **Dark Theme** with Apple/Nothing-inspired aesthetics
- **Muted neutral color palette** for sophisticated look
- **Smooth animations** and micro-interactions
- **Responsive design** for all devices

### 🤖 AI-Powered Features
- **Smart ChatBot** with Russian/English support
- **Dynamic repair form** with device-specific options
- **Intelligent ticket routing** with priority management
- **Real-time status updates**

### 📱 Core Functionality
- **Multi-step repair request form**
- **Admin dashboard** with complete ticket management
- **Telegram notifications** for real-time updates
- **GDPR-compliant** data handling
- **Secure authentication** with JWT tokens

## 🛠 Tech Stack

### Frontend
- **React 19** with hooks and context
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Router** for navigation
- **Axios** for API communication

### Backend
- **FastAPI** (Python) for REST API
- **MongoDB** for data persistence
- **JWT** authentication
- **Telegram Bot API** for notifications
- **Pydantic** for data validation

### Infrastructure
- **Docker** containerization
- **Supervisor** for process management
- **CORS** enabled for cross-origin requests
- **Environment-based** configuration

## 📦 Installation & Setup

### Prerequisites
- Node.js 18+ and Yarn
- Python 3.9+
- MongoDB
- Docker (optional)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/fixnet.git
cd fixnet
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your MongoDB URL and Telegram credentials

# Start the backend
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

3. **Frontend Setup**
```bash
cd frontend
yarn install

# Configure environment variables
cp .env.example .env
# Edit .env with your backend URL

# Start the frontend
yarn start
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- Admin Panel: http://localhost:3000/admin/login

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=fixnet
JWT_SECRET_KEY=your-secret-key
TELEGRAM_BOT_TOKEN=7983043105:AAGyFmxc3PqDfqlD7lUyPz9iGlAm2O3ANoU
TELEGRAM_CHAT_ID=673253772
```

#### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/login` - Admin login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Repair Request Endpoints
- `POST /api/repair-requests/` - Create repair request
- `GET /api/repair-requests/` - Get all requests (admin)
- `PUT /api/repair-requests/{id}/status` - Update status
- `GET /api/repair-requests/stats/dashboard` - Dashboard stats

### Contact Endpoints
- `POST /api/contact/` - Send contact message
- `GET /api/contact/` - Get messages (admin)

## 🔔 Telegram Integration

### Setup Telegram Bot
1. Message @BotFather on Telegram
2. Create new bot with `/newbot`
3. Get bot token and add to `.env`
4. Get chat ID for notifications
5. Bot will send notifications for:
   - New repair requests
   - Status updates
   - Contact form submissions

## 🌐 Deployment

### Production Deployment
1. **Build frontend**
```bash
cd frontend
yarn build
```

2. **Configure production environment**
```bash
# Update .env files with production URLs
# Set up MongoDB Atlas or production database
# Configure Telegram bot for production
```

3. **Deploy with Docker**
```bash
docker-compose up -d
```

### Environment-Specific Configs
- **Development**: Local MongoDB, localhost URLs
- **Production**: MongoDB Atlas, production domain
- **Testing**: Test database, mock services

## 📱 Features Breakdown

### User Features
- **Device Selection**: Dynamic forms based on device type
- **Issue Categories**: Comprehensive problem classification
- **Pickup Scheduling**: Flexible time slot selection
- **Progress Tracking**: Real-time repair status updates
- **Multi-language**: Russian/English support

### Admin Features
- **Dashboard**: Comprehensive ticket overview
- **Status Management**: Update repair progress
- **Search & Filter**: Find tickets quickly
- **Statistics**: Performance metrics
- **Notifications**: Telegram integration

### Technical Features
- **Responsive Design**: Works on all devices
- **Dark Theme**: Premium visual experience
- **Real-time Updates**: Live status changes
- **Secure Authentication**: JWT-based security
- **Data Validation**: Comprehensive input validation

## 🧪 Testing

### Run Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
yarn test
```

### Test Coverage
- **Backend**: API endpoints, authentication, database operations
- **Frontend**: Component rendering, user interactions, form validation
- **Integration**: End-to-end user workflows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@fixnet.com or join our Telegram channel.

---

**Built with ❤️ for the future of device repair**

*FixNet - Where technology meets craftsmanship*