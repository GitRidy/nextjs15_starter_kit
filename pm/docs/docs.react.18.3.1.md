# React 18.3.1 Framework Documentation

**File Purpose:** Essential React 18.3.1 reference for LLM-assisted development of small web applications.

**Applies To:**
* Small Web App Projects
* React 18.3.1

**Last Updated:** 2025-05-28

---

## Quick Start

### Project Setup
```bash
# Create new React app
npx create-react-app my-app --template typescript
cd my-app

# Or with Vite (faster)
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```

### Essential Dependencies
```bash
# Core dependencies usually included
npm install react@18.3.1 react-dom@18.3.1

# Common additional packages
npm install react-router-dom@6 
npm install @tanstack/react-query    # For data fetching
npm install zustand                  # Simple state management
npm install clsx                     # Conditional classes
```

---

## Core Concepts

### Function Components (Preferred)
```tsx
// Basic component
function Welcome({ name }: { name: string }) {
  return <h1>Hello, {name}!</h1>;
}

// With props interface
interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
}

function Button({ children, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}
```

### JSX Essentials
```tsx
function App() {
  const user = { name: 'Alice', age: 30 };
  const isLoggedIn = true;
  const items = ['apple', 'banana', 'cherry'];

  return (
    <div>
      {/* Conditional rendering */}
      {isLoggedIn ? <h1>Welcome, {user.name}!</h1> : <h1>Please log in</h1>}
      
      {/* Lists */}
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
      
      {/* Conditional classes */}
      <div className={`card ${isLoggedIn ? 'active' : 'inactive'}`}>
        Content
      </div>
    </div>
  );
}
```

---

## React 18 Hooks

### useState - Component State
```tsx
function Counter() {
  const [count, setCount] = useState(0);
  const [user, setUser] = useState<User | null>(null);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
      <button onClick={() => setCount(prev => prev - 1)}>-</button>
    </div>
  );
}
```

### useEffect - Side Effects
```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch data on mount and when userId changes
  useEffect(() => {
    async function fetchUser() {
      setLoading(true);
      try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        setUser(userData);
      } catch (error) {
        console.error('Failed to fetch user:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, [userId]); // Dependencies array

  // Cleanup example
  useEffect(() => {
    const timer = setInterval(() => {
      console.log('Timer tick');
    }, 1000);

    return () => clearInterval(timer); // Cleanup
  }, []);

  if (loading) return <div>Loading...</div>;
  if (!user) return <div>User not found</div>;

  return <div>Welcome, {user.name}!</div>;
}
```

### useContext - Share State
```tsx
// Create context
const ThemeContext = createContext<'light' | 'dark'>('light');

// Provider component
function App() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  return (
    <ThemeContext.Provider value={theme}>
      <Header />
      <Main />
    </ThemeContext.Provider>
  );
}

// Consume context
function Header() {
  const theme = useContext(ThemeContext);
  return <header className={`header-${theme}`}>Header</header>;
}
```

