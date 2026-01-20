# Todo App Frontend

Professional task management application with modern UI/UX built using Next.js, TypeScript, and Tailwind CSS.

## Features

- **Task Management**: Create, edit, and track tasks with due dates and descriptions
- **Authentication**: Secure login and user management
- **Responsive Design**: Mobile-first approach with tablet and desktop support
- **Accessibility**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support
- **Performance**: Optimized with lazy loading and efficient rendering

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.3+
- **Styling**: Tailwind CSS 3.4+
- **UI Components**: Shadcn/ui
- **Icons**: Lucide React
- **Forms**: React Hook Form with Zod validation
- **Animation**: Framer Motion
- **Authentication**: JWT-based authentication

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file in the root directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

3. Run the development server:
```bash
npm run dev
```

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── app/               # Next.js App Router pages
│   │   ├── (auth)/        # Authentication pages
│   │   ├── dashboard/     # Main dashboard
│   │   └── tasks/         # Task management pages
│   ├── components/        # Reusable UI components
│   ├── hooks/             # Custom React hooks
│   ├── lib/               # Utilities and API client
│   └── types/             # TypeScript type definitions
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Base URL for the backend API

## API Endpoints Used

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/:id` - Update a task
- `DELETE /api/tasks/:id` - Delete a task
- `PATCH /api/tasks/:id/toggle` - Toggle task completion
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

## Accessibility Features

- Semantic HTML structure
- Proper ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- Color contrast compliance

## Performance Optimizations

- Code splitting
- Image optimization
- Efficient rendering
- Lazy loading
- Bundle size optimization
