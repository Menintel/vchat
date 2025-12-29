# VChat

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup (pnpm monorepo)

Install dependencies (requires pnpm):

```sh
pnpm install
# or install pnpm: npm i -g pnpm
```

### Run the frontend (dev)

```sh
pnpm --filter ./apps/frontend dev
# or from root: pnpm dev
```

### Build the frontend

```sh
pnpm --filter ./apps/frontend build
# or from root: pnpm build
```

### Run backend (if added)

```sh
pnpm --filter ./apps/backend dev
```

### Lint (workspace)

```sh
pnpm -w -r run lint
```