### useReducer - Complex State Logic
```tsx
interface State {
  count: number;
  error: string | null;
}

type Action = 
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' }
  | { type: 'error'; payload: string };

function counterReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + 1, error: null };
    case 'decrement':
      return { ...state, count: state.count - 1, error: null };
    case 'reset':
      return { ...state, count: 0, error: null };
    case 'error':
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(counterReducer, { count: 0, error: null });

  return (
    <div>
      <p>Count: {state.count}</p>
      {state.error && <p>Error: {state.error}</p>}
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

### useMemo & useCallback - Performance
```tsx
function ExpensiveComponent({ items, filter }: { items: Item[]; filter: string }) {
  // Memoize expensive calculations
  const filteredItems = useMemo(() => {
    return items.filter(item => 
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);

  // Memoize callbacks to prevent unnecessary re-renders
  const handleItemClick = useCallback((itemId: string) => {
    console.log('Clicked item:', itemId);
  }, []);

  return (
    <ul>
      {filteredItems.map(item => (
        <li key={item.id} onClick={() => handleItemClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}
```

### Custom Hooks
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

// Usage
function UserList() {
  const { data: users, loading, error } = useApi<User[]>('/api/users');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!users) return <div>No users found</div>;

  return (
    <ul>
      {users.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}
```

---

## React 18 New Features

### Automatic Batching
```tsx
// React 18 automatically batches these updates
function handleClick() {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Both updates batched automatically, only one re-render
}

// Even in timeouts and promises
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Still batched in React 18
}, 1000);
```

### Suspense for Data Fetching
```tsx
import { Suspense } from 'react';

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UserProfile />
      <Posts />
    </Suspense>
  );
}

// Component that uses suspense-enabled data fetching
function UserProfile() {
  // Using a library like SWR or React Query with suspense
  const user = useSWR('/api/user', { suspense: true });
  return <div>Welcome, {user.name}!</div>;
}
```

### Concurrent Features (useTransition)
```tsx
import { useTransition, startTransition } from 'react';

function SearchResults() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  function handleSearch(newQuery: string) {
    setQuery(newQuery); // Urgent update
    
    startTransition(() => {
      // Non-urgent update - can be interrupted
      setResults(performExpensiveSearch(newQuery));
    });
  }

  return (
    <div>
      <input 
        value={query} 
        onChange={e => handleSearch(e.target.value)} 
      />
      {isPending && <div>Searching...</div>}
      <ResultsList results={results} />
    </div>
  );
}
```

---

## Component Patterns

### Composition Pattern
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

### Render Props Pattern
```tsx
interface MouseTrackerProps {
  children: (mouse: { x: number; y: number }) => React.ReactNode;
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [mouse, setMouse] = useState({ x: 0, y: 0 });

  useEffect(() => {
    function handleMouseMove(e: MouseEvent) {
      setMouse({ x: e.clientX, y: e.clientY });
    }

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{children(mouse)}</>;
}

// Usage
function App() {
  return (
    <MouseTracker>
      {({ x, y }) => (
        <div>Mouse position: {x}, {y}</div>
      )}
    </MouseTracker>
  );
}
```

### Higher-Order Component (Less Common)
```tsx
function withAuth<P extends object>(Component: React.ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const { user, loading } = useAuth();
    
    if (loading) return <div>Loading...</div>;
    if (!user) return <div>Please log in</div>;
    
    return <Component {...props} />;
  };
}

// Usage
const ProtectedProfile = withAuth(UserProfile);
```

---

## Forms and Events

### Form Handling
```tsx
function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  }

  function validateForm() {
    const newErrors: Record<string, string> = {};
    
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    if (!formData.message.trim()) newErrors.message = 'Message is required';
    
    return newErrors;
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    
    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // Submit form
    console.log('Submitting:', formData);
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>
      
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>
      
      <div>
        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleChange}
        />
        {errors.message && <span className="error">{errors.message}</span>}
      </div>
      
      <button type="submit">Send Message</button>
    </form>
  );
}
```

### Event Handling
```tsx
function EventExamples() {
  // Click events
  function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
    console.log('Button clicked');
    e.preventDefault(); // If needed
  }

  // Keyboard events
  function handleKeyPress(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') {
      console.log('Enter pressed');
    }
  }

  // Form events
  function handleFormSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    console.log('Form data:', Object.fromEntries(formData));
  }

  return (
    <div>
      <button onClick={handleClick}>Click me</button>
      <input onKeyPress={handleKeyPress} placeholder="Press Enter" />
      <form onSubmit={handleFormSubmit}>
        <input name="username" placeholder="Username" />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
```

---

## Error Boundaries

```tsx
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends React.Component<
  React.PropsWithChildren<{}>,
  ErrorBoundaryState
> {
  constructor(props: React.PropsWithChildren<{}>) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.message}</pre>
          </details>
          <button onClick={() => window.location.reload()}>
            Refresh page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary>
      <Header />
      <Main />
      <Footer />
    </ErrorBoundary>
  );
}
```

---

## Performance Optimization

### React.memo - Prevent Unnecessary Re-renders
```tsx
interface UserCardProps {
  user: User;
  onEdit: (userId: string) => void;
}

const UserCard = React.memo(({ user, onEdit }: UserCardProps) => {
  console.log(`Rendering ${user.name}`);
  
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <button onClick={() => onEdit(user.id)}>Edit</button>
    </div>
  );
});

// Custom comparison function (optional)
const MemoizedComponent = React.memo(Component, (prevProps, nextProps) => {
  return prevProps.user.id === nextProps.user.id;
});
```

### Lazy Loading Components
```tsx
import { lazy, Suspense } from 'react';

// Lazy load heavy components
const AdminPanel = lazy(() => import('./AdminPanel'));
const Chart = lazy(() => import('./Chart'));

function App() {
  const [showAdmin, setShowAdmin] = useState(false);

  return (
    <div>
      <header>My App</header>
      <main>
        <button onClick={() => setShowAdmin(!showAdmin)}>
          Toggle Admin
        </button>
        
        {showAdmin && (
          <Suspense fallback={<div>Loading admin panel...</div>}>
            <AdminPanel />
          </Suspense>
        )}
        
        <Suspense fallback={<div>Loading chart...</div>}>
          <Chart data={chartData} />
        </Suspense>
      </main>
    </div>
  );
}
```

### useDeferredValue - Defer Non-Critical Updates
```tsx
import { useDeferredValue, useMemo } from 'react';

function ProductList({ searchQuery }: { searchQuery: string }) {
  const deferredQuery = useDeferredValue(searchQuery);
  
  const filteredProducts = useMemo(() => {
    // This expensive operation uses the deferred value
    return products.filter(product =>
      product.name.toLowerCase().includes(deferredQuery.toLowerCase())
    );
  }, [deferredQuery]);

  return (
    <div>
      {/* Show immediate feedback for typing */}
      <p>Searching for: {searchQuery}</p>
      
      {/* Deferred results don't block input */}
      <ul>
        {filteredProducts.map(product => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Routing with React Router

### Basic Setup
```tsx
import { BrowserRouter, Routes, Route, Link, useParams } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/users">Users</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users" element={<Users />} />
        <Route path="/users/:id" element={<UserProfile />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

function UserProfile() {
  const { id } = useParams<{ id: string }>();
  return <div>User Profile for ID: {id}</div>;
}
```

### Navigation Hooks
```tsx
import { useNavigate, useLocation } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Get redirect path from location state
  const from = location.state?.from?.pathname || '/dashboard';

  function handleLogin() {
    // Perform login logic
    authenticate().then(() => {
      navigate(from, { replace: true });
    });
  }

  return (
    <form onSubmit={handleLogin}>
      <input type="email" placeholder="Email" />
      <input type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  );
}
```

---

## State Management

### Context + useReducer Pattern
```tsx
// Types
interface AppState {
  user: User | null;
  theme: 'light' | 'dark';
  notifications: Notification[];
}

type AppAction =
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'TOGGLE_THEME' }
  | { type: 'ADD_NOTIFICATION'; payload: Notification }
  | { type: 'REMOVE_NOTIFICATION'; payload: string };

// Reducer
function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'TOGGLE_THEME':
      return { ...state, theme: state.theme === 'light' ? 'dark' : 'light' };
    case 'ADD_NOTIFICATION':
      return { ...state, notifications: [...state.notifications, action.payload] };
    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload)
      };
    default:
      return state;
  }
}

// Context
const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | null>(null);

// Provider
function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, {
    user: null,
    theme: 'light',
    notifications: []
  });

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

// Custom hook
function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
}

