# Coding Standards & Architecture

**File Purpose:** Establishes the technical foundation for consistent, maintainable Next.js 14.2.0 apps, tuned for LLM-assisted development on small projects (tens → hundreds of users).

**Applies To:**

* Small Web App Projects built with Next.js 14.2.0

**Last Updated:** 2025-05-28

---

## Code Style

### Formatting

| Guideline | Notes |
|-----------|-------|
| 2-space indentation | Keep diffs tiny, avoid tab chaos |
| Max line length ≤ 80 | Relax if a long import is clearer |
| Trailing commas | Multi-line arrays & objects |
| Semicolons | Always |
| Quotes | JS strings → single '...'; JSX attrs → double "..." |
| Formatter | Prettier (project config checked in) |

### Naming Conventions

* **Components:** PascalCase (`UserCard`)
* **Files:** Match component (`UserCard.tsx`)
* **Functions / vars:** camelCase (`fetchUsers`)
* **Constants:** UPPER_SNAKE_CASE (`API_BASE_URL`)
* **Custom hooks:** useX (`useSession`)
* **Props:** camelCase (`isOpen`)
* **Event handlers:** handleX (`handleSubmit`)
* **Types / Interfaces:** PascalCase (`User`)

---

## Code Organization

### Project Structure

```
src/
├── app/                # App Router
│   ├── (auth)/         # Route group: auth flows
│   ├── api/            # Route handlers (formerly "pages/api")
│   ├── actions/        # ⇢ Server Actions (mutations)
│   ├── global.css      # Global styles (import in root layout.tsx)
│   └── layout.tsx      # Root layout
├── components/         # Shared/reactive UI
│   ├── ui/             # "Dumb" atoms & molecules
│   └── layout/         # Header/Footer/Shell etc.
├── hooks/              # Custom hooks
├── lib/                # Helpers (date, api, etc.)
├── providers/          # Context providers
├── types/              # TypeScript contracts
└── styles/             # Non-component CSS / tailwind.config.* (Note: tailwind.config often lives in project root)
```

* Adapt as app scales (feature-folders, "domain slices", etc.)

### Import Order

Group imports in the following order, separated by a blank line:

1. React/Next.js core ('react', 'next')
2. External libs (e.g. 'zustand')
3. Absolute aliases (@/components/...)
4. Types (import type { ... })
5. Styles ('./Card.module.css')

```tsx
import { useState } from 'react';
import { useRouter } from 'next/navigation';

import { z } from 'zod';

import Button from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';

import type { User } from '@/types';

import styles from './Component.module.css';
```

---

## Component Architecture

### Component Design

* Prefer functional components with hooks
* One component per file (unless tiny & inseparable)
* Size target: ≤ 150 LOC (excluding tailwind class lists)
* Extract complex logic into custom hooks
* Use TypeScript for prop type definitions

### Server vs Client Components

| Use case | Component Type | Marker |
|----------|----------------|--------|
| Data fetch, DB access, heavy logic | Server Component | (default) |
| Interactivity, state, browser APIs | Client Component | `use client` header |

```tsx
// Server Component (default - no marker needed)
export default function ProductList() {
  // Can fetch directly without useEffect or useState
  const products = await fetchProducts();
  
  return <div>
    {products.map(product => (
      <ProductCard key={product.id} product={product} />
    ))}
  </div>;
}

// Client Component
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

**Note:** Next.js 14 uses React 18.3.1, which includes stable hooks like `useOptimistic` and `useFormStatus` that enhance form handling and optimistic UI updates.

### Component Patterns

* **Composition Pattern**: Use children and composition for flexibility

```tsx
// Flexible card component using children
function Card({ children, className = '' }: { 
  children: React.ReactNode; 
  className?: string; 
}) {
  return (
    <div className={`card ${className}`}>
      {children}
    </div>
  );
}

