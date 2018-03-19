# Frontend Development

## 0. Frameworks

EFLA-web uses:

- NPM as package manager
- Angular for an interactive Frontend
- Fluture and Ramda for computational beauty

## 1. Tools

### 1.1 JavaScript

When editing JavaScript, run `npm run watchJS` in a separate terminal. This
continually compiles your code while you write it.

As long as your container runs as described in deployment.md, you can just
reload the frontend and your changes will be there.

### 2.2 SCSS

When editing the SCSS, you have to either set your editor up with a watcher or
regularly execute `npm run compileSCSS` or one of the specific commands.

There is also a separate compilation command for each of backend, landing page
and survey, for the case that you want to compile just one to save time.

## 2. Structure

### 2.0 bundle.js

Don't touch `app/static/js/bundle.js`! It is the result of browserify's
compilation process and will be overwritten.

### 2.1 Angular

EFLA-web uses Angular 1. to add new functionality, add new pages or edit the
existing ones, you should first look into Angular's project structure.

### 2.2 API interaction

All interaction with the REST-like API is defined in `app/static/js/API.js`.
Each domain model has a factory there with several methods for interaction with
the endpoints.

E.g. to get all locales supported by the server, you would request the `API`
module in your angular moduleand then request the `Locales` factory in your
controller. Then you can call `Locales.all().fork(...)`.

Note that the API always returns a Fluture `Future` object, since they are the
future (pun intended) of asynchronous JavaScript.
