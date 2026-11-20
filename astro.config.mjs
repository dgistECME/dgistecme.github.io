// @ts-check
import { defineConfig } from 'astro/config';
import yaml from '@rollup/plugin-yaml';
import sitemap from '@astrojs/sitemap';

// GitHub Pages: user/org site (<name>.github.io repo) -> base '/'; project site -> base '/<repo>'.
// SITE_URL / BASE_PATH come from the workflow env; defaults match production.
export default defineConfig({
  site: process.env.SITE_URL ?? 'https://dgistecme.github.io',
  base: process.env.BASE_PATH ?? '/',
  trailingSlash: 'ignore',
  integrations: [sitemap()],
  vite: { plugins: [yaml()] },
});
