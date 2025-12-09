import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Search,
  Filter,
  Bell,
  Star,
  TrendingUp,
  TrendingDown,
  Package,
  Building2,
  Globe,
  Calendar,
  Clock,
  ChevronRight,
  ExternalLink,
  Bookmark,
  BookmarkCheck,
  Phone,
  Mail,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Eye,
  BarChart3,
  Zap,
  Target,
  DollarSign,
  Factory,
  Truck,
  Users,
  Award,
  Briefcase,
  RefreshCw,
  Settings,
  MoreHorizontal,
} from 'lucide-react';

// iBood Signal Types based on spec
type SignalPriority = 'hot' | 'strategic' | 'market' | 'relationship';
type SignalStatus = 'new' | 'viewed' | 'actioned' | 'dismissed' | 'expired';
type CompanyStatus = 'new' | 'watching' | 'contacted' | 'active_supplier' | 'inactive';

// Signal type enum from spec
type IBoodSignalType =
  // Hot signals (immediate action)
  | 'inventory_surplus'
  | 'earnings_miss'
  | 'product_discontinuation'
  | 'warehouse_clearance'
  | 'leadership_change'
  | 'debt_pressure'
  // Strategic signals
  | 'european_market_entry'
  | 'new_factory'
  | 'product_launch_overrun'
  | 'seasonal_clearance'
  | 'retailer_delisting'
  | 'distribution_change'
  // Market signals
  | 'category_oversupply'
  | 'raw_material_price_drop'
  | 'competitor_bankruptcy'
  | 'trade_policy_change'
  | 'currency_shift'
  | 'shipping_cost_drop'
  // Relationship signals
  | 'trade_show_attendance'
  | 'new_product_announcement'
  | 'sustainability_initiative'
  | 'award_recognition'
  | 'new_sales_leader'
  | 'partnership_announcement';

// iBood product categories
type ProductCategory =
  | 'consumer_electronics'
  | 'home_appliances'
  | 'home_living'
  | 'garden_outdoor'
  | 'health_beauty'
  | 'sports_fitness'
  | 'fashion_accessories'
  | 'diy_tools'
  | 'household_nonfood';

interface IBoodSignal {
  id: string;
  company_id: string;
  company_name: string;
  company_logo?: string;
  company_country: string;
  signal_type: IBoodSignalType;
  signal_priority: SignalPriority;
  title: string;
  summary: string;
  confidence_score: number;
  deal_potential_score: number;
  source_url?: string;
  source_type: string;
  source_date: string;
  detected_at: string;
  expires_at?: string;
  status: SignalStatus;
  categories: ProductCategory[];
  evidence?: {
    quotes: string[];
    documents: string[];
  };
  estimated_value?: number;
  likely_discount_range?: string;
  competition_level?: 'low' | 'medium' | 'high';
  timing_recommendation?: string;
}

interface IBoodCompany {
  id: string;
  name: string;
  logo?: string;
  country: string;
  revenue_eur?: number;
  employees?: number;
  categories: ProductCategory[];
  status: CompanyStatus;
  active_signals: number;
  past_gmv?: number;
  has_contact: boolean;
  relationship_owner?: string;
  latest_signal?: string;
}

