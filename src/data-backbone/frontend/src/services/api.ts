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
}

export const api = new ApiClient();

// Re-export types for convenience
export type { Company, Employee, Deal, DealStage, OutreachSequence, HotAccount, ConnectorConfig };
