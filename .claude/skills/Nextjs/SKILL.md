---
name: NextjsComponentBuilder
description: A reusable skill for building Next.js components following App Router best practices and spec compliance
version: 1.0.0
---

# Next.js Component Builder Skill

## When to Use This Skill

Use this skill when building Next.js applications with the App Router pattern that require:
- Server Components by default with Client Components only when necessary
- Strict adherence to UI specifications
- Consistent data fetching patterns
- TypeScript and Tailwind CSS integration
- Centralized API client usage
- Component reusability across projects

## How This Skill Works

1. **Analyze Requirements**: Review UI specifications to determine component needs and data requirements
2. **Choose Component Type**: Default to Server Component; use Client Component only when client-side interactivity is required
3. **Define TypeScript Interfaces**: Create proper type definitions for props and data structures
4. **Implement Data Fetching**: Use server-side fetching in Server Components or centralized API client in Client Components
5. **Apply Styling**: Use Tailwind CSS classes following design system specifications
6. **Validate Spec Compliance**: Ensure the component matches UI specifications exactly
7. **Test Component**: Verify functionality and responsiveness across different screen sizes

## Output Format

The skill produces:
- Component file following App Router conventions (`/components/ui/ComponentName.tsx`)
- TypeScript interfaces for props and data
- Proper use of Next.js features (Suspense, Error boundaries, etc.)
- Tailwind CSS classes aligned with design specs
- Centralized API client integration for data fetching
- Component documentation with usage examples

## Quality Criteria

Components must meet these standards:
- Server Component by default unless client-side interactivity is required
- Proper TypeScript typing with no `any` types
- Tailwind CSS classes follow design system specifications
- No inline styles or business logic in components
- Centralized API client used for all data operations
- Component is reusable and follows Next.js best practices
- Strict compliance with provided UI specifications

## Example

**Input**: Create a user profile card component that displays user information and follows the provided UI spec

**Output**:
```tsx
// components/ui/UserProfileCard.tsx
import { getUserProfile } from '@/lib/api-client'
import { User } from '@/types/user'

interface UserProfileCardProps {
  userId: string
}

export async function UserProfileCard({ userId }: UserProfileCardProps) {
  const user: User = await getUserProfile(userId)

  return (
    <div className="bg-white rounded-lg shadow-md p-6 w-full max-w-sm">
      <div className="flex items-center space-x-4">
        <img
          src={user.avatar}
          alt={user.name}
          className="w-16 h-16 rounded-full object-cover"
        />
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{user.name}</h3>
          <p className="text-sm text-gray-500">{user.email}</p>
        </div>
      </div>
      <div className="mt-4">
        <p className="text-sm text-gray-600">{user.bio}</p>
      </div>
    </div>
  )
}
```

This component follows the skill requirements by using Server Component pattern, TypeScript typing, Tailwind CSS for styling, and centralized API client for data fetching.