// Signal configuration
const SIGNAL_CONFIG: Record<IBoodSignalType, { label: string; icon: React.ReactNode; color: string; priority: SignalPriority }> = {
  // Hot signals
  inventory_surplus: { label: 'Inventory Surplus', icon: <Package size={16} />, color: '#EF4444', priority: 'hot' },
  earnings_miss: { label: 'Earnings Miss', icon: <TrendingDown size={16} />, color: '#EF4444', priority: 'hot' },
  product_discontinuation: { label: 'Product Discontinuation', icon: <XCircle size={16} />, color: '#EF4444', priority: 'hot' },
  warehouse_clearance: { label: 'Warehouse Clearance', icon: <Factory size={16} />, color: '#EF4444', priority: 'hot' },
  leadership_change: { label: 'CFO/CEO Change', icon: <Users size={16} />, color: '#EF4444', priority: 'hot' },
  debt_pressure: { label: 'Debt Covenant Pressure', icon: <AlertTriangle size={16} />, color: '#EF4444', priority: 'hot' },
  // Strategic signals
  european_market_entry: { label: 'European Market Entry', icon: <Globe size={16} />, color: '#F59E0B', priority: 'strategic' },
  new_factory: { label: 'New Factory Opening', icon: <Factory size={16} />, color: '#F59E0B', priority: 'strategic' },
  product_launch_overrun: { label: 'Product Launch Overrun', icon: <Package size={16} />, color: '#F59E0B', priority: 'strategic' },
  seasonal_clearance: { label: 'Seasonal Clearance', icon: <Calendar size={16} />, color: '#F59E0B', priority: 'strategic' },
  retailer_delisting: { label: 'Retailer Delisting', icon: <Building2 size={16} />, color: '#F59E0B', priority: 'strategic' },
  distribution_change: { label: 'Distribution Change', icon: <Truck size={16} />, color: '#F59E0B', priority: 'strategic' },
  // Market signals
  category_oversupply: { label: 'Category Oversupply', icon: <BarChart3 size={16} />, color: '#3B82F6', priority: 'market' },
  raw_material_price_drop: { label: 'Raw Material Price Drop', icon: <TrendingDown size={16} />, color: '#3B82F6', priority: 'market' },
  competitor_bankruptcy: { label: 'Competitor Bankruptcy', icon: <AlertTriangle size={16} />, color: '#3B82F6', priority: 'market' },
  trade_policy_change: { label: 'Trade Policy Change', icon: <Globe size={16} />, color: '#3B82F6', priority: 'market' },
  currency_shift: { label: 'Currency Shift', icon: <DollarSign size={16} />, color: '#3B82F6', priority: 'market' },
  shipping_cost_drop: { label: 'Shipping Cost Drop', icon: <Truck size={16} />, color: '#3B82F6', priority: 'market' },
  // Relationship signals
  trade_show_attendance: { label: 'Trade Show Attendance', icon: <Calendar size={16} />, color: '#10B981', priority: 'relationship' },
  new_product_announcement: { label: 'New Product Announcement', icon: <Zap size={16} />, color: '#10B981', priority: 'relationship' },
  sustainability_initiative: { label: 'Sustainability Initiative', icon: <Target size={16} />, color: '#10B981', priority: 'relationship' },
  award_recognition: { label: 'Award/Recognition', icon: <Award size={16} />, color: '#10B981', priority: 'relationship' },
  new_sales_leader: { label: 'New Sales Leader', icon: <Briefcase size={16} />, color: '#10B981', priority: 'relationship' },
  partnership_announcement: { label: 'Partnership Announcement', icon: <Users size={16} />, color: '#10B981', priority: 'relationship' },
};

const CATEGORY_LABELS: Record<ProductCategory, string> = {
  consumer_electronics: 'Consumer Electronics',
  home_appliances: 'Home Appliances',
  home_living: 'Home & Living',
  garden_outdoor: 'Garden & Outdoor',
  health_beauty: 'Health & Beauty',
  sports_fitness: 'Sports & Fitness',
  fashion_accessories: 'Fashion & Accessories',
  diy_tools: 'DIY & Tools',
  household_nonfood: 'Household & Non-Food',
};

const PRIORITY_CONFIG = {
  hot: { label: 'Hot', icon: '🔥', color: '#EF4444', bgColor: '#FEE2E2' },
  strategic: { label: 'Strategic', icon: '⭐', color: '#F59E0B', bgColor: '#FEF3C7' },
  market: { label: 'Market Intel', icon: '📊', color: '#3B82F6', bgColor: '#DBEAFE' },
  relationship: { label: 'Nurture', icon: '🤝', color: '#10B981', bgColor: '#D1FAE5' },
};

