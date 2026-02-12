import type {
  ContentType,
  ContentStatus,
  ContentCategory,
  PersonaType,
  CampaignStatus,
} from '../types/content';

// ============================================================================
// COLOR PALETTE
// ============================================================================

export const CONTENT_COLORS = {
  // Primary colors
  primary: '#8B5CF6', // Purple - marketing brand color
  primaryLight: '#A78BFA',
  primaryDark: '#7C3AED',

  // Content type colors
  linkedinPost: '#0A66C2', // LinkedIn blue
  article: '#10B981', // Green
  landingPage: '#F59E0B', // Amber
  abmContent: '#EC4899', // Pink
  caseStudy: '#3B82F6', // Blue

  // Status colors
  draft: '#6B7280',
  review: '#F59E0B',
  approved: '#3B82F6',
  scheduled: '#8B5CF6',
  published: '#10B981',
  archived: '#9CA3AF',

  // Campaign status colors
  planning: '#6B7280',
  active: '#10B981',
  paused: '#F59E0B',
  completed: '#3B82F6',

  // UI colors
  background: '#F9FAFB',
  cardBg: '#FFFFFF',
  cardBgHover: '#F3F4F6',
  border: '#E5E7EB',
  primaryText: '#111827',
  secondaryText: '#6B7280',
  tertiaryText: '#9CA3AF',

  // Status colors (generic)
  success: '#10B981',
  warning: '#F59E0B',
  danger: '#EF4444',
  info: '#3B82F6',
};

// ============================================================================
// TYPOGRAPHY
// ============================================================================

export const CONTENT_TYPOGRAPHY = {
  h1: {
    fontSize: '1.875rem',
    fontWeight: 700,
    lineHeight: 1.2,
  },
  h2: {
    fontSize: '1.5rem',
    fontWeight: 600,
    lineHeight: 1.3,
  },
  h3: {
    fontSize: '1.25rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h4: {
    fontSize: '1rem',
    fontWeight: 600,
    lineHeight: 1.5,
  },
  body: {
    fontSize: '0.875rem',
    fontWeight: 400,
    lineHeight: 1.5,
  },
  bodySmall: {
    fontSize: '0.75rem',
    fontWeight: 400,
    lineHeight: 1.5,
  },
  label: {
    fontSize: '0.75rem',
    fontWeight: 500,
    letterSpacing: '0.025em',
    textTransform: 'uppercase' as const,
  },
};

// ============================================================================
// CONTENT TYPE CONFIGURATION
// ============================================================================

export const CONTENT_TYPE_CONFIG: Record<ContentType, {
  label: string;
  labelPlural: string;
  icon: string;
  color: string;
  description: string;
  maxLength?: number;
  supportsScheduling: boolean;
  supportsSEO: boolean;
  supportsABTesting: boolean;
}> = {
  linkedin_post: {
    label: 'LinkedIn Post',
    labelPlural: 'LinkedIn Posts',
    icon: 'linkedin',
    color: CONTENT_COLORS.linkedinPost,
    description: 'Short-form social content for LinkedIn',
    maxLength: 3000,
    supportsScheduling: true,
    supportsSEO: false,
    supportsABTesting: false,
  },
  article: {
    label: 'Article',
    labelPlural: 'Articles',
    icon: 'file-text',
    color: CONTENT_COLORS.article,
    description: 'Long-form blog content',
    supportsScheduling: true,
    supportsSEO: true,
    supportsABTesting: false,
  },
  landing_page: {
    label: 'Landing Page',
    labelPlural: 'Landing Pages',
    icon: 'layout',
    color: CONTENT_COLORS.landingPage,
    description: 'Conversion-focused web pages',
    supportsScheduling: false,
    supportsSEO: true,
    supportsABTesting: true,
  },
  abm_content: {
    label: 'ABM Content',
    labelPlural: 'ABM Content',
    icon: 'target',
    color: CONTENT_COLORS.abmContent,
    description: 'Account-based marketing content with personalization',
    supportsScheduling: false,
    supportsSEO: false,
    supportsABTesting: true,
  },
  case_study: {
    label: 'Case Study',
    labelPlural: 'Case Studies',
    icon: 'award',
    color: CONTENT_COLORS.caseStudy,
    description: 'Customer success stories',
    supportsScheduling: true,
    supportsSEO: true,
    supportsABTesting: false,
  },
};

// ============================================================================
// CONTENT STATUS CONFIGURATION
// ============================================================================

