# Next.js 14.2.0 Framework Documentation

**File Purpose:** Essential Next.js 14.2.0 reference for LLM-assisted development of small web applications.

**Applies To:**
* Small Web App Projects (tens → hundreds of users)
* Next.js 14.2.0

**Last Updated:** 2025-05-28

---

## Quick Start

### Project Setup
```bash
# Create new Next.js app with TypeScript and Tailwind CSS
npx create-next-app@14.2.0 my-app --typescript --tailwind --app --eslint --import-alias "@/*"
cd my-app

# Run the development server
pnpm dev
# or npm run dev
# or yarn dev
```

### Essential Dependencies
```bash
# Core dependencies included by create-next-app:
# next@14.2.0
# react@18.3.1
# react-dom@18.3.1
# typescript, @types/react, @types/node, tailwindcss, postcss, autoprefixer, eslint, eslint-config-next

# Common additional packages
pnpm add @tanstack/react-query        # For data fetching & server state in Client Components
pnpm add zustand                      # Simple global state management
pnpm add zod                          # Schema validation
pnpm add clsx tailwind-merge          # Conditional classes
pnpm add lucide-react                 # Icons
```

---

## Core Concepts

### App Router File System
```
app/
├── layout.tsx           # Root layout (HTML shell, <body>)
├── page.tsx             # Route: "/"
├── (marketing)/         # Route group: not in URL
│   └─ page.tsx          # Route: "/"
├── dashboard/
│   ├── layout.tsx       # Nested layout for /dashboard/*
│   ├── page.tsx         # Route: "/dashboard"
│   └── [id]/page.tsx    # Dynamic segment: "/dashboard/123"
├── api/                 # Route Handlers (REST/GraphQL/etc.)
│   └─ users/route.ts    # GET/POST handlers → "/api/users"
└── actions/             # Server Actions (mutations)
    └─ createUser.ts
```

### Server vs Client Components

```tsx
// Server Component (default - no marker needed)
export default async function ProductList() {
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

| Server Component (default) | Client Component |
|----------------------------|------------------|
| Runs in | Node.js/Edge runtime | Browser |
| Access to | DB, file system, secrets, process.env.* | window, DOM APIs, React hooks |
| Marker | none | 'use client' at top of file |
| JS bundle | Zero (compiled to HTML/CSS) | Included in JS bundle |

Rule of thumb: Start with Server Components for most content; switch to Client Components only when you need interactivity, client-side state, or browser-only APIs.

### Data Fetching & Caching

```tsx
// Server Component with data fetching
export default async function Page() {
  // With 300-second revalidation (SWR)
  const posts = await fetch(
    'https://api.example.com/posts',
    { next: { revalidate: 300 } }
  ).then(r => r.json());

  // For dynamic, uncached data
  const notifications = await fetch(
    'https://api.example.com/notifications',
    { cache: 'no-store' }
  ).then(r => r.json());

  return <Posts posts={posts} notifications={notifications} />;
}
```

| Cache Strategy | Config | Behavior |
|----------------|--------|----------|
| Static | Default or `{ cache: 'force-cache' }` | Cached at build time until manually revalidated |
| Revalidated | `{ next: { revalidate: 300 } }` | Cached for N seconds, then revalidated |
| Dynamic | `{ cache: 'no-store' }` | Always fetches fresh data, no caching |

Use `revalidatePath('/path')` or `revalidateTag('tag')` in Server Actions to invalidate cache after mutations.

---

## Next.js 14.2.0 Features

### Server Actions (Mutations)

```tsx
// app/actions/createPost.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const PostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10),
});

export async function createPost(formData: FormData) {
  // Validate the form data
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;
  
  const result = PostSchema.safeParse({ title, content });
  if (!result.success) {
    return { error: result.error.flatten() };
  }
  
  // In a real app, save to database here
  console.log('Creating post:', { title, content });
  
  // Revalidate the posts page to show the new post
  revalidatePath('/posts');
  
  return { success: true };
}