// Demo data
const createDemoSignals = (): IBoodSignal[] => [
  {
    id: 's1',
    company_id: 'c1',
    company_name: 'Philips Consumer Electronics',
    company_country: 'Netherlands',
    signal_type: 'inventory_surplus',
    signal_priority: 'hot',
    title: 'Q3 Inventory Surplus Alert',
    summary: 'Q3 report shows €120M excess inventory in Personal Health segment, seeking liquidation channels. CEO mentioned exploring "promotional partnerships with key retail partners" on earnings call.',
    confidence_score: 92,
    deal_potential_score: 88,
    source_url: 'https://www.philips.com/investor-relations',
    source_type: 'Earnings Call',
    source_date: '2024-12-05',
    detected_at: new Date(Date.now() - 2 * 3600000).toISOString(),
    status: 'new',
    categories: ['consumer_electronics', 'health_beauty'],
    evidence: {
      quotes: ['"We continue to work through elevated inventory levels in our Personal Health segment, with approximately €120 million in excess stock primarily in grooming and oral care categories."'],
      documents: ['Q3 2024 Earnings Call Transcript'],
    },
    estimated_value: 120000000,
    likely_discount_range: '40-60%',
    competition_level: 'high',
    timing_recommendation: 'Act within 2 weeks',
  },
  {
    id: 's2',
    company_id: 'c2',
    company_name: 'Xiaomi',
    company_country: 'China',
    signal_type: 'european_market_entry',
    signal_priority: 'strategic',
    title: 'EU Expansion to 12 Countries',
    summary: 'Xiaomi announced direct retail expansion to Netherlands, Belgium, Austria and 9 more EU countries by Q2 2025. Actively seeking e-commerce partners for market entry.',
    confidence_score: 88,
    deal_potential_score: 85,
    source_url: 'https://www.xiaomi.com/press',
    source_type: 'Press Release',
    source_date: '2024-12-08',
    detected_at: new Date(Date.now() - 5 * 3600000).toISOString(),
    status: 'new',
    categories: ['consumer_electronics', 'home_appliances'],
    evidence: {
      quotes: ['"We are actively seeking strategic retail and e-commerce partners to accelerate our European expansion."'],
      documents: ['EU Expansion Press Release'],
    },
    likely_discount_range: 'Launch pricing negotiable',
    competition_level: 'medium',
    timing_recommendation: 'Contact within 4 weeks for Q2 launch',
  },
  {
    id: 's3',
    company_id: 'c3',
    company_name: 'Tefal / Groupe SEB',
    company_country: 'France',
    signal_type: 'product_discontinuation',
    signal_priority: 'hot',
    title: 'Cookware Line Phase-Out',
    summary: 'Phasing out 3 cookware product lines with estimated 50,000 units to clear before Q1 2025. New line launching in March.',
    confidence_score: 95,
    deal_potential_score: 90,
    source_type: 'Industry Source',
    source_date: '2024-12-07',
    detected_at: new Date(Date.now() - 24 * 3600000).toISOString(),
    status: 'viewed',
    categories: ['home_appliances'],
    estimated_value: 2500000,
    likely_discount_range: '50-70%',
    competition_level: 'medium',
    timing_recommendation: 'Urgent - clearance deadline Q1 2025',
  },
  {
    id: 's4',
    company_id: 'c4',
    company_name: 'Dyson',
    company_country: 'United Kingdom',
    signal_type: 'new_factory',
    signal_priority: 'strategic',
    title: 'Malaysia Factory Expansion',
    summary: 'New manufacturing facility in Malaysia expected to increase production capacity by 40%. Ramp-up phase Q2 2025 may lead to initial oversupply.',
    confidence_score: 78,
    deal_potential_score: 72,
    source_type: 'News',
    source_date: '2024-12-01',
    detected_at: new Date(Date.now() - 48 * 3600000).toISOString(),
    expires_at: new Date(Date.now() + 90 * 24 * 3600000).toISOString(),
    status: 'new',
    categories: ['home_appliances'],
    timing_recommendation: 'Set reminder for Q2 2025',
  },
  {
    id: 's5',
    company_id: 'c5',
    company_name: 'Sony',
    company_country: 'Japan',
    signal_type: 'earnings_miss',
    signal_priority: 'hot',
    title: 'Consumer Electronics Division -12%',
    summary: 'Q3 results show consumer electronics division down 12% YoY. Restructuring expected. Potential inventory liquidation to improve balance sheet.',
    confidence_score: 85,
    deal_potential_score: 75,
    source_type: 'Earnings Report',
    source_date: '2024-12-06',
    detected_at: new Date(Date.now() - 72 * 3600000).toISOString(),
    status: 'new',
    categories: ['consumer_electronics'],
    competition_level: 'high',
    timing_recommendation: 'Monitor for liquidation announcements',
  },
  {
    id: 's6',
    company_id: 'c6',
    company_name: 'Bosch Home',
    company_country: 'Germany',
    signal_type: 'trade_show_attendance',
    signal_priority: 'relationship',
    title: 'IFA Berlin 2025 Exhibitor',
    summary: 'Confirmed exhibitor at IFA Berlin 2025. New product launches expected. Good opportunity for face-to-face meeting.',
    confidence_score: 100,
    deal_potential_score: 60,
    source_type: 'Trade Show Calendar',
    source_date: '2024-12-09',
    detected_at: new Date(Date.now() - 1 * 3600000).toISOString(),
    status: 'new',
    categories: ['home_appliances'],
    timing_recommendation: 'Schedule meeting at IFA',
  },
  {
    id: 's7',
    company_id: 'c7',
    company_name: 'Garmin',
    company_country: 'United States',
    signal_type: 'category_oversupply',
    signal_priority: 'market',
    title: 'Fitness Tracker Market Oversupply',
    summary: 'Industry analysts report 15% oversupply in fitness wearables category. Multiple brands likely to offer discounts to clear inventory.',
    confidence_score: 72,
    deal_potential_score: 68,
    source_type: 'Market Research',
    source_date: '2024-12-04',
    detected_at: new Date(Date.now() - 96 * 3600000).toISOString(),
    status: 'new',
    categories: ['consumer_electronics', 'sports_fitness'],
    timing_recommendation: 'Reach out to category leaders',
  },
  {
    id: 's8',
    company_id: 'c8',
    company_name: 'Braun (P&G)',
    company_country: 'Germany',
    signal_type: 'new_sales_leader',
    signal_priority: 'relationship',
    title: 'New Commercial Director EMEA',
    summary: 'Appointed new Commercial Director for EMEA region. Fresh leadership often open to new partnerships.',
    confidence_score: 90,
    deal_potential_score: 55,
    source_type: 'LinkedIn',
    source_date: '2024-12-03',
    detected_at: new Date(Date.now() - 120 * 3600000).toISOString(),
    status: 'new',
    categories: ['health_beauty'],
    timing_recommendation: 'Congratulate and introduce iBood',
  },
];

