# Quality Assurance Guide for LLM-Assisted Development

**File Purpose:** Provides concise QA guidelines for LLM coding agents to ensure the generation of reliable, testable, and production-ready code for small to medium projects.

**Applies To:**
*   Small-Medium Web App Projects
*   React 18.3.1
*   Next.js 14.2.0

**Last Updated:** 2025-05-28

---

## Core QA Principles for LLMs

When generating or reviewing code, LLM agents should prioritize:

*   **Testable Code:** Generate functions, components, and modules that are easily testable in isolation.
*   **Critical Path Focus:** Emphasize testing core user flows and business-critical logic.
*   **Clear Assertions:** Tests should have obvious and unambiguous success/failure conditions.
*   **Error State Coverage:** Ensure basic error handling and unhappy paths are considered.
*   **Accessibility Basics:** Incorporate fundamental accessibility attributes.

---

## Simplified Testing Strategies

### 1. Unit Tests (Jest)

**Focus:** Utility functions, custom hooks, complex business logic.
**LLM Task:** "Write Jest unit tests for the following utility function..."

```typescript
// Example: utils/math.ts
export function add(a: number, b: number): number {
  return a + b;
}

// Example Test: utils/math.test.ts
import { add } from './math';

describe('add', () => {
  it('should return the sum of two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('should handle negative numbers', () => {
    expect(add(-1, -1)).toBe(-2);
  });
});
```

### 2. Component Tests (React Testing Library + Jest)

**Focus:** Component rendering, basic user interactions, prop handling.
**LLM Task:** "Write React Testing Library tests for this Button component to check rendering and click handling."

```tsx
// Example: components/ui/Button.tsx
'use client'; // If client-side interactivity is needed

interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  disabled?: boolean;
}

export default function Button({ onClick, children, disabled }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

// Example Test: components/ui/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders correctly with children', () => {
    render(<Button onClick={() => {}}>Click Me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick prop when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Submit</Button>);
    fireEvent.click(screen.getByText(/submit/i));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button onClick={() => {}} disabled>Disabled</Button>);
    expect(screen.getByRole('button', { name: /disabled/i })).toBeDisabled();
  });
});
```

### 3. E2E Tests (Playwright - Minimalist)

**Focus:** 1-2 critical user flows (e.g., login, core feature).
**LLM Task:** "Write a simple Playwright E2E test for the login flow on the `/login` page."

```typescript
// Example: tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test('user can log in successfully', async ({ page }) => {
  await page.goto('/login'); // Assuming a login page route

  // Fill in credentials
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');

  // Click login button
  await page.click('button[type="submit"]');

  // Assert navigation to dashboard or welcome message
  await expect(page).toHaveURL('/dashboard'); // Or other expected outcome
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

### 4. Mocking & Test Data

*   Use Jest's mocking capabilities (`jest.fn()`, `jest.spyOn()`, `jest.mock()`) for dependencies.
*   For API calls in Client Components, mock `fetch` or the API client module.
*   Keep test data simple and focused on the specific scenario being tested.

---

### 5. Next.js 14 Specific Testing Considerations

**Server Components Testing:**
* Test Server Components by rendering them in a test environment and asserting on their HTML output.
* Use `@testing-library/react/server` for Server Component testing.
* Focus on the rendered output rather than implementation details.

**Data Fetching Patterns:**
* Test Server Actions by mocking the server environment and asserting on return values.
* For `fetch` in Server Components, mock the global fetch or use MSW (Mock Service Worker).
* Test client-side data mutations by mocking the server response and verifying UI updates.

**Middleware Testing:**
* Create unit tests for middleware logic in isolation.
* Use integration tests with mocked Request/Response objects to test middleware behavior.
* E2E tests should verify the complete middleware flow in critical user paths.

---

## Key QA Checks for LLM-Generated Code

LLMs should be prompted or configured to adhere to these checks:

*   **Linting & Formatting:**
    *   Ensure code passes ESLint checks (refer to `guide.coding.next.js.14.2.0.md` or `guide.coding.react.18.3.1.md`).
    *   Apply Prettier formatting.
*   **Type Checking (TypeScript):**
    *   Strictly avoid `any` type unless absolutely necessary and justified.
    *   Ensure all functions have explicit return types.
    *   Props and state should be strongly typed.
*   **Basic Accessibility:**
    *   Images must have `alt` attributes: `<Image src="..." alt="Descriptive text" ... />`.
    *   Use semantic HTML elements (`<nav>`, `<main>`, `<button>`).
    *   Interactive elements should be keyboard navigable.
*   **Error Handling:**
    *   Server Components & Actions: Use `try/catch` for operations that can fail.
    *   Client Components: Handle promise rejections, display user-friendly error messages.
    *   Forms: Implement basic client-side and server-side validation.
    ```tsx
    // Basic error display in a Client Component
    'use client';
    import { useState, useEffect } from 'react';

    function UserData({ userId }) {
      const [data, setData] = useState(null);
      const [error, setError] = useState<string | null>(null);

      useEffect(() => {
        fetch(`/api/users/${userId}`)
          .then(res => {
            if (!res.ok) throw new Error('Failed to fetch user');
            return res.json();
          })
          .then(setData)
          .catch(err => setError(err.message));
      }, [userId]);

      if (error) return <p>Error: {error}</p>;
      if (!data) return <p>Loading...</p>;
      return <div>{/* Render data */}</div>;
    }
    ```
*   **Performance Snippets:**
    *   Next.js: Use `<Image>` for image optimization.
    *   Next.js: Use `next/dynamic` for lazy loading components/pages.
    *   React: Use `React.lazy` and `<Suspense>` for code splitting.
*   **Security Snippets:**
    *   Validate user input on both client and server (e.g., using Zod).
    *   Do not expose sensitive keys or logic in client-side code.
    *   Use environment variables for API keys (`process.env.MY_API_KEY` on server, `process.env.NEXT_PUBLIC_MY_KEY` for client-side Next.js).

---

## LLM Interaction for QA

*   **Prompt for Test Generation:**
    *   "Generate unit tests for this function using Jest."
    *   "Write React Testing Library tests for this component's loading and error states."
    *   "Create a Playwright test for the add-to-cart functionality."
*   **Request Testable Code:**
    *   "Refactor this component to make it more testable."
    *   "Implement this feature ensuring all crucial logic is unit-testable."
*   **Analyze Test Failures:**
    *   "This Jest test is failing with [error message]. What could be the cause?"
    *   "Explain why this Playwright test might be flaky."

---

## Essential Tools & Commands (Simplified)

| Task                  | Tool/Command                            | Notes                                     |
| --------------------- | --------------------------------------- | ----------------------------------------- |
| Run Unit/Comp. Tests  | `pnpm test` or `npm test`               | Executes Jest tests                       |
| Run E2E Tests         | `pnpm playwright test`                  | Executes Playwright tests                 |
| Lint Code             | `pnpm lint` or `npm run lint`           | Runs ESLint                               |
| Type Check            | `pnpm type-check` or `npm run tsc`      | Runs TypeScript compiler (`tsc --noEmit`) |
| Check Bundle (Next.js)| `pnpm build && pnpm analyze`            | (If `next-bundle-analyzer` is set up)     |
| Format Code           | `pnpm format` or `npm run prettier`     | Runs Prettier                             |

---

This guide aims to streamline the QA process when working with LLM coding agents, focusing on practical steps to enhance code quality and reliability.