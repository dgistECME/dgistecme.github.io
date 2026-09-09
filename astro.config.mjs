// @ts-check
import { defineConfig } from 'astro/config';
import yaml from '@rollup/plugin-yaml';

// GitHub Pages:
//  - user/org site  (<name>.github.io repo)  -> site: 'https://<name>.github.io', base: '/'
//  - project site   (any other repo name)    -> site: 'https://<name>.github.io', base: '/<repo>'
// Set SITE_URL / BASE_PATH in the workflow env; defaults work for local dev.
export default defineConfig({
  site: process.env.SITE_URL ?? 'https://example.github.io',
  base: process.env.BASE_PATH ?? '/',
  trailingSlash: 'ignore',
  vite: { plugins: [yaml()] },
});
