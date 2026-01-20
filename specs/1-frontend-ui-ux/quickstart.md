# Quickstart: Frontend Web Application Development

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- Code editor (VS Code recommended)

## Initial Setup

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-root>
```

### 2. Install Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the `frontend` directory with the following variables:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-key-here

# JWT Secret (must match backend)
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-key-here
```

## Development Workflow

### 1. Start Development Server
```bash
# From the frontend directory
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

### 2. Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Lint code
npm run lint

# Format code with Prettier
npm run format
```

## Project Structure Reference

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # Reusable UI components
│   ├── lib/                 # Utility functions and API client
│   ├── hooks/               # Custom React hooks
│   └── types/               # TypeScript type definitions
├── public/                  # Static assets
├── styles/                  # Global styles and theme
└── package.json
```

## Key Development Patterns

### 1. Component Development
- Create new components in `src/components/`
- Follow the category structure: `ui/`, `forms/`, `task/`, `layout/`, `auth/`
- Use TypeScript interfaces for props
- Follow accessibility best practices

### 2. API Integration
- All API calls through centralized client in `src/lib/api.ts`
- Include JWT tokens in Authorization header
- Handle loading and error states consistently
- Follow the API contract defined in constitution

### 3. Authentication Flow
- Use Better Auth components and hooks
- Protect routes with AuthGuard
- Store JWT tokens securely
- Redirect appropriately based on auth state

### 4. Styling Guidelines
- Use Tailwind CSS utility classes exclusively
- No inline styles
- Follow the design system established in theme
- Ensure responsive design at mobile, tablet, desktop

## Testing Guidelines

### 1. Unit Tests
- Place tests alongside components (e.g., `Button.test.tsx`)
- Test component rendering and user interactions
- Mock API calls and external dependencies

### 2. Integration Tests
- Test component combinations
- Verify API integration flows
- Test authentication flows

### 3. Accessibility Testing
- Ensure all components pass a11y audits
- Test keyboard navigation
- Verify screen reader compatibility

## Common Tasks

### 1. Adding a New Page
1. Create new directory in `src/app/`
2. Add `page.tsx` file
3. Implement Server Component by default
4. Add Client Component only if interaction required

### 2. Creating a New Component
1. Create file in appropriate category in `src/components/`
2. Use TypeScript interfaces for props
3. Add proper accessibility attributes
4. Write tests if component has complex logic

### 3. Adding API Endpoints
1. Update API client in `src/lib/api.ts`
2. Add proper error handling
3. Include JWT token in headers
4. Follow existing patterns for consistency

## Environment-Specific Notes

### Local Development
- API server should run on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- Use development environment variables

### Production Deployment
- Ensure environment variables are properly set
- Build process generates optimized assets
- CDN recommended for static assets

## Troubleshooting

### Common Issues

1. **Authentication not working**
   - Verify JWT secret matches backend
   - Check that tokens are properly included in requests
   - Ensure API URL is correctly configured

2. **Styling issues**
   - Verify Tailwind is properly configured
   - Check for conflicting class names
   - Ensure responsive breakpoints are correct

3. **API calls failing**
   - Verify API URL is correct
   - Check that JWT tokens are included
   - Confirm backend server is running

### Development Tips

- Use VS Code with recommended extensions
- Enable TypeScript strict mode
- Utilize React Developer Tools browser extension
- Use Tailwind CSS IntelliSense for class completion