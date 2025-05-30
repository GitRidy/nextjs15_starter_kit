# Coding Standards & Architecture

**File Purpose:** Establishes the technical foundation for consistent, maintainable code architecture, component design patterns, and state management approaches.

**Applies To:**

* Small Web App Projects built with React 18.3.1

**Edited**: 2025-05-29

---

## Code Style

### Formatting

* Use 2-space indentation
* Maximum line length: 80 characters (unless otherwise agreed)
* Include trailing commas in multiline arrays and objects
* Use semicolons at the end of statements
* Prefer single quotes for JavaScript strings, double quotes for JSX attributes
* Format with Prettier using project configuration

### Naming Conventions

* **Components:** PascalCase (`UserProfile`, `NavBar`)
* **Files:** Match component name (`UserProfile.tsx`, `NavBar.tsx`)
* **Functions & Variables:** camelCase (`handleSubmit`, `userData`)
* **Constants:** UPPER\_SNAKE\_CASE (`API_URL`)
* **Custom hooks:** Start with "use" (`useAuth`)
* **Props:** camelCase, descriptive (`userProfile`, `isEnabled`)
* **Event handlers:** handle + event (`handleClick`)
* **Types/Interfaces:** PascalCase (`UserData`)

---

## Code Organization

### Project Structure

```
src/
├── assets/              # Static assets (images, fonts)
├── components/          # Shared components
│   ├── ui/              # Basic UI components
│   └── layout/          # Layout components
├── contexts/            # React context providers
├── hooks/               # Custom hooks
├── pages/               # Page components (if using React Router)
├── services/            # API services and data fetching
├── styles/              # Global styles and themes
├── types/               # TypeScript type definitions
├── utils/               # Utility functions
├── App.tsx              # Main App component
└── index.tsx            # Entry point
```

### Import Order

Group imports in the following order, separated by a blank line:

1. React
2. External libraries
3. Internal modules (components, hooks, utils)
4. Types/interfaces
5. Styles

```tsx
import { useState } from 'react';
import { z } from 'zod';

import Button from '../components/ui/Button';
import { useAuth } from '../hooks/useAuth';

import type { User } from '../types';

import styles from './Component.module.css';
```

---

## Build Tools

React 18.3.1 can be used with various build tools:

* **Create React App:** Traditional but no longer actively maintained
* **Vite:** Recommended for new projects, faster development experience
* **Next.js:** For full-stack applications (outside the scope of this guide)
* **Custom Webpack/Rollup:** For specialized requirements

This guide assumes a Vite-based setup, but principles apply to any build tool.

## Component Architecture

### Component Design

* Prefer functional components with hooks
* One component per file unless tightly coupled
* Keep components focused on a single responsibility
* Extract complex logic into custom hooks
* Limit component size (aim for under 150 lines, excluding tailwind classes)
* Use TypeScript for prop type definitions

### Component Patterns

* **Composition over props:** Use children and composition for flexibility
* **Container/Presenter Pattern:** Separate data logic from presentation for complex components

```tsx
// Container: handles data
const UserProfileContainer = ({ userId }) => {
  const { data, loading, error } = useUser(userId);
  return <UserProfile user={data} isLoading={loading} error={error} />;
};

// Presenter: handles UI
const UserProfile = ({ user, isLoading, error }) => {
  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage message={error.message} />;
  return <div>{/* render user profile */}</div>;
};
```

* **Component Props:** Destructure props at the function parameter level

---

## Hooks Usage

