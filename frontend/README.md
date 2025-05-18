# Digital Wallet Frontend

A modern React frontend for the Digital Wallet application, built with TypeScript, Material-UI, and Vite.

## Features

- User authentication (login/register)
- Wallet management
- Transaction operations (deposit, withdraw, transfer)
- Transaction history
- Responsive design
- Real-time balance updates
- JWT authentication
- Protected routes

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend API running (see backend README)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

## Building for Production

To create a production build:

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Project Structure

```
src/
  ├── components/     # Reusable UI components
  ├── contexts/       # React contexts (auth, etc.)
  ├── hooks/         # Custom React hooks
  ├── pages/         # Page components
  ├── services/      # API services
  ├── types/         # TypeScript interfaces
  ├── utils/         # Utility functions
  └── assets/        # Static assets
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## API Integration

The frontend communicates with the backend API endpoints:

- `/auth/login` - User login
- `/auth/register` - User registration
- `/wallet` - Wallet operations
- `/transactions` - Transaction operations
- `/users/me` - Current user info

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
