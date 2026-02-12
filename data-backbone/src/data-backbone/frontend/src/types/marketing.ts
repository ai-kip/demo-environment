// ============================================================================
// MARKETING INTELLIGENCE MODULE TYPES
// ============================================================================

import type {
  Content,
  ContentType,
  ContentStatus,
  ContentCategory,
  Campaign,
  CampaignStatus,
  MarketingAnalytics,
  LinkedInPost,
  Article,
  LandingPage,
  ABMContent,
  CaseStudy,
} from './content';

// Re-export content types for convenience
export type {
  Content,
  ContentType,
  ContentStatus,
  ContentCategory,
  Campaign,
  CampaignStatus,
  MarketingAnalytics,
  LinkedInPost,
  Article,
  LandingPage,
  ABMContent,
  CaseStudy,
};

// ============================================================================
// NAVIGATION
// ============================================================================

export interface MarketingNavItem {
  id: string;
  labelKey: string;
  icon: string;
  href: string;
  badge?: number | string;
}

// ============================================================================
// DASHBOARD
// ============================================================================

export interface MarketingDashboardStats {
  totalContent: number;
  publishedContent: number;
  draftContent: number;
  scheduledPosts: number;
  activeCampaigns: number;
  totalImpressions: number;
  totalEngagement: number;
  avgEngagementRate: number;
}

export interface RecentContentActivity {
  id: string;
  contentId: string;
  contentTitle: string;
  contentType: ContentType;
  action: 'created' | 'updated' | 'published' | 'scheduled';
  actorName: string;
  timestamp: string;
}

export interface ScheduledPost {
  id: string;
  title: string;
  contentType: ContentType;
  scheduledTime: string;
  platform: 'linkedin' | 'blog' | 'landing_page';
  status: 'scheduled' | 'publishing' | 'failed';
}

// ============================================================================
// CONTENT LIBRARY
// ============================================================================

export type ContentViewMode = 'grid' | 'list';

export type ContentSortOption =
  | 'updated_desc'
  | 'updated_asc'
  | 'created_desc'
  | 'created_asc'
  | 'title_asc'
  | 'title_desc'
  | 'status';

export interface ContentFilters {
  contentType?: ContentType;
  status?: ContentStatus;
  category?: ContentCategory;
  campaignId?: string;
  authorId?: string;
  search?: string;
  dateFrom?: string;
  dateTo?: string;
}

// ============================================================================
// LINKEDIN
// ============================================================================

export interface LinkedInPostValidation {
  valid: boolean;
  errors: string[];
  warnings: string[];
  characterCount: number;
  charactersRemaining: number;
  hashtagCount: number;
}

export interface LinkedInAnalytics {
  totalPosts: number;
  totalImpressions: number;
  totalReactions: number;
  totalComments: number;
  totalShares: number;
  totalClicks: number;
  avgEngagementRate: number;
}

export interface LinkedInBestTimes {
  day: string;
  hour: number;
  engagementScore: number;
}

// ============================================================================
// ARTICLES
// ============================================================================

export interface ArticleTemplate {
  id: string;
  name: string;
  description: string;
  sections: string[];
  category: ContentCategory;
}

export interface SEOScore {
  overall: number;
  title: number;
  description: number;
  keywords: number;
  readability: number;
  suggestions: string[];
}

// ============================================================================
// LANDING PAGES
// ============================================================================

export interface LandingPageTemplate {
  id: string;
  name: string;
  description: string;
  thumbnail: string;
  category: 'lead_gen' | 'webinar' | 'ebook' | 'demo' | 'generic';
}

export interface ABTestVariant {
  id: string;
  name: string;
  weight: number;
  views: number;
  conversions: number;
  conversionRate: number;
}

// ============================================================================
// ABM
// ============================================================================

export interface TargetAccount {
  id: string;
  name: string;
  industry?: string;
  tier?: 'tier1' | 'tier2' | 'tier3';
  contentCount: number;
  engagementScore: number;
}

export interface PersonaDefinition {
  type: string;
  label: string;
  description: string;
  icon: string;
  color: string;
}

// ============================================================================
// CAMPAIGNS
// ============================================================================

export interface CampaignTimeline {
  id: string;
  date: string;
  type: 'start' | 'content_added' | 'content_published' | 'milestone' | 'end';
  title: string;
  description?: string;
  contentId?: string;
}

export interface CampaignMetrics {
  impressions: number;
  engagement: number;
  leads: number;
  conversions: number;
  costPerLead?: number;
  roi?: number;
}

// ============================================================================
// AI GENERATION
// ============================================================================

export interface AIGenerationOptions {
  contentType: ContentType;
  prompt: string;
  tone: 'professional' | 'casual' | 'formal' | 'friendly';
  targetAudience?: string;
  keyPoints?: string[];
  maxLength?: number;
  companyContext?: string;
  productContext?: string;
}

export interface AIGenerationResult {
  success: boolean;
  content: Record<string, unknown>;
  tokensUsed: number;
  suggestions?: string[];
}

export interface AIVariation {
  variationNumber: number;
  title: string;
  content: string;
}

// ============================================================================
// SEQUENCE INTEGRATION
// ============================================================================

export interface ContentForSequence {
  id: string;
  title: string;
  contentType: ContentType;
  status: ContentStatus;
  publishedAt?: string;
  url?: string;
  cta?: string;
}

export interface SequenceContentLink {
  contentId: string;
  sequenceId: string;
  stepId: string;
  linkedAt: string;
}

// Content merge fields available in sequences
export const CONTENT_MERGE_FIELDS = [
  { field: '{{content.title}}', description: 'Content title' },
  { field: '{{content.url}}', description: 'Content URL' },
  { field: '{{content.cta}}', description: 'Call to action text' },
  { field: '{{content.summary}}', description: 'Content summary' },
] as const;
