import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  FileText,
  Eye,
  Calendar,
  Flag,
  TrendingUp,
  Plus,
  Linkedin,
  Layout,
  ArrowRight,
} from 'lucide-react';
import { CONTENT_COLORS, CONTENT_TYPE_CONFIG, createDemoContentStats, createDemoRecentActivity, createDemoScheduledPosts, formatContentDateTime } from '../../constants/content';
import { DASHBOARD_QUICK_ACTIONS } from '../../constants/marketing';
import { api } from '../../services/api';
import { ContentStatusBadge } from './shared';

interface MarketingDashboardProps {
  onNavigate?: (page: string) => void;
}

const MarketingDashboard: React.FC<MarketingDashboardProps> = ({ onNavigate }) => {
  const { t } = useTranslation('marketing');
  const [stats, setStats] = useState(createDemoContentStats());
  const [recentActivity, setRecentActivity] = useState(createDemoRecentActivity());
  const [scheduledPosts, setScheduledPosts] = useState(createDemoScheduledPosts());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const analytics = await api.getMarketingAnalytics();
      setStats({
        totalContent: analytics.total_content,
        publishedContent: analytics.content_by_status?.published || 0,
        draftContent: analytics.content_by_status?.draft || 0,
        scheduledPosts: analytics.content_by_status?.scheduled || 0,
        activeCampaigns: analytics.active_campaigns,
        totalImpressions: analytics.total_impressions,
        totalEngagement: analytics.total_engagement,
        avgEngagementRate: analytics.avg_engagement_rate,
      });
    } catch (error) {
      // Use demo data on error
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = (href: string) => {
    if (onNavigate) {
      const page = href.replace('/marketing/', '').replace('/new', '') || 'marketing-dashboard';
      onNavigate(page);
    }
  };

  const kpis = [
    { label: t('dashboard.kpis.totalContent'), value: stats.totalContent, icon: <FileText size={20} />, color: CONTENT_COLORS.primary },
    { label: t('dashboard.kpis.publishedContent'), value: stats.publishedContent, icon: <Eye size={20} />, color: CONTENT_COLORS.success },
    { label: t('dashboard.kpis.scheduledPosts'), value: stats.scheduledPosts, icon: <Calendar size={20} />, color: CONTENT_COLORS.scheduled },
    { label: t('dashboard.kpis.activeCampaigns'), value: stats.activeCampaigns, icon: <Flag size={20} />, color: CONTENT_COLORS.warning },
    { label: t('dashboard.kpis.totalImpressions'), value: stats.totalImpressions.toLocaleString(), icon: <TrendingUp size={20} />, color: CONTENT_COLORS.info },
    { label: t('dashboard.kpis.avgEngagementRate'), value: `${stats.avgEngagementRate.toFixed(1)}%`, icon: <TrendingUp size={20} />, color: CONTENT_COLORS.success },
  ];

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: CONTENT_COLORS.primaryText, margin: 0 }}>
          {t('dashboard.title')}
        </h1>
        <p style={{ fontSize: '0.875rem', color: CONTENT_COLORS.secondaryText, marginTop: '4px' }}>
          {t('dashboard.subtitle')}
        </p>
      </div>

      {/* KPI Cards */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          marginBottom: '24px',
        }}
      >
        {kpis.map((kpi, index) => (
          <div
            key={index}
            style={{
              backgroundColor: CONTENT_COLORS.cardBg,
              borderRadius: '12px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              padding: '20px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <span style={{ color: CONTENT_COLORS.secondaryText, fontSize: '0.875rem' }}>{kpi.label}</span>
              <div
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '8px',
                  backgroundColor: `${kpi.color}15`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: kpi.color,
                }}
              >
                {kpi.icon}
              </div>
            </div>
            <div style={{ fontSize: '1.75rem', fontWeight: 700, color: CONTENT_COLORS.primaryText }}>
              {kpi.value}
            </div>
          </div>
        ))}
      </div>

      {/* Quick Create */}
      <div
        style={{
          backgroundColor: CONTENT_COLORS.cardBg,
          borderRadius: '12px',
          border: `1px solid ${CONTENT_COLORS.border}`,
          padding: '20px',
          marginBottom: '24px',
        }}
      >
        <h2 style={{ fontSize: '1rem', fontWeight: 600, color: CONTENT_COLORS.primaryText, marginBottom: '16px' }}>
          {t('dashboard.quickCreate')}
        </h2>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
          {DASHBOARD_QUICK_ACTIONS.map((action) => (
            <button
              key={action.id}
              onClick={() => handleQuickAction(action.href)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '12px 20px',
                borderRadius: '8px',
                border: `1px solid ${CONTENT_COLORS.border}`,
                backgroundColor: CONTENT_COLORS.cardBg,
                color: CONTENT_COLORS.primaryText,
                fontSize: '0.875rem',
                fontWeight: 500,
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
            >
              <Plus size={18} color={action.color} />
              {t(action.labelKey)}
            </button>
          ))}
        </div>
      </div>

      {/* Two Column Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
        {/* Recent Activity */}
        <div
          style={{
            backgroundColor: CONTENT_COLORS.cardBg,
            borderRadius: '12px',
            border: `1px solid ${CONTENT_COLORS.border}`,
            padding: '20px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <h2 style={{ fontSize: '1rem', fontWeight: 600, color: CONTENT_COLORS.primaryText, margin: 0 }}>
              {t('dashboard.recentActivity')}
            </h2>
            <button
              onClick={() => onNavigate && onNavigate('content-library')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                background: 'none',
                border: 'none',
                color: CONTENT_COLORS.primary,
                fontSize: '0.875rem',
                cursor: 'pointer',
              }}
            >
              View All <ArrowRight size={14} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {recentActivity.map((activity) => {
              const typeConfig = CONTENT_TYPE_CONFIG[activity.contentType];
              return (
                <div
                  key={activity.id}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '12px',
                    padding: '12px',
                    borderRadius: '8px',
                    backgroundColor: CONTENT_COLORS.background,
                  }}
                >
                  <div
                    style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '6px',
                      backgroundColor: `${typeConfig.color}15`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: typeConfig.color,
                      flexShrink: 0,
                    }}
                  >
                    {activity.contentType === 'linkedin_post' ? <Linkedin size={16} /> : <FileText size={16} />}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div
                      style={{
                        fontSize: '0.875rem',
                        fontWeight: 500,
                        color: CONTENT_COLORS.primaryText,
                        marginBottom: '4px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {activity.contentTitle}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: CONTENT_COLORS.secondaryText }}>
                      {activity.action} by {activity.actorName}
                    </div>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: CONTENT_COLORS.tertiaryText, flexShrink: 0 }}>
                    {formatContentDateTime(activity.timestamp)}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Upcoming Scheduled Posts */}
        <div
          style={{
            backgroundColor: CONTENT_COLORS.cardBg,
            borderRadius: '12px',
            border: `1px solid ${CONTENT_COLORS.border}`,
            padding: '20px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <h2 style={{ fontSize: '1rem', fontWeight: 600, color: CONTENT_COLORS.primaryText, margin: 0 }}>
              {t('dashboard.upcomingPosts')}
            </h2>
            <button
              onClick={() => onNavigate && onNavigate('linkedin')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                background: 'none',
                border: 'none',
                color: CONTENT_COLORS.primary,
                fontSize: '0.875rem',
                cursor: 'pointer',
              }}
            >
              View All <ArrowRight size={14} />
            </button>
          </div>

          {scheduledPosts.length === 0 ? (
            <div
              style={{
                padding: '40px',
                textAlign: 'center',
                color: CONTENT_COLORS.secondaryText,
              }}
            >
              No scheduled posts
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {scheduledPosts.map((post) => (
                <div
                  key={post.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px',
                    borderRadius: '8px',
                    border: `1px solid ${CONTENT_COLORS.border}`,
                  }}
                >
                  <div
                    style={{
                      width: '40px',
                      height: '40px',
                      borderRadius: '8px',
                      backgroundColor: `${CONTENT_COLORS.linkedinPost}15`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: CONTENT_COLORS.linkedinPost,
                      flexShrink: 0,
                    }}
                  >
                    {post.platform === 'linkedin' ? <Linkedin size={20} /> : <Layout size={20} />}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div
                      style={{
                        fontSize: '0.875rem',
                        fontWeight: 500,
                        color: CONTENT_COLORS.primaryText,
                        marginBottom: '4px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {post.title}
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Calendar size={12} color={CONTENT_COLORS.tertiaryText} />
                      <span style={{ fontSize: '0.75rem', color: CONTENT_COLORS.secondaryText }}>
                        {formatContentDateTime(post.scheduledTime)}
                      </span>
                    </div>
                  </div>
                  <ContentStatusBadge status="scheduled" size="sm" />
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MarketingDashboard;