const createDemoCompanies = (): IBoodCompany[] => [
  {
    id: 'c1',
    name: 'Philips Consumer Lifestyle',
    country: 'Netherlands',
    revenue_eur: 6800000000,
    employees: 25000,
    categories: ['consumer_electronics', 'health_beauty', 'home_appliances'],
    status: 'active_supplier',
    active_signals: 3,
    past_gmv: 2400000,
    has_contact: true,
    relationship_owner: 'Daan',
    latest_signal: 'Inventory Surplus (Q3 2024)',
  },
  {
    id: 'c2',
    name: 'Xiaomi',
    country: 'China',
    revenue_eur: 32000000000,
    employees: 35000,
    categories: ['consumer_electronics', 'home_appliances'],
    status: 'new',
    active_signals: 1,
    has_contact: false,
    latest_signal: 'European Market Entry',
  },
  {
    id: 'c3',
    name: 'Groupe SEB (Tefal, Krups, Rowenta)',
    country: 'France',
    revenue_eur: 8100000000,
    employees: 33000,
    categories: ['home_appliances'],
    status: 'contacted',
    active_signals: 2,
    past_gmv: 850000,
    has_contact: true,
    latest_signal: 'Product Discontinuation',
  },
  {
    id: 'c4',
    name: 'Dyson',
    country: 'United Kingdom',
    revenue_eur: 7200000000,
    employees: 14000,
    categories: ['home_appliances'],
    status: 'watching',
    active_signals: 1,
    has_contact: false,
    latest_signal: 'New Factory Opening',
  },
];

// Format helpers
const formatCurrency = (value: number): string => {
  if (value >= 1000000000) return `€${(value / 1000000000).toFixed(1)}B`;
  if (value >= 1000000) return `€${(value / 1000000).toFixed(1)}M`;
  if (value >= 1000) return `€${(value / 1000).toFixed(0)}K`;
  return `€${value}`;
};

const formatTimeAgo = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return `${Math.floor(diffDays / 7)}w ago`;
};

// Signal Card Component
const SignalCard: React.FC<{
  signal: IBoodSignal;
  onView: (signal: IBoodSignal) => void;
  onSave: (signal: IBoodSignal) => void;
  onContact: (signal: IBoodSignal) => void;
  saved?: boolean;
}> = ({ signal, onView, onSave, onContact, saved = false }) => {
  const config = SIGNAL_CONFIG[signal.signal_type];
  const priorityConfig = PRIORITY_CONFIG[signal.signal_priority];

  return (
    <div className="signal-card" onClick={() => onView(signal)}>
      <div className="signal-card-header">
        <div className="signal-type-badge" style={{ backgroundColor: priorityConfig.bgColor, color: priorityConfig.color }}>
          <span>{priorityConfig.icon}</span>
          <span>{config.label}</span>
        </div>
        <div className="signal-meta">
          <span className="signal-confidence">
            {signal.confidence_score}% confidence
          </span>
          <span className="signal-time">{formatTimeAgo(signal.detected_at)}</span>
        </div>
      </div>

      <div className="signal-card-company">
        <Building2 size={16} />
        <span className="company-name">{signal.company_name}</span>
        <span className="company-country">{signal.company_country}</span>
      </div>

      <h3 className="signal-card-title">{signal.title}</h3>
      <p className="signal-card-summary">{signal.summary}</p>

      <div className="signal-card-categories">
        {signal.categories.slice(0, 3).map((cat) => (
          <span key={cat} className="category-tag">{CATEGORY_LABELS[cat]}</span>
        ))}
      </div>

      {(signal.estimated_value || signal.likely_discount_range) && (
        <div className="signal-card-deal-info">
          {signal.estimated_value && (
            <div className="deal-info-item">
              <DollarSign size={14} />
              <span>Est. Value: {formatCurrency(signal.estimated_value)}</span>
            </div>
          )}
          {signal.likely_discount_range && (
            <div className="deal-info-item">
              <TrendingDown size={14} />
              <span>Discount: {signal.likely_discount_range}</span>
            </div>
          )}
          {signal.competition_level && (
            <div className={`deal-info-item competition-${signal.competition_level}`}>
              <Users size={14} />
              <span>Competition: {signal.competition_level}</span>
            </div>
          )}
        </div>
      )}

      <div className="signal-card-actions">
        <button className="btn-signal-action primary" onClick={(e) => { e.stopPropagation(); onView(signal); }}>
          <Eye size={14} /> View Details
        </button>
        <button className="btn-signal-action" onClick={(e) => { e.stopPropagation(); onContact(signal); }}>
          <Mail size={14} /> Contact
        </button>
        <button className={`btn-signal-action ${saved ? 'saved' : ''}`} onClick={(e) => { e.stopPropagation(); onSave(signal); }}>
          {saved ? <BookmarkCheck size={14} /> : <Bookmark size={14} />}
        </button>
      </div>
    </div>
  );
};

