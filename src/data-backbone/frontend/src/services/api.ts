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
    return this.fetch('/analytics/departments');
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
    return this.fetch('/deals');
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
    return this.fetch('/deals/pipeline-stats');
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
    return this.fetch(`/signals/hot-accounts?min_score=${minScore}&limit=${limit}`);
  }

  async getSignalStats(days: number = 30) {
    return this.fetch(`/signals/stats?days=${days}`);
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
    return this.fetch('/sequences');
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
    return this.fetch(`/leads?limit=${limit}`);
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
    return this.fetch('/analytics/bowtie');
  }

  async getConversionFunnel() {
    return this.fetch('/analytics/funnel');
  }
}

export const api = new ApiClient();

// Re-export types for convenience
export type { Company, Employee, Deal, DealStage, OutreachSequence, HotAccount };
