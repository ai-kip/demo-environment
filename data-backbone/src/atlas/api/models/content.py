"""
Marketing Intelligence Content Models

Pydantic models for all marketing content types:
- LinkedIn Posts
- Articles (Blog)
- Landing Pages
- ABM Content
- Case Studies
- Campaigns
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


# ============================================================================
# ENUMS
# ============================================================================

class ContentType(str, Enum):
    """Content type enumeration"""
    LINKEDIN_POST = "linkedin_post"
    ARTICLE = "article"
    LANDING_PAGE = "landing_page"
    ABM_CONTENT = "abm_content"
    CASE_STUDY = "case_study"


class ContentStatus(str, Enum):
    """Content workflow status"""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ContentCategory(str, Enum):
    """Content category for filtering"""
    THOUGHT_LEADERSHIP = "thought_leadership"
    PRODUCT = "product"
    CASE_STUDY = "case_study"
    INDUSTRY = "industry"
    COMPANY_NEWS = "company_news"
    EDUCATIONAL = "educational"
    PROMOTIONAL = "promotional"


class PersonaType(str, Enum):
    """Target persona types for ABM"""
    EXECUTIVE = "executive"
    DECISION_MAKER = "decision_maker"
    INFLUENCER = "influencer"
    PRACTITIONER = "practitioner"
    TECHNICAL = "technical"
    FINANCIAL = "financial"


# ============================================================================
# BASE CONTENT MODEL
# ============================================================================

class ContentBase(BaseModel):
    """Base model for all content types"""
    title: str = Field(..., description="Content title", min_length=1, max_length=200)
    content_type: ContentType = Field(..., description="Type of content")
    status: ContentStatus = Field(default=ContentStatus.DRAFT, description="Workflow status")
    category: Optional[ContentCategory] = Field(None, description="Content category")

    # Author and ownership
    author_id: Optional[str] = Field(None, description="Author user ID")
    author_name: Optional[str] = Field(None, description="Author display name")

    # Tags and SEO
    tags: list[str] = Field(default_factory=list, description="Content tags")

    # Targeting
    target_personas: list[PersonaType] = Field(default_factory=list, description="Target personas")
    target_industries: list[str] = Field(default_factory=list, description="Target industries")
    target_accounts: list[str] = Field(default_factory=list, description="Target account IDs for ABM")

    # Campaign association
    campaign_id: Optional[str] = Field(None, description="Associated campaign ID")

    # AI generation
    ai_generated: bool = Field(default=False, description="Whether AI generated this content")
    ai_prompt: Optional[str] = Field(None, description="Prompt used for AI generation")

    # Timestamps
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    published_at: Optional[datetime] = Field(default=None, description="Publication timestamp")
    scheduled_at: Optional[datetime] = Field(default=None, description="Scheduled publication time")


class Content(ContentBase):
    """Full content model with ID"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique content ID")


# ============================================================================
# LINKEDIN POST
# ============================================================================

class LinkedInPostContent(BaseModel):
    """LinkedIn-specific content fields"""
    body: str = Field(..., description="Post body text", max_length=3000)
    hashtags: list[str] = Field(default_factory=list, description="Hashtags to include")
    mentions: list[str] = Field(default_factory=list, description="LinkedIn profile URLs to mention")

    # Media
    image_url: Optional[str] = Field(None, description="Image URL")
    image_alt_text: Optional[str] = Field(None, description="Image alt text for accessibility")
    video_url: Optional[str] = Field(None, description="Video URL")
    document_url: Optional[str] = Field(None, description="Document/PDF URL")

    # Link preview
    link_url: Optional[str] = Field(None, description="External link URL")

    # Engagement
    call_to_action: Optional[str] = Field(None, description="Call to action text")


class LinkedInPost(Content):
    """LinkedIn post content"""
    content_type: ContentType = Field(default=ContentType.LINKEDIN_POST, const=True)
    linkedin: LinkedInPostContent = Field(..., description="LinkedIn-specific content")

    # Scheduling
    scheduled_time: Optional[datetime] = Field(None, description="Scheduled post time")
    timezone: str = Field(default="Europe/Amsterdam", description="Timezone for scheduling")

    # Analytics
    impressions: int = Field(default=0, description="Post impressions")
    reactions: int = Field(default=0, description="Total reactions")
    comments: int = Field(default=0, description="Comment count")
    shares: int = Field(default=0, description="Share count")
    clicks: int = Field(default=0, description="Link click count")
    engagement_rate: float = Field(default=0.0, description="Engagement rate percentage")