// Company Card Component
const CompanyCard: React.FC<{
  company: IBoodCompany;
  onView: (company: IBoodCompany) => void;
}> = ({ company, onView }) => {
  const statusColors: Record<CompanyStatus, string> = {
    new: '#3B82F6',
    watching: '#F59E0B',
    contacted: '#8B5CF6',
    active_supplier: '#10B981',
    inactive: '#6B7280',
  };

  return (
    <div className="company-card" onClick={() => onView(company)}>
      <div className="company-card-header">
        <div className="company-logo">
          {company.logo ? (
            <img src={company.logo} alt={company.name} />
          ) : (
            <Building2 size={24} />
          )}
        </div>
        <div className="company-info">
          <h4 className="company-name">{company.name}</h4>
          <span className="company-details">
            {company.country} • {company.revenue_eur ? formatCurrency(company.revenue_eur) + ' Revenue' : ''}
            {company.employees ? ` • ${company.employees.toLocaleString()} employees` : ''}
          </span>
        </div>
      </div>

      <div className="company-card-categories">
        {company.categories.map((cat) => (
          <span key={cat} className="category-tag small">{CATEGORY_LABELS[cat]}</span>
        ))}
      </div>

      <div className="company-card-stats">
        <div className="stat-item">
          <span className="stat-icon" style={{ color: '#EF4444' }}>🔥</span>
          <span className="stat-value">{company.active_signals}</span>
          <span className="stat-label">Signals</span>
        </div>
        <div className="stat-item">
          <span className="stat-icon" style={{ backgroundColor: statusColors[company.status] }}></span>
          <span className="stat-value">{company.status.replace('_', ' ')}</span>
          <span className="stat-label">Status</span>
        </div>
        {company.has_contact && (
          <div className="stat-item">
            <Phone size={14} />
            <span className="stat-value">Yes</span>
            <span className="stat-label">Contact</span>
          </div>
        )}
        {company.past_gmv && (
          <div className="stat-item">
            <DollarSign size={14} />
            <span className="stat-value">{formatCurrency(company.past_gmv)}</span>
            <span className="stat-label">Past GMV</span>
          </div>
        )}
      </div>

      {company.latest_signal && (
        <div className="company-latest-signal">
          <Zap size={12} />
          <span>Latest: {company.latest_signal}</span>
        </div>
      )}

      <button className="btn-view-company">
        View Details <ChevronRight size={16} />
      </button>
    </div>
  );
};

