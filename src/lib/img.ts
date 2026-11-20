import map from '../data/images.json';
import archived from '../data/archived.json';

const base = import.meta.env.BASE_URL.replace(/\/$/, '');
const stems: Record<string, string> = map;
// old gallery photos live in the separate repo dgistECME/media (own 1 GB Pages limit); see tools/archive_photos.py
const ARCHIVE = 'https://dgistecme.github.io/media';
const archivedSet = new Set<string>(archived);
const at = (stem: string) => (archivedSet.has(stem) ? ARCHIVE : base);

/** Resolve a Wix media uri (as stored in the YAML data) to a site image path. */
export function img(uri: string | null | undefined, size: 'full' | 'thumb' = 'full'): string | undefined {
  if (!uri) return undefined;
  const stem = stems[uri];
  if (stem) return `${at(stem)}/img/${size}/${stem}.webp`;
  // plain filename added by hand (e.g. "hong.jpg") -> served as-is from public/img/<size>/
  if (/\.(webp|jpe?g|png|gif|avif)$/i.test(uri)) return `${base}/img/${size}/${uri}`;
  return undefined;
}

export function href(path: string): string {
  return `${base}${path.startsWith('/') ? path : '/' + path}`;
}
