import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// Project Pages URL: https://donbjerring.github.io/solvstenbjerring/
// When www.solvstenbjerring.dk is connected, change base to '/' and site to the custom domain.
export default defineConfig({
  site: 'https://donbjerring.github.io',
  base: '/solvstenbjerring/',
  output: 'static',
  vite: {
    plugins: [tailwindcss()],
  },
});
