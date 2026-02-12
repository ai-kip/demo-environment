"""
Marketing Intelligence Content API Router

Full API for marketing content management including:
- Content CRUD (all types)
- Workflow transitions
- LinkedIn scheduling
- AI content generation
- Campaigns
- Sequence integration
- Analytics
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, Body
from pydantic import BaseModel, Field
from neo4j import Session

from atlas.services.query_api.deps import neo4j_session
from atlas.services.content import ContentService, LinkedInService
from atlas.api.models.content import (
    Content,
    ContentType,
    ContentStatus,
    ContentCategory,
    ContentCreateRequest,
    ContentUpdateRequest,
    ContentListResponse,
    ContentGenerateRequest,
    HashtagSuggestionRequest,
    HashtagSuggestionResponse,
    LinkedInScheduleRequest,
    ContentSequenceLinkRequest,
    Campaign,
    CampaignStatus,
    MarketingAnalytics,
    LinkedInPostContent,
)


router = APIRouter(prefix="/content", tags=["Marketing Intelligence - Content"])


# ============================================================================
# DEPENDENCIES
# ============================================================================

def get_content_service(s: Annotated[Session, Depends(neo4j_session)]) -> ContentService:
    """Get content service instance"""
    return ContentService(neo4j_session=s)


def get_linkedin_service(s: Annotated[Session, Depends(neo4j_session)]) -> LinkedInService:
    """Get LinkedIn service instance"""
    return LinkedInService(neo4j_session=s)


# ============================================================================
# PYDANTIC MODELS FOR REQUESTS/RESPONSES
# ============================================================================

class ContentResponse(BaseModel):
    """Standard content response"""
    success: bool = True
    content: Optional[dict] = None
    message: Optional[str] = None


class CampaignCreateRequest(BaseModel):
    """Request to create a campaign"""
    name: str = Field(..., description="Campaign name")
    description: Optional[str] = Field(None, description="Campaign description")
    start_date: Optional[datetime] = Field(None, description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")
    target_accounts: list[str] = Field(default_factory=list)
    target_industries: list[str] = Field(default_factory=list)
    budget: Optional[float] = Field(None, description="Budget")
    goal_type: Optional[str] = Field(None, description="Goal type")
    goal_value: Optional[float] = Field(None, description="Goal value")


class AddContentToCampaignRequest(BaseModel):
    """Request to add content to campaign"""
    content_id: str = Field(..., description="Content ID to add")


class GenerateContentResponse(BaseModel):
    """Response from AI content generation"""
    success: bool = True
    content: dict = Field(..., description="Generated content")
    tokens_used: int = Field(default=0, description="Tokens used for generation")


# ============================================================================
# CONTENT CRUD ENDPOINTS
# ============================================================================

@router.post("", response_model=ContentResponse)
def create_content(
    request: ContentCreateRequest,
    service: Annotated[ContentService, Depends(get_content_service)],
    author_id: Optional[str] = Query(None, description="Author user ID"),
):
    """
    Create new marketing content.

    Supports all content types:
    - LinkedIn Post
    - Article (Blog)
    - Landing Page
    - ABM Content
    - Case Study
    """
    try:
        content = service.create_content(request, author_id)
        return ContentResponse(success=True, content=content.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=ContentListResponse)
def list_content(
    service: Annotated[ContentService, Depends(get_content_service)],
    content_type: Optional[ContentType] = Query(None, description="Filter by content type"),
    status: Optional[ContentStatus] = Query(None, description="Filter by status"),
    category: Optional[ContentCategory] = Query(None, description="Filter by category"),
    campaign_id: Optional[str] = Query(None, description="Filter by campaign"),
    author_id: Optional[str] = Query(None, description="Filter by author"),
    search: Optional[str] = Query(None, description="Search in title"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """
    List marketing content with filters.

    Supports filtering by:
    - Content type (linkedin_post, article, landing_page, abm_content, case_study)
    - Status (draft, review, approved, scheduled, published, archived)
    - Category
    - Campaign
    - Author
    - Search term
    """
    offset = (page - 1) * page_size
    items, total = service.list_content(
        content_type=content_type,
        status=status,
        category=category,
        campaign_id=campaign_id,
        author_id=author_id,
        search=search,
        limit=page_size,
        offset=offset,
    )

    return ContentListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{content_id}")
def get_content(
    content_id: str,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Get content by ID"""
    content = service.get_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content.model_dump()


