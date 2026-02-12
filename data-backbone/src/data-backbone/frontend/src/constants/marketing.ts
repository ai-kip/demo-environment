import type { MarketingNavItem } from '../types/marketing';

// ============================================================================
// MARKETING NAVIGATION CONFIGURATION
// ============================================================================

export const MARKETING_NAV_ITEMS: MarketingNavItem[] = [
  {
    id: 'marketing-dashboard',
    labelKey: 'marketing.navigation.dashboard',
    icon: 'layout-dashboard',
    href: '/marketing',
  },
  {
    id: 'content-library',
    labelKey: 'marketing.navigation.contentLibrary',
    icon: 'library',
    href: '/marketing/content',
  },
  {
    id: 'linkedin',
    labelKey: 'marketing.navigation.linkedin',
    icon: 'linkedin',
    href: '/marketing/linkedin',
  },
  {
    id: 'articles',
    labelKey: 'marketing.navigation.articles',
    icon: 'file-text',
    href: '/marketing/articles',
  },
  {
    id: 'landing-pages',
    labelKey: 'marketing.navigation.landingPages',
    icon: 'layout',
    href: '/marketing/landing-pages',
  },
  {
    id: 'abm',
    labelKey: 'marketing.navigation.abm',
    icon: 'target',
    href: '/marketing/abm',
  },
  {
    id: 'campaigns',
    labelKey: 'marketing.navigation.campaigns',
    icon: 'flag',
    href: '/marketing/campaigns',
  },
  {
    id: 'marketing-analytics',
    labelKey: 'marketing.navigation.analytics',
    icon: 'bar-chart-2',
    href: '/marketing/analytics',
  },
];

// ============================================================================
// MARKETING COLORS
// ============================================================================

export const MARKETING_COLORS = {
  // Primary brand colors
  primary: '#8B5CF6',
  primaryLight: '#A78BFA',
  primaryDark: '#7C3AED',

  // Secondary colors
  secondary: '#10B981',
  secondaryLight: '#34D399',
  secondaryDark: '#059669',

  // Accent colors
  accent: '#F59E0B',
  accentLight: '#FBBF24',
  accentDark: '#D97706',

  // LinkedIn
  linkedin: '#0A66C2',
  linkedinLight: '#378FE9',

  // Background colors
  background: '#F9FAFB',
  surface: '#FFFFFF',
  surfaceHover: '#F3F4F6',

  // Text colors
  textPrimary: '#111827',
  textSecondary: '#6B7280',
  textTertiary: '#9CA3AF',

  // Border colors
  border: '#E5E7EB',
  borderLight: '#F3F4F6',

  // Status colors
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',
};

// ============================================================================
// MARKETING DASHBOARD CONFIGURATION
// ============================================================================

export const DASHBOARD_QUICK_ACTIONS = [
  {
    id: 'new-linkedin-post',
    labelKey: 'marketing.quickActions.newLinkedInPost',
    icon: 'linkedin',
    color: MARKETING_COLORS.linkedin,
    href: '/marketing/linkedin/new',
  },
  {
    id: 'new-article',
    labelKey: 'marketing.quickActions.newArticle',
    icon: 'file-text',
    color: MARKETING_COLORS.secondary,
    href: '/marketing/articles/new',
  },
  {
    id: 'new-landing-page',
    labelKey: 'marketing.quickActions.newLandingPage',
    icon: 'layout',
    color: MARKETING_COLORS.accent,
    href: '/marketing/landing-pages/new',
  },
  {
    id: 'new-campaign',
    labelKey: 'marketing.quickActions.newCampaign',
    icon: 'flag',
    color: MARKETING_COLORS.primary,
    href: '/marketing/campaigns/new',
  },
];

// ============================================================================
// CONTENT EDITOR CONFIGURATION
// ============================================================================

export const EDITOR_TOOLBAR_CONFIG = {
  basic: ['bold', 'italic', 'underline', 'link'],
  standard: ['bold', 'italic', 'underline', 'strikethrough', 'link', 'image'],
  full: [
    'heading',
    'bold',
    'italic',
    'underline',
    'strikethrough',
    'link',
    'image',
    'video',
    'quote',
    'code',
    'bulletList',
    'orderedList',
    'table',
  ],
};

// ============================================================================
// AI GENERATION TONES
// ============================================================================

export const AI_TONE_OPTIONS = [
  {
    value: 'professional',
    labelKey: 'marketing.ai.tones.professional',
    description: 'Formal and business-appropriate',
  },
  {
    value: 'casual',
    labelKey: 'marketing.ai.tones.casual',
    description: 'Relaxed and conversational',
  },
  {
    value: 'formal',
    labelKey: 'marketing.ai.tones.formal',
    description: 'Very formal and structured',
  },
  {
    value: 'friendly',
    labelKey: 'marketing.ai.tones.friendly',
    description: 'Warm and approachable',
  },
];

// ============================================================================
// CONTENT SORT OPTIONS
// ============================================================================

export const CONTENT_SORT_OPTIONS = [
  { value: 'updated_desc', labelKey: 'marketing.sort.updatedNewest' },
  { value: 'updated_asc', labelKey: 'marketing.sort.updatedOldest' },
  { value: 'created_desc', labelKey: 'marketing.sort.createdNewest' },
  { value: 'created_asc', labelKey: 'marketing.sort.createdOldest' },
  { value: 'title_asc', labelKey: 'marketing.sort.titleAZ' },
  { value: 'title_desc', labelKey: 'marketing.sort.titleZA' },
  { value: 'status', labelKey: 'marketing.sort.status' },
];

// ============================================================================
// ANALYTICS TIME RANGES
// ============================================================================

export const ANALYTICS_TIME_RANGES = [
  { value: '7d', labelKey: 'marketing.analytics.last7Days' },
  { value: '30d', labelKey: 'marketing.analytics.last30Days' },
  { value: '90d', labelKey: 'marketing.analytics.last90Days' },
  { value: 'ytd', labelKey: 'marketing.analytics.yearToDate' },
  { value: 'all', labelKey: 'marketing.analytics.allTime' },
];

// ============================================================================
// SEQUENCE INTEGRATION
// ============================================================================

export const SEQUENCE_CONTENT_MERGE_FIELDS = [
  {
    field: '{{content.title}}',
    labelKey: 'marketing.mergeFields.title',
    description: 'The content title',
  },
  {
    field: '{{content.url}}',
    labelKey: 'marketing.mergeFields.url',
    description: 'Link to the content',
  },
  {
    field: '{{content.cta}}',
    labelKey: 'marketing.mergeFields.cta',
    description: 'Call to action text',
  },
  {
    field: '{{content.summary}}',
    labelKey: 'marketing.mergeFields.summary',
    description: 'Content summary or excerpt',
  },
];

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

export function getMarketingNavItemById(id: string): MarketingNavItem | undefined {
  return MARKETING_NAV_ITEMS.find(item => item.id === id);
}

export function isMarketingRoute(path: string): boolean {
  return path.startsWith('/marketing');
}

export function getMarketingPageTitle(pageId: string): string {
  const item = MARKETING_NAV_ITEMS.find(i => i.id === pageId);
  return item?.labelKey || 'marketing.title';
}