// Usage
function Header() {
  const { state, dispatch } = useApp();
  
  return (
    <header className={`header-${state.theme}`}>
      <h1>My App</h1>
      {state.user && <span>Welcome, {state.user.name}</span>}
      <button onClick={() => dispatch({ type: 'TOGGLE_THEME' })}>
        Toggle Theme
      </button>
    </header>
  );
}
```

### Simple Global State with Zustand
```tsx
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

## Data Fetching with TanStack Query

### Basic Setup
```tsx
import { QueryClient, QueryClientProvider, useQuery, useMutation } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <UserList />
    </QueryClientProvider>
  );
}

// Fetch data
function UserList() {
  const { 
    data: users, 
    isLoading, 
    error 
  } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(res => res.json())
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading users</div>;

  return (
    <ul>
      {users?.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}

// Mutations
function CreateUser() {
  const mutation = useMutation({
    mutationFn: (userData: User) => 
      fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });

  return (
    <button 
      onClick={() => mutation.mutate({ name: 'New User', email: 'user@example.com' })}
      disabled={mutation.isPending}
    >
      {mutation.isPending ? 'Creating...' : 'Create User'}
    </button>
  );
}
```

---

## Testing with Jest & React Testing Library

### Component Testing
```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

test('increments count when button is clicked', async () => {
  const user = userEvent.setup();
  render(<Counter />);
  
  const button = screen.getByRole('button', { name: /increment/i });
  const countDisplay = screen.getByText(/count: 0/i);
  
  await user.click(button);
  
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
});

test('loads and displays user data', async () => {
  // Mock API response
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ id: 1, name: 'John Doe' }),
    })
  ) as jest.Mock;

  render(<UserProfile userId="1" />);
  
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  await waitFor(() => {
    expect(screen.getByText(/john doe/i)).toBeInTheDocument();
  });
  
  expect(fetch).toHaveBeenCalledWith('/api/users/1');
});
```

