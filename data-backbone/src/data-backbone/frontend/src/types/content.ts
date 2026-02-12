// ============================================================================
// MARKETING CONTENT TYPE DEFINITIONS
// ============================================================================

// Content Types
export type ContentType =
  | 'linkedin_post'
  | 'article'
  | 'landing_page'
  | 'abm_content'
  | 'case_study';

// Content Status (workflow)
export type ContentStatus =
  | 'draft'
  | 'review'
  | 'approved'
  | 'scheduled'
  | 'published'
  | 'archived';

// Content Category
export type ContentCategory =
  | 'thought_leadership'
  | 'product'
  | 'case_study'
  | 'industry'
  | 'company_news'
  | 'educational'
  | 'promotional';

// Persona Types for ABM
export type PersonaType =
  | 'executive'
  | 'decision_maker'
  | 'influencer'
  | 'practitioner'
  | 'technical'
  | 'financial';

// Campaign Status
export type CampaignStatus =
  | 'planning'
  | 'active'
  | 'paused'
  | 'completed'
  | 'archived';

// ============================================================================
// BASE CONTENT INTERFACES
// ============================================================================

export interface ContentBase {
  id: string;
  title: string;
  content_type: ContentType;
  status: ContentStatus;
  category?: ContentCategory;

  // Author
  author_id?: string;
  author_name?: string;

  // Tags and targeting
  tags: string[];
  target_personas: PersonaType[];
  target_industries: string[];
  target_accounts: string[];

  // Campaign association
  campaign_id?: string;

  // AI generation
  ai_generated: boolean;
  ai_prompt?: string;

  // Timestamps
  created_at?: string;
  updated_at?: string;
  published_at?: string;
  scheduled_at?: string;
}

// ============================================================================
// LINKEDIN POST
// ============================================================================

export interface LinkedInPostContent {
  body: string;
  hashtags: string[];
  mentions: string[];
  image_url?: string;
  image_alt_text?: string;
  video_url?: string;
  document_url?: string;
  link_url?: string;
  call_to_action?: string;
}

export interface LinkedInPost extends ContentBase {
  content_type: 'linkedin_post';
  linkedin: LinkedInPostContent;

  // Scheduling
  scheduled_time?: string;
  timezone: string;

  // Analytics
  impressions: number;
  reactions: number;
  comments: number;
  shares: number;
  clicks: number;
  engagement_rate: number;
}

// ============================================================================
// ARTICLE
// ============================================================================

export interface ArticleSection {
  id: string;
  type: 'paragraph' | 'heading' | 'image' | 'quote' | 'list';
  content: string;
  order: number;
}

export interface ArticleSEO {
  meta_title?: string;
  meta_description?: string;
  focus_keyword?: string;
  secondary_keywords: string[];
  canonical_url?: string;
  og_image_url?: string;
  no_index: boolean;
}

export interface ArticleContent {
  subtitle?: string;
  summary?: string;
  body: string;
  sections: ArticleSection[];
  featured_image_url?: string;
  featured_image_alt?: string;
  reading_time_minutes: number;
  word_count: number;
  seo: ArticleSEO;
  slug?: string;
}

export interface Article extends ContentBase {
  content_type: 'article';
  article: ArticleContent;

  // Analytics
  views: number;
  unique_visitors: number;
  avg_time_on_page: number;
  scroll_depth: number;
  conversions: number;
}

// ============================================================================
// LANDING PAGE
// ============================================================================

export interface LandingPageCTA {
  id: string;
  text: string;
  url: string;
  style: 'primary' | 'secondary' | 'outline';
  position: string;
}

export interface FormField {
  id: string;
  name: string;
  type: 'text' | 'email' | 'phone' | 'select' | 'textarea' | 'checkbox';
  label: string;
  required: boolean;
  placeholder?: string;
  options?: string[];
}

export interface LandingPageForm {
  id: string;
  title?: string;
  fields: FormField[];
  submit_button_text: string;
  success_message: string;
  redirect_url?: string;
  webhook_url?: string;
}

export interface LandingPageContent {
  headline: string;
  subheadline?: string;
  body?: string;
  hero_image_url?: string;
  hero_video_url?: string;
  value_props: Array<{
    title: string;
    description: string;
    icon?: string;
  }>;
  testimonials: Array<{
    quote: string;
    author: string;
    title?: string;
    image_url?: string;
  }>;
  logos: string[];
  ctas: LandingPageCTA[];
  forms: LandingPageForm[];
  template_id?: string;
  custom_css?: string;
  custom_js?: string;
}

export interface LandingPage extends ContentBase {
  content_type: 'landing_page';
  landing_page: LandingPageContent;
  slug: string;
  full_url?: string;

  // A/B testing
  variant_of?: string;
  variant_name?: string;
  variant_weight: number;

  // Analytics
  views: number;
  unique_visitors: number;
  form_submissions: number;
  conversion_rate: number;
  bounce_rate: number;
}

// ============================================================================
// ABM CONTENT
// ============================================================================

export interface PersonalizationToken {
  key: string;
  default_value: string;
  description?: string;
}

export interface ABMVariation {
  id: string;
  account_id?: string;
  account_name?: string;
  persona?: PersonaType;
  headline?: string;
  body?: string;
  image_url?: string;
  cta_text?: string;
}

