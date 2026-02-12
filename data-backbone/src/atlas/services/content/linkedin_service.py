"""
LinkedIn Service

Specialized service for LinkedIn content management including:
- Post scheduling
- Analytics tracking
- Hashtag suggestions
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from neo4j import Session

from atlas.api.models.content import (
    Content,
    ContentStatus,
    ContentType,
    LinkedInPost,
    LinkedInPostContent,
    HashtagSuggestionResponse,
)


# Default popular hashtags by industry/topic
DEFAULT_HASHTAGS = {
    "general": ["#business", "#innovation", "#leadership", "#growth", "#success"],
    "technology": ["#tech", "#digital", "#AI", "#innovation", "#software"],
    "marketing": ["#marketing", "#digitalmarketing", "#contentmarketing", "#branding", "#socialmedia"],
    "sales": ["#sales", "#b2b", "#revenue", "#pipeline", "#closing"],
    "sustainability": ["#sustainability", "#ESG", "#green", "#climateaction", "#sustainable"],
    "workplace": ["#workplace", "#futureofwork", "#remotework", "#hybrid", "#officedesign"],
    "leadership": ["#leadership", "#management", "#CEO", "#executive", "#leadershipdevelopment"],
}

# Trending hashtags (would be updated from real data in production)
TRENDING_HASHTAGS = ["#AI", "#2024", "#innovation", "#leadership", "#sustainability"]


class LinkedInService:
    """Service for LinkedIn-specific functionality"""

    def __init__(self, neo4j_session: Session):
        """Initialize the LinkedIn service"""
        self.session = neo4j_session

    # ========================================================================
    # POST SCHEDULING
    # ========================================================================

    def schedule_post(
        self,
        content_id: str,
        scheduled_time: datetime,
        timezone: str = "Europe/Amsterdam",
    ) -> LinkedInPost | None:
        """Schedule a LinkedIn post for publishing"""
        query = """
        MATCH (c:Content {id: $id, content_type: 'linkedin_post'})
        SET c.scheduled_time = $scheduled_time,
            c.timezone = $timezone,
            c.status = $status,
            c.updated_at = $updated_at
        RETURN c
        """

        result = self.session.run(query, {
            "id": content_id,
            "scheduled_time": scheduled_time.isoformat(),
            "timezone": timezone,
            "status": ContentStatus.SCHEDULED.value,
            "updated_at": datetime.utcnow().isoformat(),
        }).single()

        if not result:
            return None

        return self._build_linkedin_post(dict(result["c"]))

    def unschedule_post(self, content_id: str) -> LinkedInPost | None:
        """Remove scheduling from a post"""
        query = """
        MATCH (c:Content {id: $id, content_type: 'linkedin_post'})
        SET c.scheduled_time = null,
            c.status = $status,
            c.updated_at = $updated_at
        RETURN c
        """

        result = self.session.run(query, {
            "id": content_id,
            "status": ContentStatus.APPROVED.value,
            "updated_at": datetime.utcnow().isoformat(),
        }).single()

        if not result:
            return None

        return self._build_linkedin_post(dict(result["c"]))

    def get_scheduled_posts(
        self,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        limit: int = 50,
    ) -> list[LinkedInPost]:
        """Get scheduled LinkedIn posts"""
        conditions = [
            "c.content_type = 'linkedin_post'",
            "c.status = 'scheduled'",
        ]
        params = {"limit": limit}

        if from_date:
            conditions.append("c.scheduled_time >= $from_date")
            params["from_date"] = from_date.isoformat()
        if to_date:
            conditions.append("c.scheduled_time <= $to_date")
            params["to_date"] = to_date.isoformat()

        where_clause = f"WHERE {' AND '.join(conditions)}"

        query = f"""
        MATCH (c:Content)
        {where_clause}
        RETURN c
        ORDER BY c.scheduled_time ASC
        LIMIT $limit
        """

        results = self.session.run(query, params).data()
        return [self._build_linkedin_post(dict(r["c"])) for r in results]

    def get_posts_due_for_publishing(self) -> list[LinkedInPost]:
        """Get posts that are due to be published"""
        now = datetime.utcnow()

        query = """
        MATCH (c:Content)
        WHERE c.content_type = 'linkedin_post'
        AND c.status = 'scheduled'
        AND c.scheduled_time <= $now
        RETURN c
        ORDER BY c.scheduled_time ASC
        """

        results = self.session.run(query, {"now": now.isoformat()}).data()
        return [self._build_linkedin_post(dict(r["c"])) for r in results]

    def mark_as_published(self, content_id: str) -> LinkedInPost | None:
        """Mark a post as published"""
        now = datetime.utcnow()

        query = """
        MATCH (c:Content {id: $id, content_type: 'linkedin_post'})
        SET c.status = $status,
            c.published_at = $published_at,
            c.updated_at = $updated_at
        RETURN c
        """

        result = self.session.run(query, {
            "id": content_id,
            "status": ContentStatus.PUBLISHED.value,
            "published_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }).single()

        if not result:
            return None

        return self._build_linkedin_post(dict(result["c"]))

    # ========================================================================
    # HASHTAG SUGGESTIONS
    # ========================================================================

    def suggest_hashtags(
        self,
        content: str,
        industry: str | None = None,
        count: int = 5,
    ) -> HashtagSuggestionResponse:
        """Suggest hashtags based on content"""
        content_lower = content.lower()

        # Determine categories based on content
        suggested = set()

        # Check for keywords and add relevant hashtags
        keyword_mappings = {
            "ai": ["#AI", "#artificialintelligence", "#machinelearning"],
            "artificial intelligence": ["#AI", "#artificialintelligence", "#machinelearning"],
            "sustainability": ["#sustainability", "#ESG", "#green", "#climateaction"],
            "green": ["#sustainability", "#green", "#eco"],
            "leadership": ["#leadership", "#management", "#executive"],
            "marketing": ["#marketing", "#digitalmarketing", "#growth"],
            "sales": ["#sales", "#b2b", "#revenue"],
            "innovation": ["#innovation", "#tech", "#digital"],
            "workplace": ["#workplace", "#futureofwork", "#office"],
            "remote": ["#remotework", "#hybrid", "#futureofwork"],
            "growth": ["#growth", "#business", "#success"],
        }

        for keyword, hashtags in keyword_mappings.items():
            if keyword in content_lower:
                suggested.update(hashtags)

        # Add industry-specific hashtags
        if industry and industry.lower() in DEFAULT_HASHTAGS:
            suggested.update(DEFAULT_HASHTAGS[industry.lower()])
        else:
            suggested.update(DEFAULT_HASHTAGS["general"])

        # Convert to list and limit
        suggested_list = list(suggested)[:count]

        # Fill remaining slots with general hashtags if needed
        if len(suggested_list) < count:
            for tag in DEFAULT_HASHTAGS["general"]:
                if tag not in suggested_list:
                    suggested_list.append(tag)
                    if len(suggested_list) >= count:
                        break

        return HashtagSuggestionResponse(
            hashtags=suggested_list[:count],
            trending=TRENDING_HASHTAGS[:3],
        )

    # ========================================================================
    # ANALYTICS
    # ========================================================================

    def update_post_analytics(
        self,
        content_id: str,
        impressions: int | None = None,
        reactions: int | None = None,
        comments: int | None = None,
        shares: int | None = None,
        clicks: int | None = None,
    ) -> LinkedInPost | None:
        """Update analytics for a LinkedIn post"""
        updates = {"updated_at": datetime.utcnow().isoformat()}

        if impressions is not None:
            updates["impressions"] = impressions
        if reactions is not None:
            updates["reactions"] = reactions
        if comments is not None:
            updates["comments"] = comments
        if shares is not None:
            updates["shares"] = shares
        if clicks is not None:
            updates["clicks"] = clicks

        # Calculate engagement rate
        if impressions and impressions > 0:
            total_engagement = (reactions or 0) + (comments or 0) + (shares or 0) + (clicks or 0)
            updates["engagement_rate"] = (total_engagement / impressions) * 100

        set_clauses = [f"c.{k} = ${k}" for k in updates.keys()]
        set_clause = ", ".join(set_clauses)

        query = f"""
        MATCH (c:Content {{id: $id, content_type: 'linkedin_post'}})
        SET {set_clause}
        RETURN c
        """

        result = self.session.run(query, {"id": content_id, **updates}).single()
        if not result:
            return None

        return self._build_linkedin_post(dict(result["c"]))

    def get_linkedin_analytics(
        self,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> dict:
        """Get aggregated LinkedIn analytics"""
        conditions = [
            "c.content_type = 'linkedin_post'",
            "c.status = 'published'",
        ]
        params = {}

        if from_date:
            conditions.append("c.published_at >= $from_date")
            params["from_date"] = from_date.isoformat()
        if to_date:
            conditions.append("c.published_at <= $to_date")
            params["to_date"] = to_date.isoformat()

        where_clause = f"WHERE {' AND '.join(conditions)}"

        query = f"""
        MATCH (c:Content)
        {where_clause}
        RETURN
            count(c) as total_posts,
            sum(c.impressions) as total_impressions,
            sum(c.reactions) as total_reactions,
            sum(c.comments) as total_comments,
            sum(c.shares) as total_shares,
            sum(c.clicks) as total_clicks,
            avg(c.engagement_rate) as avg_engagement_rate
        """

        result = self.session.run(query, params).single()
        if not result:
            return {
                "total_posts": 0,
                "total_impressions": 0,
                "total_reactions": 0,
                "total_comments": 0,
                "total_shares": 0,
                "total_clicks": 0,
                "avg_engagement_rate": 0.0,
            }

        return {
            "total_posts": result["total_posts"] or 0,
            "total_impressions": result["total_impressions"] or 0,
            "total_reactions": result["total_reactions"] or 0,
            "total_comments": result["total_comments"] or 0,
            "total_shares": result["total_shares"] or 0,
            "total_clicks": result["total_clicks"] or 0,
            "avg_engagement_rate": result["avg_engagement_rate"] or 0.0,
        }

    def get_top_performing_posts(self, limit: int = 5) -> list[LinkedInPost]:
        """Get top performing LinkedIn posts by engagement"""
        query = """
        MATCH (c:Content)
        WHERE c.content_type = 'linkedin_post' AND c.status = 'published'
        RETURN c
        ORDER BY c.engagement_rate DESC, c.impressions DESC
        LIMIT $limit
        """

        results = self.session.run(query, {"limit": limit}).data()
        return [self._build_linkedin_post(dict(r["c"])) for r in results]

    # ========================================================================
    # CHARACTER COUNT & VALIDATION
    # ========================================================================

    def validate_post(self, content: LinkedInPostContent) -> dict:
        """Validate LinkedIn post content"""
        errors = []
        warnings = []

        # Character limit
        if len(content.body) > 3000:
            errors.append(f"Post body exceeds 3000 character limit ({len(content.body)} characters)")
        elif len(content.body) > 2500:
            warnings.append("Post is getting long - consider shortening for better engagement")

        # Hashtag recommendations
        if len(content.hashtags) > 5:
            warnings.append("More than 5 hashtags may reduce reach")
        elif len(content.hashtags) == 0:
            warnings.append("Consider adding 2-5 relevant hashtags")

        # Link check
        if content.link_url and content.image_url:
            warnings.append("Posts with both images and links may have the image take precedence")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "character_count": len(content.body),
            "characters_remaining": 3000 - len(content.body),
            "hashtag_count": len(content.hashtags),
        }

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _build_linkedin_post(self, data: dict) -> LinkedInPost:
        """Build LinkedInPost from Neo4j data"""
        # Parse type_specific if stored as string
        type_specific = {}
        if "type_specific" in data:
            try:
                import ast
                type_specific = ast.literal_eval(data["type_specific"])
            except (ValueError, SyntaxError):
                type_specific = {}

        return LinkedInPost(
            id=data.get("id"),
            title=data.get("title", ""),
            content_type=ContentType.LINKEDIN_POST,
            status=ContentStatus(data.get("status", "draft")),
            category=data.get("category"),
            tags=data.get("tags", []),
            target_personas=data.get("target_personas", []),
            target_industries=data.get("target_industries", []),
            target_accounts=data.get("target_accounts", []),
            campaign_id=data.get("campaign_id"),
            author_id=data.get("author_id"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
            published_at=datetime.fromisoformat(data["published_at"]) if data.get("published_at") else None,
            linkedin=LinkedInPostContent(
                body=type_specific.get("body", data.get("body", "")),
                hashtags=type_specific.get("hashtags", data.get("hashtags", [])),
                mentions=type_specific.get("mentions", data.get("mentions", [])),
                image_url=type_specific.get("image_url", data.get("image_url")),
                video_url=type_specific.get("video_url", data.get("video_url")),
                link_url=type_specific.get("link_url", data.get("link_url")),
                call_to_action=type_specific.get("call_to_action", data.get("call_to_action")),
            ),
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]) if data.get("scheduled_time") else None,
            timezone=data.get("timezone", "Europe/Amsterdam"),
            impressions=data.get("impressions", 0),
            reactions=data.get("reactions", 0),
            comments=data.get("comments", 0),
            shares=data.get("shares", 0),
            clicks=data.get("clicks", 0),
            engagement_rate=data.get("engagement_rate", 0.0),
        )