### Custom Hook Testing
```tsx
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

test('useCounter increments count', () => {
  const { result } = renderHook(() => useCounter());
  
  expect(result.current.count).toBe(0);
  
  act(() => {
    result.current.increment();
  });
  
  expect(result.current.count).toBe(1);
});
```

---

## TypeScript Integration

### Component Props
```tsx
// Basic props
interface UserProps {
  name: string;
  age?: number;
  onEdit: (id: string) => void;
}

// Children props
interface LayoutProps {
  children: React.ReactNode;
  sidebar?: React.ReactNode;
}

// Generic components
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
}
```

### Event Types
```tsx
function FormExample() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
  };

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    console.log('Clicked');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      console.log('Enter pressed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} onKeyDown={handleKeyDown} />
      <button onClick={handleClick}>Submit</button>
    </form>
  );
}
```

### Ref Types
```tsx
function RefExample() {
  const inputRef = useRef<HTMLInputElement>(null);
  const divRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div ref={divRef}>
      <input ref={inputRef} type="text" />
    </div>
  );
}
```

---

## Common Patterns & Best Practices

### Compound Components
```tsx
interface TabsContextType {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function Tabs({ children, defaultTab }: { children: React.ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">
        {children}
      </div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');
  
  const { activeTab, setActiveTab } = context;
  
  return (
    <button
      className={`tab ${activeTab === id ? 'active' : ''}`}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabPanel must be used within Tabs');
  
  const { activeTab } = context;
  
  if (activeTab !== id) return null;
  
  return <div className="tab-panel">{children}</div>;
}

// Usage
function App() {
  return (
    <Tabs defaultTab="tab1">
      <TabList>
        <Tab id="tab1">Tab 1</Tab>
        <Tab id="tab2">Tab 2</Tab>
        <Tab id="tab3">Tab 3</Tab>
      </TabList>
      
      <TabPanel id="tab1">Content of Tab 1</TabPanel>
      <TabPanel id="tab2">Content of Tab 2</TabPanel>
      <TabPanel id="tab3">Content of Tab 3</TabPanel>
    </Tabs>
  );
}
```

