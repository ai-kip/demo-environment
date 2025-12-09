import React, { useState } from 'react';
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
} from 'lucide-react';
import { Header } from './Header';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  href: string;
  badge?: number | string;
}

interface AppLayoutProps {
  children: React.ReactNode;
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

const mainNavItems: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={20} />, href: '/' },
  { id: 'pipeline', label: 'Pipeline', icon: <Target size={20} />, href: '/pipeline' },
  { id: 'leads', label: 'Leads', icon: <UserPlus size={20} />, href: '/leads', badge: 12 },
  { id: 'deals', label: 'Deals', icon: <Building2 size={20} />, href: '/deals', badge: 47 },
  { id: 'contacts', label: 'Contacts', icon: <Users size={20} />, href: '/contacts' },
  { id: 'signals', label: 'Signals', icon: <Zap size={20} />, href: '/signals', badge: '3 Hot' },
  { id: 'intent', label: 'Intent', icon: <Radio size={20} />, href: '/intent' },
  { id: 'sequences', label: 'Sequences', icon: <Send size={20} />, href: '/sequences' },
  { id: 'analytics', label: 'Analytics', icon: <BarChart2 size={20} />, href: '/analytics' },
];

const bottomNavItems: NavItem[] = [
  { id: 'settings', label: 'Settings', icon: <Settings size={20} />, href: '/settings' },
  { id: 'help', label: 'Help & Support', icon: <HelpCircle size={20} />, href: '/help' },
];

export const AppLayout: React.FC<AppLayoutProps> = ({ children, currentPage = 'dashboard', onNavigate }) => {
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

  return (
    <div className={`app-layout ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      {/* Skip link for accessibility */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      {/* Header */}
      <Header onMenuClick={toggleSidebar} />

      {/* Sidebar */}
      <aside className={`app-sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <nav className="sidebar-nav" aria-label="Main navigation">
          <ul className="nav-list">
            {mainNavItems.map((item) => (
              <li key={item.id}>
                <a
                  href={item.href}
                  className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
                  title={sidebarCollapsed ? item.label : undefined}
                  onClick={(e) => handleNavClick(e, item.id)}
                >
                  <span className="nav-icon">{item.icon}</span>
                  {!sidebarCollapsed && (
                    <>
                      <span className="nav-label">{item.label}</span>
                      {item.badge && (
                        <span className="nav-badge">{item.badge}</span>
                      )}
                    </>
                  )}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <div className="sidebar-bottom">
          <ul className="nav-list">
            {bottomNavItems.map((item) => (
              <li key={item.id}>
                <a
                  href={item.href}
                  className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
                  title={sidebarCollapsed ? item.label : undefined}
                  onClick={(e) => handleNavClick(e, item.id)}
                >
                  <span className="nav-icon">{item.icon}</span>
                  {!sidebarCollapsed && <span className="nav-label">{item.label}</span>}
                </a>
              </li>
            ))}
          </ul>

          <button
            className="sidebar-toggle"
            onClick={toggleSidebar}
            aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {sidebarCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main id="main-content" className="app-main">
        {children}
      </main>
    </div>
  );
};

export default AppLayout;
