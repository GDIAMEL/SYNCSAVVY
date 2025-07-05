# Freelancers Bot - AI-Powered Freelance Management Platform

**Streamline your freelance business with AI-powered automation, M-Pesa integration, and professional tools**

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser to http://localhost:5000
```

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🎯 Overview

Freelancers Bot is a comprehensive Flask-based platform designed to streamline freelance operations with AI-powered automation, M-Pesa payment integration, and professional client management tools.

### Key Benefits
- **AI-Powered Tools**: Email rewriting and price negotiation assistance
- **M-Pesa Integration**: Direct payment processing via Safaricom M-Pesa
- **Professional Templates**: Automated invoice and contract generation
- **Modern Dashboard**: Real-time analytics and project tracking
- **Mobile-Responsive**: Works seamlessly on all devices

## ✨ Features

### 🧠 AI Capabilities
- **Email Rewriter**: Transform emails with different tones and purposes
- **Price Negotiator**: AI-powered negotiation assistance
- **Smart Suggestions**: Context-aware recommendations

### 💰 Payment Integration
- **M-Pesa STK Push**: Direct mobile money payments
- **Payment Tracking**: Real-time transaction status
- **Invoice Generation**: Professional PDF invoices
- **Payment History**: Complete transaction records

### 📊 Management Tools
- **Client Management**: Add, edit, and track clients
- **Project Tracking**: Monitor project status and progress
- **Invoice Management**: Generate and send invoices
- **Contract Creation**: Professional contract templates
- **Analytics Dashboard**: Performance insights and statistics

### 📱 User Interface
- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live data without page refresh
- **Toast Notifications**: User-friendly feedback system

## 🛠️ Installation

### System Requirements
- Python 3.7+
- SQLite (included with Python)
- Modern web browser

### Quick Installation

1. **Clone Repository**
```bash
git clone https://github.com/GDIAMEL/SYNCSAVVY.git
cd SYNCSAVVY
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
```bash
python app.py
```

4. **Access the Application**
Open your browser and go to: `http://localhost:5000`

### Alternative: Using the Startup Script

```bash
# Make script executable (Linux/Mac)
chmod +x start.sh

# Run startup script
./start.sh

# Or on Windows PowerShell
.\start.sh
```

## ⚙️ Configuration

### Environment Variables (Optional)

Create a `.env` file for advanced configuration:

```env
# Safaricom M-Pesa API Credentials
MPESA_CONSUMER_KEY=your_consumer_key_here
MPESA_CONSUMER_SECRET=your_consumer_secret_here
MPESA_SHORTCODE=your_shortcode_here
MPESA_PASSKEY=your_passkey_here
MPESA_ENVIRONMENT=sandbox

# OpenAI API Key for AI features
OPENAI_API_KEY=your_openai_key_here

# Database
DATABASE_URL=sqlite:///freelancers_bot.db

# Flask Settings
SECRET_KEY=your_secret_key_here
DEBUG=True
```

**Note**: The application works without API keys for basic functionality. M-Pesa credentials are pre-configured for testing.

## 📖 Usage

### Dashboard
- View overall statistics and performance metrics
- Access quick actions for common tasks
- Monitor recent projects and invoices
- View revenue charts and project status

### Client Management
- Add new clients with contact information
- View all clients in a searchable table
- Generate invoices and contracts for clients
- Track client project history

### Project Tracking
- Create and manage projects
- Set budgets and timelines
- Track project status (pending, active, completed)
- Link projects to clients and invoices

### Invoice Generation
- Create professional invoices
- Generate PDF invoices automatically
- Request M-Pesa payments
- Track payment status

### Contract Management
- Generate professional contracts
- Use customizable templates
- Export contracts as PDF
- Track contract status

### AI Tools
- **Email Rewriter**: Transform emails with different tones
- **Price Negotiator**: Get AI assistance for negotiations

### M-Pesa Integration
- Request payments via STK Push
- Track transaction status
- Process payment callbacks
- Generate payment receipts

## 🔌 API Documentation

### Core Endpoints

