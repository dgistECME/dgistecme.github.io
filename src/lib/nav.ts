export type NavItem = { label: string; href?: string; children?: { label: string; href: string }[] };

export const NAV: NavItem[] = [
  { label: 'Home', href: '/' },
  { label: 'Professor', children: [{ label: 'Prof. Ju-Hyuck Lee', href: '/professor' }] },
  { label: 'Peoples', children: [{ label: 'Members', href: '/members' }, { label: 'Alumni', href: '/alumni' }] },
  { label: 'Research', children: [{ label: 'Research Interest', href: '/research' }] },
  { label: 'Publication', children: [{ label: 'Papers', href: '/papers' }, { label: 'Patents', href: '/patents' }] },
  { label: 'NEWS', children: [{ label: 'Articles', href: '/articles' }, { label: 'Photos', href: '/photos' }] },
  { label: 'Contact', children: [{ label: 'Opening', href: '/opening' }] },
];