# ============================================================================
# ARTICLE (BLOG)
# ============================================================================

class ArticleSection(BaseModel):
    """Article section/block"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Section ID")
    type: str = Field(default="paragraph", description="Section type: paragraph, heading, image, quote, list")
    content: str = Field(..., description="Section content (HTML or markdown)")
    order: int = Field(default=0, description="Section order")


class ArticleSEO(BaseModel):
    """Article SEO settings"""
    meta_title: Optional[str] = Field(None, description="Meta title (defaults to article title)", max_length=60)
    meta_description: Optional[str] = Field(None, description="Meta description", max_length=160)
    focus_keyword: Optional[str] = Field(None, description="Primary SEO keyword")
    secondary_keywords: list[str] = Field(default_factory=list, description="Secondary keywords")
    canonical_url: Optional[str] = Field(None, description="Canonical URL")
    og_image_url: Optional[str] = Field(None, description="Open Graph image URL")
    no_index: bool = Field(default=False, description="Prevent indexing")


class ArticleContent(BaseModel):
    """Article-specific content fields"""
    subtitle: Optional[str] = Field(None, description="Article subtitle")
    summary: Optional[str] = Field(None, description="Article summary/excerpt", max_length=500)
    body: str = Field(..., description="Article body (HTML or markdown)")
    sections: list[ArticleSection] = Field(default_factory=list, description="Structured sections")

    # Media
    featured_image_url: Optional[str] = Field(None, description="Featured image URL")
    featured_image_alt: Optional[str] = Field(None, description="Featured image alt text")

    # Reading
    reading_time_minutes: int = Field(default=5, description="Estimated reading time")
    word_count: int = Field(default=0, description="Word count")

    # SEO
    seo: ArticleSEO = Field(default_factory=ArticleSEO, description="SEO settings")
    slug: Optional[str] = Field(None, description="URL slug")


class Article(Content):
    """Blog article content"""
    content_type: ContentType = Field(default=ContentType.ARTICLE, const=True)
    article: ArticleContent = Field(..., description="Article-specific content")

    # Analytics
    views: int = Field(default=0, description="Page views")
    unique_visitors: int = Field(default=0, description="Unique visitors")
    avg_time_on_page: float = Field(default=0.0, description="Average time on page (seconds)")
    scroll_depth: float = Field(default=0.0, description="Average scroll depth percentage")
    conversions: int = Field(default=0, description="Conversion count")


# ============================================================================
# LANDING PAGE
# ============================================================================

class LandingPageCTA(BaseModel):
    """Call to action button"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="CTA ID")
    text: str = Field(..., description="Button text")
    url: str = Field(..., description="Button URL or action")
    style: str = Field(default="primary", description="Button style: primary, secondary, outline")
    position: str = Field(default="hero", description="Position on page")


