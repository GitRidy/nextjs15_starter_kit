This guide provides a condensed overview of developing with Next.js 15, focusing on the App Router and highlighting key changes from Next.js 14.

## Project Setup

### Initialize a new project

Use `create-next-app` for the latest version:

```bash
npx create-next-app@latest
# Follow prompts for setup (TypeScript, ESLint, Tailwind CSS, App Router recommended)
```

Or specify a project name and options:

```bash
npx create-next-app@latest my-next-app --typescript --eslint --tailwind --app
```

### Running the Development Server

Navigate to your project directory and run:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

The server typically starts at `http://localhost:3000`.

## Core Concepts (App Router)

### Root Layout (`app/layout.tsx` or `app/layout.jsx`)

The Root Layout is mandatory and must include `<html>` and `<body>` tags.

TypeScript

```
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
```

This replaces the older `pages/_app.js` and `pages/_document.js`.

### Layouts

Define shared UI for route segments.

TypeScript

```
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <section><h1>Dashboard</h1>{children}</section>;
}
```

### Server Components

- Default component type in the App Router.
- Run on the server, allowing direct data fetching and access to backend resources.
- Can be `async` functions.

TypeScript

```
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
  return res.json();
}

export default async function PostsPage() {
  const posts = await getPosts();
  return (
    <ul>
      {posts.map((post: any) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Client Components

- Opt-in with the `'use client'` directive at the top of the file.
- Enable client-side interactivity (event handlers, state, browser APIs).

TypeScript

```
// app/ui/like-button.tsx
'use client';

import { useState } from 'react';

export default function LikeButton({ initialLikes }: { initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes);
  return <button onClick={() => setLikes(likes + 1)}>{likes} Likes</button>;
}
```

### Passing Data from Server to Client Components

Fetch data in a Server Component and pass it as props to a Client Component.

TypeScript

```
// app/page.tsx
import LikeButton from '@/app/ui/like-button';
import { getPost } from '@/lib/data'; // Assume this fetches post data

export default async function Page({ params }: { params: { id: string } }) {
  const post = await getPost(params.id);
  return <LikeButton initialLikes={post.likes} />;
}
```

### Protecting Server-Only Code

Use the `server-only` package to prevent accidental client-side bundling of sensitive code.

JavaScript

```
// lib/data.js
import 'server-only';

export async function getDataWithApiKey() {
  const res = await fetch('https://external-service.com/data', {
    headers: {
      authorization: process.env.API_KEY, // Kept on server
    },
  });
  return res.json();
}
```

## Data Fetching

### Extended `fetch` API

The global `fetch` API is extended in Server Components. It replaces `getStaticProps` and `getServerSideProps`.

TypeScript

```
// app/some-page/page.tsx
export default async function Page() {
  // Default: { cache: 'force-cache' } (similar to getStaticProps)
  const staticData = await fetch(`https://.../static`);

  // Dynamic: { cache: 'no-store' } (similar to getServerSideProps)
  const dynamicData = await fetch(`https://.../dynamic`, { cache: 'no-store' });

  // Revalidated: { next: { revalidate: 10 } } (similar to getStaticProps with revalidate)
  const revalidatedData = await fetch(`https://.../revalidated`, {
    next: { revalidate: 10 }, // Revalidate every 10 seconds
  });

  return <div>...</div>;
}
```

### Caching Database/ORM Queries

Use `unstable_cache` for caching data from ORMs or databases.

TypeScript

```
// lib/posts.ts
import { unstable_cache } from 'next/cache';
import { db } from '@/lib/db'; // Your DB client

export const getCachedPosts = unstable_cache(
  async () => {
    return await db.query('SELECT * FROM posts');
  },
  ['posts-cache-key'], // Cache key parts
  { revalidate: 3600, tags: ['posts'] } // Options: revalidation time, tags for on-demand revalidation
);
```

## Server Actions

Functions executed on the server, callable from Client or Server Components. Typically used for form submissions and data mutations.

### Basic Definition

Define in a Server Component or a separate file with `'use server'`.

TypeScript

```
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  // ... logic to save post to database ...
  revalidatePath('/posts'); // Revalidate the posts page
  return { message: 'Post created successfully' };
}
```

### Handling Forms

Assign the Server Action to a form's `action` attribute.

TypeScript

```
// app/new-post/page.tsx
import { createPost } from '@/app/actions';

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input type="text" name="title" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