export interface ABMContentData {
  base_headline: string;
  base_body: string;
  tokens: PersonalizationToken[];
  variations: ABMVariation[];
  base_image_url?: string;
  use_in_ads: boolean;
  use_in_email: boolean;
  use_in_landing_pages: boolean;
}

export interface ABMContent extends ContentBase {
  content_type: 'abm_content';
  abm: ABMContentData;

  // Stats
  accounts_targeted: number;
  personas_targeted: number;

  // Analytics
  impressions: number;
  engagement: number;
  engagement_rate: number;
}

// ============================================================================
// CASE STUDY
// ============================================================================

export interface CaseStudyMetric {
  metric_name: string;
  metric_value: string;
  metric_description?: string;
}

export interface CaseStudyQuote {
  quote: string;
  author_name: string;
  author_title?: string;
  author_image_url?: string;
}

export interface CaseStudyContent {
  customer_name: string;
  customer_logo_url?: string;
  customer_industry?: string;
  customer_size?: string;
  challenge: string;
  solution: string;
  results: string;
  full_story?: string;
  metrics: CaseStudyMetric[];
  quotes: CaseStudyQuote[];
  featured_image_url?: string;
  video_url?: string;
  pdf_url?: string;
}

export interface CaseStudy extends ContentBase {
  content_type: 'case_study';
  case_study: CaseStudyContent;

  // Analytics
  views: number;
  downloads: number;
  video_plays: number;
}

// ============================================================================
// CAMPAIGN
// ============================================================================

export interface Campaign {
  id: string;
  name: string;
  description?: string;
  status: CampaignStatus;

  // Timeline
  start_date?: string;
  end_date?: string;

  // Targeting
  target_accounts: string[];
  target_personas: PersonaType[];
  target_industries: string[];

  // Content
  content_ids: string[];

  // Budget
  budget?: number;
  spent: number;

  // Goals
  goal_type?: 'awareness' | 'leads' | 'engagement';
  goal_value?: number;
  current_value: number;

  // Analytics
  total_impressions: number;
  total_engagement: number;
  total_leads: number;
  total_conversions: number;

  // Timestamps
  created_at?: string;
  updated_at?: string;
  created_by?: string;
}

// ============================================================================
// UNION TYPE FOR ALL CONTENT
// ============================================================================

export type Content = LinkedInPost | Article | LandingPage | ABMContent | CaseStudy;

// ============================================================================
// API REQUEST/RESPONSE TYPES
// ============================================================================

export interface ContentCreateRequest {
  content_type: ContentType;
  title: string;
  category?: ContentCategory;
  tags?: string[];
  linkedin?: Partial<LinkedInPostContent>;
  article?: Partial<ArticleContent>;
  landing_page?: Partial<LandingPageContent>;
  abm?: Partial<ABMContentData>;
  case_study?: Partial<CaseStudyContent>;
  target_personas?: PersonaType[];
  target_industries?: string[];
  target_accounts?: string[];
  campaign_id?: string;
}

export interface ContentUpdateRequest {
  title?: string;
  status?: ContentStatus;
  category?: ContentCategory;
  tags?: string[];
  linkedin?: Partial<LinkedInPostContent>;
  article?: Partial<ArticleContent>;
  landing_page?: Partial<LandingPageContent>;
  abm?: Partial<ABMContentData>;
  case_study?: Partial<CaseStudyContent>;
  target_personas?: PersonaType[];
  target_industries?: string[];
  target_accounts?: string[];
  campaign_id?: string;
}

export interface ContentListResponse {
  items: Content[];
  total: number;
  page: number;
  page_size: number;
}

export interface ContentGenerateRequest {
  content_type: ContentType;
  prompt: string;
  tone?: 'professional' | 'casual' | 'formal' | 'friendly';
  target_audience?: string;
  key_points?: string[];
  max_length?: number;
  company_context?: string;
  product_context?: string;
  reference_content_ids?: string[];
}

export interface HashtagSuggestionResponse {
  hashtags: string[];
  trending: string[];
}

export interface LinkedInScheduleRequest {
  content_id: string;
  scheduled_time: string;
  timezone?: string;
}

export interface ContentSequenceLinkRequest {
  content_id: string;
  sequence_id: string;
  step_id: string;
}

// ============================================================================
// ANALYTICS
// ============================================================================

export interface MarketingAnalytics {
  total_content: number;
  content_by_type: Record<ContentType, number>;
  content_by_status: Record<ContentStatus, number>;
  total_impressions: number;
  total_engagement: number;
  avg_engagement_rate: number;
  top_performing: Array<{
    id: string;
    title: string;
    type: ContentType;
    engagement: number;
  }>;
  active_campaigns: number;
  campaign_performance: Array<{
    id: string;
    name: string;
    leads: number;
    conversions: number;
  }>;
  content_created_trend: Array<{
    date: string;
    count: number;
  }>;
  engagement_trend: Array<{
    date: string;
    engagement: number;
  }>;
}

export interface ContentAnalytics {
  content_id: string;
  content_type: ContentType;
  views: number;
  impressions: number;
  engagement: number;
  engagement_rate: number;
  clicks: number;
  conversions: number;
}

// ============================================================================
// LINKED CONTENT FOR SEQUENCES
// ============================================================================

export interface LinkedContent {
  content_id: string;
  content_type: ContentType;
  title: string;
  url?: string;
  cta?: string;
}

// Merge fields for sequences
export interface ContentMergeFields {
  'content.title': string;
  'content.url': string;
  'content.cta': string;
  'content.summary': string;
}
