import { useState, useEffect } from 'react';
import { api } from '../services/api';

interface IndustryStat {
  industry: string;
  company_count: number;
  companies: Array<{
    name: string;
    domain: string;
    location?: string;
  }>;
}

export default function Dashboard() {
  const [industries, setIndustries] = useState<IndustryStat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getIndustryAnalytics();
      setIndustries(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    
    const handleDataUpdate = () => {
      loadData();
    };
    window.addEventListener('dataUpdated', handleDataUpdate);
    
    return () => {
      window.removeEventListener('dataUpdated', handleDataUpdate);
    };
  }, []);

  const totalCompanies = industries.reduce((sum, ind) => sum + ind.company_count, 0);

  return (
    <div style={{ maxWidth: '56rem', margin: '0 auto' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.875rem', fontWeight: 'bold', color: '#111827', marginBottom: '0.5rem' }}>
          Dashboard
        </h2>
        <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
          Overview of your data pipeline results
        </p>
      </div>

      {error && (
        <div style={{
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '0.5rem',
          padding: '1rem',
          marginBottom: '1.5rem'
        }}>
          <p style={{ color: '#dc2626', margin: 0, fontSize: '0.875rem' }}>
            Error: {error}
          </p>
        </div>
      )}

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1.25rem',
        marginBottom: '2rem'
      }}>
        <div style={{
          backgroundColor: 'white',
          borderRadius: '0.5rem',
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
          padding: '1.25rem'
        }}>
          <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: '0 0 0.5rem 0' }}>
            Total Companies
          </p>
          {loading ? (
            <div style={{ height: '1.5rem', backgroundColor: '#e5e7eb', borderRadius: '0.25rem', width: '60%' }}></div>
          ) : (
            <p style={{ fontSize: '1.5rem', fontWeight: '600', color: '#111827', margin: 0 }}>
              {totalCompanies.toLocaleString()}
            </p>
          )}
        </div>

        <div style={{
          backgroundColor: 'white',
          borderRadius: '0.5rem',
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
          padding: '1.25rem'
        }}>
          <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: '0 0 0.5rem 0' }}>
            Industries
          </p>
          {loading ? (
            <div style={{ height: '1.5rem', backgroundColor: '#e5e7eb', borderRadius: '0.25rem', width: '60%' }}></div>
          ) : (
            <p style={{ fontSize: '1.5rem', fontWeight: '600', color: '#111827', margin: 0 }}>
              {industries.length}
            </p>
          )}
        </div>

        <div style={{
          backgroundColor: 'white',
          borderRadius: '0.5rem',
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
          padding: '1.25rem'
        }}>
          <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: '0 0 0.5rem 0' }}>
            Top Industry
          </p>
          {loading ? (
            <div style={{ height: '1.5rem', backgroundColor: '#e5e7eb', borderRadius: '0.25rem', width: '60%' }}></div>
          ) : (
            <p style={{ fontSize: '1.5rem', fontWeight: '600', color: '#111827', margin: 0 }}>
              {industries.filter((ind) => ind.industry !== null && ind.industry !== undefined)[0]?.industry || 'N/A'}
            </p>
          )}
        </div>
      </div>

      <div style={{
        backgroundColor: 'white',
        borderRadius: '0.5rem',
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        padding: '1.5rem'
      }}>
        <h3 style={{
          fontSize: '1.125rem',
          fontWeight: '600',
          color: '#111827',
          marginBottom: '1rem'
        }}>
          Top Industries
        </h3>

        {loading ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} style={{
                height: '2rem',
                backgroundColor: '#e5e7eb',
                borderRadius: '0.25rem'
              }}></div>
            ))}
          </div>
        ) : industries.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {industries
              .filter((ind) => ind.industry !== null && ind.industry !== undefined)
              .slice(0, 5)
              .map((industry) => (
                <div key={industry.industry || 'unknown'} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '0.75rem',
                  backgroundColor: '#f9fafb',
                  borderRadius: '0.375rem'
                }}>
                  <span style={{ fontWeight: '500', color: '#111827' }}>
                    {industry.industry || 'Unknown'}
                  </span>
                  <span style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                    {industry.company_count} {industry.company_count === 1 ? 'company' : 'companies'}
                  </span>
                </div>
              ))}
            {industries.filter((ind) => ind.industry === null || ind.industry === undefined).length > 0 && (
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '0.75rem',
                backgroundColor: '#fef3c7',
                borderRadius: '0.375rem',
                border: '1px solid #fde68a'
              }}>
                <span style={{ fontWeight: '500', color: '#92400e' }}>
                  ⚠️ Unclassified
                </span>
                <span style={{ color: '#78350f', fontSize: '0.875rem' }}>
                  {industries.filter((ind) => ind.industry === null || ind.industry === undefined).reduce((sum, ind) => sum + ind.company_count, 0)} companies
                </span>
              </div>
            )}
          </div>
        ) : (
          <p style={{ color: '#6b7280', margin: 0 }}>
            No data available
          </p>
        )}
      </div>
    </div>
  );
}
