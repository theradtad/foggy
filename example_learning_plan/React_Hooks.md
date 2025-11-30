# Learning Plan: Mastering React Hooks

## Learning Plan: Mastering React Hooks

**Goal:** To understand, implement, and effectively use React Hooks to build robust and maintainable React applications.

**Prerequisites Assessed:**
*   **JavaScript Fundamentals:** Decent knowledge (Good to go!)
*   **React Fundamentals (Components, Props):** Basic understanding (We'll build upon this!)
*   **HTML & CSS Basics:** Assumed basic knowledge for web development.

---

### Phase 1: Core Concepts & Understanding Hooks

**Objective:** Understand what React Hooks are, why they were introduced, and grasp the fundamental `useState` and `useEffect` hooks.

**Modules:**

1.  **Introduction to React Hooks:**
    *   **Concepts:**
        *   What problems do Hooks solve? (e.g., class components complexity, `this` binding, prop drilling, reusable logic)
        *   The "Rules of Hooks" (Why they exist and how to follow them)
        *   Function Components vs. Class Components with Hooks
    *   **Examples:**
        *   Simple function component before and after hooks.
        *   Illustrating the limitations of class components that hooks address.
    *   **Assessment:** Explain in your own words the main benefits of using Hooks.

2.  **`useState` Hook: Managing State in Function Components:**
    *   **Concepts:**
        *   Declaring state variables with `useState`.
        *   Reading and updating state.
        *   Understanding the immutability of state.
        *   Initial state values (functions for expensive initializations).
    *   **Examples:**
        *   Counter application using `useState`.
        *   Form input management with multiple `useState` calls.
        *   Toggling visibility of an element.
    *   **Project Idea (Mini):** Build a simple "To-Do List" application where you can add and mark items as complete using `useState`.
    *   **Assessment:** Implement a component that manages a user's name and age using `useState`.

3.  **`useEffect` Hook: Handling Side Effects:**
    *   **Concepts:**
        *   What are side effects in React? (data fetching, subscriptions, manually changing the DOM)
        *   When and how `useEffect` runs (after every render, cleanup function).
        *   Dependency array: controlling effect re-runs.
        *   Cleanup function for effects (e.g., unsubscribing, clearing timers).
    *   **Examples:**
        *   Fetching data from an API on component mount.
        *   Setting up and tearing down event listeners.
        *   Updating the document title.
        *   Comparing effects with and without dependency array.
    *   **Project Idea (Mini):** Create a component that fetches a list of posts from a public API (e.g., JSONPlaceholder) and displays them. Implement a cleanup function for any subscriptions or timers.
    *   **Assessment:** Create a component that displays the current window width and updates it on resize, using `useEffect` with proper cleanup.

---

### Phase 2: Advanced Hooks & Custom Hooks

**Objective:** Explore more advanced built-in hooks and learn to create reusable logic with custom hooks.

**Modules:**

4.  **`useContext` Hook: Global State Management:**
    *   **Concepts:**
        *   The problem of "prop drilling."
        *   Creating and providing context.
        *   Consuming context with `useContext`.
    *   **Examples:**
        *   Implementing a theme switcher (light/dark mode) using `useContext`.
        *   Passing user authentication status down the component tree.
    *   **Assessment:** Refactor your "To-Do List" application to use `useContext` for managing a global filter (e.g., "All", "Active", "Completed").

5.  **`useRef` Hook: Accessing DOM and Mutable Values:**
    *   **Concepts:**
        *   When to use `useRef` (not for re-renders).
        *   Accessing DOM elements directly.
        *   Storing mutable values that don't trigger re-renders.
    *   **Examples:**
        *   Focusing an input field on component mount.
        *   Creating a generic ref for a video player.
        *   Storing a previous value of a state variable.
    *   **Assessment:** Build a component with an input field and a button. When the button is clicked, the input field should be focused using `useRef`.

6.  **`useReducer` Hook: Complex State Logic:**
    *   **Concepts:**
        *   When `useReducer` is preferred over `useState` (complex state transitions, multiple sub-values).
        *   Reducer function structure (`(state, action) => newState`).
        *   Dispatching actions.
        *   Initial state and lazy initialization.
    *   **Examples:**
        *   Re-implementing the counter with `useReducer` (increment, decrement, reset).
        *   Managing a more complex form state (e.g., multiple fields with validation).
    *   **Assessment:** Convert your "To-Do List" application's state management from `useState` to `useReducer`.

7.  **`useCallback` & `useMemo` Hooks: Performance Optimization:**
    *   **Concepts:**
        *   Understanding unnecessary re-renders in React.
        *   `useCallback`: memoizing functions to prevent re-creation on every render.
        *   `useMemo`: memoizing expensive computations.
        *   When and when *not* to use these hooks.
    *   **Examples:**
        *   Passing a memoized callback to a child component to prevent its re-render.
        *   Memoizing a filtered list or a complex calculation.
    *   **Assessment:** Identify a scenario in one of your previous projects where `useCallback` or `useMemo` could improve performance and implement it.

8.  **Custom Hooks: Reusable Logic:**
    *   **Concepts:**
        *   The "use" naming convention.
        *   Extracting common logic into custom hooks.
        *   Sharing stateful logic between components.
    *   **Examples:**
        *   Creating a `useWindowSize` hook.
        *   Building a `useLocalStorage` hook.
        *   Developing a `useFetch` hook for data fetching.
    *   **Project Idea (Mini):** Create a custom hook called `useDarkMode` that manages a dark mode setting using `localStorage` and provides a toggle function.
    *   **Assessment:** Develop a custom hook that tracks whether a component is currently hovered over.

---

### Phase 3: Putting It All Together (Project)

**Objective:** Apply all learned concepts to build a more substantial application.

**Project: Interactive Dashboard/Data Viewer**

*   **Description:** Build a single-page application that fetches data from an API (e.g., a list of products, users, or articles) and allows users to interact with it.
*   **Requirements:**
    *   **Data Fetching:** Use `useEffect` and a custom `useFetch` hook to fetch data.
    *   **State Management:** Utilize `useState` and/or `useReducer` for managing UI state (e.g., loading indicators, error messages, form inputs).
    *   **Filtering/Sorting:** Implement filtering and sorting options for the displayed data using `useState` and potentially `useMemo` for performance.
    *   **Theming (Optional but Recommended):** Implement a theme switcher using `useContext` and a custom `useTheme` hook.
    *   **User Interactions:** Include interactive elements like buttons, input fields, and potentially modals.
    *   **Refs:** Use `useRef` for any direct DOM manipulations (e.g., focusing an input).
*   **Assessment:**
    *   Code review of the project, focusing on correct and idiomatic use of React Hooks.
    *   Ability to explain design choices and hook implementations.

---

**Next Steps:**

I'll now save this learning plan for you. You can refer back to it as you progress. Let me know if you have any questions or want to adjust anything!