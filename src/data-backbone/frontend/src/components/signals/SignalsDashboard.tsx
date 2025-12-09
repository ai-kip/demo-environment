import React, { useState, useEffect } from 'react';
import type { HotAccount, SignalEvent, SignalStats } from '../../types/signals';
import {
  SIGNALS_COLORS,
  SIGNALS_TYPOGRAPHY,
  createDemoSignalStats,
  createDemoHotAccounts,
  createDemoRecentSignals,
} from '../../constants/signals';
import SignalOverviewCards from './SignalOverviewCards';
import HotAccountsList from './HotAccountsList';
import RecentSignalsTable from './RecentSignalsTable';
import { api } from '../../services/api';
import type { HotAccount as DbHotAccount } from '../../types/database';

const SignalsDashboard: React.FC = () => {
  const [stats, setStats] = useState<SignalStats>(createDemoSignalStats());
  const [hotAccounts, setHotAccounts] = useState<HotAccount[]>(createDemoHotAccounts());
  const [recentSignals, setRecentSignals] = useState<SignalEvent[]>(createDemoRecentSignals());
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [loading, setLoading] = useState(true);

  // Fetch real data from API
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Fetch hot accounts and signal stats in parallel
        const [hotAccountsData, signalStatsData] = await Promise.all([
          api.getHotAccounts(50, 20).catch(() => [] as DbHotAccount[]),
          api.getSignalStats(30).catch(() => ({})),
        ]);

        // Transform hot accounts from API to local type
        if (hotAccountsData.length > 0) {
          const transformedHotAccounts: HotAccount[] = hotAccountsData.map((account) => ({
            id: account.company.id,
            company_name: account.company.name,
            domain: account.company.domain,
            main_industry: account.company.main_industry,
            hq_city: account.company.hq_city,
            hq_country: account.company.hq_country,
            overall_score: account.company.intent_score || 0,
            intent_category: (account.company.intent_score || 0) >= 80 ? 'hot' :
                            (account.company.intent_score || 0) >= 60 ? 'warm' :
                            (account.company.intent_score || 0) >= 40 ? 'engaged' :
                            (account.company.intent_score || 0) >= 20 ? 'aware' : 'cold',
            score_trend: 'stable',
            active_signal_count: account.signal_count,
            strongest_signal_type: undefined,
            newest_signal_at: account.newest_signal ? new Date(account.newest_signal) : undefined,
            company_narrative: undefined,
            recommended_approach: undefined,
            icp_tier: account.company.icp_tier?.toString(),
            champion: account.champion_name ? {
              id: '',
              name: account.champion_name,
              title: account.champion_title || '',
              score: 80,
            } : undefined,
          }));
          setHotAccounts(transformedHotAccounts);
        }

        // Transform signal stats if available
        if (signalStatsData && typeof signalStatsData === 'object') {
          const statsArray = Array.isArray(signalStatsData) ? signalStatsData : [];
          const totalSignals = statsArray.reduce((sum: number, s: { signal_count?: number }) => sum + (s.signal_count || 0), 0);

          setStats({
            total_signals: totalSignals || stats.total_signals,
            signals_change_percent: 15, // placeholder
            hot_accounts: hotAccountsData.filter((a) => (a.company.intent_score || 0) >= 80).length || stats.hot_accounts,
            hot_accounts_change_percent: 8,
            warm_accounts: hotAccountsData.filter((a) => (a.company.intent_score || 0) >= 60 && (a.company.intent_score || 0) < 80).length || stats.warm_accounts,
            warm_accounts_change_percent: 12,
            new_today: Math.floor(totalSignals / 30) || stats.new_today,
            new_today_change_percent: 5,
          });
        }

        setLastUpdated(new Date());
      } catch (err) {
        console.error('Failed to fetch signals data:', err);
        // Keep using demo data on error
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSelectAccount = (account: HotAccount) => {
    console.log('Selected account:', account);
    // Would navigate to company detail view
  };

  const handleStartSequence = (account: HotAccount) => {
    console.log('Start sequence for:', account);
    // Would open outreach sequence builder
  };

  const handleSelectSignal = (signal: SignalEvent) => {
    console.log('Selected signal:', signal);
    // Would show signal detail modal
  };

  // Simple sparkline visualization
  const renderSparkline = () => {
    const data = [20, 35, 40, 45, 42, 55, 65, 60, 70, 85, 95, 90, 80, 85, 95, 98, 88, 95, 92, 100, 100, 100, 100, 100, 100, 100, 95, 100, 100, 100];
    const max = Math.max(...data);
    const width = 600;
    const height = 40;
    const barWidth = width / data.length - 2;

    return (
      <svg width={width} height={height} style={{ display: 'block' }}>
        {data.map((value, index) => (
          <rect
            key={index}
            x={index * (barWidth + 2)}
            y={height - (value / max) * height}
            width={barWidth}
            height={(value / max) * height}
            fill={SIGNALS_COLORS.primary}
            opacity={0.3 + (index / data.length) * 0.7}
            rx={1}
          />
        ))}
      </svg>
    );
  };

  return (
    <div style={{ padding: '0' }}>
      {/* Header */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '1.5rem',
        }}
      >
        <div>
          <h2 style={{ ...SIGNALS_TYPOGRAPHY.h2, color: SIGNALS_COLORS.primaryText, margin: 0 }}>
            Signals Intelligence
          </h2>
          <p style={{ ...SIGNALS_TYPOGRAPHY.body, color: SIGNALS_COLORS.secondaryText, margin: '0.25rem 0 0 0' }}>
            Monitor buying signals and intent across your target accounts
          </p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span
            style={{
              ...SIGNALS_TYPOGRAPHY.bodySmall,
              color: SIGNALS_COLORS.tertiaryText,
            }}
          >
            Last updated: {Math.floor((Date.now() - lastUpdated.getTime()) / 60000)}m ago
          </span>
          <button
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: SIGNALS_COLORS.cardBg,
              color: SIGNALS_COLORS.primary,
              border: `1px solid ${SIGNALS_COLORS.border}`,
              borderRadius: '0.375rem',
              cursor: 'pointer',
              fontSize: '0.875rem',
              fontWeight: 500,
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <span style={{ fontSize: '1rem' }}>⚙️</span>
            Configure
          </button>
        </div>
      </div>

      {/* Signal Overview Section */}
      <div
        style={{
          backgroundColor: SIGNALS_COLORS.cardBg,
          borderRadius: '0.5rem',
          border: `1px solid ${SIGNALS_COLORS.border}`,
          padding: '1.5rem',
          marginBottom: '1.5rem',
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '1rem',
          }}
        >
          <h3 style={{ ...SIGNALS_TYPOGRAPHY.h4, color: SIGNALS_COLORS.primaryText, margin: 0 }}>
            Signal Overview
          </h3>
          <span style={{ ...SIGNALS_TYPOGRAPHY.bodySmall, color: SIGNALS_COLORS.tertiaryText }}>
            Past 30 days
          </span>
        </div>

        <SignalOverviewCards stats={stats} />

        {/* Trend Chart */}
        <div style={{ marginTop: '1.5rem' }}>
          <div style={{ ...SIGNALS_TYPOGRAPHY.bodySmall, color: SIGNALS_COLORS.secondaryText, marginBottom: '0.5rem' }}>
            Signal Trend (30 days)
          </div>
          <div style={{ overflowX: 'auto' }}>
            {renderSparkline()}
          </div>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: '0.25rem',
              ...SIGNALS_TYPOGRAPHY.bodySmall,
              color: SIGNALS_COLORS.tertiaryText,
            }}
          >
            <span>Week 1</span>
            <span>Week 2</span>
            <span>Week 3</span>
            <span>Week 4</span>
          </div>
        </div>
      </div>

      {/* Two Column Layout */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '1.5rem',
          marginBottom: '1.5rem',
        }}
      >
        {/* Hot Accounts */}
        <HotAccountsList
          accounts={hotAccounts}
          onSelectAccount={handleSelectAccount}
          onStartSequence={handleStartSequence}
        />

        {/* Category Breakdown */}
        <div
          style={{
            backgroundColor: SIGNALS_COLORS.cardBg,
            borderRadius: '0.5rem',
            border: `1px solid ${SIGNALS_COLORS.border}`,
            padding: '1.5rem',
          }}
        >
          <h3 style={{ ...SIGNALS_TYPOGRAPHY.h4, color: SIGNALS_COLORS.primaryText, margin: '0 0 1rem 0' }}>
            Signal Categories
          </h3>

          {[
            { label: 'Direct Engagement', score: 847, color: SIGNALS_COLORS.engagement, icon: '🎯' },
            { label: 'Sustainability', score: 523, color: SIGNALS_COLORS.sustainability, icon: '🌱' },
            { label: 'Growth & Expansion', score: 412, color: SIGNALS_COLORS.growth, icon: '📈' },
            { label: 'Workplace Experience', score: 389, color: SIGNALS_COLORS.workplace, icon: '🏢' },
            { label: 'Employee Wellbeing', score: 276, color: SIGNALS_COLORS.wellbeing, icon: '💚' },
          ].map((category, index) => (
            <div
              key={index}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.75rem 0',
                borderBottom: index < 4 ? `1px solid ${SIGNALS_COLORS.border}` : 'none',
              }}
            >
              <span style={{ fontSize: '1.25rem' }}>{category.icon}</span>
              <div style={{ flex: 1 }}>
                <div style={{ ...SIGNALS_TYPOGRAPHY.body, color: SIGNALS_COLORS.primaryText }}>
                  {category.label}
                </div>
                <div
                  style={{
                    marginTop: '0.25rem',
                    height: '4px',
                    backgroundColor: SIGNALS_COLORS.background,
                    borderRadius: '2px',
                    overflow: 'hidden',
                  }}
                >
                  <div
                    style={{
                      width: `${(category.score / 847) * 100}%`,
                      height: '100%',
                      backgroundColor: category.color,
                      borderRadius: '2px',
                    }}
                  />
                </div>
              </div>
              <span
                style={{
                  ...SIGNALS_TYPOGRAPHY.body,
                  fontWeight: 600,
                  color: SIGNALS_COLORS.primaryText,
                }}
              >
                {category.score}
              </span>
            </div>
          ))}

          <div style={{ marginTop: '1rem' }}>
            <button
              style={{
                width: '100%',
                padding: '0.75rem',
                backgroundColor: 'transparent',
                color: SIGNALS_COLORS.primary,
                border: `1px solid ${SIGNALS_COLORS.primary}`,
                borderRadius: '0.375rem',
                cursor: 'pointer',
                fontSize: '0.875rem',
                fontWeight: 500,
              }}
            >
              View Detailed Analytics
            </button>
          </div>
        </div>
      </div>

      {/* Recent Signals Table */}
      <RecentSignalsTable
        signals={recentSignals}
        onSelectSignal={handleSelectSignal}
      />
    </div>
  );
};

export default SignalsDashboard;
