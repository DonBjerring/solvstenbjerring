/** Prefix a site path with Astro `base` (works on github.io project pages and custom domains). */
export function withBase(path = '/'): string {
  const raw = import.meta.env.BASE_URL || '/';
  const base = raw.endsWith('/') ? raw : `${raw}/`;
  if (path === '/' || path === '') return base;
  return `${base}${path.replace(/^\//, '')}`;
}