// Usage in a Server Component:
// <form action={createPost}>...</form>
```

### Route Handlers (API Endpoints)

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server';

// GET /api/users
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('query') || '';
  
  // In a real app, fetch from database
  const users = [{ id: 1, name: 'John' }, { id: 2, name: 'Jane' }];
  
  return NextResponse.json(users);
}

// POST /api/users
export async function POST(request: Request) {
  const body = await request.json();
  
  // In a real app, save to database
  console.log('Creating user:', body);
  
  return NextResponse.json({ id: 123, ...body }, { status: 201 });
}
```

### Image Optimization

```tsx
import Image from 'next/image';

function Avatar({ user }) {
  return (
    <div className="relative h-10 w-10">
      <Image
        src={user.avatar}
        alt={`${user.name}'s profile picture`}
        fill
        sizes="(max-width: 768px) 100vw, 40px"
        className="rounded-full object-cover"
        priority
      />
    </div>
  );
}
```

### Font Optimization

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';
// import LocalFont from 'next/font/local'; // For local fonts

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

---

## Routing & Navigation

### File-Based Routing

```
/app/about/page.tsx → /about
/app/blog/[slug]/page.tsx → /blog/:slug (e.g., /blog/hello-world)
/app/shop/[...catchAll]/page.tsx → /shop/* (e.g., /shop/categories/shoes/nike)
```

### Client-Side Navigation

```tsx
// Basic navigation with next/link
import Link from 'next/link';

function NavBar() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link
        href={{
          pathname: '/blog/[slug]',
          query: { slug: 'hello-world' },
        }}
      >
        Blog Post
      </Link>
    </nav>
  );
}

// Programmatic navigation
'use client';

import { useRouter } from 'next/navigation';

function LoginForm() {
  const router = useRouter();
  
  function handleSubmit(e) {
    e.preventDefault();
    // Process login...
    router.push('/dashboard');
    // Other methods: router.back(), router.forward(), router.refresh()
  }
  
  return <form onSubmit={handleSubmit}>...</form>;
}
```

### Advanced Routing Patterns

```
Route Groups: (folderName)/ - Organize routes without affecting URL structure
Parallel Routes: @slot/ - Render multiple pages in the same layout
Intercepting Routes: (.)folder/ - Show UI while keeping current context
Layout Nesting: Each route segment can have its own layout
```

---

## Data Fetching & Mutations

### Server-Side Data Fetching

```tsx
// In a Server Component
export default async function ProductPage({ params }: { params: { id: string } }) {
  // Cached data with revalidation every hour
  const product = await fetch(
    `https://api.example.com/products/${params.id}`,
    { next: { revalidate: 3600 } }
  ).then(r => r.json());
  
  // Always fresh data
  const stock = await fetch(
    `https://api.example.com/stock/${params.id}`,
    { cache: 'no-store' }
  ).then(r => r.json());
  
  return (
    <div>
      <h1>{product.name}</h1>
      <p>Price: ${product.price}</p>
      <p>In stock: {stock.available ? 'Yes' : 'No'}</p>
    </div>
  );
}
```

### Client-Side Data Fetching (with TanStack Query)

```tsx
'use client';

import { useQuery, useMutation, QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Set up the client provider in a parent component
function Providers({ children }) {
  const [queryClient] = useState(() => new QueryClient());
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

// Use in a Client Component
function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json()),
  });
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.email}</p>
    </div>
  );
}
```

### Forms & Mutations

```tsx
// app/products/new/page.tsx
import { createProduct } from '@/app/actions/products';

export default function NewProductPage() {
  return (
    <form action={createProduct}>
      <label htmlFor="name">Name:</label>
      <input id="name" name="name" required />
      
      <label htmlFor="price">Price:</label>
      <input id="price" name="price" type="number" step="0.01" required />
      
      <button type="submit">Create Product</button>
    </form>
  );
}

// app/actions/products.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const ProductSchema = z.object({
  name: z.string().min(1),
  price: z.coerce.number().positive(),
});

export async function createProduct(formData: FormData) {
  const validatedFields = ProductSchema.safeParse({
    name: formData.get('name'),
    price: formData.get('price'),
  });
  
  if (!validatedFields.success) {
    return { error: validatedFields.error.flatten() };
  }
  
  // Create product in database
  const product = validatedFields.data;
  // db.products.create({ data: product });
  
  revalidatePath('/products');
  return { success: true, product };
}
```

---

## State Management

### Server-Side State
Use `fetch` with caching options in Server Components as your primary data store.

### Client-Side State

```tsx
// Local Component State
'use client';

import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

// Global State with Zustand
// store/authStore.ts
import { create } from 'zustand';

interface AuthState {
  user: { id: string; name: string } | null;
  isLoggedIn: boolean;
  login: (user: AuthState['user']) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoggedIn: false,
  login: (user) => set({ user, isLoggedIn: true }),
  logout: () => set({ user: null, isLoggedIn: false }),
}));

// Usage in a Client Component
'use client';

import { useAuthStore } from '@/store/authStore';

function ProfileButton() {
  const { user, isLoggedIn, logout } = useAuthStore();
  
  if (!isLoggedIn) return <LoginButton />;
  
  return (
    <div>
      <span>Welcome, {user.name}</span>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

---

## Error Handling

### Route-Level Error Boundary

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
    // Log the error to monitoring service
    console.error('Dashboard error:', error);
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong in the dashboard</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Not Found Page

```tsx
// app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div>
      <h2>404 - Page Not Found</h2>
      <p>We couldn't find the page you were looking for.</p>
      <Link href="/">Return Home</Link>
    </div>
  );
}

// Triggering not-found.tsx programmatically
import { notFound } from 'next/navigation';

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);
  
  if (!product) {
    notFound(); // This will render the nearest not-found.tsx
  }
  
  return <div>...</div>;
}
```

### Error Handling in Components

```tsx
// Try/catch in Server Components
export default async function ProductsPage() {
  try {
    const products = await fetchProducts();
    return <ProductList products={products} />;
  } catch (error) {
    console.error('Failed to fetch products:', error);
    return <div>Failed to load products. Please try again later.</div>;
  }
}

// Error boundary in Client Components
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

export function ProductsComponent() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <ProductList />
    </ErrorBoundary>
  );
}
```

---

## Middleware & Edge

```tsx
// middleware.ts (project root)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Example: Add security headers to all responses
  const response = NextResponse.next();
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  
  // Example: Redirect users to login page
  const isAuthenticated = request.cookies.has('auth-token');
  if (!isAuthenticated && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return response;
}

export const config = {
  matcher: [
    /*
     * Match all paths except:
     * 1. /api routes
     * 2. /_next (Next.js internals)
     * 3. /fonts, /icons, /public (static files)
     * 4. .*\.png, .*\.jpg, etc. (static files)
     */
    '/((?!api|_next|fonts|icons|public|.*\\.png$|.*\\.jpg$).*)',
  ],
};
```

Middleware runs on the Edge runtime (a subset of Node.js APIs) before a request is completed. Use it for:
- Authentication & authorization
- A/B testing
- Rewrites & redirects
- Response & request manipulation
- Geolocation & localization
- Bot protection

---

## CSS & Styling

### Tailwind CSS (Preferred)

```tsx
function Button({ primary, children }) {
  return (
    <button
      className={`
        px-4 py-2 rounded text-sm font-medium transition-colors
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

```css
/* Button.module.css */
.button {
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.primary {
  background-color: #3b82f6;
  color: white;
}

.primary:hover {
  background-color: #2563eb;
}

.secondary {
  background-color: #e5e7eb;
  color: #1f2937;
}

.secondary:hover {
  background-color: #d1d5db;
}
```

```tsx
import styles from './Button.module.css';
import { cn } from '@/lib/utils';

export function Button({ primary, className, children }) {
  return (
    <button 
      className={cn(
        styles.button,
        primary ? styles.primary : styles.secondary,
        className
      )}
    >
      {children}
    </button>
  );
}

// lib/utils.ts - utility for merging class names
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### Global Styles

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: rgb(var(--background-rgb));
}
```

---

## Testing

### Component Testing

```tsx
// components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button component', () => {
  test('renders button with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  test('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Testing Server Components

```tsx
// Using React's testing utilities to test Server Components
// Use jest-fetch-mock to mock fetch requests
import { renderToString } from 'react-dom/server';
import { DataTable } from './DataTable';
import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

beforeEach(() => {
  fetchMock.resetMocks();
});

test('DataTable renders with correct data', async () => {
  const mockData = [{ id: 1, name: 'Test Item' }];
  fetchMock.mockResponseOnce(JSON.stringify(mockData));
  
  const html = await renderToString(
    <DataTable endpoint="/api/items" />
  );
  
  expect(html).toContain('Test Item');
});
```

### E2E Testing with Playwright

```tsx
// tests/homepage.spec.ts
import { test, expect } from '@playwright/test';

test('homepage has correct title and content', async ({ page }) => {
  await page.goto('/');
  
  // Check page title
  await expect(page).toHaveTitle(/My App/);
  
  // Check heading
  const heading = page.locator('h1');
  await expect(heading).toContainText('Welcome to My App');
  
  // Fill search form and check results
  await page.fill('input[placeholder="Search"]', 'test');
  await page.click('button[type="submit"]');
  await expect(page.locator('.search-results')).toBeVisible();
});
```

---

## TypeScript Integration

### Route Parameters

```tsx
// app/users/[id]/page.tsx
export default function UserPage({ 
  params,
  searchParams,
}: { 
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const { id } = params;
  const tab = searchParams.tab || 'profile';
  
  return (
    <div>
      <h1>User {id}</h1>
      <div>Active tab: {tab}</div>
    </div>
  );
}
```

### API & Form Types

```tsx
// Types for API responses
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
}

type ApiResponse<T> = {
  data: T;
  meta: {
    totalCount: number;
    page: number;
    pageSize: number;
  };
};

// Server Action with validation
import { z } from 'zod';

const UserFormSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'editor']),
});

type UserFormData = z.infer<typeof UserFormSchema>;

export async function createUser(formData: FormData) {
  const validatedFields = UserFormSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    role: formData.get('role'),
  });
  
  if (!validatedFields.success) {
    return { error: validatedFields.error.flatten() };
  }
  
  const userData: UserFormData = validatedFields.data;
  // Save to database...
}
```

---

## Security

### Authentication & Authorization

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Check if user is authenticated
  const authToken = request.cookies.get('auth-token')?.value;
  
  // Protected routes pattern
  const isProtectedRoute = request.nextUrl.pathname.startsWith('/dashboard');
  
  if (isProtectedRoute && !authToken) {
    // Redirect to login page with return URL
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('from', request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }
  
  return NextResponse.next();
}

// Server-side authentication check
// app/dashboard/page.tsx
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const cookieStore = cookies();
  const authToken = cookieStore.get('auth-token');
  
  if (!authToken) {
    redirect('/login');
  }
  
  // Verify token on server
  const user = await verifyAuthToken(authToken.value);
  
  if (!user) {
    redirect('/login');
  }
  
  return <Dashboard user={user} />;
}
```

### Environment Variables

```
# .env.local (not committed to git)
DATABASE_URL="postgres://user:password@localhost:5432/mydb"
NEXTAUTH_SECRET="your-nextauth-secret"
NEXTAUTH_URL="http://localhost:3000"

# For client-side access (prefixed with NEXT_PUBLIC_)
NEXT_PUBLIC_API_URL="https://api.example.com"
```

```tsx
// Server-side access (secure)
export async function GET() {
  const dbUrl = process.env.DATABASE_URL;
  // ...
}

// Client-side access (only NEXT_PUBLIC_ vars)
'use client';

function ApiStatus() {
  return <div>API URL: {process.env.NEXT_PUBLIC_API_URL}</div>;
}
```

### Form Validation & Sanitization

```tsx
// With zod for validation
import { z } from 'zod';

const ContactFormSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters')
    .max(500, 'Message cannot exceed 500 characters'),
});

export async function submitContactForm(formData: FormData) {
  'use server';
  
  const validatedFields = ContactFormSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
  });
  
  if (!validatedFields.success) {
    return { error: validatedFields.error.flatten() };
  }
  
  // Process sanitized data
  const { name, email, message } = validatedFields.data;
  // ...
}
```

---

## Performance Optimization

### Core Web Vitals Tips

1. **Use Server Components** for non-interactive content to reduce JS bundle size
2. **Streaming with Suspense** for better loading experience:

```tsx
import { Suspense } from 'react';
import Loading from './loading';