export const CONTENT_STATUS_CONFIG: Record<ContentStatus, {
  label: string;
  color: string;
  bgColor: string;
  icon: string;
  description: string;
}> = {
  draft: {
    label: 'Draft',
    color: CONTENT_COLORS.draft,
    bgColor: '#F3F4F6',
    icon: 'edit-3',
    description: 'Work in progress',
  },
  review: {
    label: 'In Review',
    color: CONTENT_COLORS.review,
    bgColor: '#FEF3C7',
    icon: 'eye',
    description: 'Awaiting approval',
  },
  approved: {
    label: 'Approved',
    color: CONTENT_COLORS.approved,
    bgColor: '#DBEAFE',
    icon: 'check-circle',
    description: 'Ready to publish',
  },
  scheduled: {
    label: 'Scheduled',
    color: CONTENT_COLORS.scheduled,
    bgColor: '#EDE9FE',
    icon: 'clock',
    description: 'Scheduled for publishing',
  },
  published: {
    label: 'Published',
    color: CONTENT_COLORS.published,
    bgColor: '#D1FAE5',
    icon: 'globe',
    description: 'Live and visible',
  },
  archived: {
    label: 'Archived',
    color: CONTENT_COLORS.archived,
    bgColor: '#F3F4F6',
    icon: 'archive',
    description: 'No longer active',
  },
};

// ============================================================================
// CONTENT CATEGORY CONFIGURATION
// ============================================================================

export const CONTENT_CATEGORY_CONFIG: Record<ContentCategory, {
  label: string;
  icon: string;
  color: string;
}> = {
  thought_leadership: {
    label: 'Thought Leadership',
    icon: 'lightbulb',
    color: '#F59E0B',
  },
  product: {
    label: 'Product',
    icon: 'package',
    color: '#3B82F6',
  },
  case_study: {
    label: 'Case Study',
    icon: 'file-check',
    color: '#10B981',
  },
  industry: {
    label: 'Industry',
    icon: 'building',
    color: '#6366F1',
  },
  company_news: {
    label: 'Company News',
    icon: 'newspaper',
    color: '#EC4899',
  },
  educational: {
    label: 'Educational',
    icon: 'graduation-cap',
    color: '#8B5CF6',
  },
  promotional: {
    label: 'Promotional',
    icon: 'megaphone',
    color: '#EF4444',
  },
};

// ============================================================================
// PERSONA CONFIGURATION
// ============================================================================

export const PERSONA_CONFIG: Record<PersonaType, {
  label: string;
  description: string;
  icon: string;
  color: string;
}> = {
  executive: {
    label: 'Executive',
    description: 'C-level and VP decision makers',
    icon: 'crown',
    color: '#F59E0B',
  },
  decision_maker: {
    label: 'Decision Maker',
    description: 'Budget holders and final approvers',
    icon: 'check-square',
    color: '#10B981',
  },
  influencer: {
    label: 'Influencer',
    description: 'Internal champions and advocates',
    icon: 'star',
    color: '#8B5CF6',
  },
  practitioner: {
    label: 'Practitioner',
    description: 'Day-to-day users',
    icon: 'user',
    color: '#3B82F6',
  },
  technical: {
    label: 'Technical',
    description: 'IT and technical evaluators',
    icon: 'code',
    color: '#6366F1',
  },
  financial: {
    label: 'Financial',
    description: 'Finance and procurement',
    icon: 'dollar-sign',
    color: '#EC4899',
  },
};

// ============================================================================
// CAMPAIGN STATUS CONFIGURATION
// ============================================================================

export const CAMPAIGN_STATUS_CONFIG: Record<CampaignStatus, {
  label: string;
  color: string;
  bgColor: string;
  icon: string;
}> = {
  planning: {
    label: 'Planning',
    color: CONTENT_COLORS.planning,
    bgColor: '#F3F4F6',
    icon: 'clipboard',
  },
  active: {
    label: 'Active',
    color: CONTENT_COLORS.active,
    bgColor: '#D1FAE5',
    icon: 'play',
  },
  paused: {
    label: 'Paused',
    color: CONTENT_COLORS.paused,
    bgColor: '#FEF3C7',
    icon: 'pause',
  },
  completed: {
    label: 'Completed',
    color: CONTENT_COLORS.completed,
    bgColor: '#DBEAFE',
    icon: 'check',
  },
  archived: {
    label: 'Archived',
    color: CONTENT_COLORS.archived,
    bgColor: '#F3F4F6',
    icon: 'archive',
  },
};

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

export function getContentTypeColor(type: ContentType): string {
  return CONTENT_TYPE_CONFIG[type]?.color || CONTENT_COLORS.primary;
}

export function getContentTypeLabel(type: ContentType): string {
  return CONTENT_TYPE_CONFIG[type]?.label || type;
}

export function getContentStatusColor(status: ContentStatus): string {
  return CONTENT_STATUS_CONFIG[status]?.color || CONTENT_COLORS.draft;
}

export function getContentStatusLabel(status: ContentStatus): string {
  return CONTENT_STATUS_CONFIG[status]?.label || status;
}

export function getCampaignStatusColor(status: CampaignStatus): string {
  return CAMPAIGN_STATUS_CONFIG[status]?.color || CONTENT_COLORS.planning;
}

