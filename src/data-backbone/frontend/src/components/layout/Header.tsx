import React, { useState } from 'react';
import {
  Search,
  Bell,
  Settings,
  User,
  ChevronDown,
  Menu,
} from 'lucide-react';

interface HeaderProps {
  onMenuClick?: () => void;
  user?: {
    name: string;
    email: string;
    avatar?: string;
  };
}

export const Header: React.FC<HeaderProps> = ({
  onMenuClick,
  user = { name: 'Hugo', email: 'hugo@duinrell.com' },
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="app-header">
      <div className="header-left">
        <button
          className="header-menu-btn"
          onClick={onMenuClick}
          aria-label="Toggle menu"
        >
          <Menu size={20} />
        </button>

        <div className="header-logo">
          <span className="logo-icon">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
              <path
                d="M14 2L2 8v12l12 6 12-6V8L14 2z"
                fill="url(#logo-gradient)"
              />
              <defs>
                <linearGradient id="logo-gradient" x1="2" y1="2" x2="26" y2="26">
                  <stop stopColor="#0A84FF" />
                  <stop offset="1" stopColor="#00B4B4" />
                </linearGradient>
              </defs>
            </svg>
          </span>
          <span className="logo-text">Duinrell</span>
        </div>
      </div>

      <div className="header-center">
        <div className="header-search">
          <Search size={18} className="search-icon" />
          <input
            type="text"
            className="search-input"
            placeholder="Search deals, companies, contacts..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            aria-label="Search"
          />
          <kbd className="search-shortcut">
            <span>Cmd</span>K
          </kbd>
        </div>
      </div>

      <div className="header-right">
        <button
          className="header-icon-btn"
          onClick={() => setShowNotifications(!showNotifications)}
          aria-label="Notifications"
        >
          <Bell size={20} />
          <span className="notification-badge">3</span>
        </button>

        <button className="header-icon-btn" aria-label="Settings">
          <Settings size={20} />
        </button>

        <div className="header-user">
          <button
            className="user-btn"
            onClick={() => setShowUserMenu(!showUserMenu)}
            aria-expanded={showUserMenu}
            aria-haspopup="true"
          >
            <div className="user-avatar">
              {user.avatar ? (
                <img src={user.avatar} alt={user.name} />
              ) : (
                <User size={18} />
              )}
            </div>
            <span className="user-name">{user.name}</span>
            <ChevronDown size={16} className={`user-chevron ${showUserMenu ? 'open' : ''}`} />
          </button>

          {showUserMenu && (
            <div className="user-menu">
              <div className="user-menu-header">
                <div className="user-menu-name">{user.name}</div>
                <div className="user-menu-email">{user.email}</div>
              </div>
              <div className="user-menu-divider" />
              <a href="#profile" className="user-menu-item">Profile</a>
              <a href="#preferences" className="user-menu-item">Preferences</a>
              <div className="user-menu-divider" />
              <button className="user-menu-item user-menu-logout">Sign out</button>
            </div>
          )}
        </div>
      </div>

      {/* Notifications dropdown */}
      {showNotifications && (
        <div className="notifications-dropdown">
          <div className="notifications-header">
            <h3>Notifications</h3>
            <button className="mark-all-read">Mark all read</button>
          </div>
          <div className="notifications-list">
            <div className="notification-item unread">
              <div className="notification-icon hot">
                <span>🔥</span>
              </div>
              <div className="notification-content">
                <div className="notification-title">ACME Corp reached Hot status</div>
                <div className="notification-time">2 minutes ago</div>
              </div>
            </div>
            <div className="notification-item unread">
              <div className="notification-icon signal">
                <span>📰</span>
              </div>
              <div className="notification-content">
                <div className="notification-title">New signal: TechFlow sustainability initiative</div>
                <div className="notification-time">15 minutes ago</div>
              </div>
            </div>
            <div className="notification-item">
              <div className="notification-icon deal">
                <span>💼</span>
              </div>
              <div className="notification-content">
                <div className="notification-title">Deal moved to SAL: Nordic Hotels</div>
                <div className="notification-time">1 hour ago</div>
              </div>
            </div>
          </div>
          <a href="#all-notifications" className="notifications-view-all">
            View all notifications
          </a>
        </div>
      )}
    </header>
  );
};

export default Header;