### Portal Usage
```tsx
import { createPortal } from 'react-dom';

function Modal({ isOpen, onClose, children }: {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        {children}
      </div>
    </div>,
    document.body
  );
}
```

### Custom Hooks Patterns
```tsx
// Local storage hook
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}

// Debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Online status hook
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(() => 
    typeof navigator !== 'undefined' && typeof navigator.onLine === 'boolean'
      ? navigator.onLine
      : true
  );

  useEffect(() => {
    const updateOnlineStatus = () => setIsOnline(navigator.onLine);

    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);

    return () => {
      window.removeEventListener('online', updateOnlineStatus);
      window.removeEventListener('offline', updateOnlineStatus);
    };
  }, []);

  return isOnline;
}

// Previous value hook
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => {
    ref.current = value;
  });
  return ref.current;
}
```

---

## Performance Tips & Common Pitfalls

### Avoid Unnecessary Re-renders
```tsx
// ❌ Bad - creates new object on every render
function BadExample({ items }: { items: Item[] }) {
  return <ItemList items={items} style={{ margin: 10 }} />;
}

// ✅ Good - stable object reference
const listStyle = { margin: 10 };
function GoodExample({ items }: { items: Item[] }) {
  return <ItemList items={items} style={listStyle} />;
}

// ❌ Bad - creates new function on every render
function BadEventHandler({ onSave }: { onSave: (data: Data) => void }) {
  return (
    <Form onSubmit={(data) => {
      console.log('Submitting:', data);
      onSave(data);
    }} />
  );
}

// ✅ Good - memoized callback
function GoodEventHandler({ onSave }: { onSave: (data: Data) => void }) {
  const handleSubmit = useCallback((data: Data) => {
    console.log('Submitting:', data);
    onSave(data);
  }, [onSave]);

  return <Form onSubmit={handleSubmit} />;
}
```

### Proper Key Usage
```tsx
// ❌ Bad - using array index as key
function BadList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{item.name}</li>
      ))}
    </ul>
  );
}

// ✅ Good - using stable unique identifier
function GoodList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

### State Updates
```tsx
// ❌ Bad - mutating state directly
function BadCounter() {
  const [items, setItems] = useState([]);
  
  const addItem = (item) => {
    items.push(item); // Direct mutation
    setItems(items);
  };
}

// ✅ Good - immutable updates
function GoodCounter() {
  const [items, setItems] = useState([]);
  
  const addItem = useCallback((item) => {
    setItems(prev => [...prev, item]);
  }, []);
}
```

---

## Development Tools & Debugging

### React DevTools
```tsx
// Add display names for debugging
const MyComponent = () => <div>Hello</div>;
MyComponent.displayName = 'MyComponent';

// Use React.StrictMode in development
function App() {
  return (
    <React.StrictMode>
      <MyApp />
    </React.StrictMode>
  );
}
```

### Error Handling & Logging
```tsx
// Development vs Production error handling
const isDevelopment = process.env.NODE_ENV === 'development';

function logError(error: Error, errorInfo?: any) {
  if (isDevelopment) {
    console.error('Error:', error);
    console.error('Error Info:', errorInfo);
  } else {
    // Send to error reporting service
    // errorReportingService.captureException(error, errorInfo);
  }
}

// Custom error hook
function useErrorHandler() {
  return useCallback((error: Error, errorInfo?: any) => {
    logError(error, errorInfo);
  }, []);
}
```

---

## Build & Deployment Considerations

### Environment Variables
```tsx
// Using environment variables
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';
const IS_PRODUCTION = process.env.NODE_ENV === 'production';

// Type-safe environment variables
interface EnvironmentVariables {
  REACT_APP_API_URL: string;
  REACT_APP_GA_TRACKING_ID?: string;
}