class LandingPageForm(BaseModel):
    """Form configuration"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Form ID")
    title: Optional[str] = Field(None, description="Form title")
    fields: list[dict] = Field(default_factory=list, description="Form field definitions")
    submit_button_text: str = Field(default="Submit", description="Submit button text")
    success_message: str = Field(default="Thank you for your submission!", description="Success message")
    redirect_url: Optional[str] = Field(None, description="Redirect URL after submission")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for submissions")


class LandingPageContent(BaseModel):
    """Landing page content fields"""
    headline: str = Field(..., description="Main headline")
    subheadline: Optional[str] = Field(None, description="Subheadline")
    body: Optional[str] = Field(None, description="Body content (HTML)")

    # Hero section
    hero_image_url: Optional[str] = Field(None, description="Hero image URL")
    hero_video_url: Optional[str] = Field(None, description="Hero video URL")

    # Value proposition
    value_props: list[dict] = Field(default_factory=list, description="Value proposition items")

    # Social proof
    testimonials: list[dict] = Field(default_factory=list, description="Testimonial items")
    logos: list[str] = Field(default_factory=list, description="Customer logo URLs")

    # CTAs and forms
    ctas: list[LandingPageCTA] = Field(default_factory=list, description="Call to action buttons")
    forms: list[LandingPageForm] = Field(default_factory=list, description="Forms")

    # Template
    template_id: Optional[str] = Field(None, description="Template ID if using a template")
    custom_css: Optional[str] = Field(None, description="Custom CSS")
    custom_js: Optional[str] = Field(None, description="Custom JavaScript")


class LandingPage(Content):
    """Landing page content"""
    content_type: ContentType = Field(default=ContentType.LANDING_PAGE, const=True)
    landing_page: LandingPageContent = Field(..., description="Landing page content")

    # URL
    slug: str = Field(..., description="URL slug")
    full_url: Optional[str] = Field(None, description="Full page URL")

    # A/B testing
    variant_of: Optional[str] = Field(None, description="Parent page ID if this is a variant")
    variant_name: Optional[str] = Field(None, description="Variant name (A, B, etc.)")
    variant_weight: int = Field(default=50, description="Traffic weight percentage")

    # Analytics
    views: int = Field(default=0, description="Page views")
    unique_visitors: int = Field(default=0, description="Unique visitors")
    form_submissions: int = Field(default=0, description="Form submission count")
    conversion_rate: float = Field(default=0.0, description="Conversion rate percentage")
    bounce_rate: float = Field(default=0.0, description="Bounce rate percentage")


# ============================================================================
# ABM CONTENT
# ============================================================================

class PersonalizationToken(BaseModel):
    """Personalization token definition"""
    key: str = Field(..., description="Token key (e.g., 'company_name')")
    default_value: str = Field(..., description="Default value if data unavailable")
    description: Optional[str] = Field(None, description="Token description")


class ABMVariation(BaseModel):
    """ABM content variation for specific account/persona"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Variation ID")
    account_id: Optional[str] = Field(None, description="Target account ID")
    account_name: Optional[str] = Field(None, description="Target account name")
    persona: Optional[PersonaType] = Field(None, description="Target persona")

    # Variation content
    headline: Optional[str] = Field(None, description="Customized headline")
    body: Optional[str] = Field(None, description="Customized body")
    image_url: Optional[str] = Field(None, description="Customized image")
    cta_text: Optional[str] = Field(None, description="Customized CTA")


class ABMContentData(BaseModel):
    """ABM-specific content fields"""
    base_headline: str = Field(..., description="Base headline template")
    base_body: str = Field(..., description="Base body template")

    # Personalization
    tokens: list[PersonalizationToken] = Field(default_factory=list, description="Personalization tokens")
    variations: list[ABMVariation] = Field(default_factory=list, description="Account/persona variations")

    # Media
    base_image_url: Optional[str] = Field(None, description="Base image URL")

    # Integration
    use_in_ads: bool = Field(default=False, description="Use in advertising campaigns")
    use_in_email: bool = Field(default=False, description="Use in email sequences")
    use_in_landing_pages: bool = Field(default=False, description="Use in landing pages")


class ABMContent(Content):
    """Account-based marketing content"""
    content_type: ContentType = Field(default=ContentType.ABM_CONTENT, const=True)
    abm: ABMContentData = Field(..., description="ABM-specific content")

    # Targeting stats
    accounts_targeted: int = Field(default=0, description="Number of accounts targeted")
    personas_targeted: int = Field(default=0, description="Number of persona variations")

    # Analytics
    impressions: int = Field(default=0, description="Total impressions")
    engagement: int = Field(default=0, description="Total engagements")
    engagement_rate: float = Field(default=0.0, description="Engagement rate")


# ============================================================================
# CASE STUDY
# ============================================================================

class CaseStudyMetrics(BaseModel):
    """Case study success metrics"""
    metric_name: str = Field(..., description="Metric name (e.g., 'Revenue Increase')")
    metric_value: str = Field(..., description="Metric value (e.g., '45%')")
    metric_description: Optional[str] = Field(None, description="Additional context")


class CaseStudyQuote(BaseModel):
    """Customer quote/testimonial"""
    quote: str = Field(..., description="Quote text")
    author_name: str = Field(..., description="Author name")
    author_title: Optional[str] = Field(None, description="Author job title")
    author_image_url: Optional[str] = Field(None, description="Author photo URL")