// Usage
function App() {
  return (
    <Card className="user-card">
      <h2>User Profile</h2>
      <p>User details here</p>
      <button>Edit</button>
    </Card>
  );
}
```

* **Container/Presenter Pattern**: Separate data logic from presentation.
  **Note for RSC:** While this pattern is useful, especially for client-side interactions or re-fetching, prefer Server Components for initial data loading to leverage server-side rendering and reduce client-side JavaScript. The example below demonstrates a client-side fetching approach.

```tsx
// Container (e.g., a Client Component that fetches data)
'use client';

import { useState, useEffect } from 'react';
import UserProfile from './UserProfile'; // Presenter

const UserProfileContainer = ({ userId }: { userId: string }) => {
  const [user, setUser] = useState<User | null>(null); // Assuming 'User' type is defined
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) throw new Error('Failed to fetch user');
        const userData = await response.json();
        setUser(userData);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, [userId]);

  return <UserProfile user={user} isLoading={loading} error={error} />;
};
```

---

## Hooks Usage

* Extract reusable logic into custom hooks
* Keep hooks focused and composable
* Obey [Rules of Hooks](https://react.dev/reference/react/hooks)
* Name custom hooks with "use" prefix
* Memoize expensive computations (`useMemo`, `useCallback`) after profiling

```tsx
// Custom hook for API data fetching
function useApi<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

---

## State Management

### Local State

* `useState` for simple component state
* `useReducer` for complex state logic
* Keep state close to where it's used

### Shared State

* **Context API**: For theme, auth, and rarely-changing state
* **Zustand**: Simple global state (recommended for most small-medium projects)
* **Jotai**: Atomic state management for fine-grained control
* **TanStack Query / SWR**: For server state in Client Components

```tsx
// Using Zustand for simple global state
import { create } from 'zustand';

interface Store {
  count: number;
  user: User | null;
  increment: () => void;
  decrement: () => void;
  setUser: (user: User | null) => void;
}

const useStore = create<Store>((set) => ({
  count: 0,
  user: null,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  setUser: (user) => set({ user }),
}));

// Usage
function Counter() {
  const { count, increment, decrement } = useStore();
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

---

## Data Fetching & Mutations

| Pattern | When to use | Location |
|---------|-------------|----------|
| Server-side fetch | Read-only data | Server Component |
| Route Handler | RESTful API (GET / POST) | `/app/api/**/route.ts` |
| Server Action | Form-bound mutation | `/app/actions/` or inline |

```tsx
// Server Component data fetching
export default async function UserPage({ params }: { params: { id: string } }) {
  // Direct fetch - no useEffect or useState needed
  const user = await fetch(`https://api.example.com/users/${params.id}`);
  const userData = await user.json();
  
  return <UserProfile user={userData} />;
}

// Route Handler for API endpoints
// app/api/users/route.ts
export async function GET() {
  const users = await db.users.findMany();
  return Response.json(users);
}

// Server Action for mutations
// app/actions/createUser.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const UserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export async function createUser(formData: FormData) {
  const validatedFields = UserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
  });
  
  if (!validatedFields.success) {
    return { error: validatedFields.error.flatten().fieldErrors };
  }
  
  await db.users.create({ data: validatedFields.data });
  revalidatePath('/users');
  
  return { success: true };
}
```

Control caching with:

```tsx
// Time-based revalidation (5 minutes)
await fetch('/api/posts', { next: { revalidate: 300 } });

// Disable caching
await fetch('/api/dynamic-data', { cache: 'no-store' });

// Revalidate after mutations
revalidatePath('/posts');
```

### API Integration

```tsx
// lib/api.ts
export async function api<T>(
  path: string,
  init?: RequestInit & { auth?: boolean }
): Promise<T> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json() as Promise<T>;
}
```

---

## Error Handling

### Route-level Errors

* `error.tsx`: Catches errors in the route and its children
* `not-found.tsx`: Handles 404 errors or `notFound()` calls

```tsx
// app/dashboard/error.tsx
'use client'; // Error components must be Client Components