export default function Page() {
  return (
    <div>
      <h1>My Dashboard</h1>
      
      {/* Each section can load independently */}
      <Suspense fallback={<Loading />}>
        <RevenueChart />
      </Suspense>
      
      <Suspense fallback={<Loading />}>
        <LatestOrders />
      </Suspense>
    </div>
  );
}
```

3. **Optimize Images** with next/image (auto-sizing, formats, lazy loading)
4. **Optimize Fonts** with next/font (zero layout shift, preloading)
5. **Route Segments** - each segment can have its own loading state

### React Optimization Techniques

1. **Memoization** for expensive computations:

```tsx
'use client';

import { useMemo } from 'react';

function ExpensiveList({ items, filter }) {
  // Memoize filtered items to prevent recalculation on every render
  const filteredItems = useMemo(() => {
    console.log('Filtering items...');
    return items.filter(item => item.name.includes(filter));
  }, [items, filter]);
  
  return (
    <ul>
      {filteredItems.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

2. **Lazy Loading** for non-critical components:

```tsx
import { lazy, Suspense } from 'react';

// Lazy load heavy component
const AdminPanel = lazy(() => import('./AdminPanel'));

function Dashboard({ isAdmin }) {
  return (
    <div>
      <Header />
      <MainContent />
      
      {isAdmin && (
        <Suspense fallback={<div>Loading admin panel...</div>}>
          <AdminPanel />
        </Suspense>
      )}
    </div>
  );
}
```

3. **Bundle Analysis** to identify and fix large packages:

```bash
# Install bundle analyzer
pnpm add -D @next/bundle-analyzer

# In next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
module.exports = withBundleAnalyzer({
  // your next config
});

# Run with analysis
ANALYZE=true pnpm build
```

---

## Deployment & Configuration

### Environment Setup

```bash
# Development
pnpm dev

# Production build
pnpm build

# Start production server
pnpm start

# Static export (for static hosting without Node.js server)
pnpm build
pnpm export
```

### Configuration Options (`next.config.js`)

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React Strict Mode for development
  reactStrictMode: true,
  
  // Configure image domains for next/image
  images: {
    domains: ['cdn.example.com', 'uploads.example.com'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },
  
  // Add custom headers to all pages
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ];
  },
  
  // Add URL rewrites for API proxying
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: 'https://api.example.com/:path*',
      },
    ];
  },
  
  // For optimal Docker builds using the standalone output (as shown in the Dockerfile example),
  // ensure 'output: "standalone"' is configured:
  // output: 'standalone',
};

