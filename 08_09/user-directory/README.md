# UserDirectory – Angular Demo Application

## Overview

**UserDirectory** is a simple, educational Angular application

The goal of this project is **not** to build a feature-complete product, but to **demonstrate core Angular concepts clearly and cleanly**, including:

- Component–Template separation
- Data binding (interpolation, event binding, two-way binding)
- Routing with parameters
- Services and Dependency Injection
- HTTP communication with `HttpClient`
- Observable-based asynchronous data flow
- Error handling
- HTTP Interceptors
- Clean, readable project structure

The application fetches user data from a public REST API and displays it in a simple UI.

---

## Application Features

- 📋 User list loaded from a REST API
- 🔍 Client-side search (name / email)
- 📄 User details page with route parameters
- ⏳ Loading state handling
- ❌ Error handling (network / backend errors)
- 🔐 HTTP interceptor example (custom header + logging)

---

## Technology Stack

- **Angular**: 17+
- **Node.js**: 22.x
- **Angular CLI**
- **TypeScript**
- **RxJS**
- **REST API**: https://jsonplaceholder.typicode.com/users

---

## Project Architecture (High Level)

```
src/app/
 ├── core/            # Services, interceptors (application logic)
 ├── models/          # TypeScript interfaces (data models)
 ├── pages/           # Feature pages (User List, User Details)
 ├── shared/          # Shared UI components (Navbar, etc.)
 ├── app.module.ts    # Root Angular module (NgModule-based)
 ├── app-routing.module.ts
```

> ⚠️ **Important:**  
> This project intentionally uses the **classic `AppModule` (NgModule) architecture**,  
> not the newer standalone component approach, because it is easier to teach and understand.

---

## Prerequisites

Make sure the following tools are installed on your machine:

- **Node.js** `22.x`
- **npm** (comes with Node.js)
- **Angular CLI** (optional – project can also be run via `npx`)

Verify versions:

```bash
node -v
npm -v
```

---

## Install Dependencies

After cloning or downloading the project:

```bash
npm install
```

---

## Run in Development Mode

To start the development server:

```bash
ng serve
```

or (without global CLI):

```bash
npx ng serve
```

Then open your browser at:

```
http://localhost:4200
```

### Development Mode Characteristics
- Hot reload enabled
- Source maps enabled
- Optimized for debugging and learning
- Not optimized for performance

---

## Run in Production Mode

### Build the application

```bash
ng build
```

The production build output will be generated in:

```
dist/user-directory/
```

### Serve the production build

Angular itself does **not** serve production builds.
You can use any static web server, for example:

#### Option 1: `serve` (simple local test)
```bash
npx serve dist/user-directory
```

#### Option 2: Any web server
- Nginx
- Apache
- IIS
- Cloud hosting (S3, Azure Static Web Apps, etc.)

### Production Mode Characteristics
- Minified and optimized code
- No hot reload
- Faster load time
- Suitable for deployment

---

## Environment Configuration

This demo uses a **public REST API**, so no backend setup is required.

API URL used:
```
https://jsonplaceholder.typicode.com/users
```

---

## Educational Notes

- HTTP calls are handled **only in services**
- Components are responsible **only for UI and state**
- Observables are used instead of Promises
- Error handling is centralized and simplified
- Code is intentionally verbose and commented for clarity

This structure mirrors **real-world Angular enterprise applications**, while remaining easy to understand for beginners.

---

## Common Commands Reference

```bash
ng serve              # Run dev server
ng build              # Production build
ng generate component # Generate component
ng generate service   # Generate service
```

---

## License / Usage

This project is intended for **educational purposes**.
You are free to modify, extend, and reuse it for learning or teaching.