class CaseStudyContent(BaseModel):
    """Case study content fields"""
    # Customer info
    customer_name: str = Field(..., description="Customer company name")
    customer_logo_url: Optional[str] = Field(None, description="Customer logo URL")
    customer_industry: Optional[str] = Field(None, description="Customer industry")
    customer_size: Optional[str] = Field(None, description="Customer company size")

    # Story structure
    challenge: str = Field(..., description="The challenge/problem")
    solution: str = Field(..., description="The solution provided")
    results: str = Field(..., description="The results achieved")

    # Extended content
    full_story: Optional[str] = Field(None, description="Full case study content (HTML)")

    # Metrics and quotes
    metrics: list[CaseStudyMetrics] = Field(default_factory=list, description="Success metrics")
    quotes: list[CaseStudyQuote] = Field(default_factory=list, description="Customer quotes")

    # Media
    featured_image_url: Optional[str] = Field(None, description="Featured image URL")
    video_url: Optional[str] = Field(None, description="Video testimonial URL")
    pdf_url: Optional[str] = Field(None, description="Downloadable PDF URL")


class CaseStudy(Content):
    """Case study content"""
    content_type: ContentType = Field(default=ContentType.CASE_STUDY, const=True)
    case_study: CaseStudyContent = Field(..., description="Case study content")

    # Analytics
    views: int = Field(default=0, description="Page views")
    downloads: int = Field(default=0, description="PDF downloads")
    video_plays: int = Field(default=0, description="Video plays")


# ============================================================================
# CAMPAIGN
# ============================================================================

