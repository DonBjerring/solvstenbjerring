/** Helpers for story posts: derive dates/titles from image filenames. */

const MONTHS_DA = [
  'januar',
  'februar',
  'marts',
  'april',
  'maj',
  'juni',
  'juli',
  'august',
  'september',
  'oktober',
  'november',
  'december',
];

/** Parse a date from filenames like 20260513-160309.jpg or IMG20260513160309.jpg */
export function parseDateFromImageName(filename: string): Date | null {
  const name = filename.split('/').pop() ?? filename;

  const stamped = name.match(/^(\d{4})(\d{2})(\d{2})(?:-(\d{2})(\d{2})(\d{2}))?/);
  if (stamped) {
    const [, y, m, d, hh = '12', mm = '0', ss = '0'] = stamped;
    return new Date(
      Number(y),
      Number(m) - 1,
      Number(d),
      Number(hh),
      Number(mm),
      Number(ss),
    );
  }

  const android = name.match(/^IMG(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/i);
  if (android) {
    const [, y, m, d, hh, mm, ss] = android;
    return new Date(
      Number(y),
      Number(m) - 1,
      Number(d),
      Number(hh),
      Number(mm),
      Number(ss),
    );
  }

  return null;
}

export function formatStoryTitle(date: Date): string {
  const day = date.getDate();
  const month = MONTHS_DA[date.getMonth()];
  const year = date.getFullYear();
  return `${day}. ${month} ${year}`;
}

export function resolveStoryDate(options: {
  date?: Date;
  image?: string;
}): Date | null {
  if (options.date) return options.date;
  if (options.image) return parseDateFromImageName(options.image);
  return null;
}

export function storyImageSrc(filename: string): string {
  const clean = filename.replace(/^\//, '');
  if (clean.startsWith('images/')) return clean;
  return `images/markus/story/${clean}`;
}