* Extract reusable logic into custom hooks
* Keep hooks focused and composable
* Follow the [Rules of Hooks](https://react.dev/reference/react/hooks)
* Name hooks with "use"
* Memoize with `useMemo`/`useCallback` for expensive calculations (Avoid premature optimization; measure if needed)
* Use appropriate dependency arrays
* React 18.3.1 includes stable hooks like `useOptimistic` and `useFormStatus` that enhance form handling and optimistic UI updates

---

## State Management

### Local State

* Use `useState` for simple component state
* Use `useReducer` for complex state or where updates depend on previous state
* Keep state as close to usage as possible
* Avoid redundant or derived state

### Application State

* Use React Context for shared state
  * Prefer focused contexts (auth, theme) rather than global state
  * Avoid frequent updates to contexts with many consumers
* Consider state libraries as complexity grows:
  * Zustand (simple global state)
  * Redux Toolkit (complex global state)
  * Jotai (atomic state)
  * TanStack Query / SWR (recommended for managing server state, caching, and data fetching)

---

## Data Fetching

* Fetch data in `useEffect` or use SWR / TanStack Query
* Transform API data at boundaries, not in components
* Define types/interfaces for API responses
* Use zod for runtime validation (optional, recommended)
* Handle loading, error, and success states consistently

```tsx
// Example using TanStack Query
const UserProfile = ({ userId }) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage message={error.message} />;
  
  return <div>{/* render user profile */}</div>;
};
```

---

## API Integration

* Create a centralized API client
* Abstract API calls into service functions
* Handle authentication and headers centrally
* Implement consistent error handling

```tsx
// lib/api.ts
export async function fetchData(endpoint, options = {}) {
  const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}
```

---

## Error Handling

### Component Error Handling

* Use error boundaries for catching/displaying errors
* Implement consistent error states in components
* Provide helpful user feedback

```tsx
// ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  fallback?: ReactNode;
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error("Uncaught error:", error, errorInfo);
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return this.props.fallback || <div>Something went wrong.</div>;
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

### Async Error Handling

* Use try/catch for async operations
* Implement consistent error handling for API calls
* Log errors for debugging
* Present user-friendly error messages

---

## CSS and Styling

### Approaches

1. **CSS Modules:** Scoped, recommended for component styles (co-locate files like `UserProfile.module.css` with their components)
2. **Tailwind CSS:** Utility-first, excellent for rapid prototyping
3. **CSS-in-JS:** (e.g. styled-components, emotion) – be aware of client-side perf
4. **Global Styles:** In `src/index.css` or `src/styles/global.css`

### Best Practices

* Prefer Tailwind CSS for new components
* Use consistent class naming
* Prefer composable utility classes
* Keep styles close to components
* Use CSS variables for theming
* Build with responsive design in mind
* Use `clsx` or `tailwind-merge` for conditional classes

---

## Testing Approach

* Write tests for business logic and UI components
* Use React Testing Library for component tests
* Test custom hooks with `renderHook`
* Use Playwright or Cypress for end-to-end testing if full-journey tests needed
* Focus on testing behavior, not implementation details

```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

test('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click me</Button>);
  
  fireEvent.click(screen.getByText('Click me'));
  
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

---

## TypeScript Usage

* Use TypeScript for all new files
* Define clear interfaces for props
* Use explicit return types for functions
* Avoid using `any`
* Leverage TypeScript utility types (`Partial`, `Pick`, etc.)
* Use zod for runtime validation where possible

```tsx
// Example of TypeScript with React
import { FC, useState } from 'react';

interface UserProps {
  id: string;
  name: string;
  email: string;
  onUpdate?: (id: string, data: Partial<UserData>) => void;
}

interface UserData {
  name: string;
  email: string;
}

const User: FC<UserProps> = ({ id, name, email, onUpdate }) => {
  const [isEditing, setIsEditing] = useState<boolean>(false);
  
  // Component implementation...
  
  return (
    // JSX...
  );
};

export default User;
```

---

## Security Considerations

* Validate all user inputs
* Use built-in XSS protection (`dangerouslySetInnerHTML` should be avoided)
* Implement proper authentication and authorization
* Sanitize data from external sources
* Follow [OWASP security best practices](https://owasp.org/www-project-top-ten/)

---

## Accessibility

* Use semantic HTML elements
* Provide alt text for images
* Ensure keyboard navigation
* Implement ARIA attributes where necessary
* Test with screen readers
* Use React's built-in accessibility features

```tsx
// Accessible button example
const Button = ({ onClick, disabled, children }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    aria-disabled={disabled}
    className={`btn ${disabled ? 'btn-disabled' : ''}`}
  >
    {children}
  </button>
);
```

---

## Environment & Secrets

* Use `.env` files for environment variables
  * Use `REACT_APP_` prefix for Create React App
  * Use `VITE_` prefix for Vite projects
* Use `dotenv` or similar for non-CRA projects
* Document required env vars in the `README`
* Consider tools like `dotenv-flow` for multi-env support

---

## Linting, Formatting, and CI

* Use Prettier for consistent formatting (`.prettierrc`)
* Use ESLint with recommended configs
  * `eslint:recommended` and `eslint-plugin-react`
  * Consider `eslint-config-react-app` for comprehensive rules
* For import aliases (like `@/components`), configure in:
  * Vite: `vite.config.js` resolve.alias
  * Webpack: `webpack.config.js` resolve.alias
  * tsconfig.json: `compilerOptions.paths`
* Use **pnpm** as the project package manager (or document if using `npm`/`yarn`)
* Add pre-commit/push hooks to run `pnpm lint && pnpm test` before pushing

---

## Images & Fonts

* Use `<img>` with `loading="lazy"` for basic lazy loading
* Consider libraries like `react-lazy-load-image-component` for advanced image loading
* Load fonts via CSS or @font-face
* Consider using Web Fonts or local font files

---

## Routing

* Use React Router (or similar) for client-side routing

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/profile/:id" element={<UserProfile />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  </BrowserRouter>
);
```

---

## Internationalization

* Use libraries like `react-i18next` or `react-intl` for translations
* Structure translation files by language
* Use context for language selection

---

## Performance

* Use code-splitting and lazy loading with `React.lazy` and `Suspense`
* Use React Profiler to analyze performance
* Memoize expensive calculations with `useMemo`
* Memoize callback functions with `useCallback`
* Use virtualization for long lists (react-window or react-virtualized)
* Implement proper loading states

```tsx
// Code splitting example
import React, { Suspense, lazy } from 'react';

const LazyComponent = lazy(() => import('./LazyComponent'));

const App = () => (
  <Suspense fallback={<div>Loading...</div>}>
    <LazyComponent />
  </Suspense>
);
```

---

## Upgrades & Compatibility

* Target **React 18.3.1** for all new projects
* Use official codemods for upgrades
* Be aware of breaking changes when upgrading
* Consider using the React 18 concurrent features:
  * `useTransition` for non-blocking updates
  * `useDeferredValue` for deferred re-renders
  * Automatic batching for better performance

---

## Appendix: Framework Comparison

| Feature                      | React        | Next.js    |
| ---------------------------- | ------------ | ---------- |
| Routing                      | React Router | App Router |
| Server Components            | No           | Yes        |
| API Routes                   | No           | Yes        |
| Data Fetch                   | Client only  | Both       |
| Built-in image/font          | No           | Yes        |
| Route-level error boundaries | No           | Yes        |