import { useEffect } from 'react';

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to monitoring service
    console.error(error);
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong in the dashboard</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Component-level Errors

Use error boundaries for Client Components:

```tsx
'use client';

import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

export function ProtectedComponent() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <YourComponent />
    </ErrorBoundary>
  );
}
```

### Async Errors

* Try/catch in Server Components and Server Actions
* Surface toast/alerts for user feedback
* Log errors on the server, client logs to monitoring service

---

## Styling

### Tailwind CSS (Preferred)

```tsx
function Button({ primary, children }) {
  return (
    <button
      className={`
        px-4 py-2 rounded text-sm font-medium
        ${primary 
          ? 'bg-blue-500 text-white hover:bg-blue-600' 
          : 'bg-gray-200 text-gray-800 hover:bg-gray-300'}
      `}
    >
      {children}
    </button>
  );
}
```

### CSS Modules

For uniquely styled, reusable components:

```tsx
// Card.module.css
.card {
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.primary {
  background-color: #f0f9ff;
  border: 1px solid #bae6fd;
}

// Card.tsx
import styles from './Card.module.css';
import { cn } from '@/lib/utils';

export function Card({ primary, className, children }) {
  return (
    <div className={cn(
      styles.card,
      primary && styles.primary,
      className
    )}>
      {children}
    </div>
  );
}
```

### Utils

```tsx
// lib/utils.ts - tiny clsx wrapper
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

## Testing

| Layer | Tool | Focus |
|-------|------|-------|
| Unit / hooks | Vitest | Pure JS/TS logic |
| Component | React Testing Library | Behavior > implementation |
| E2E | Playwright | Critical user flows |

```tsx
// Example component test
import { render, screen, fireEvent } from '@testing-library/react';
import { Counter } from './Counter';

test('increments count when button is clicked', async () => {
  render(<Counter />);
  
  const button = screen.getByRole('button', { name: /increment/i });
  fireEvent.click(button);
  
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
});
```

Skip exhaustive tests on micro-projects; cover "can't-break" flows.

---

## TypeScript

* `strict: true` in tsconfig
* Never use `any` (use `unknown`, then narrow)
* `interface` for objects, `type` for unions
* Use utility types: `Partial<T>`, `Omit<T, K>`, `ReturnType<T>`

```tsx
// Component props interface
interface UserCardProps {
  user: User;
  isExpanded?: boolean;
  onEdit: (userId: string) => void;
}

// API response type
type ApiResponse<T> = {
  data: T;
  meta: {
    page: number;
    total: number;
  };
};

// Utility type usage
type UserUpdateParams = Partial<Omit<User, 'id'>>;
```

---

## Security

* Validate inputs server-side (zod)
* Store secrets in `.env.local` only. Remember:
  * Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.
  * Other variables are only available on the server-side.
* Escape user HTML; avoid `dangerouslySetInnerHTML`
* Harden headers via `next.config.js`

```tsx
// Input validation with Zod
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

