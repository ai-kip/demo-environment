import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  LayoutDashboard,
  Target,
  Building2,
  Users,
  Zap,
  Send,
  BarChart2,
  Settings,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  UserPlus,
  Radio,
  Brain,
  Sparkles,
  // Marketing Intelligence icons
  Megaphone,
  Library,
  Linkedin,
  FileText,
  Layout,
  Flag,
  TrendingUp,
} from 'lucide-react';
import { Header } from './Header';

interface NavItem {
  id: string;
  labelKey: string;
  icon: React.ReactNode;
  href: string;
  badge?: number | string;
}

interface NavSection {
  id: string;
  labelKey: string;
  items: NavItem[];
}

interface AppLayoutProps {
  children: React.ReactNode;
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

// Sales Intelligence navigation items
const salesNavItems: NavItem[] = [
  { id: 'dashboard', labelKey: 'navigation.dashboard', icon: <LayoutDashboard size={20} />, href: '/' },
  { id: 'pipeline', labelKey: 'navigation.pipeline', icon: <Target size={20} />, href: '/pipeline' },
  { id: 'leads', labelKey: 'navigation.leads', icon: <UserPlus size={20} />, href: '/leads' },
  { id: 'deals', labelKey: 'navigation.deals', icon: <Building2 size={20} />, href: '/deals', badge: 47 },
  { id: 'contacts', labelKey: 'navigation.contacts', icon: <Users size={20} />, href: '/contacts' },
  { id: 'signals', labelKey: 'navigation.signals', icon: <Zap size={20} />, href: '/signals', badge: '3 Hot' },
  { id: 'intent', labelKey: 'navigation.intent', icon: <Radio size={20} />, href: '/intent' },
  { id: 'sequences', labelKey: 'navigation.sequences', icon: <Send size={20} />, href: '/sequences' },
  { id: 'thought-leadership', labelKey: 'navigation.thoughtLeadership', icon: <Sparkles size={20} />, href: '/thought-leadership' },
  { id: 'deep-work', labelKey: 'navigation.deepWork', icon: <Brain size={20} />, href: '/deep-work' },
  { id: 'analytics', labelKey: 'navigation.analytics', icon: <BarChart2 size={20} />, href: '/analytics' },
];

// Marketing Intelligence navigation items
const marketingNavItems: NavItem[] = [
  { id: 'marketing-dashboard', labelKey: 'navigation.marketingDashboard', icon: <Megaphone size={20} />, href: '/marketing' },
  { id: 'content-library', labelKey: 'navigation.contentLibrary', icon: <Library size={20} />, href: '/marketing/content' },
  { id: 'linkedin', labelKey: 'navigation.linkedin', icon: <Linkedin size={20} />, href: '/marketing/linkedin' },
  { id: 'articles', labelKey: 'navigation.articles', icon: <FileText size={20} />, href: '/marketing/articles' },
  { id: 'landing-pages', labelKey: 'navigation.landingPages', icon: <Layout size={20} />, href: '/marketing/landing-pages' },
  { id: 'abm', labelKey: 'navigation.abm', icon: <Target size={20} />, href: '/marketing/abm' },
  { id: 'campaigns', labelKey: 'navigation.campaigns', icon: <Flag size={20} />, href: '/marketing/campaigns' },
  { id: 'marketing-analytics', labelKey: 'navigation.marketingAnalytics', icon: <TrendingUp size={20} />, href: '/marketing/analytics' },
];

// Navigation sections
const navSections: NavSection[] = [
  {
    id: 'sales',
    labelKey: 'navigation.salesIntelligence',
    items: salesNavItems,
  },
  {
    id: 'marketing',
    labelKey: 'navigation.marketingIntelligence',
    items: marketingNavItems,
  },
];

const bottomNavItemsConfig: NavItem[] = [
  { id: 'settings', labelKey: 'navigation.settings', icon: <Settings size={20} />, href: '/settings' },
  { id: 'help', labelKey: 'navigation.help', icon: <HelpCircle size={20} />, href: '/help' },
];

export const AppLayout: React.FC<AppLayoutProps> = ({ children, currentPage = 'dashboard', onNavigate }) => {
  const { t } = useTranslation('common');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleNavClick = (e: React.MouseEvent, pageId: string) => {
    e.preventDefault();
    if (onNavigate) {
      onNavigate(pageId);
    }
  };

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  const renderNavItem = (item: NavItem) => {
    const label = t(item.labelKey);
    return (
      <li key={item.id}>
        <a
          href={item.href}
          className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
          title={sidebarCollapsed ? label : undefined}
          onClick={(e) => handleNavClick(e, item.id)}
        >
          <span className="nav-icon">{item.icon}</span>
          {!sidebarCollapsed && (
            <>
              <span className="nav-label">{label}</span>
              {item.badge && (
                <span className="nav-badge">{item.badge}</span>
              )}
            </>
          )}
        </a>
      </li>
    );
  };

  return (
    <div className={`app-layout ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      {/* Skip link for accessibility */}
      <a href="#main-content" className="skip-link">
        {t('sidebar.skipToMainContent')}
      </a>

      {/* Header */}
      <Header onMenuClick={toggleSidebar} />

      {/* Sidebar */}
      <aside className={`app-sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <nav className="sidebar-nav" aria-label={t('sidebar.mainNavigation')}>
          {navSections.map((section, sectionIndex) => (
            <div key={section.id} className="nav-section">
              {/* Section Header */}
              {!sidebarCollapsed && (
                <div className="nav-section-header">
                  <span className="nav-section-label">{t(section.labelKey)}</span>
                </div>
              )}
              {sidebarCollapsed && sectionIndex > 0 && (
                <div className="nav-section-divider" />
              )}

              {/* Section Items */}
              <ul className="nav-list">
                {section.items.map(renderNavItem)}
              </ul>
            </div>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <ul className="nav-list">
            {bottomNavItemsConfig.map((item) => {
              const label = t(item.labelKey);
              return (
                <li key={item.id}>
                  <a
                    href={item.href}
                    className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
                    title={sidebarCollapsed ? label : undefined}
                    onClick={(e) => handleNavClick(e, item.id)}
                  >
                    <span className="nav-icon">{item.icon}</span>
                    {!sidebarCollapsed && <span className="nav-label">{label}</span>}
                  </a>
                </li>
              );
            })}
          </ul>

          <button
            className="sidebar-toggle"
            onClick={toggleSidebar}
            aria-label={sidebarCollapsed ? t('sidebar.expandSidebar') : t('sidebar.collapseSidebar')}
          >
            {sidebarCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main id="main-content" className="app-main">
        {children}
      </main>

      {/* Styles for section headers */}
      <style>{`
        .nav-section {
          margin-bottom: 0.5rem;
        }

        .nav-section-header {
          padding: 0.75rem 1rem 0.5rem;
          margin-top: 0.5rem;
        }

        .nav-section:first-child .nav-section-header {
          margin-top: 0;
        }

        .nav-section-label {
          font-size: 0.625rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: var(--color-text-tertiary, #9CA3AF);
        }

        .nav-section-divider {
          height: 1px;
          background: var(--color-border, #E5E7EB);
          margin: 0.75rem 1rem;
        }
      `}</style>
    </div>
  );
};

export default AppLayout;