class CampaignStatus(str, Enum):
    """Campaign status"""
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Campaign(BaseModel):
    """Marketing campaign grouping content"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Campaign ID")
    name: str = Field(..., description="Campaign name")
    description: Optional[str] = Field(None, description="Campaign description")
    status: CampaignStatus = Field(default=CampaignStatus.PLANNING, description="Campaign status")

    # Timeline
    start_date: Optional[datetime] = Field(None, description="Campaign start date")
    end_date: Optional[datetime] = Field(None, description="Campaign end date")

    # Targeting
    target_accounts: list[str] = Field(default_factory=list, description="Target account IDs")
    target_personas: list[PersonaType] = Field(default_factory=list, description="Target personas")
    target_industries: list[str] = Field(default_factory=list, description="Target industries")

    # Content
    content_ids: list[str] = Field(default_factory=list, description="Associated content IDs")

    # Budget
    budget: Optional[float] = Field(None, description="Campaign budget")
    spent: float = Field(default=0.0, description="Amount spent")

    # Goals
    goal_type: Optional[str] = Field(None, description="Goal type: awareness, leads, engagement")
    goal_value: Optional[float] = Field(None, description="Goal target value")
    current_value: float = Field(default=0.0, description="Current goal progress")

    # Analytics
    total_impressions: int = Field(default=0, description="Total impressions")
    total_engagement: int = Field(default=0, description="Total engagements")
    total_leads: int = Field(default=0, description="Total leads generated")
    total_conversions: int = Field(default=0, description="Total conversions")

    # Timestamps
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    created_by: Optional[str] = Field(None, description="Creator user ID")


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ContentCreateRequest(BaseModel):
    """Request to create content"""
    content_type: ContentType = Field(..., description="Type of content to create")
    title: str = Field(..., description="Content title")
    category: Optional[ContentCategory] = Field(None, description="Content category")
    tags: list[str] = Field(default_factory=list, description="Tags")

    # Type-specific content (one of these based on content_type)
    linkedin: Optional[LinkedInPostContent] = Field(None, description="LinkedIn content")
    article: Optional[ArticleContent] = Field(None, description="Article content")
    landing_page: Optional[LandingPageContent] = Field(None, description="Landing page content")
    abm: Optional[ABMContentData] = Field(None, description="ABM content")
    case_study: Optional[CaseStudyContent] = Field(None, description="Case study content")

    # Targeting
    target_personas: list[PersonaType] = Field(default_factory=list, description="Target personas")
    target_industries: list[str] = Field(default_factory=list, description="Target industries")
    target_accounts: list[str] = Field(default_factory=list, description="Target account IDs")

    # Campaign
    campaign_id: Optional[str] = Field(None, description="Campaign ID")


class ContentUpdateRequest(BaseModel):
    """Request to update content"""
    title: Optional[str] = Field(None, description="New title")
    status: Optional[ContentStatus] = Field(None, description="New status")
    category: Optional[ContentCategory] = Field(None, description="New category")
    tags: Optional[list[str]] = Field(None, description="New tags")

    # Type-specific content updates
    linkedin: Optional[LinkedInPostContent] = Field(None, description="LinkedIn content update")
    article: Optional[ArticleContent] = Field(None, description="Article content update")
    landing_page: Optional[LandingPageContent] = Field(None, description="Landing page content update")
    abm: Optional[ABMContentData] = Field(None, description="ABM content update")
    case_study: Optional[CaseStudyContent] = Field(None, description="Case study content update")

    # Targeting updates
    target_personas: Optional[list[PersonaType]] = Field(None, description="Target personas")
    target_industries: Optional[list[str]] = Field(None, description="Target industries")
    target_accounts: Optional[list[str]] = Field(None, description="Target account IDs")

    # Campaign
    campaign_id: Optional[str] = Field(None, description="Campaign ID")


class ContentListResponse(BaseModel):
    """Response for content list"""
    items: list[Content] = Field(..., description="List of content items")
    total: int = Field(..., description="Total count")
    page: int = Field(default=1, description="Current page")
    page_size: int = Field(default=20, description="Items per page")


class ContentGenerateRequest(BaseModel):
    """Request to generate content with AI"""
    content_type: ContentType = Field(..., description="Type of content to generate")
    prompt: str = Field(..., description="Generation prompt/instructions")
    tone: str = Field(default="professional", description="Tone: professional, casual, formal, friendly")
    target_audience: Optional[str] = Field(None, description="Target audience description")
    key_points: list[str] = Field(default_factory=list, description="Key points to include")
    max_length: Optional[int] = Field(None, description="Maximum length (chars)")

    # Context
    company_context: Optional[str] = Field(None, description="Company context for personalization")
    product_context: Optional[str] = Field(None, description="Product context")

    # Reference content
    reference_content_ids: list[str] = Field(default_factory=list, description="IDs of content to reference")


class HashtagSuggestionRequest(BaseModel):
    """Request for hashtag suggestions"""
    content: str = Field(..., description="Content to analyze")
    industry: Optional[str] = Field(None, description="Industry context")
    count: int = Field(default=5, description="Number of suggestions")


class HashtagSuggestionResponse(BaseModel):
    """Response with hashtag suggestions"""
    hashtags: list[str] = Field(..., description="Suggested hashtags")
    trending: list[str] = Field(default_factory=list, description="Currently trending hashtags")


class LinkedInScheduleRequest(BaseModel):
    """Request to schedule a LinkedIn post"""
    content_id: str = Field(..., description="Content ID to schedule")
    scheduled_time: datetime = Field(..., description="Time to publish")
    timezone: str = Field(default="Europe/Amsterdam", description="Timezone")


class ContentSequenceLinkRequest(BaseModel):
    """Request to link content to a sequence step"""
    content_id: str = Field(..., description="Content ID")
    sequence_id: str = Field(..., description="Sequence ID")
    step_id: str = Field(..., description="Step ID within sequence")


class MarketingAnalytics(BaseModel):
    """Marketing analytics overview"""
    # Content metrics
    total_content: int = Field(default=0, description="Total content pieces")
    content_by_type: dict[str, int] = Field(default_factory=dict, description="Content count by type")
    content_by_status: dict[str, int] = Field(default_factory=dict, description="Content count by status")

    # Performance metrics
    total_impressions: int = Field(default=0, description="Total impressions")
    total_engagement: int = Field(default=0, description="Total engagements")
    avg_engagement_rate: float = Field(default=0.0, description="Average engagement rate")

    # Content performance
    top_performing: list[dict] = Field(default_factory=list, description="Top performing content")

    # Campaign metrics
    active_campaigns: int = Field(default=0, description="Active campaigns")
    campaign_performance: list[dict] = Field(default_factory=list, description="Campaign performance")

    # Trends
    content_created_trend: list[dict] = Field(default_factory=list, description="Content creation trend")
    engagement_trend: list[dict] = Field(default_factory=list, description="Engagement trend")