@router.patch("/{content_id}", response_model=ContentResponse)
def update_content(
    content_id: str,
    request: ContentUpdateRequest,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Update content"""
    content = service.update_content(content_id, request)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return ContentResponse(success=True, content=content.model_dump())


@router.delete("/{content_id}")
def delete_content(
    content_id: str,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Delete content"""
    success = service.delete_content(content_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"success": True, "message": "Content deleted"}


# ============================================================================
# WORKFLOW ENDPOINTS
# ============================================================================

@router.post("/{content_id}/submit", response_model=ContentResponse)
def submit_for_review(
    content_id: str,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Submit content for review"""
    content = service.submit_for_review(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return ContentResponse(success=True, content=content.model_dump(), message="Submitted for review")


@router.post("/{content_id}/approve", response_model=ContentResponse)
def approve_content(
    content_id: str,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Approve content"""
    content = service.approve_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return ContentResponse(success=True, content=content.model_dump(), message="Content approved")


@router.post("/{content_id}/publish", response_model=ContentResponse)
def publish_content(
    content_id: str,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Publish content"""
    content = service.publish_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return ContentResponse(success=True, content=content.model_dump(), message="Content published")


@router.post("/{content_id}/archive", response_model=ContentResponse)
def archive_content(
    content_id: str,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Archive content"""
    content = service.archive_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return ContentResponse(success=True, content=content.model_dump(), message="Content archived")


# ============================================================================
# LINKEDIN ENDPOINTS
# ============================================================================

@router.post("/linkedin/schedule")
def schedule_linkedin_post(
    request: LinkedInScheduleRequest,
    linkedin_service: Annotated[LinkedInService, Depends(get_linkedin_service)],
):
    """Schedule a LinkedIn post for publishing"""
    post = linkedin_service.schedule_post(
        content_id=request.content_id,
        scheduled_time=request.scheduled_time,
        timezone=request.timezone,
    )
    if not post:
        raise HTTPException(status_code=404, detail="LinkedIn post not found")
    return {
        "success": True,
        "message": f"Post scheduled for {request.scheduled_time}",
        "post": post.model_dump(),
    }


@router.delete("/linkedin/{content_id}/schedule")
def unschedule_linkedin_post(
    content_id: str,
    linkedin_service: Annotated[LinkedInService, Depends(get_linkedin_service)],
):
    """Remove scheduling from a LinkedIn post"""
    post = linkedin_service.unschedule_post(content_id)
    if not post:
        raise HTTPException(status_code=404, detail="LinkedIn post not found")
    return {"success": True, "message": "Scheduling removed", "post": post.model_dump()}


@router.get("/linkedin/scheduled")
def get_scheduled_posts(
    linkedin_service: Annotated[LinkedInService, Depends(get_linkedin_service)],
    from_date: Optional[datetime] = Query(None, description="From date"),
    to_date: Optional[datetime] = Query(None, description="To date"),
    limit: int = Query(50, ge=1, le=200),
):
    """Get scheduled LinkedIn posts"""
    posts = linkedin_service.get_scheduled_posts(
        from_date=from_date,
        to_date=to_date,
        limit=limit,
    )
    return {"posts": [p.model_dump() for p in posts], "count": len(posts)}


@router.get("/linkedin/analytics")
def get_linkedin_analytics(
    linkedin_service: Annotated[LinkedInService, Depends(get_linkedin_service)],
    from_date: Optional[datetime] = Query(None, description="From date"),
    to_date: Optional[datetime] = Query(None, description="To date"),
):
    """Get LinkedIn analytics overview"""
    return linkedin_service.get_linkedin_analytics(from_date, to_date)


@router.get("/linkedin/top-performing")
def get_top_performing_posts(
    linkedin_service: Annotated[LinkedInService, Depends(get_linkedin_service)],
    limit: int = Query(5, ge=1, le=20),
):
    """Get top performing LinkedIn posts"""
    posts = linkedin_service.get_top_performing_posts(limit)
    return {"posts": [p.model_dump() for p in posts], "count": len(posts)}


@router.post("/linkedin/validate")
def validate_linkedin_post(
    content: LinkedInPostContent,
    linkedin_service: Annotated[LinkedInService, Depends(get_linkedin_service)],
):
    """Validate LinkedIn post content"""
    return linkedin_service.validate_post(content)


# ============================================================================
# AI GENERATION ENDPOINTS
# ============================================================================

@router.post("/generate", response_model=GenerateContentResponse)
def generate_content(
    request: ContentGenerateRequest,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """
    Generate content using AI.

    Supports generating:
    - LinkedIn posts
    - Article outlines and content
    - Landing page copy
    - ABM personalized content
    - Case study drafts
    """
    # This is a placeholder - in production, integrate with AI service
    # For now, return a structured template

    generated = {
        "content_type": request.content_type.value,
        "generated": True,
        "prompt_used": request.prompt,
    }

    if request.content_type == ContentType.LINKEDIN_POST:
        generated["content"] = {
            "body": f"[AI-generated post based on: {request.prompt}]\n\nShare your thoughts below!",
            "hashtags": ["#AI", "#marketing", "#content"],
            "call_to_action": "Comment your thoughts below!",
        }
    elif request.content_type == ContentType.ARTICLE:
        generated["content"] = {
            "title": f"[AI Title]: {request.prompt[:50]}...",
            "subtitle": "A comprehensive guide",
            "summary": f"This article explores {request.prompt}",
            "body": f"<h2>Introduction</h2><p>[AI-generated content about: {request.prompt}]</p>",
            "reading_time_minutes": 5,
        }
    elif request.content_type == ContentType.LANDING_PAGE:
        generated["content"] = {
            "headline": f"Transform Your Business with {request.prompt[:30]}",
            "subheadline": "The solution you've been looking for",
            "body": "<p>[AI-generated landing page content]</p>",
        }
    elif request.content_type == ContentType.ABM_CONTENT:
        generated["content"] = {
            "base_headline": f"{{{{company_name}}}}, here's how to {request.prompt[:30]}",
            "base_body": f"[Personalized content for {{{{company_name}}}} about {request.prompt}]",
        }
    else:
        generated["content"] = {
            "body": f"[AI-generated content for: {request.prompt}]",
        }

    return GenerateContentResponse(
        success=True,
        content=generated,
        tokens_used=100,  # Placeholder
    )


@router.post("/variations")
def generate_variations(
    content_id: str = Body(..., description="Content ID to create variations of"),
    count: int = Body(3, description="Number of variations"),
    service: Annotated[ContentService, Depends(get_content_service)] = None,
):
    """Generate content variations for A/B testing"""
    content = service.get_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Placeholder - in production, use AI to generate variations
    variations = []
    for i in range(count):
        variations.append({
            "variation_number": i + 1,
            "title": f"{content.title} - Variation {chr(65 + i)}",
            "content": f"[Variation {chr(65 + i)} of original content]",
        })

    return {"original_id": content_id, "variations": variations}


@router.post("/hashtags", response_model=HashtagSuggestionResponse)
def suggest_hashtags(
    request: HashtagSuggestionRequest,
    linkedin_service: Annotated[LinkedInService, Depends(get_linkedin_service)],
):
    """Suggest hashtags for content"""
    return linkedin_service.suggest_hashtags(
        content=request.content,
        industry=request.industry,
        count=request.count,
    )


# ============================================================================
# SEQUENCE INTEGRATION ENDPOINTS
# ============================================================================

@router.post("/link-sequence")
def link_content_to_sequence(
    request: ContentSequenceLinkRequest,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Link content to a sequence step"""
    success = service.link_to_sequence(
        content_id=request.content_id,
        sequence_id=request.sequence_id,
        step_id=request.step_id,
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to link content to sequence")
    return {"success": True, "message": "Content linked to sequence"}


@router.get("/for-sequences")
def get_content_for_sequences(
    service: Annotated[ContentService, Depends(get_content_service)],
    content_type: Optional[ContentType] = Query(None, description="Filter by type"),
    limit: int = Query(50, ge=1, le=200),
):
    """Get publishable content that can be linked to sequences"""
    items = service.get_content_for_sequences(content_type, limit)
    return {"items": [c.model_dump() for c in items], "count": len(items)}


# ============================================================================
# CAMPAIGN ENDPOINTS
# ============================================================================

@router.post("/campaigns")
def create_campaign(
    request: CampaignCreateRequest,
    service: Annotated[ContentService, Depends(get_content_service)],
    created_by: Optional[str] = Query(None, description="Creator user ID"),
):
    """Create a marketing campaign"""
    campaign = Campaign(
        name=request.name,
        description=request.description,
        start_date=request.start_date,
        end_date=request.end_date,
        target_accounts=request.target_accounts,
        target_industries=request.target_industries,
        budget=request.budget,
        goal_type=request.goal_type,
        goal_value=request.goal_value,
        created_by=created_by,
    )

    created = service.create_campaign(campaign)
    return {"success": True, "campaign": created.model_dump()}


@router.get("/campaigns")
def list_campaigns(
    service: Annotated[ContentService, Depends(get_content_service)],
    status: Optional[CampaignStatus] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List marketing campaigns"""
    offset = (page - 1) * page_size
    items, total = service.list_campaigns(status=status, limit=page_size, offset=offset)
    return {
        "campaigns": [c.model_dump() for c in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/campaigns/{campaign_id}")
def get_campaign(
    campaign_id: str,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Get campaign by ID"""
    campaign = service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign.model_dump()


@router.post("/campaigns/{campaign_id}/content")
def add_content_to_campaign(
    campaign_id: str,
    request: AddContentToCampaignRequest,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Add content to a campaign"""
    success = service.add_content_to_campaign(campaign_id, request.content_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add content to campaign")
    return {"success": True, "message": "Content added to campaign"}


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/analytics", response_model=MarketingAnalytics)
def get_marketing_analytics(
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Get marketing analytics overview"""
    return service.get_marketing_analytics()


@router.get("/{content_id}/analytics")
def get_content_analytics(
    content_id: str,
    service: Annotated[ContentService, Depends(get_content_service)],
):
    """Get analytics for specific content"""
    analytics = service.get_content_analytics(content_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Content not found")
    return analytics


# ============================================================================
# REFERENCE DATA ENDPOINTS
# ============================================================================

@router.get("/types")
def get_content_types():
    """Get all content types with descriptions"""
    return {
        ContentType.LINKEDIN_POST.value: {
            "label": "LinkedIn Post",
            "description": "Short-form social content for LinkedIn",
            "max_length": 3000,
            "supports_scheduling": True,
        },
        ContentType.ARTICLE.value: {
            "label": "Article",
            "description": "Long-form blog content",
            "supports_seo": True,
            "supports_sections": True,
        },
        ContentType.LANDING_PAGE.value: {
            "label": "Landing Page",
            "description": "Conversion-focused web page",
            "supports_forms": True,
            "supports_ab_testing": True,
        },
        ContentType.ABM_CONTENT.value: {
            "label": "ABM Content",
            "description": "Account-based marketing content with personalization",
            "supports_personalization": True,
            "supports_variations": True,
        },
        ContentType.CASE_STUDY.value: {
            "label": "Case Study",
            "description": "Customer success story",
            "supports_metrics": True,
            "supports_testimonials": True,
        },
    }


@router.get("/statuses")
def get_content_statuses():
    """Get all content statuses"""
    return {
        ContentStatus.DRAFT.value: {"label": "Draft", "color": "#6B7280"},
        ContentStatus.REVIEW.value: {"label": "In Review", "color": "#F59E0B"},
        ContentStatus.APPROVED.value: {"label": "Approved", "color": "#3B82F6"},
        ContentStatus.SCHEDULED.value: {"label": "Scheduled", "color": "#8B5CF6"},
        ContentStatus.PUBLISHED.value: {"label": "Published", "color": "#10B981"},
        ContentStatus.ARCHIVED.value: {"label": "Archived", "color": "#9CA3AF"},
    }


@router.get("/categories")
def get_content_categories():
    """Get all content categories"""
    return {
        ContentCategory.THOUGHT_LEADERSHIP.value: {"label": "Thought Leadership", "icon": "lightbulb"},
        ContentCategory.PRODUCT.value: {"label": "Product", "icon": "package"},
        ContentCategory.CASE_STUDY.value: {"label": "Case Study", "icon": "file-check"},
        ContentCategory.INDUSTRY.value: {"label": "Industry", "icon": "building"},
        ContentCategory.COMPANY_NEWS.value: {"label": "Company News", "icon": "newspaper"},
        ContentCategory.EDUCATIONAL.value: {"label": "Educational", "icon": "graduation-cap"},
        ContentCategory.PROMOTIONAL.value: {"label": "Promotional", "icon": "megaphone"},
    }
