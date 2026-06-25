# Frontend Architecture – Vite + React + TS

This directory holds the Single Page Application UI built on React, TypeScript, and TailwindCSS.

## Project Structure

* **`src/app/`**: Application state handlers and query clients.
* **`src/components/`**: Common presentation components (e.g. ErrorBoundary, ProtectedRoute).
* **`src/contexts/`**: Shared session providers (e.g. ThemeContext).
* **`src/layouts/`**: UI frame layouts (e.g. DashboardLayout, AuthLayout).
* **`src/pages/`**: View endpoints.
* **`src/routes/`**: Central routing table mapping routes.
* **`src/api/`**: Central Axios instances and request configurations.

## Running Locally

1. **Install Dependencies**:
   ```bash
   npm install
   ```
2. **Start Dev Server**:
   ```bash
   npm run dev
   ```
3. **Build Bundle**:
   ```bash
   npm run build
   ```