### Inline Server Actions

Define directly within a Server Component.

TypeScript

```
// app/posts/[id]/page.tsx
import { revalidatePath } from 'next/cache';
import { getPost, savePost } from '@/lib/posts'; // Your data functions

export default async function PostPage({ params }: { params: { id: string } }) {
  const post = await getPost(params.id);

  async function updatePost(formData: FormData) {
    'use server';
    await savePost(params.id, formData);
    revalidatePath(`/posts/${params.id}`);
  }

  return (
    <form action={updatePost}>
      {/* Form fields for editing post */}
      <button type="submit">Update Post</button>
    </form>
  );
}
```

### Authentication in Server Actions

TypeScript

```
// app/actions.ts
'use server';
import { db } from '@/lib/db';
import { authenticate } from '@/lib/auth'; // Your auth logic

export async function createUser(data: { name: string; email: string }, token: string) {
  const user = authenticate(token);
  if (!user) {
    throw new Error('Unauthorized');
  }
  const newUser = await db.user.create({ data });
  return newUser;
}
```

## Routing & Metadata

### **Next.js 15 GOTCHA:** Asynchronous `params` and `searchParams`

In Next.js 15, `params` and `searchParams` in page components are Promises and must be `await`ed.

TypeScript

```
// app/blog/[slug]/page.tsx
export default async function BlogPostPage({ params, searchParams }: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { slug } = await params; // MUST await
  const { someQueryParam } = await searchParams; // MUST await

  return <div>Slug: {slug}, Query: {someQueryParam}</div>;
}
```

### Dynamic Metadata (`generateMetadata`)

TypeScript

```
// app/products/[id]/page.tsx
import type { Metadata, ResolvingMetadata } from 'next';

type Props = {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
};

export async function generateMetadata(
  { params, searchParams }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const { id } = await params;
  const product = await fetch(`https://api.example.com/products/${id}`).then((res) => res.json());

  return {
    title: product.name,
    description: product.description,
  };
}

export default async function ProductPage({ params }: Props) {
  const { id } = await params;
  // ... page content ...
  return <div>Product ID: {id}</div>;
}
```

### Title Template

Define in a layout to apply a template to child route titles.

TypeScript

```
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | My Site', // %s will be replaced by child segment title
    default: 'My Site', // Default title if no child provides one
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### Open Graph Images

Generate dynamic OG images. Create `opengraph-image.tsx` (or `.js`).

TypeScript

```
// app/posts/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og';

export const alt = 'Post Title';
export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

export default async function Image({ params }: { params: { slug: string } }) {
  const post = await fetch(`https://.../posts/${params.slug}`).then((res) => res.json());

  return new ImageResponse(
    (
      <div style={{ fontSize: 48, background: 'white', width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        {post.title}
      </div>
    ),
    { ...size }
  );
}
```

## Caching & Revalidation

### `revalidatePath()`

Invalidate cache for a specific path, typically after a mutation.

TypeScript

```
// app/actions.ts
'use server';
import { revalidatePath } from 'next/cache';

export async function updateSettings(formData: FormData) {
  // ... update logic ...
  revalidatePath('/profile');
  revalidatePath('/');
}
```

### `revalidateTag()`

Invalidate cache based on tags assigned during `fetch` or `unstable_cache`.

TypeScript

```
// app/actions.ts
'use server';
import { revalidateTag } from 'next/cache';

export async function addPost(formData: FormData) {
  // ... add post logic (data fetched with tag 'posts') ...
  revalidateTag('posts');
}
```

## Working with APIs

### **Next.js 15 GOTCHA:** Asynchronous `cookies()` API

The `cookies()` function from `next/headers` is now asynchronous.

TypeScript

```
// app/api/some-route/route.ts or in a Server Component
import { cookies } from 'next/headers';

export async function GET(request: Request) {
  // Before Next.js 15: const cookieStore = cookies();
  const cookieStore = await cookies(); // MUST await in Next.js 15
  const token = cookieStore.get('token');
  // ...
  return Response.json({ tokenValue: token?.value });
}
```

## Advanced Rendering & UI

### Partial Prerendering (PPR)

Enable experimental PPR for improved performance by prerendering static shells and streaming dynamic content.

TypeScript

```
// app/some-page/page.tsx
import { Suspense } from 'react';
import { User, AvatarSkeleton } from './user'; // User is a dynamic component

export const experimental_ppr = true; // Enable PPR for this page

export default function Page() {
  return (
    <section>
      <h1>This part is static and prerendered</h1>
      <Suspense fallback={<AvatarSkeleton />}>
        <User /> {/* This part is dynamic and streamed */}
      </Suspense>
    </section>
  );
}
```

### Using Multiple Fonts with CSS Variables

TypeScript

```
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter', // CSS variable name
  display: 'swap',
});

