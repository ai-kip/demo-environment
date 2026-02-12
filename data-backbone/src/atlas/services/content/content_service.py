"""
Content Service

Business logic for managing marketing content across all types.
Handles CRUD operations, workflow transitions, and analytics.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from neo4j import Session

from atlas.api.models.content import (
    Content,
    ContentType,
    ContentStatus,
    ContentCategory,
    ContentCreateRequest,
    ContentUpdateRequest,
    LinkedInPost,
    LinkedInPostContent,
    Article,
    ArticleContent,
    LandingPage,
    LandingPageContent,
    ABMContent,
    ABMContentData,
    CaseStudy,
    CaseStudyContent,
    Campaign,
    CampaignStatus,
    MarketingAnalytics,
    PersonaType,
)


class ContentService:
    """Service for managing marketing content"""

    def __init__(self, neo4j_session: Session):
        """Initialize the content service with Neo4j session"""
        self.session = neo4j_session

    # ========================================================================
    # CONTENT CRUD
    # ========================================================================

    def create_content(self, request: ContentCreateRequest, author_id: str | None = None) -> Content:
        """Create new content based on type"""
        content_id = str(uuid4())
        now = datetime.utcnow()

        # Build base content
        base_data = {
            "id": content_id,
            "title": request.title,
            "content_type": request.content_type.value,
            "status": ContentStatus.DRAFT.value,
            "category": request.category.value if request.category else None,
            "tags": request.tags,
            "target_personas": [p.value for p in request.target_personas],
            "target_industries": request.target_industries,
            "target_accounts": request.target_accounts,
            "campaign_id": request.campaign_id,
            "author_id": author_id,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }

        # Add type-specific content
        type_specific = {}
        if request.content_type == ContentType.LINKEDIN_POST and request.linkedin:
            type_specific = {
                "body": request.linkedin.body,
                "hashtags": request.linkedin.hashtags,
                "mentions": request.linkedin.mentions,
                "image_url": request.linkedin.image_url,
                "video_url": request.linkedin.video_url,
                "link_url": request.linkedin.link_url,
                "call_to_action": request.linkedin.call_to_action,
            }
        elif request.content_type == ContentType.ARTICLE and request.article:
            type_specific = {
                "subtitle": request.article.subtitle,
                "summary": request.article.summary,
                "body": request.article.body,
                "featured_image_url": request.article.featured_image_url,
                "slug": request.article.slug,
                "reading_time_minutes": request.article.reading_time_minutes,
                "word_count": request.article.word_count,
            }
        elif request.content_type == ContentType.LANDING_PAGE and request.landing_page:
            type_specific = {
                "headline": request.landing_page.headline,
                "subheadline": request.landing_page.subheadline,
                "body": request.landing_page.body,
                "hero_image_url": request.landing_page.hero_image_url,
                "template_id": request.landing_page.template_id,
            }
        elif request.content_type == ContentType.ABM_CONTENT and request.abm:
            type_specific = {
                "base_headline": request.abm.base_headline,
                "base_body": request.abm.base_body,
                "base_image_url": request.abm.base_image_url,
                "use_in_ads": request.abm.use_in_ads,
                "use_in_email": request.abm.use_in_email,
                "use_in_landing_pages": request.abm.use_in_landing_pages,
            }
        elif request.content_type == ContentType.CASE_STUDY and request.case_study:
            type_specific = {
                "customer_name": request.case_study.customer_name,
                "customer_logo_url": request.case_study.customer_logo_url,
                "customer_industry": request.case_study.customer_industry,
                "challenge": request.case_study.challenge,
                "solution": request.case_study.solution,
                "results": request.case_study.results,
                "full_story": request.case_study.full_story,
                "featured_image_url": request.case_study.featured_image_url,
            }

        # Store in Neo4j
        query = """
        CREATE (c:Content {
            id: $id,
            title: $title,
            content_type: $content_type,
            status: $status,
            category: $category,
            tags: $tags,
            target_personas: $target_personas,
            target_industries: $target_industries,
            target_accounts: $target_accounts,
            campaign_id: $campaign_id,
            author_id: $author_id,
            created_at: $created_at,
            updated_at: $updated_at,
            type_specific: $type_specific
        })
        RETURN c
        """

        self.session.run(query, {
            **base_data,
            "type_specific": str(type_specific),  # Store as JSON string
        })

        # Return appropriate content type
        return self._build_content_object(base_data, type_specific)

    def get_content(self, content_id: str) -> Content | None:
        """Get content by ID"""
        query = """
        MATCH (c:Content {id: $id})
        RETURN c
        """

        result = self.session.run(query, {"id": content_id}).single()
        if not result:
            return None

        data = dict(result["c"])
        return self._build_content_from_neo4j(data)

    def list_content(
        self,
        content_type: ContentType | None = None,
        status: ContentStatus | None = None,
        category: ContentCategory | None = None,
        campaign_id: str | None = None,
        author_id: str | None = None,
        search: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Content], int]:
        """List content with filters"""
        conditions = []
        params = {"limit": limit, "offset": offset}

        if content_type:
            conditions.append("c.content_type = $content_type")
            params["content_type"] = content_type.value
        if status:
            conditions.append("c.status = $status")
            params["status"] = status.value
        if category:
            conditions.append("c.category = $category")
            params["category"] = category.value
        if campaign_id:
            conditions.append("c.campaign_id = $campaign_id")
            params["campaign_id"] = campaign_id
        if author_id:
            conditions.append("c.author_id = $author_id")
            params["author_id"] = author_id
        if search:
            conditions.append("toLower(c.title) CONTAINS toLower($search)")
            params["search"] = search

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        # Get count
        count_query = f"""
        MATCH (c:Content)
        {where_clause}
        RETURN count(c) as total
        """
        count_result = self.session.run(count_query, params).single()
        total = count_result["total"] if count_result else 0

        # Get items
        query = f"""
        MATCH (c:Content)
        {where_clause}
        RETURN c
        ORDER BY c.updated_at DESC
        SKIP $offset
        LIMIT $limit
        """

        results = self.session.run(query, params).data()
        items = [self._build_content_from_neo4j(dict(r["c"])) for r in results]

        return items, total

    def update_content(self, content_id: str, request: ContentUpdateRequest) -> Content | None:
        """Update content"""
        updates = {"updated_at": datetime.utcnow().isoformat()}

        if request.title:
            updates["title"] = request.title
        if request.status:
            updates["status"] = request.status.value
        if request.category:
            updates["category"] = request.category.value
        if request.tags is not None:
            updates["tags"] = request.tags
        if request.target_personas is not None:
            updates["target_personas"] = [p.value for p in request.target_personas]
        if request.target_industries is not None:
            updates["target_industries"] = request.target_industries
        if request.target_accounts is not None:
            updates["target_accounts"] = request.target_accounts
        if request.campaign_id is not None:
            updates["campaign_id"] = request.campaign_id

        # Build SET clause
        set_clauses = [f"c.{k} = ${k}" for k in updates.keys()]
        set_clause = ", ".join(set_clauses)

        query = f"""
        MATCH (c:Content {{id: $id}})
        SET {set_clause}
        RETURN c
        """

        result = self.session.run(query, {"id": content_id, **updates}).single()
        if not result:
            return None

        return self._build_content_from_neo4j(dict(result["c"]))

    def delete_content(self, content_id: str) -> bool:
        """Delete content"""
        query = """
        MATCH (c:Content {id: $id})
        DELETE c
        RETURN count(c) as deleted
        """

        result = self.session.run(query, {"id": content_id}).single()
        return result["deleted"] > 0 if result else False

    # ========================================================================
    # WORKFLOW
    # ========================================================================

    def submit_for_review(self, content_id: str) -> Content | None:
        """Submit content for review"""
        return self._transition_status(content_id, ContentStatus.REVIEW)

    def approve_content(self, content_id: str) -> Content | None:
        """Approve content"""
        return self._transition_status(content_id, ContentStatus.APPROVED)

    def publish_content(self, content_id: str) -> Content | None:
        """Publish content"""
        query = """
        MATCH (c:Content {id: $id})
        SET c.status = $status, c.published_at = $published_at, c.updated_at = $updated_at
        RETURN c
        """

        now = datetime.utcnow().isoformat()
        result = self.session.run(query, {
            "id": content_id,
            "status": ContentStatus.PUBLISHED.value,
            "published_at": now,
            "updated_at": now,
        }).single()

        if not result:
            return None
        return self._build_content_from_neo4j(dict(result["c"]))

    def archive_content(self, content_id: str) -> Content | None:
        """Archive content"""
        return self._transition_status(content_id, ContentStatus.ARCHIVED)

    def _transition_status(self, content_id: str, new_status: ContentStatus) -> Content | None:
        """Transition content to new status"""
        query = """
        MATCH (c:Content {id: $id})
        SET c.status = $status, c.updated_at = $updated_at
        RETURN c
        """

        result = self.session.run(query, {
            "id": content_id,
            "status": new_status.value,
            "updated_at": datetime.utcnow().isoformat(),
        }).single()

        if not result:
            return None
        return self._build_content_from_neo4j(dict(result["c"]))

    # ========================================================================
    # CAMPAIGNS
    # ========================================================================

    def create_campaign(self, campaign: Campaign) -> Campaign:
        """Create a new campaign"""
        now = datetime.utcnow()
        campaign.id = str(uuid4())
        campaign.created_at = now
        campaign.updated_at = now

        query = """
        CREATE (camp:Campaign {
            id: $id,
            name: $name,
            description: $description,
            status: $status,
            start_date: $start_date,
            end_date: $end_date,
            target_accounts: $target_accounts,
            target_personas: $target_personas,
            target_industries: $target_industries,
            content_ids: $content_ids,
            budget: $budget,
            spent: $spent,
            goal_type: $goal_type,
            goal_value: $goal_value,
            current_value: $current_value,
            created_at: $created_at,
            updated_at: $updated_at,
            created_by: $created_by
        })
        RETURN camp
        """

        self.session.run(query, {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "status": campaign.status.value,
            "start_date": campaign.start_date.isoformat() if campaign.start_date else None,
            "end_date": campaign.end_date.isoformat() if campaign.end_date else None,
            "target_accounts": campaign.target_accounts,
            "target_personas": [p.value for p in campaign.target_personas],
            "target_industries": campaign.target_industries,
            "content_ids": campaign.content_ids,
            "budget": campaign.budget,
            "spent": campaign.spent,
            "goal_type": campaign.goal_type,
            "goal_value": campaign.goal_value,
            "current_value": campaign.current_value,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "created_by": campaign.created_by,
        })

        return campaign

    def get_campaign(self, campaign_id: str) -> Campaign | None:
        """Get campaign by ID"""
        query = """
        MATCH (camp:Campaign {id: $id})
        RETURN camp
        """

        result = self.session.run(query, {"id": campaign_id}).single()
        if not result:
            return None

        return self._build_campaign_from_neo4j(dict(result["camp"]))

    def list_campaigns(
        self,
        status: CampaignStatus | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Campaign], int]:
        """List campaigns with filters"""
        conditions = []
        params = {"limit": limit, "offset": offset}

        if status:
            conditions.append("camp.status = $status")
            params["status"] = status.value

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        # Get count
        count_query = f"""
        MATCH (camp:Campaign)
        {where_clause}
        RETURN count(camp) as total
        """
        count_result = self.session.run(count_query, params).single()
        total = count_result["total"] if count_result else 0

        # Get items
        query = f"""
        MATCH (camp:Campaign)
        {where_clause}
        RETURN camp
        ORDER BY camp.updated_at DESC
        SKIP $offset
        LIMIT $limit
        """

        results = self.session.run(query, params).data()
        items = [self._build_campaign_from_neo4j(dict(r["camp"])) for r in results]

        return items, total

    def add_content_to_campaign(self, campaign_id: str, content_id: str) -> bool:
        """Add content to a campaign"""
        query = """
        MATCH (camp:Campaign {id: $campaign_id})
        SET camp.content_ids = camp.content_ids + $content_id
        WITH camp
        MATCH (c:Content {id: $content_id})
        SET c.campaign_id = $campaign_id
        RETURN camp
        """

        result = self.session.run(query, {
            "campaign_id": campaign_id,
            "content_id": content_id,
        }).single()

        return result is not None

    # ========================================================================
    # SEQUENCE INTEGRATION
    # ========================================================================

    def link_to_sequence(self, content_id: str, sequence_id: str, step_id: str) -> bool:
        """Link content to a sequence step"""
        query = """
        MATCH (c:Content {id: $content_id})
        CREATE (link:ContentSequenceLink {
            id: $link_id,
            content_id: $content_id,
            sequence_id: $sequence_id,
            step_id: $step_id,
            created_at: $created_at
        })
        CREATE (c)-[:LINKED_TO_SEQUENCE]->(link)
        RETURN link
        """

        result = self.session.run(query, {
            "link_id": str(uuid4()),
            "content_id": content_id,
            "sequence_id": sequence_id,
            "step_id": step_id,
            "created_at": datetime.utcnow().isoformat(),
        }).single()

        return result is not None

    def get_content_for_sequences(
        self,
        content_type: ContentType | None = None,
        limit: int = 50,
    ) -> list[Content]:
        """Get publishable content that can be linked to sequences"""
        conditions = ["c.status IN ['approved', 'published']"]
        params = {"limit": limit}

        if content_type:
            conditions.append("c.content_type = $content_type")
            params["content_type"] = content_type.value

        where_clause = f"WHERE {' AND '.join(conditions)}"

        query = f"""
        MATCH (c:Content)
        {where_clause}
        RETURN c
        ORDER BY c.updated_at DESC
        LIMIT $limit
        """

        results = self.session.run(query, params).data()
        return [self._build_content_from_neo4j(dict(r["c"])) for r in results]

    # ========================================================================
    # ANALYTICS
    # ========================================================================

    def get_marketing_analytics(self) -> MarketingAnalytics:
        """Get marketing analytics overview"""
        # Total content
        total_query = """
        MATCH (c:Content)
        RETURN count(c) as total
        """
        total_result = self.session.run(total_query).single()
        total_content = total_result["total"] if total_result else 0

        # Content by type
        type_query = """
        MATCH (c:Content)
        RETURN c.content_type as type, count(c) as count
        """
        type_results = self.session.run(type_query).data()
        content_by_type = {r["type"]: r["count"] for r in type_results}

        # Content by status
        status_query = """
        MATCH (c:Content)
        RETURN c.status as status, count(c) as count
        """
        status_results = self.session.run(status_query).data()
        content_by_status = {r["status"]: r["count"] for r in status_results}

        # Active campaigns
        campaign_query = """
        MATCH (camp:Campaign {status: 'active'})
        RETURN count(camp) as count
        """
        campaign_result = self.session.run(campaign_query).single()
        active_campaigns = campaign_result["count"] if campaign_result else 0

        return MarketingAnalytics(
            total_content=total_content,
            content_by_type=content_by_type,
            content_by_status=content_by_status,
            active_campaigns=active_campaigns,
            # Additional metrics would be calculated from actual data
            total_impressions=0,
            total_engagement=0,
            avg_engagement_rate=0.0,
            top_performing=[],
            campaign_performance=[],
            content_created_trend=[],
            engagement_trend=[],
        )

    def get_content_analytics(self, content_id: str) -> dict:
        """Get analytics for specific content"""
        query = """
        MATCH (c:Content {id: $id})
        RETURN c
        """

        result = self.session.run(query, {"id": content_id}).single()
        if not result:
            return {}

        content_data = dict(result["c"])

        # Return analytics based on content type
        return {
            "content_id": content_id,
            "content_type": content_data.get("content_type"),
            "views": content_data.get("views", 0),
            "impressions": content_data.get("impressions", 0),
            "engagement": content_data.get("engagement", 0),
            "engagement_rate": content_data.get("engagement_rate", 0.0),
            "clicks": content_data.get("clicks", 0),
            "conversions": content_data.get("conversions", 0),
        }

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _build_content_object(self, base_data: dict, type_specific: dict) -> Content:
        """Build appropriate content object based on type"""
        content_type = ContentType(base_data["content_type"])

        if content_type == ContentType.LINKEDIN_POST:
            return LinkedInPost(
                **base_data,
                linkedin=LinkedInPostContent(**type_specific) if type_specific else LinkedInPostContent(body=""),
            )
        elif content_type == ContentType.ARTICLE:
            return Article(
                **base_data,
                article=ArticleContent(**type_specific) if type_specific else ArticleContent(body=""),
            )
        elif content_type == ContentType.LANDING_PAGE:
            return LandingPage(
                **base_data,
                landing_page=LandingPageContent(**type_specific) if type_specific else LandingPageContent(headline=""),
                slug=type_specific.get("slug", ""),
            )
        elif content_type == ContentType.ABM_CONTENT:
            return ABMContent(
                **base_data,
                abm=ABMContentData(**type_specific) if type_specific else ABMContentData(base_headline="", base_body=""),
            )
        elif content_type == ContentType.CASE_STUDY:
            return CaseStudy(
                **base_data,
                case_study=CaseStudyContent(**type_specific) if type_specific else CaseStudyContent(
                    customer_name="",
                    challenge="",
                    solution="",
                    results="",
                ),
            )

        return Content(**base_data)

    def _build_content_from_neo4j(self, data: dict) -> Content:
        """Build content object from Neo4j data"""
        # Parse type_specific if stored as string
        type_specific = {}
        if "type_specific" in data:
            try:
                import ast
                type_specific = ast.literal_eval(data["type_specific"])
            except (ValueError, SyntaxError):
                type_specific = {}

        base_data = {
            "id": data.get("id"),
            "title": data.get("title"),
            "content_type": data.get("content_type"),
            "status": data.get("status"),
            "category": data.get("category"),
            "tags": data.get("tags", []),
            "target_personas": data.get("target_personas", []),
            "target_industries": data.get("target_industries", []),
            "target_accounts": data.get("target_accounts", []),
            "campaign_id": data.get("campaign_id"),
            "author_id": data.get("author_id"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
            "published_at": data.get("published_at"),
        }

        return self._build_content_object(base_data, type_specific)

    def _build_campaign_from_neo4j(self, data: dict) -> Campaign:
        """Build campaign object from Neo4j data"""
        return Campaign(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            status=CampaignStatus(data.get("status", "planning")),
            start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]) if data.get("end_date") else None,
            target_accounts=data.get("target_accounts", []),
            target_personas=[PersonaType(p) for p in data.get("target_personas", [])],
            target_industries=data.get("target_industries", []),
            content_ids=data.get("content_ids", []),
            budget=data.get("budget"),
            spent=data.get("spent", 0.0),
            goal_type=data.get("goal_type"),
            goal_value=data.get("goal_value"),
            current_value=data.get("current_value", 0.0),
            total_impressions=data.get("total_impressions", 0),
            total_engagement=data.get("total_engagement", 0),
            total_leads=data.get("total_leads", 0),
            total_conversions=data.get("total_conversions", 0),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
            created_by=data.get("created_by"),
        )