export function getPersonaLabel(persona: PersonaType): string {
  return PERSONA_CONFIG[persona]?.label || persona;
}

export function getPersonaColor(persona: PersonaType): string {
  return PERSONA_CONFIG[persona]?.color || CONTENT_COLORS.primary;
}

export function formatContentDate(dateString: string | undefined): string {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

export function formatContentTime(dateString: string | undefined): string {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatContentDateTime(dateString: string | undefined): string {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function getCharacterCountColor(current: number, max: number): string {
  const ratio = current / max;
  if (ratio >= 1) return CONTENT_COLORS.danger;
  if (ratio >= 0.9) return CONTENT_COLORS.warning;
  return CONTENT_COLORS.success;
}

// ============================================================================
// LINKEDIN SPECIFIC
// ============================================================================

export const LINKEDIN_CONFIG = {
  maxBodyLength: 3000,
  recommendedHashtags: { min: 2, max: 5 },
  optimalPostLength: { min: 150, max: 1300 },
  bestPostingTimes: [
    { day: 'Tuesday', hour: 10, label: '10:00 AM' },
    { day: 'Wednesday', hour: 10, label: '10:00 AM' },
    { day: 'Thursday', hour: 10, label: '10:00 AM' },
    { day: 'Tuesday', hour: 12, label: '12:00 PM' },
    { day: 'Wednesday', hour: 12, label: '12:00 PM' },
  ],
};

// ============================================================================
// ARTICLE SEO
// ============================================================================

export const ARTICLE_SEO_CONFIG = {
  titleLength: { min: 30, max: 60 },
  descriptionLength: { min: 120, max: 160 },
  minWordCount: 300,
  recommendedWordCount: 1500,
  maxWordCount: 5000,
};

// ============================================================================
// LANDING PAGE TEMPLATES
// ============================================================================

export const LANDING_PAGE_TEMPLATES = [
  {
    id: 'lead-gen-basic',
    name: 'Lead Generation',
    description: 'Simple lead capture with form',
    category: 'lead_gen',
    thumbnail: '/templates/lead-gen.png',
  },
  {
    id: 'webinar-registration',
    name: 'Webinar Registration',
    description: 'Event registration with countdown',
    category: 'webinar',
    thumbnail: '/templates/webinar.png',
  },
  {
    id: 'ebook-download',
    name: 'eBook Download',
    description: 'Content download gate',
    category: 'ebook',
    thumbnail: '/templates/ebook.png',
  },
  {
    id: 'demo-request',
    name: 'Demo Request',
    description: 'Product demo scheduling',
    category: 'demo',
    thumbnail: '/templates/demo.png',
  },
  {
    id: 'blank',
    name: 'Blank Template',
    description: 'Start from scratch',
    category: 'generic',
    thumbnail: '/templates/blank.png',
  },
];

// ============================================================================
// DEMO DATA
// ============================================================================

export const createDemoContentStats = () => ({
  totalContent: 47,
  publishedContent: 28,
  draftContent: 12,
  scheduledPosts: 7,
  activeCampaigns: 3,
  totalImpressions: 125000,
  totalEngagement: 8500,
  avgEngagementRate: 6.8,
});

export const createDemoRecentActivity = () => [
  {
    id: '1',
    contentId: 'c1',
    contentTitle: 'Q4 Sustainability Report Highlights',
    contentType: 'linkedin_post' as ContentType,
    action: 'published' as const,
    actorName: 'Sarah Johnson',
    timestamp: new Date(Date.now() - 2 * 3600000).toISOString(),
  },
  {
    id: '2',
    contentId: 'c2',
    contentTitle: 'The Future of Workplace Design',
    contentType: 'article' as ContentType,
    action: 'updated' as const,
    actorName: 'Mark de Vries',
    timestamp: new Date(Date.now() - 5 * 3600000).toISOString(),
  },
  {
    id: '3',
    contentId: 'c3',
    contentTitle: 'Product Demo Landing Page',
    contentType: 'landing_page' as ContentType,
    action: 'created' as const,
    actorName: 'Lisa Chen',
    timestamp: new Date(Date.now() - 8 * 3600000).toISOString(),
  },
];

export const createDemoScheduledPosts = () => [
  {
    id: '1',
    title: 'Employee Wellness Initiative Launch',
    contentType: 'linkedin_post' as ContentType,
    scheduledTime: new Date(Date.now() + 24 * 3600000).toISOString(),
    platform: 'linkedin' as const,
    status: 'scheduled' as const,
  },
  {
    id: '2',
    title: 'Case Study: TechCorp Success Story',
    contentType: 'linkedin_post' as ContentType,
    scheduledTime: new Date(Date.now() + 48 * 3600000).toISOString(),
    platform: 'linkedin' as const,
    status: 'scheduled' as const,
  },
];
