# Public Service Complaint Management System

A complete MVP for managing public service complaints with AI tagging and role-based access control.

## Tech Stack
- **Frontend**: React (Vite) + TailwindCSS
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Auth**: JWT-based authentication
- **AI**: Rule-based NLP classification

## Features
- Role-based authentication (Citizen, Officer, Admin)
- Complaint submission and tracking
- AI-powered complaint categorization and prioritization
- Officer assignment and status updates
- Admin dashboard for complaint management

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local installation or cloud instance)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Start MongoDB service (if using local MongoDB)
# mongod  # In a separate terminal

# Run the backend server
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 3. Seed Sample Data

With the backend running, seed the database with sample data:

```bash
cd backend
python seed.py
```

### 4. Test the Application

Use these sample accounts to test different roles:

- **Citizen**: `citizen@example.com` / `password123`
- **Officer**: `officer@example.com` / `password123`
- **Admin**: `admin@example.com` / `password123`

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Complaints
- `POST /api/complaints` - Submit complaint (Citizen)
- `GET /api/complaints/me` - Get user's complaints (Citizen)
- `GET /api/complaints/assigned` - Get assigned complaints (Officer)
- `GET /api/complaints` - Get all complaints (Admin)
- `PUT /api/complaints/{id}/status` - Update complaint status (Officer)
- `PUT /api/complaints/{id}/assign` - Assign officer to complaint (Admin)

## Project Structure

```
complaint-management-system/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── seed.py                 # Database seeding script
│   ├── auth/
│   │   └── auth.py            # Authentication utilities
│   ├── models/
│   │   ├── user.py            # User data models
│   │   └── complaint.py       # Complaint data models
│   ├── routes/
│   │   ├── auth.py            # Authentication routes
│   │   └── complaints.py      # Complaint routes
│   └── services/
│       ├── database.py        # Database operations
│       └── ai_service.py      # AI classification service
└── frontend/
    ├── package.json           # Node.js dependencies
    ├── vite.config.js         # Vite configuration
    ├── tailwind.config.js     # Tailwind CSS config
    ├── index.html             # HTML template
    └── src/
        ├── main.jsx           # React entry point
        ├── App.jsx            # Main App component
        ├── App.css            # Additional styles
        ├── index.css          # Tailwind CSS imports
        ├── context/
        │   └── AuthContext.jsx # Authentication context
        ├── services/
        │   └── api.js         # API service functions
        ├── components/
        │   └── Sidebar.jsx    # Navigation sidebar
        └── pages/
            ├── Login.jsx      # Login page
            ├── Register.jsx   # Registration page
            ├── ComplaintForm.jsx # Complaint submission
            ├── CitizenDashboard.jsx # Citizen dashboard
            ├── OfficerDashboard.jsx # Officer dashboard
            └── AdminDashboard.jsx   # Admin dashboard
```

## AI Classification

The system uses a rule-based approach for complaint classification:

### Categories
- **Road**: Potholes, street repairs, traffic issues
- **Water**: Leaks, supply problems, contamination
- **Electricity**: Power outages, wiring issues, lighting
- **Sanitation**: Waste collection, garbage, cleanliness
- **Other**: Everything else

### Priority Levels
- **High**: Emergency situations, safety hazards, urgent issues
- **Medium**: Important but not critical problems
- **Low**: Minor issues, improvements, suggestions

## Security Features

- JWT-based authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- CORS protection
- Input validation

## Development Notes

- The AI classification is currently rule-based but designed for easy extension to ML models
- The frontend uses a Swiss-inspired design with high contrast and minimal styling
- All rounded corners are removed (`rounded-none`) as per design requirements
- Color coding: Red for high priority, Yellow for medium, Blue for low priority

## Future Enhancements

- Replace rule-based AI with machine learning models
- Add real-time notifications
- Implement file attachments for complaints
- Add complaint search and filtering
- Generate reports and analytics
- Add email notifications
- Implement complaint escalation workflows