const env: EnvironmentVariables = {
  REACT_APP_API_URL: process.env.REACT_APP_API_URL!,
  REACT_APP_GA_TRACKING_ID: process.env.REACT_APP_GA_TRACKING_ID,
};
```

### Code Splitting Strategies
```tsx
// Route-based code splitting
const HomePage = lazy(() => import('./pages/HomePage'));
const AboutPage = lazy(() => import('./pages/AboutPage'));
const AdminPage = lazy(() => import('./pages/AdminPage'));

function App() {
  return (
    <Router>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

// Feature-based code splitting
const AdminFeatures = lazy(() => 
  import('./features/admin').then(module => ({ default: module.AdminFeatures }))
);
```

---

## Migration & Upgrade Notes

### From React 17 to 18
```tsx
// React 18 root API
// Old way (React 17)
import ReactDOM from 'react-dom';
ReactDOM.render(<App />, document.getElementById('root'));

// New way (React 18)
import { createRoot } from 'react-dom/client';
const container = document.getElementById('root')!;
const root = createRoot(container);
root.render(<App />);
```

### Preparing for React 19
```tsx
// Use React 18.3.1 compatible patterns
// Avoid deprecated features like:
// - String refs (use useRef instead)
// - Legacy context API (use new Context API)
// - UNSAFE_* lifecycle methods

// Prepare for future features
// - Use Suspense for data fetching when libraries support it
// - Consider Server Components patterns for Next.js projects
// - Use concurrent features like useTransition when appropriate
```

---

## Quick Reference

### Essential Hooks Summary
| Hook | Purpose | Example |
|------|---------|---------|
| `useState` | Local component state | `const [count, setCount] = useState(0)` |
| `useEffect` | Side effects, lifecycle | `useEffect(() => {}, [deps])` |
| `useContext` | Consume context | `const value = useContext(MyContext)` |
| `useReducer` | Complex state logic | `const [state, dispatch] = useReducer(reducer, initial)` |
| `useMemo` | Memoize expensive calculations | `const value = useMemo(() => calculate(), [deps])` |
| `useCallback` | Memoize functions | `const fn = useCallback(() => {}, [deps])` |
| `useRef` | DOM access, mutable values | `const ref = useRef(null)` |

### Common Patterns Checklist
- [ ] Use functional components with hooks
- [ ] Implement proper error boundaries
- [ ] Use TypeScript for type safety
- [ ] Implement loading and error states
- [ ] Use React.memo for performance optimization
- [ ] Implement proper key props for lists
- [ ] Use custom hooks for reusable logic
- [ ] Implement proper form validation
- [ ] Use Suspense for code splitting
- [ ] Follow accessibility best practices

### Performance Checklist
- [ ] Use React DevTools Profiler
- [ ] Implement code splitting for large apps
- [ ] Optimize images and assets
- [ ] Use production builds for deployment
- [ ] Monitor bundle size
- [ ] Implement proper caching strategies
- [ ] Use memoization judiciously
- [ ] Avoid unnecessary re-renders

---

## Resources

### Official Documentation
- [React 18 Documentation](https://18.react.dev/reference/react)

### Recommended Libraries
- **Routing**: React Router v6
- **State Management**: Zustand, Redux Toolkit
- **Data Fetching**: TanStack Query, SWR
- **Forms**: React Hook Form, Formik
- **UI Libraries**: Material-UI, Ant Design, Chakra UI
- **Testing**: React Testing Library, Jest
- **Build Tools**: Vite, Create React App

### Best Practices
- Follow the [Rules of Hooks](https://react.dev/warnings/invalid-hook-call-warning)
- Use [ESLint React Hooks plugin](https://www.npmjs.com/package/eslint-plugin-react-hooks)
- Implement proper [Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- Follow [React accessibility guidelines](https://react.dev/learn/accessibility)
- Use [React Strict Mode](https://react.dev/reference/react/StrictMode) in development