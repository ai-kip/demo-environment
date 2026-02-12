import type {
  Company,
  Employee,
  Deal,
  DealStage,
  DealPipelineStats,
  OutreachSequence,
  HotAccount,
  AttributionJourney,
  CompanyWithPeople,
  DealWithDetails,
  SequenceWithEnrollments,
} from '../types/database';

// Connector types
export interface ConnectorConfig {
  id: string;
  name: string;
  type: string;
  auth_type: string;
  auth_fields: string[];
  base_url: string;
  rate_limit: number;
  rate_limit_window: number;
  supports_search: boolean;
  supports_enrich: boolean;
  supports_people: boolean;
  supports_webhook: boolean;
  docs_url: string;
  icon: string;
  description: string;
}

const API_BASE = import.meta.env.DEV ? '/api' : 'http://localhost:8000';

class ApiClient {
  private async fetch<T = unknown>(endpoint: string, options?: RequestInit): Promise<T> {
    const separator = endpoint.includes('?') ? '&' : '?';
    const cacheBuster = `_t=${Date.now()}`;
    const url = `${API_BASE}${endpoint}${separator}${cacheBuster}`;
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0',
          ...options?.headers,
        },
        cache: 'no-store',
        ...options,
      });

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const json = await response.json();
        if (!response.ok) {
          throw new Error(json.message || json.error || `API Error: ${response.status} ${response.statusText}`);
        }
        return json as T;
      } else {
        if (!response.ok) {
          const text = await response.text();
          throw new Error(`API Error: ${response.status} ${response.statusText} - ${text.substring(0, 100)}`);
        }
        const text = await response.text();
        throw new Error(`Unexpected response format: ${text.substring(0, 100)}`);
      }
    } catch (err) {
      if (err instanceof TypeError && (err.message.includes('Failed to fetch') || err.message.includes('ECONNREFUSED'))) {
        throw new Error('Cannot connect to API. Is backend running on http://localhost:8000?');
      }
      if (err instanceof Error) {
        throw err;
      }
      throw new Error('Unknown error occurred');
    }
  }

  async healthCheck() {
    return this.fetch('/healthz');
  }

  async getIndustryAnalytics() {
    return this.fetch('/analytics/industries');
  }

  async getDepartmentAnalytics() {
    try {
      return await this.fetch('/analytics/departments');
    } catch {
      return []; // Return empty array if endpoint doesn't exist
    }
  }

  async getCompaniesByIndustry(industry: string) {
    return this.fetch(`/companies/by-industry?industry=${encodeURIComponent(industry)}`);
  }

  async getCompaniesByLocation(location: string) {
    return this.fetch(`/companies/by-location?location=${encodeURIComponent(location)}`);
  }

  async getCompanyByDomain(domain: string) {
    return this.fetch(`/companies?domain=${encodeURIComponent(domain)}`);
  }

  async semanticSearch(query: string, types: string = 'company,person', limit: number = 10) {
    return this.fetch(`/search?q=${encodeURIComponent(query)}&types=${encodeURIComponent(types)}&k=${limit}`);
  }

  async hybridSearch(query: string, limit: number = 5, depth: number = 1) {
    return this.fetch(`/search/hybrid?q=${encodeURIComponent(query)}&k=${limit}&depth=${depth}`);
  }

  async getPeopleByDepartment(department: string) {
    return this.fetch(`/people/by-department?department=${encodeURIComponent(department)}`);
  }

  async searchPeople(query: string) {
    return this.fetch(`/people?q=${encodeURIComponent(query)}`);
  }

  async getNeighbors(id: string, depth: number = 2) {
    return this.fetch(`/neighbors?id=${encodeURIComponent(id)}&depth=${depth}`);
  }

  async ingestCompanies(
    query: string,
    limit: number = 10,
    useGoogle: boolean = true,
    useHunter: boolean = false,
    loadToNeo4j: boolean = true,
    loadToQdrant: boolean = true
  ) {
    return this.fetch('/ingest', {
      method: 'POST',
      body: JSON.stringify({
        query,
        limit,
        use_google: useGoogle,
        use_hunter: useHunter,
        load_to_neo4j: loadToNeo4j,
        load_to_qdrant: loadToQdrant,
      }),
    });
  }

  async clearAllData() {
    return this.fetch('/clear', {
      method: 'POST',
    });
  }

  // ============================================================================
  // COMPANY ENDPOINTS
  // ============================================================================

  async getCompanyById(id: string): Promise<CompanyWithPeople> {
    return this.fetch(`/companies/${encodeURIComponent(id)}`);
  }

  async getCompanyRelationships(companyId: string) {
    return this.fetch(`/companies/${encodeURIComponent(companyId)}/relationships`);
  }

  // ============================================================================
  // DEAL ENDPOINTS (MEDDPICC)
  // ============================================================================

  async getDeals(): Promise<Array<{ deal: Deal; company: { id: string; name: string; domain: string }; owner_name?: string; champion_name?: string }>> {
    try {
      return await this.fetch('/deals');
    } catch {
      return []; // Return empty array if endpoint doesn't exist
    }
  }

  async getDealById(id: string): Promise<DealWithDetails> {
    return this.fetch(`/deals/${encodeURIComponent(id)}`);
  }

  async getDealsByCompany(companyId: string): Promise<Array<{ deal: Deal; owner_name?: string }>> {
    return this.fetch(`/deals/by-company/${encodeURIComponent(companyId)}`);
  }

  async getDealsByStage(stage: DealStage): Promise<Array<{ deal: Deal; company: { id: string; name: string }; owner_name?: string }>> {
    return this.fetch(`/deals/by-stage/${encodeURIComponent(stage)}`);
  }

  async getDealPipelineStats(): Promise<DealPipelineStats[]> {
    try {
      return await this.fetch('/deals/pipeline-stats');
    } catch {
      return []; // Return empty array if endpoint doesn't exist
    }
  }

  async createDeal(deal: Partial<Deal>): Promise<{ success: boolean; deal_id: string }> {
    return this.fetch('/deals', {
      method: 'POST',
      body: JSON.stringify(deal),
    });
  }

  async updateDeal(id: string, updates: Partial<Deal>): Promise<{ success: boolean }> {
    return this.fetch(`/deals/${encodeURIComponent(id)}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  }

  async updateDealStage(id: string, stage: DealStage): Promise<{ success: boolean }> {
    return this.fetch(`/deals/${encodeURIComponent(id)}/stage`, {
      method: 'PATCH',
      body: JSON.stringify({ stage }),
    });
  }

  // ============================================================================
  // SIGNAL ENDPOINTS
  // ============================================================================

  async getSignalsByCompany(companyId: string, limit: number = 20) {
    return this.fetch(`/signals/company/${encodeURIComponent(companyId)}?limit=${limit}`);
  }

  async getHotAccounts(minScore: number = 70, limit: number = 20): Promise<HotAccount[]> {
    try {
      return await this.fetch(`/signals/hot-accounts?min_score=${minScore}&limit=${limit}`);
    } catch {
      return []; // Return empty array if endpoint doesn't exist
    }
  }

  async getSignalStats(days: number = 30) {
    try {
      return await this.fetch(`/signals/stats?days=${days}`);
    } catch {
      return null; // Return null if endpoint doesn't exist
    }
  }

  // ============================================================================
  // OUTREACH & SEQUENCE ENDPOINTS
  // ============================================================================

  async getSequences(): Promise<Array<{
    sequence: OutreachSequence;
    created_by?: string;
    enrolled_count: number;
    replied_count: number;
    meetings_count: number;
    reply_rate: number;
  }>> {
    try {
      return await this.fetch('/sequences');
    } catch {
      return []; // Return empty array if endpoint doesn't exist
    }
  }

  async getSequenceById(id: string): Promise<SequenceWithEnrollments> {
    return this.fetch(`/sequences/${encodeURIComponent(id)}`);
  }

  async getSequenceEnrollments(sequenceId: string) {
    return this.fetch(`/sequences/${encodeURIComponent(sequenceId)}/enrollments`);
  }

  async createSequence(sequence: Partial<OutreachSequence>): Promise<{ success: boolean; sequence_id: string }> {
    return this.fetch('/sequences', {
      method: 'POST',
      body: JSON.stringify(sequence),
    });
  }

  async enrollInSequence(sequenceId: string, employeeId: string, companyId: string): Promise<{ success: boolean; enrollment_id: string }> {
    return this.fetch(`/sequences/${encodeURIComponent(sequenceId)}/enroll`, {
      method: 'POST',
      body: JSON.stringify({ employee_id: employeeId, company_id: companyId }),
    });
  }

  // ============================================================================
  // ATTRIBUTION ENDPOINTS
  // ============================================================================

  async getTouchpointsByDeal(dealId: string) {
    return this.fetch(`/attribution/deal/${encodeURIComponent(dealId)}`);
  }

  async getCampaignAttribution() {
    return this.fetch('/attribution/campaigns');
  }

  async getAttributionJourney(companyId: string): Promise<AttributionJourney[]> {
    return this.fetch(`/attribution/journey/${encodeURIComponent(companyId)}`);
  }

  // ============================================================================
  // LEAD ENDPOINTS
  // ============================================================================

  async getLeads(limit: number = 50) {
    try {
      return await this.fetch(`/leads?limit=${limit}`);
    } catch {
      return []; // Return empty array if endpoint doesn't exist
    }
  }

  async updateLeadStatus(companyId: string, status: string): Promise<{ success: boolean }> {
    return this.fetch(`/leads/${encodeURIComponent(companyId)}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
  }

  // ============================================================================
  // ANALYTICS ENDPOINTS
  // ============================================================================

  async getBowtieMetrics() {
    try {
      return await this.fetch('/analytics/bowtie');
    } catch {
      return null; // Return null if endpoint doesn't exist
    }
  }

  async getConversionFunnel() {
    try {
      return await this.fetch('/analytics/funnel');
    } catch {
      return null; // Return null if endpoint doesn't exist
    }
  }

  // ============================================================================
  // CONNECTOR ENDPOINTS
  // ============================================================================

  async getConnectorRegistry(): Promise<{ connectors: ConnectorConfig[]; count: number }> {
    return this.fetch('/connectors/registry');
  }

  async getConnectorInfo(connectorId: string): Promise<ConnectorConfig> {
    return this.fetch(`/connectors/registry/${encodeURIComponent(connectorId)}`);
  }

  async testConnectorConnection(
    connectorId: string,
    authConfig: Record<string, string>
  ): Promise<{ status: string; message: string; rate_limit?: Record<string, unknown> }> {
    return this.fetch('/connectors/test', {
      method: 'POST',
      body: JSON.stringify({
        connector_id: connectorId,
        auth_config: authConfig,
      }),
    });
  }

  async searchWithConnector(
    connectorId: string,
    authConfig: Record<string, string>,
    query: string,
    limit: number = 20,
    filters?: Record<string, unknown>
  ) {
    return this.fetch('/connectors/search', {
      method: 'POST',
      body: JSON.stringify({
        connector_id: connectorId,
        auth_config: authConfig,
        query,
        limit,
        filters,
      }),
    });
  }

  async enrichWithConnector(
    connectorId: string,
    authConfig: Record<string, string>,
    domain?: string,
    kvkNumber?: string,
    linkedinUrl?: string
  ) {
    return this.fetch('/connectors/enrich', {
      method: 'POST',
      body: JSON.stringify({
        connector_id: connectorId,
        auth_config: authConfig,
        domain,
        kvk_number: kvkNumber,
        linkedin_url: linkedinUrl,
      }),
    });
  }

  async findPeopleWithConnector(
    connectorId: string,
    authConfig: Record<string, string>,
    domain: string,
    limit: number = 50,
    titles?: string[],
    seniorities?: string[]
  ) {
    return this.fetch('/connectors/people', {
      method: 'POST',
      body: JSON.stringify({
        connector_id: connectorId,
        auth_config: authConfig,
        domain,
        limit,
        titles,
        seniorities,
      }),
    });
  }

  async previewFile(file: File, sheetName?: string) {
    const formData = new FormData();
    formData.append('file', file);
    if (sheetName) formData.append('sheet_name', sheetName);

    const response = await fetch(`${API_BASE}/connectors/file/preview`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to preview file');
    }

    return response.json();
  }

  async importFile(
    file: File,
    columnMapping: Record<string, string>,
    recordType: 'company' | 'contact' = 'company',
    skipRows: number = 0,
    sheetName?: string
  ) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('column_mapping', JSON.stringify(columnMapping));
    formData.append('record_type', recordType);
    formData.append('skip_rows', skipRows.toString());
    if (sheetName) formData.append('sheet_name', sheetName);

    const response = await fetch(`${API_BASE}/connectors/file/import`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to import file');
    }

    return response.json();
  }

  async verifyEmail(apiKey: string, email: string) {
    return this.fetch('/connectors/email/verify', {
      method: 'POST',
      body: JSON.stringify({ api_key: apiKey, email }),
    });
  }

  async findEmail(apiKey: string, domain: string, firstName: string, lastName: string) {
    return this.fetch('/connectors/email/find', {
      method: 'POST',
      body: JSON.stringify({
        api_key: apiKey,
        domain,
        first_name: firstName,
        last_name: lastName,
      }),
    });
  }

  // ============================================================================
  // NEW DATA API ENDPOINTS (with synthetic data)
  // ============================================================================

  async getDashboardMetrics(): Promise<{
    companies: number;
    contacts: number;
    open_deals: number;
    pipeline_value: number;
    unread_signals: number;
    upcoming_meetings: number;
    won_deals: number;
    won_value: number;
    activity_counts: Record<string, number>;
    currency: string;
  }> {
    return this.fetch('/api/dashboard/metrics');
  }

  async getActivityFeed(limit: number = 20): Promise<{
    activities: Array<{
      id: string;
      type: string;
      subject: string;
      description: string;
      performed_by: string;
      performed_at: string;
      deal_name: string;
      company_name: string;
    }>;
  }> {
    return this.fetch(`/api/dashboard/activity-feed?limit=${limit}`);
  }

  async getCompaniesData(params?: {
    industry?: string;
    country?: string;
    size?: string;
    limit?: number;
    offset?: number;
  }): Promise<{
    companies: Array<{
      id: string;
      name: string;
      industry: string;
      size: string;
      country: string;
      region: string;
      employee_count: number;
      annual_revenue: number;
      health_score: number;
      engagement_score: number;
      icp_fit_score: number;
      contact_count: number;
      deal_count: number;
    }>;
    total: number;
  }> {
    const searchParams = new URLSearchParams();
    if (params?.industry) searchParams.append('industry', params.industry);
    if (params?.country) searchParams.append('country', params.country);
    if (params?.size) searchParams.append('size', params.size);
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.offset) searchParams.append('offset', params.offset.toString());
    const query = searchParams.toString();
    return this.fetch(`/api/companies${query ? '?' + query : ''}`);
  }

  async getCompanyDetails(companyId: string): Promise<{
    id: string;
    name: string;
    industry: string;
    contacts: Array<{
      id: string;
      full_name: string;
      job_title: string;
      email: string;
      seniority: string;
    }>;
    deals: Array<{
      id: string;
      name: string;
      stage: string;
      value: number;
    }>;
    signals: Array<{
      id: string;
      title: string;
      type: string;
      impact: string;
    }>;
  }> {
    return this.fetch(`/api/companies/${encodeURIComponent(companyId)}`);
  }

  async getContactsData(params?: {
    company_id?: string;
    seniority?: string;
    limit?: number;
    offset?: number;
  }): Promise<{
    contacts: Array<{
      id: string;
      full_name: string;
      email: string;
      job_title: string;
      seniority: string;
      department: string;
      company_name: string;
      company_id: string;
      engagement_score: number;
    }>;
    total: number;
  }> {
    const searchParams = new URLSearchParams();
    if (params?.company_id) searchParams.append('company_id', params.company_id);
    if (params?.seniority) searchParams.append('seniority', params.seniority);
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.offset) searchParams.append('offset', params.offset.toString());
    const query = searchParams.toString();
    return this.fetch(`/api/contacts${query ? '?' + query : ''}`);
  }

  async getDealsData(params?: {
    stage?: string;
    company_id?: string;
    owner?: string;
    limit?: number;
    offset?: number;
  }): Promise<{
    deals: Array<{
      id: string;
      name: string;
      stage: string;
      value: number;
      probability: number;
      product: string;
      owner: string;
      company_name: string;
      company_id: string;
      expected_close_date: string;
      created_at: string;
    }>;
    total: number;
  }> {
    const searchParams = new URLSearchParams();
    if (params?.stage) searchParams.append('stage', params.stage);
    if (params?.company_id) searchParams.append('company_id', params.company_id);
    if (params?.owner) searchParams.append('owner', params.owner);
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.offset) searchParams.append('offset', params.offset.toString());
    const query = searchParams.toString();
    return this.fetch(`/api/deals${query ? '?' + query : ''}`);
  }

  async getPipelineStats(): Promise<{
    stages: Array<{
      stage: string;
      count: number;
      value: number;
    }>;
    total_count: number;
    total_value: number;
    weighted_value: number;
    currency: string;
  }> {
    return this.fetch('/api/deals/pipeline-stats');
  }

  async getDealDetails(dealId: string): Promise<{
    id: string;
    name: string;
    stage: string;
    value: number;
    company: {
      id: string;
      name: string;
    };
    primary_contact?: {
      id: string;
      full_name: string;
    };
    activities: Array<{
      id: string;
      type: string;
      subject: string;
      performed_at: string;
    }>;
  }> {
    return this.fetch(`/api/deals/${encodeURIComponent(dealId)}`);
  }

  async getSignalsData(params?: {
    signal_type?: string;
    impact?: string;
    company_id?: string;
    is_read?: boolean;
    limit?: number;
    offset?: number;
  }): Promise<{
    signals: Array<{
      id: string;
      title: string;
      description: string;
      type: string;
      category: string;
      impact: string;
      company_name: string;
      company_id: string;
      detected_at: string;
      is_read: boolean;
      confidence_score: number;
    }>;
    total: number;
  }> {
    const searchParams = new URLSearchParams();
    if (params?.signal_type) searchParams.append('signal_type', params.signal_type);
    if (params?.impact) searchParams.append('impact', params.impact);
    if (params?.company_id) searchParams.append('company_id', params.company_id);
    if (params?.is_read !== undefined) searchParams.append('is_read', params.is_read.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.offset) searchParams.append('offset', params.offset.toString());
    const query = searchParams.toString();
    return this.fetch(`/api/signals${query ? '?' + query : ''}`);
  }

  async getSignalsSummary(): Promise<{
    total: number;
    unread: number;
    by_type: Record<string, number>;
    by_impact: Record<string, number>;
  }> {
    return this.fetch('/api/signals/summary');
  }

  async getMeetingsData(upcoming_only: boolean = true, limit: number = 20): Promise<{
    meetings: Array<{
      id: string;
      title: string;
      start_time: string;
      end_time: string;
      location: string;
      company_name: string;
      company_id: string;
      deal_name?: string;
      prep_status: string;
      attendees: Array<{
        id: string;
        name: string;
        email: string;
      }>;
    }>;
    total: number;
  }> {
    return this.fetch(`/api/meetings?upcoming_only=${upcoming_only}&limit=${limit}`);
  }

  async searchData(q: string, entity_type?: string): Promise<{
    companies: Array<{ id: string; name: string; industry: string }>;
    contacts: Array<{ id: string; full_name: string; job_title: string; company_name: string }>;
    deals: Array<{ id: string; name: string; stage: string; company_name: string }>;
  }> {
    const searchParams = new URLSearchParams({ q });
    if (entity_type) searchParams.append('entity_type', entity_type);
    return this.fetch(`/api/search?${searchParams.toString()}`);
  }

  // ============================================================================
  // MARKETING CONTENT ENDPOINTS
  // ============================================================================

  async createContent(data: {
    content_type: string;
    title: string;
    category?: string;
    tags?: string[];
    linkedin?: Record<string, unknown>;
    article?: Record<string, unknown>;
    landing_page?: Record<string, unknown>;
    abm?: Record<string, unknown>;
    case_study?: Record<string, unknown>;
    target_personas?: string[];
    target_industries?: string[];
    target_accounts?: string[];
    campaign_id?: string;
  }): Promise<{ success: boolean; content: Record<string, unknown> }> {
    return this.fetch('/content', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getContentList(params?: {
    content_type?: string;
    status?: string;
    category?: string;
    campaign_id?: string;
    author_id?: string;
    search?: string;
    page?: number;
    page_size?: number;
  }): Promise<{
    items: Array<Record<string, unknown>>;
    total: number;
    page: number;
    page_size: number;
  }> {
    const searchParams = new URLSearchParams();
    if (params?.content_type) searchParams.append('content_type', params.content_type);
    if (params?.status) searchParams.append('status', params.status);
    if (params?.category) searchParams.append('category', params.category);
    if (params?.campaign_id) searchParams.append('campaign_id', params.campaign_id);
    if (params?.author_id) searchParams.append('author_id', params.author_id);
    if (params?.search) searchParams.append('search', params.search);
    if (params?.page) searchParams.append('page', params.page.toString());
    if (params?.page_size) searchParams.append('page_size', params.page_size.toString());
    const query = searchParams.toString();
    return this.fetch(`/content${query ? '?' + query : ''}`);
  }

  async getContent(contentId: string): Promise<Record<string, unknown>> {
    return this.fetch(`/content/${encodeURIComponent(contentId)}`);
  }

  async updateContent(contentId: string, data: Record<string, unknown>): Promise<{ success: boolean; content: Record<string, unknown> }> {
    return this.fetch(`/content/${encodeURIComponent(contentId)}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async deleteContent(contentId: string): Promise<{ success: boolean; message: string }> {
    return this.fetch(`/content/${encodeURIComponent(contentId)}`, {
      method: 'DELETE',
    });
  }

  // Content Workflow
  async submitContentForReview(contentId: string): Promise<{ success: boolean; content: Record<string, unknown> }> {
    return this.fetch(`/content/${encodeURIComponent(contentId)}/submit`, {
      method: 'POST',
    });
  }

  async approveContent(contentId: string): Promise<{ success: boolean; content: Record<string, unknown> }> {
    return this.fetch(`/content/${encodeURIComponent(contentId)}/approve`, {
      method: 'POST',
    });
  }

  async publishContent(contentId: string): Promise<{ success: boolean; content: Record<string, unknown> }> {
    return this.fetch(`/content/${encodeURIComponent(contentId)}/publish`, {
      method: 'POST',
    });
  }

  async archiveContent(contentId: string): Promise<{ success: boolean; content: Record<string, unknown> }> {
    return this.fetch(`/content/${encodeURIComponent(contentId)}/archive`, {
      method: 'POST',
    });
  }

  // LinkedIn
  async scheduleLinkedInPost(contentId: string, scheduledTime: string, timezone?: string): Promise<{
    success: boolean;
    message: string;
    post: Record<string, unknown>;
  }> {
    return this.fetch('/content/linkedin/schedule', {
      method: 'POST',
      body: JSON.stringify({
        content_id: contentId,
        scheduled_time: scheduledTime,
        timezone: timezone || 'Europe/Amsterdam',
      }),
    });
  }

  async unscheduleLinkedInPost(contentId: string): Promise<{ success: boolean; message: string }> {
    return this.fetch(`/content/linkedin/${encodeURIComponent(contentId)}/schedule`, {
      method: 'DELETE',
    });
  }

  async getScheduledLinkedInPosts(fromDate?: string, toDate?: string, limit?: number): Promise<{
    posts: Array<Record<string, unknown>>;
    count: number;
  }> {
    const searchParams = new URLSearchParams();
    if (fromDate) searchParams.append('from_date', fromDate);
    if (toDate) searchParams.append('to_date', toDate);
    if (limit) searchParams.append('limit', limit.toString());
    const query = searchParams.toString();
    return this.fetch(`/content/linkedin/scheduled${query ? '?' + query : ''}`);
  }

  async getLinkedInAnalytics(fromDate?: string, toDate?: string): Promise<{
    total_posts: number;
    total_impressions: number;
    total_reactions: number;
    total_comments: number;
    total_shares: number;
    total_clicks: number;
    avg_engagement_rate: number;
  }> {
    const searchParams = new URLSearchParams();
    if (fromDate) searchParams.append('from_date', fromDate);
    if (toDate) searchParams.append('to_date', toDate);
    const query = searchParams.toString();
    return this.fetch(`/content/linkedin/analytics${query ? '?' + query : ''}`);
  }

  async validateLinkedInPost(content: {
    body: string;
    hashtags?: string[];
  }): Promise<{
    valid: boolean;
    errors: string[];
    warnings: string[];
    character_count: number;
    characters_remaining: number;
    hashtag_count: number;
  }> {
    return this.fetch('/content/linkedin/validate', {
      method: 'POST',
      body: JSON.stringify(content),
    });
  }

  // AI Generation
  async generateContent(data: {
    content_type: string;
    prompt: string;
    tone?: string;
    target_audience?: string;
    key_points?: string[];
    max_length?: number;
  }): Promise<{
    success: boolean;
    content: Record<string, unknown>;
    tokens_used: number;
  }> {
    return this.fetch('/content/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async generateContentVariations(contentId: string, count?: number): Promise<{
    original_id: string;
    variations: Array<{
      variation_number: number;
      title: string;
      content: string;
    }>;
  }> {
    return this.fetch('/content/variations', {
      method: 'POST',
      body: JSON.stringify({ content_id: contentId, count: count || 3 }),
    });
  }

  async suggestHashtags(content: string, industry?: string, count?: number): Promise<{
    hashtags: string[];
    trending: string[];
  }> {
    return this.fetch('/content/hashtags', {
      method: 'POST',
      body: JSON.stringify({ content, industry, count: count || 5 }),
    });
  }

  // Sequence Integration
  async linkContentToSequence(contentId: string, sequenceId: string, stepId: string): Promise<{ success: boolean; message: string }> {
    return this.fetch('/content/link-sequence', {
      method: 'POST',
      body: JSON.stringify({
        content_id: contentId,
        sequence_id: sequenceId,
        step_id: stepId,
      }),
    });
  }

  async getContentForSequences(contentType?: string, limit?: number): Promise<{
    items: Array<Record<string, unknown>>;
    count: number;
  }> {
    const searchParams = new URLSearchParams();
    if (contentType) searchParams.append('content_type', contentType);
    if (limit) searchParams.append('limit', limit.toString());
    const query = searchParams.toString();
    return this.fetch(`/content/for-sequences${query ? '?' + query : ''}`);
  }

  // Campaigns
  async createCampaign(data: {
    name: string;
    description?: string;
    start_date?: string;
    end_date?: string;
    target_accounts?: string[];
    target_industries?: string[];
    budget?: number;
    goal_type?: string;
    goal_value?: number;
  }): Promise<{ success: boolean; campaign: Record<string, unknown> }> {
    return this.fetch('/content/campaigns', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getCampaigns(status?: string, page?: number, pageSize?: number): Promise<{
    campaigns: Array<Record<string, unknown>>;
    total: number;
    page: number;
    page_size: number;
  }> {
    const searchParams = new URLSearchParams();
    if (status) searchParams.append('status', status);
    if (page) searchParams.append('page', page.toString());
    if (pageSize) searchParams.append('page_size', pageSize.toString());
    const query = searchParams.toString();
    return this.fetch(`/content/campaigns${query ? '?' + query : ''}`);
  }

  async getCampaign(campaignId: string): Promise<Record<string, unknown>> {
    return this.fetch(`/content/campaigns/${encodeURIComponent(campaignId)}`);
  }

  async addContentToCampaign(campaignId: string, contentId: string): Promise<{ success: boolean; message: string }> {
    return this.fetch(`/content/campaigns/${encodeURIComponent(campaignId)}/content`, {
      method: 'POST',
      body: JSON.stringify({ content_id: contentId }),
    });
  }

  // Marketing Analytics
  async getMarketingAnalytics(): Promise<{
    total_content: number;
    content_by_type: Record<string, number>;
    content_by_status: Record<string, number>;
    total_impressions: number;
    total_engagement: number;
    avg_engagement_rate: number;
    top_performing: Array<Record<string, unknown>>;
    active_campaigns: number;
    campaign_performance: Array<Record<string, unknown>>;
    content_created_trend: Array<Record<string, unknown>>;
    engagement_trend: Array<Record<string, unknown>>;
  }> {
    return this.fetch('/content/analytics');
  }

  async getContentAnalytics(contentId: string): Promise<{
    content_id: string;
    content_type: string;
    views: number;
    impressions: number;
    engagement: number;
    engagement_rate: number;
    clicks: number;
    conversions: number;
  }> {
    return this.fetch(`/content/${encodeURIComponent(contentId)}/analytics`);
  }

  // Reference Data
  async getContentTypes(): Promise<Record<string, {
    label: string;
    description: string;
    max_length?: number;
    supports_scheduling: boolean;
    supports_seo?: boolean;
    supports_ab_testing?: boolean;
  }>> {
    return this.fetch('/content/types');
  }

  async getContentStatuses(): Promise<Record<string, {
    label: string;
    color: string;
  }>> {
    return this.fetch('/content/statuses');
  }

  async getContentCategories(): Promise<Record<string, {
    label: string;
    icon: string;
  }>> {
    return this.fetch('/content/categories');
  }
}

export const api = new ApiClient();

// Re-export types for convenience
export type { Company, Employee, Deal, DealStage, OutreachSequence, HotAccount, ConnectorConfig };
