/** Prefix a site path with Astro `base` (works on github.io project pages and custom domains). */
export function withBase(path = '/'): string {
  const base = import.meta.env.BASE_URL; // e.g. "/" or "/solvstenbjerring/"
  if (path === '/' || path === '') return base;
  return `${base}${path.replace(/^\//, '')}`;
}
