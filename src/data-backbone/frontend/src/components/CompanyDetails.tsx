import { useState, useEffect } from 'react';
import { api } from '../services/api';

interface Person {
  id: string;
  full_name: string;
  title?: string;
  department?: string;
}

interface CompanyDetails {
  company: {
    id: string;
    name: string;
    domain: string;
    industry?: string;
    location?: string;
    employee_count?: number;
  } | null;
  people: Person[];
  emails: string[];
}

interface CompanyDetailsProps {
  domain: string;
  onClose: () => void;
}

export default function CompanyDetails({ domain, onClose }: CompanyDetailsProps) {
  const [details, setDetails] = useState<CompanyDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadDetails = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await api.getCompanyByDomain(domain);
        setDetails(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load company details');
      } finally {
        setLoading(false);
      }
    };

    loadDetails();
  }, [domain]);

  if (loading) {
    return (
      <div style={{
        backgroundColor: 'white',
        borderRadius: '0.5rem',
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        padding: '2rem'
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ height: '1.5rem', backgroundColor: '#e5e7eb', borderRadius: '0.25rem', width: '60%' }}></div>
          <div style={{ height: '1rem', backgroundColor: '#e5e7eb', borderRadius: '0.25rem', width: '40%' }}></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        backgroundColor: '#fef2f2',
        border: '1px solid #fecaca',
        borderRadius: '0.5rem',
        padding: '1.5rem',
        marginBottom: '1.5rem'
      }}>
        <p style={{ color: '#dc2626', margin: '0 0 1rem 0' }}>Error: {error}</p>
        <button
          onClick={onClose}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#dc2626',
            color: 'white',
            border: 'none',
            borderRadius: '0.375rem',
            cursor: 'pointer',
            fontSize: '0.875rem'
          }}
        >
          Go Back
        </button>
      </div>
    );
  }

  if (!details || !details.company) {
    return (
      <div style={{
        backgroundColor: 'white',
        borderRadius: '0.5rem',
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        padding: '2rem',
        textAlign: 'center'
      }}>
        <p style={{ color: '#6b7280', margin: '0 0 1rem 0' }}>Company not found</p>
        <button
          onClick={onClose}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '0.375rem',
            cursor: 'pointer',
            fontSize: '0.875rem'
          }}
        >
          Go Back
        </button>
      </div>
    );
  }

  const company = details.company;

  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '0.5rem',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
      padding: '2rem'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1.5rem' }}>
        <div>
          <h3 style={{
            fontSize: '1.5rem',
            fontWeight: '600',
            color: '#111827',
            margin: '0 0 0.5rem 0'
          }}>
            {company.name}
          </h3>
          <p style={{
            fontSize: '0.875rem',
            color: '#6b7280',
            margin: 0
          }}>
            {company.domain}
          </p>
        </div>
        <button
          onClick={onClose}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#f3f4f6',
            color: '#374151',
            border: 'none',
            borderRadius: '0.375rem',
            cursor: 'pointer',
            fontSize: '0.875rem',
            fontWeight: '500'
          }}
        >
          ← Back
        </button>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '2rem',
        paddingBottom: '1.5rem',
        borderBottom: '1px solid #e5e7eb'
      }}>
        {company.industry && (
          <div>
            <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0 0 0.25rem 0' }}>Industry</p>
            <p style={{ fontSize: '0.875rem', color: '#111827', fontWeight: '500', margin: 0 }}>
              {company.industry}
            </p>
          </div>
        )}
        {company.location && (
          <div>
            <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0 0 0.25rem 0' }}>Location</p>
            <p style={{ fontSize: '0.875rem', color: '#111827', fontWeight: '500', margin: 0 }}>
              📍 {company.location}
            </p>
          </div>
        )}
        {company.employee_count !== undefined && (
          <div>
            <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0 0 0.25rem 0' }}>Employees</p>
            <p style={{ fontSize: '0.875rem', color: '#111827', fontWeight: '500', margin: 0 }}>
              👥 {company.employee_count}
            </p>
          </div>
        )}
      </div>

      {details.people && details.people.length > 0 && (
        <div style={{ marginBottom: '2rem' }}>
          <h4 style={{
            fontSize: '1.125rem',
            fontWeight: '600',
            color: '#111827',
            margin: '0 0 1rem 0'
          }}>
            People ({details.people.length})
          </h4>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
            gap: '1rem'
          }}>
            {details.people.map((person, index) => (
              <div
                key={person.id || index}
                style={{
                  padding: '1rem',
                  backgroundColor: '#f9fafb',
                  borderRadius: '0.375rem',
                  border: '1px solid #e5e7eb'
                }}
              >
                <p style={{
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#111827',
                  margin: '0 0 0.5rem 0'
                }}>
                  {person.full_name}
                </p>
                {person.title && (
                  <p style={{
                    fontSize: '0.75rem',
                    color: '#6b7280',
                    margin: '0 0 0.25rem 0'
                  }}>
                    {person.title}
                  </p>
                )}
                {person.department && (
                  <p style={{
                    fontSize: '0.75rem',
                    color: '#6b7280',
                    margin: 0
                  }}>
                    Department: {person.department}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {details.emails && details.emails.length > 0 && (
        <div>
          <h4 style={{
            fontSize: '1.125rem',
            fontWeight: '600',
            color: '#111827',
            margin: '0 0 1rem 0'
          }}>
            Email Addresses ({details.emails.length})
          </h4>
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '0.5rem'
          }}>
            {details.emails.map((email, index) => (
              <a
                key={index}
                href={`mailto:${email}`}
                style={{
                  padding: '0.5rem 0.75rem',
                  backgroundColor: '#eff6ff',
                  color: '#1e40af',
                  borderRadius: '0.375rem',
                  textDecoration: 'none',
                  fontSize: '0.875rem',
                  border: '1px solid #bfdbfe',
                  display: 'inline-block'
                }}
              >
                ✉️ {email}
              </a>
            ))}
          </div>
        </div>
      )}

      {(!details.people || details.people.length === 0) && (!details.emails || details.emails.length === 0) && (
        <p style={{ color: '#6b7280', margin: 0, fontStyle: 'italic' }}>
          No additional information available
        </p>
      )}
    </div>
  );
}