// Main Dashboard Component
const SignalsDashboard: React.FC = () => {
  const { t } = useTranslation(['signals', 'common']);
  const [signals, setSignals] = useState<IBoodSignal[]>([]);
  const [companies, setCompanies] = useState<IBoodCompany[]>([]);
  const [savedSignals, setSavedSignals] = useState<Set<string>>(new Set());
  const [activeTab, setActiveTab] = useState<'signals' | 'companies' | 'categories' | 'watchlist'>('signals');
  const [filterPriority, setFilterPriority] = useState<SignalPriority | 'all'>('all');
  const [filterCategory, setFilterCategory] = useState<ProductCategory | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedSignal, setSelectedSignal] = useState<IBoodSignal | null>(null);

  useEffect(() => {
    // Load demo data
    setLoading(true);
    setTimeout(() => {
      setSignals(createDemoSignals());
      setCompanies(createDemoCompanies());
      setLoading(false);
    }, 500);
  }, []);

  // Filter signals
  const filteredSignals = signals.filter((signal) => {
    if (filterPriority !== 'all' && signal.signal_priority !== filterPriority) return false;
    if (filterCategory !== 'all' && !signal.categories.includes(filterCategory)) return false;
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      return (
        signal.company_name.toLowerCase().includes(query) ||
        signal.title.toLowerCase().includes(query) ||
        signal.summary.toLowerCase().includes(query)
      );
    }
    return true;
  });

  // Group signals by priority
  const hotSignals = filteredSignals.filter((s) => s.signal_priority === 'hot');
  const strategicSignals = filteredSignals.filter((s) => s.signal_priority === 'strategic');
  const marketSignals = filteredSignals.filter((s) => s.signal_priority === 'market');
  const relationshipSignals = filteredSignals.filter((s) => s.signal_priority === 'relationship');

  // Stats
  const stats = {
    newSignals: signals.filter((s) => s.status === 'new').length,
    hotSignals: hotSignals.length,
    companiesWithSurplus: signals.filter((s) => s.signal_type === 'inventory_surplus').length,
    expiringThisWeek: signals.filter((s) => {
      if (!s.expires_at) return false;
      const expires = new Date(s.expires_at);
      const now = new Date();
      const weekFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
      return expires <= weekFromNow;
    }).length,
  };

  const handleViewSignal = (signal: IBoodSignal) => {
    setSelectedSignal(signal);
    // Update status to viewed
    setSignals((prev) =>
      prev.map((s) => (s.id === signal.id ? { ...s, status: 'viewed' as SignalStatus } : s))
    );
  };

  const handleSaveSignal = (signal: IBoodSignal) => {
    setSavedSignals((prev) => {
      const next = new Set(prev);
      if (next.has(signal.id)) {
        next.delete(signal.id);
      } else {
        next.add(signal.id);
      }
      return next;
    });
  };

  const handleContactSignal = (signal: IBoodSignal) => {
    console.log('Contact for signal:', signal);
    // Would open contact modal
  };

  const handleViewCompany = (company: IBoodCompany) => {
    console.log('View company:', company);
    // Would navigate to company detail
  };

  // Get current user name
  const userName = 'Daan';
  const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div className="signals-dashboard">
      {/* Header */}
      <div className="signals-header">
        <div className="signals-header-left">
          <h1>Good morning, {userName}</h1>
          <p className="signals-subtitle">
            {stats.newSignals} new signals detected • {stats.hotSignals} high-priority opportunities
          </p>
        </div>
        <div className="signals-header-right">
          <span className="signals-date">{currentDate}</span>
          <button className="btn-icon">
            <Bell size={20} />
            <span className="notification-dot"></span>
          </button>
          <button className="btn-icon">
            <Settings size={20} />
          </button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="signals-quick-stats">
        <div className="quick-stat-card your-categories">
          <div className="quick-stat-icon">🔥</div>
          <div className="quick-stat-content">
            <span className="quick-stat-value">{stats.hotSignals} hot signals</span>
            <span className="quick-stat-label">in your categories</span>
          </div>
        </div>
        <div className="quick-stat-card global-market">
          <div className="quick-stat-icon">📊</div>
          <div className="quick-stat-content">
            <span className="quick-stat-value">{stats.companiesWithSurplus} companies</span>
            <span className="quick-stat-label">with inventory surplus</span>
          </div>
        </div>
        <div className="quick-stat-card action-required">
          <div className="quick-stat-icon">⏰</div>
          <div className="quick-stat-content">
            <span className="quick-stat-value">{stats.expiringThisWeek} expiring</span>
            <span className="quick-stat-label">this week</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="signals-tabs">
        <button
          className={`signals-tab ${activeTab === 'signals' ? 'active' : ''}`}
          onClick={() => setActiveTab('signals')}
        >
          <Zap size={16} /> Signals
        </button>
        <button
          className={`signals-tab ${activeTab === 'companies' ? 'active' : ''}`}
          onClick={() => setActiveTab('companies')}
        >
          <Building2 size={16} /> Companies
        </button>
        <button
          className={`signals-tab ${activeTab === 'categories' ? 'active' : ''}`}
          onClick={() => setActiveTab('categories')}
        >
          <BarChart3 size={16} /> Category Intel
        </button>
        <button
          className={`signals-tab ${activeTab === 'watchlist' ? 'active' : ''}`}
          onClick={() => setActiveTab('watchlist')}
        >
          <Bookmark size={16} /> Watchlist
          {savedSignals.size > 0 && <span className="tab-badge">{savedSignals.size}</span>}
        </button>
      </div>

      {/* Filters */}
      <div className="signals-filters">
        <div className="search-box">
          <Search size={16} />
          <input
            type="text"
            placeholder="Search signals, companies..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="filter-group">
          <Filter size={16} />
          <select
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value as SignalPriority | 'all')}
          >
            <option value="all">All Priorities</option>
            <option value="hot">🔥 Hot</option>
            <option value="strategic">⭐ Strategic</option>
            <option value="market">📊 Market Intel</option>
            <option value="relationship">🤝 Relationship</option>
          </select>
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value as ProductCategory | 'all')}
          >
            <option value="all">All Categories</option>
            {Object.entries(CATEGORY_LABELS).map(([key, label]) => (
              <option key={key} value={key}>{label}</option>
            ))}
          </select>
        </div>
        <button className="btn-refresh">
          <RefreshCw size={16} /> Refresh
        </button>
      </div>

      {/* Content */}
      {activeTab === 'signals' && (
        <div className="signals-content">
          {/* Hot Opportunities */}
          {hotSignals.length > 0 && (
            <div className="signal-section">
              <h2 className="section-title">
                <span className="section-icon hot">🔥</span>
                Hot Opportunities
                <span className="section-count">{hotSignals.length}</span>
              </h2>
              <p className="section-subtitle">Immediate action required - motivated sellers</p>
              <div className="signals-grid">
                {hotSignals.map((signal) => (
                  <SignalCard
                    key={signal.id}
                    signal={signal}
                    onView={handleViewSignal}
                    onSave={handleSaveSignal}
                    onContact={handleContactSignal}
                    saved={savedSignals.has(signal.id)}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Strategic Opportunities */}
          {strategicSignals.length > 0 && (
            <div className="signal-section">
              <h2 className="section-title">
                <span className="section-icon strategic">⭐</span>
                Strategic Opportunities
                <span className="section-count">{strategicSignals.length}</span>
              </h2>
              <p className="section-subtitle">Worth monitoring for upcoming deals</p>
              <div className="signals-grid">
                {strategicSignals.map((signal) => (
                  <SignalCard
                    key={signal.id}
                    signal={signal}
                    onView={handleViewSignal}
                    onSave={handleSaveSignal}
                    onContact={handleContactSignal}
                    saved={savedSignals.has(signal.id)}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Market Intelligence */}
          {marketSignals.length > 0 && (
            <div className="signal-section">
              <h2 className="section-title">
                <span className="section-icon market">📊</span>
                Market Intelligence
                <span className="section-count">{marketSignals.length}</span>
              </h2>
              <p className="section-subtitle">Broader market trends and opportunities</p>
              <div className="signals-grid">
                {marketSignals.map((signal) => (
                  <SignalCard
                    key={signal.id}
                    signal={signal}
                    onView={handleViewSignal}
                    onSave={handleSaveSignal}
                    onContact={handleContactSignal}
                    saved={savedSignals.has(signal.id)}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Relationship Signals */}
          {relationshipSignals.length > 0 && (
            <div className="signal-section">
              <h2 className="section-title">
                <span className="section-icon relationship">🤝</span>
                Relationship Building
                <span className="section-count">{relationshipSignals.length}</span>
              </h2>
              <p className="section-subtitle">Long-term partnership opportunities</p>
              <div className="signals-grid">
                {relationshipSignals.map((signal) => (
                  <SignalCard
                    key={signal.id}
                    signal={signal}
                    onView={handleViewSignal}
                    onSave={handleSaveSignal}
                    onContact={handleContactSignal}
                    saved={savedSignals.has(signal.id)}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'companies' && (
        <div className="companies-content">
          <div className="companies-grid">
            {companies.map((company) => (
              <CompanyCard
                key={company.id}
                company={company}
                onView={handleViewCompany}
              />
            ))}
          </div>
        </div>
      )}

      {activeTab === 'categories' && (
        <div className="categories-content">
          <div className="category-intel-grid">
            {Object.entries(CATEGORY_LABELS).map(([key, label]) => {
              const categorySignals = signals.filter((s) => s.categories.includes(key as ProductCategory));
              const hotCount = categorySignals.filter((s) => s.signal_priority === 'hot').length;

              return (
                <div key={key} className="category-intel-card">
                  <h3>{label}</h3>
                  <div className="category-stats">
                    <div className="cat-stat">
                      <span className="cat-stat-value">{categorySignals.length}</span>
                      <span className="cat-stat-label">Total Signals</span>
                    </div>
                    <div className="cat-stat hot">
                      <span className="cat-stat-value">{hotCount}</span>
                      <span className="cat-stat-label">Hot</span>
                    </div>
                  </div>
                  <button className="btn-view-category">
                    View Signals <ChevronRight size={14} />
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {activeTab === 'watchlist' && (
        <div className="watchlist-content">
          {savedSignals.size === 0 ? (
            <div className="empty-watchlist">
              <Bookmark size={48} />
              <h3>No saved signals yet</h3>
              <p>Save signals to your watchlist to track them here</p>
            </div>
          ) : (
            <div className="signals-grid">
              {signals
                .filter((s) => savedSignals.has(s.id))
                .map((signal) => (
                  <SignalCard
                    key={signal.id}
                    signal={signal}
                    onView={handleViewSignal}
                    onSave={handleSaveSignal}
                    onContact={handleContactSignal}
                    saved={true}
                  />
                ))}
            </div>
          )}
        </div>
      )}

      {/* Signal Detail Modal */}
      {selectedSignal && (
        <div className="signal-modal-overlay" onClick={() => setSelectedSignal(null)}>
          <div className="signal-modal" onClick={(e) => e.stopPropagation()}>
            <div className="signal-modal-header">
              <div className="signal-type-badge large" style={{
                backgroundColor: PRIORITY_CONFIG[selectedSignal.signal_priority].bgColor,
                color: PRIORITY_CONFIG[selectedSignal.signal_priority].color
              }}>
                <span>{PRIORITY_CONFIG[selectedSignal.signal_priority].icon}</span>
                <span>{SIGNAL_CONFIG[selectedSignal.signal_type].label}</span>
              </div>
              <button className="btn-close" onClick={() => setSelectedSignal(null)}>
                <XCircle size={24} />
              </button>
            </div>

            <div className="signal-modal-content">
              <div className="signal-modal-company">
                <Building2 size={20} />
                <span className="company-name">{selectedSignal.company_name}</span>
                <span className="company-country">{selectedSignal.company_country}</span>
              </div>

              <h2>{selectedSignal.title}</h2>
              <p className="signal-summary">{selectedSignal.summary}</p>

              <div className="signal-scores">
                <div className="score-item">
                  <span className="score-label">Confidence</span>
                  <div className="score-bar">
                    <div className="score-fill" style={{ width: `${selectedSignal.confidence_score}%` }}></div>
                  </div>
                  <span className="score-value">{selectedSignal.confidence_score}%</span>
                </div>
                <div className="score-item">
                  <span className="score-label">Deal Potential</span>
                  <div className="score-bar">
                    <div className="score-fill deal" style={{ width: `${selectedSignal.deal_potential_score}%` }}></div>
                  </div>
                  <span className="score-value">{selectedSignal.deal_potential_score}%</span>
                </div>
              </div>

              {selectedSignal.evidence && selectedSignal.evidence.quotes.length > 0 && (
                <div className="signal-evidence">
                  <h4>Key Evidence</h4>
                  {selectedSignal.evidence.quotes.map((quote, idx) => (
                    <blockquote key={idx}>{quote}</blockquote>
                  ))}
                </div>
              )}

              <div className="signal-deal-assessment">
                <h4>Deal Assessment</h4>
                <div className="assessment-grid">
                  {selectedSignal.estimated_value && (
                    <div className="assessment-item">
                      <DollarSign size={16} />
                      <span className="assessment-label">Estimated Value</span>
                      <span className="assessment-value">{formatCurrency(selectedSignal.estimated_value)}</span>
                    </div>
                  )}
                  {selectedSignal.likely_discount_range && (
                    <div className="assessment-item">
                      <TrendingDown size={16} />
                      <span className="assessment-label">Likely Discount</span>
                      <span className="assessment-value">{selectedSignal.likely_discount_range}</span>
                    </div>
                  )}
                  {selectedSignal.competition_level && (
                    <div className="assessment-item">
                      <Users size={16} />
                      <span className="assessment-label">Competition</span>
                      <span className={`assessment-value ${selectedSignal.competition_level}`}>
                        {selectedSignal.competition_level.charAt(0).toUpperCase() + selectedSignal.competition_level.slice(1)}
                      </span>
                    </div>
                  )}
                  {selectedSignal.timing_recommendation && (
                    <div className="assessment-item full-width">
                      <Clock size={16} />
                      <span className="assessment-label">Timing</span>
                      <span className="assessment-value">{selectedSignal.timing_recommendation}</span>
                    </div>
                  )}
                </div>
              </div>

              <div className="signal-modal-actions">
                <button className="btn-primary">
                  <Mail size={16} /> Contact Supplier
                </button>
                <button className="btn-secondary">
                  <Phone size={16} /> Schedule Call
                </button>
                <button className="btn-secondary" onClick={() => handleSaveSignal(selectedSignal)}>
                  {savedSignals.has(selectedSignal.id) ? <BookmarkCheck size={16} /> : <Bookmark size={16} />}
                  {savedSignals.has(selectedSignal.id) ? 'Saved' : 'Save'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SignalsDashboard;