module.exports = nextConfig;
```

### Deployment Platforms

| Platform | Command | Notes |
|----------|---------|-------|
| Vercel | `vercel --prod` | Zero-config, edge by default |
| Netlify | Connect GitHub | Auto-detects Next.js |
| Docker | See Dockerfile | For custom deployments |
| AWS | Various | Amplify or custom setup |

#### Example Dockerfile

```dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME 0.0.0.0

CMD ["node", "server.js"]
```

### Using with next-intl

```tsx
// Install next-intl
// pnpm add next-intl

// messages/en.json
{
  "home": {
    "title": "Welcome to our app",
    "description": "This is a sample application"
  },
  "dashboard": {
    "greeting": "Hello, {name}!",
    "stats": "You have {count, plural, =0 {no notifications} =1 {# notification} other {# notifications}}"
  }
}

// app/[locale]/layout.tsx
import { createTranslator, NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export async function generateStaticParams() {
  return ['en', 'fr', 'es', 'de'].map((locale) => ({ locale }));
}

export default async function LocaleLayout({ 
  children,
  params: { locale }
}) {
  const messages = await getMessages(locale);
  
  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      {children}
    </NextIntlClientProvider>
  );
}

// Usage in a Server Component
import { getTranslations } from 'next-intl/server';

export default async function Page() {
  const t = await getTranslations('home');
  
  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description')}</p>
    </div>
  );
}

// Usage in a Client Component
'use client';

import { useTranslations } from 'next-intl';

export default function Greeting({ name }) {
  const t = useTranslations('dashboard');
  
  return (
    <div>
      <h2>{t('greeting', { name })}</h2>
      <p>{t('stats', { count: 3 })}</p>
    </div>
  );
}
```