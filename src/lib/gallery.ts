import fs from 'node:fs';
import path from 'node:path';

const IMAGE_EXT = new Set(['.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif']);

/** List image files under public/images/<subdir>, sorted by filename. */
export function listPublicImages(subdir: string): { src: string; name: string }[] {
  const dir = path.join(process.cwd(), 'public', 'images', subdir);
  if (!fs.existsSync(dir)) return [];

  return fs
    .readdirSync(dir)
    .filter((name) => IMAGE_EXT.has(path.extname(name).toLowerCase()))
    .sort((a, b) => a.localeCompare(b, 'da'))
    .map((name) => {
      const relative = `images/${subdir.replace(/\\/g, '/')}/${name}`;
      const base = import.meta.env.BASE_URL ?? '/';
      return {
        name,
        src: `${base}${relative}`,
      };
    });
}