const roboto_mono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
  display: 'swap',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${roboto_mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

Then use in CSS: `font-family: var(--font-inter);`

### Handling `Math.random()` or other non-deterministic code during prerendering

If `Math.random()` causes issues with static generation due to mismatches, ensure the component using it is dynamically rendered. One way: use `await connection()` from `next/server` within an `async` component wrapped in `Suspense`.

JavaScript

```
// app/dynamic-products/page.jsx
import { Suspense } from 'react';
import { connection } from 'next/server'; // For dynamic rendering indication

async function ProductsSkeleton() { /* ... */ return <p>Loading products...</p>; }

async function DynamicProductsView({ products }) {
  await connection(); // Informs Next.js this part is dynamic
  const randomSeed = Math.random();
  // const randomizedProducts = randomize(products, randomSeed); // Your randomization logic
  return <div>{/* Render randomizedProducts */}</div>;
}

export default async function Page() {
  // const products = await getCachedProducts();
  return (
    <Suspense fallback={<ProductsSkeleton />}>
      <DynamicProductsView products={products} />
    </Suspense>
  );
}
```

## Middleware (`middleware.ts` or `.js` at root or in `src/`)

### Extracting Path Parameters (Fix for deprecated `request.page`)

Use `URLPattern` for robust path parameter extraction.

TypeScript

```
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

const PATTERNS = [
  [
    new URLPattern({ pathname: '/:locale/:slug' }),
    (pathnameResult: any) => pathnameResult.pathname.groups, // Adjusted for clarity
  ],
  // Add more patterns as needed
];

function extractParams(url: string) {
  const HackedURL = URL // Prevent TS error "Cannot find name 'URL'. Do you need to change your target library?"
  const input = new HackedURL(url).pathname; // Use only pathname for matching
  let result = {};

  for (const [pattern, handler] of PATTERNS) {
    const patternResult = (pattern as URLPattern).exec(input);
    if (patternResult !== null && 'pathname' in patternResult) {
      result = handler(patternResult);
      break;
    }
  }
  return result;
}

export function middleware(request: NextRequest) {
  const { locale, slug } = extractParams(request.url) as { locale?: string; slug?: string };

  if (locale && slug && request.nextUrl.pathname.startsWith(`/${locale}/${slug}`)) {
    // Example: Rewrite or redirect based on params
    // const newUrl = new URL(`/rewritten/${locale}/${slug}`, request.url);
    // return NextResponse.rewrite(newUrl);
  }
  return NextResponse.next();
}
```

## Key Differences from Next.js 14 (Recap for LLMs)

- **Asynchronous `params` and `searchParams`:** Page/Layout component props `params` and `searchParams` are now Promises and must be `await`ed.
- **Asynchronous `cookies()`:** The `cookies()` function from `next/headers` is now asynchronous and must be `await`ed.
- **App Router is Mature:** Data fetching via `fetch` in Server Components is the primary pattern, replacing `getStaticProps`/`getServerSideProps`.
- **Server Actions are mainstream:** For form submissions and mutations.
- **Partial Prerendering (`experimental_ppr`):** A significant feature for blending static and dynamic content