export async function createUser(formData: FormData) {
  // Validate input before processing
  const result = UserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    age: formData.get('age') ? Number(formData.get('age')) : undefined,
  });
  
  if (!result.success) {
    return { error: result.error.flatten() };
  }
  
  // Process validated data
  const user = result.data;
  // ...
}
```

---

## Accessibility

* Semantic HTML (`<button>`, `<nav>`, etc.)
* `alt` on images, `labels` for form controls
* Keyboard focus order & outline intact
* Use `@radix-ui/react-*` for accessible primitives

```tsx
// Accessible form field
function FormField({ id, label, error, ...props }) {
  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium">
        {label}
      </label>
      <input 
        id={id}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        className={`mt-1 block w-full rounded-md ${error ? 'border-red-500' : 'border-gray-300'}`}
        {...props}
      />
      {error && (
        <p id={`${id}-error`} className="mt-1 text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}
```

---

## Environment & CI

* Package manager: pnpm
* ESLint config: next/core-web-vitals
* Pre-commit: lint-staged → pnpm lint && pnpm test
* CI (GitHub Actions): run pnpm lint, pnpm test, pnpm build

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm lint
      - run: pnpm test
      - run: pnpm build
```

---

## Images & Fonts

* `next/image` for optimization, responsive images
* `next/font/google` for inlined, performant fonts

```tsx
import Image from 'next/image';
import { Inter } from 'next/font/google';

// Initialize the font object
const inter = Inter({ subsets: ['latin'] });

export default function Profile() {
  return (
    <div className={inter.className}>
      <h1>User Profile</h1>
      <div className="relative h-48 w-48">
        <Image
          src="/profile.jpg"
          alt="User profile picture"
          fill
          sizes="(max-width: 768px) 100vw, 33vw"
          className="object-cover rounded-full"
        />
      </div>
    </div>
  );
}
```

---

## Routing

* File-based under `/app`
* Nested layouts, route groups `(marketing)/`
* Intercepting routes for modals: `(.)photo/@modal`
* Dynamic segments: `[id]/page.tsx`

```
app/
├── layout.tsx          # Root layout (applies to all routes)
├── page.tsx            # Home page (/)
├── about/
│   └── page.tsx        # About page (/about)
├── blog/
│   ├── page.tsx        # Blog index (/blog)
│   └── [slug]/
│       └── page.tsx    # Blog post (/blog/[slug])
├── (auth)/             # Route group (doesn't affect URL)
│   ├── login/
│   │   └── page.tsx    # Login page (/login)
│   └── signup/
│       └── page.tsx    # Signup page (/signup)
└── dashboard/
    ├── layout.tsx      # Dashboard layout
    ├── page.tsx        # Dashboard index (/dashboard)
    └── settings/
        └── page.tsx    # Settings page (/dashboard/settings)
```

## Middleware & Edge

* File: `/middleware.ts`
* Runs on Edge Runtime (Web-API subset) before request hits routes
* Common uses: redirects, rewrites, authentication guards, A/B tests
* Example:

```ts
  // middleware.ts
  import { NextResponse } from 'next/server'
  import type { NextRequest } from 'next/server'

  export function middleware(req: NextRequest) {
    // redirect non-www → www
    const url = req.nextUrl.clone()
    if (url.hostname === 'example.com') {
      url.hostname = 'www.example.com'
      return NextResponse.redirect(url)
    }
    return NextResponse.next()
  }

  export const config = {
    matcher: ['/dashboard/:path*', '/api/:path*'],
  }
```

---

## Internationalization

* Configure i18n in `next.config.js`
* Use `next-intl` or `next-translate` for string management

```js
// next.config.js
module.exports = {
  i18n: {
    locales: ['en', 'fr', 'es'],
    defaultLocale: 'en',
  },
};
```

---

## Performance Tips

* Keep initial JS < 100 kB (tailwind + few components)
* Defer client components; prefer server where possible
* Enable Turbopack: `pnpm next dev --turbo` for faster startup & refresh
* Audit with `pnpm next dev`, Lighthouse, and React DevTools Profiler

---

## Upgrades & Compatibility

* Target Next.js 14.2.0 + React 18.3.1
* Apply official codemods on major upgrades
* Re-evaluate LLM familiarity before jumping to bleeding-edge

---

## Appendix — Quick Reference

| Feature | Next.js 14 |
|---------|------------|
| Routing | App Router (`/app`) |
| Server Components | ✅ |
| API Routes | ✅ (`/app/api`) |
| Server Actions | ✅ (Stable) |
| Image / Font optimization | ✅ (`next/image`, `next/font`) |
| Route-level error pages | ✅ (`error.tsx`, `not-found.tsx`) |
| Turbopack | ✅ Rust-based compiler; use `next dev --turbo` for turbo-powered dev server |