#### Dashboard
- `GET /` - Main dashboard with statistics

#### Clients
- `GET /clients` - List all clients
- `POST /clients/add` - Add new client

#### Projects
- `GET /projects` - List all projects
- `POST /projects/add` - Add new project

#### Invoices
- `GET /invoices` - List all invoices
- `POST /invoices/create` - Create new invoice
- `GET /invoices/<id>/pdf` - Generate invoice PDF

#### Contracts
- `GET /contracts` - List all contracts
- `POST /contracts/create` - Create new contract
- `GET /contracts/<id>/pdf` - Generate contract PDF

#### M-Pesa Payments
- `POST /payments/mpesa/stk-push` - Initiate STK Push payment
- `POST /payments/mpesa/callback` - Handle payment callback

#### AI Services
- `POST /ai/rewrite-email` - Rewrite email with AI
- `POST /ai/negotiate-price` - AI price negotiation

### Response Format
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```

## 📁 Project Structure

```
SYNCSAVVY/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── models/init.py         # Database models
├── services/              # Business logic services
└── templates/             # HTML templates
```

## 🧪 Testing

### Manual Testing
1. **Start the application**: `python app.py`
2. **Access dashboard**: Navigate to `http://localhost:5000`
3. **Test features**:
   - Add a client
   - Create a project
   - Generate an invoice
   - Create a contract
   - Test AI tools
   - Test M-Pesa integration

### Database
The application uses SQLite by default, which is automatically created on first run.

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production (Using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 coding standards
- Add docstrings to new functions
- Test your changes before submitting
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
1. **Check the documentation** in this README
2. **Review existing issues** on GitHub
3. **Create a new issue** with detailed information

### Common Issues

#### Import Errors
```bash
# Make sure you're in the correct directory
cd SYNCSAVVY

# Reinstall dependencies
pip install -r requirements.txt
```

#### Database Issues
The SQLite database is automatically created on first run. If you encounter issues:
```bash
# Remove existing database (if any)
rm freelancers_bot.db

# Restart the application
python app.py
```

#### Port Already in Use
```bash
# Change port in app.py
app.run(debug=Config.DEBUG, host='0.0.0.0', port=5001)
```

## 🎉 What's Next?

### Immediate Features
- ✅ **Client Management** - Add and manage clients
- ✅ **Project Tracking** - Monitor project progress
- ✅ **Invoice Generation** - Create professional invoices
- ✅ **Contract Creation** - Generate legal contracts
- ✅ **AI Tools** - Email rewriting and negotiation
- ✅ **M-Pesa Integration** - Direct payment processing

### Future Enhancements
- 🔄 **Multi-language Support** - Internationalization
- 🔄 **Advanced Analytics** - Detailed reporting
- 🔄 **Email Notifications** - Automated alerts
- 🔄 **Mobile App** - Native mobile application
- 🔄 **API Rate Limiting** - Enhanced security
- 🔄 **User Authentication** - Multi-user support

## 📊 Performance

- **Fast Startup**: Application starts in under 5 seconds
- **Responsive UI**: Modern, mobile-friendly interface
- **Efficient Database**: SQLite for simplicity and performance
- **Real-time Updates**: Live data without page refresh

## 🔒 Security

- **Input Validation**: All user inputs are validated
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **XSS Protection**: Template escaping enabled
- **CSRF Protection**: Built-in Flask protection

---

## 🚀 Ready to Get Started?

Your Freelancers Bot is ready to revolutionize your freelance business!

**Quick Commands:**
```bash
# Install and run
pip install -r requirements.txt
python app.py

# Visit http://localhost:5000
```

**Features Available:**
- 📊 **Dashboard** with real-time statistics
- 👥 **Client Management** with professional interface
- 📋 **Project Tracking** with status monitoring
- 💰 **Invoice Generation** with PDF export
- 📄 **Contract Creation** with legal templates
- 🤖 **AI Tools** for email and negotiation
- 📱 **M-Pesa Integration** for payments

---

*Built with ❤️ for freelancers worldwide*

**Version**: 1.0.0 | **Last Updated**: July 2025
