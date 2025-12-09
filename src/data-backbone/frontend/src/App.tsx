import { useState } from 'react'
import HealthStatus from './components/HealthStatus'
import CompanyList from './components/CompanyList'
import PeopleList from './components/PeopleList'
import Search from './components/Search'
import Login from './components/Login'
import DarkModeToggle from './components/DarkModeToggle'
import { LeadsDashboard } from './components/leads'
import { BowtieDashboard } from './components/bowtie'
import { OutreachSequences } from './components/outreach'
import { SignalsDashboard } from './components/signals'
import { AppLayout } from './components/layout'
import { DealDetail } from './components/deals'
import { api } from './services/api'
import { useDarkMode } from './context/DarkModeContext'

type Page = 'dashboard' | 'pipeline' | 'leads' | 'deals' | 'deal-detail' | 'contacts' | 'signals' | 'intent' | 'sequences' | 'analytics' | 'settings' | 'help'

function App() {
  const { isDarkMode } = useDarkMode()
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return sessionStorage.getItem('isAuthenticated') === 'true'
  })
  const [currentPage, setCurrentPage] = useState<Page>('dashboard')
  const [searchQuery, setSearchQuery] = useState('')
  const [useGoogle, setUseGoogle] = useState(true)
  const [useHunter, setUseHunter] = useState(false)
  const [limit, setLimit] = useState(10)
  const [ingesting, setIngesting] = useState(false)
  const [ingestStatus, setIngestStatus] = useState<string | null>(null)
  const [selectedDealId, setSelectedDealId] = useState<string | null>(null)

  const handleViewDeal = (dealId: string) => {
    setSelectedDealId(dealId)
    setCurrentPage('deal-detail')
  }

  const handleBackFromDeal = () => {
    setSelectedDealId(null)
    setCurrentPage('deals')
  }

  const handleIngest = async () => {
    if (!searchQuery.trim()) {
      setIngestStatus('Please enter a search query')
      return
    }

    try {
      setIngesting(true)
      setIngestStatus('Loading data...')

      const result = await api.ingestCompanies(
        searchQuery.trim(),
        limit,
        useGoogle,
        useHunter,
        true,
        true
      )

      if (result.error || !result.success) {
        setIngestStatus(`Error: ${result.error || 'Unknown error'}`)
      } else {
        setIngestStatus(`Loaded! Batch: ${result.batch_id || 'N/A'}`)
        setTimeout(() => {
          window.location.reload()
        }, 2000)
      }
    } catch (err) {
      setIngestStatus(`Error: ${err instanceof Error ? err.message : 'Unknown error'}`)
    } finally {
      setIngesting(false)
    }
  }

  const handleLogin = () => {
    setIsAuthenticated(true)
    sessionStorage.setItem('isAuthenticated', 'true')
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />
  }

  // Render page content based on current page
  const renderPageContent = () => {
    switch (currentPage) {
      case 'dashboard':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Dashboard</h1>
                <p className="page-subtitle">Good morning, Hugo. Here's your pipeline overview.</p>
              </div>
              <div className="page-actions">
                <DarkModeToggle />
              </div>
            </div>
            <BowtieDashboard />

            {/* Search Companies Block */}
            <div className="card" style={{ marginTop: '24px' }}>
              <div className="card-header">
                <h3 className="card-title">Search Companies</h3>
              </div>
              <div className="card-content">
                <div className="input-wrapper" style={{ marginBottom: '16px' }}>
                  <input
                    type="text"
                    className="input"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="e.g., 'HR companies in Austin' or 'tech companies in San Francisco'"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && !ingesting) {
                        handleIngest()
                      }
                    }}
                  />
                </div>

                <div style={{ display: 'flex', gap: '24px', marginBottom: '16px', flexWrap: 'wrap' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={useGoogle}
                      onChange={(e) => setUseGoogle(e.target.checked)}
                      disabled={ingesting}
                    />
                    <span className="text-body-sm">Google Places</span>
                  </label>

                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={useHunter}
                      onChange={(e) => setUseHunter(e.target.checked)}
                      disabled={ingesting || !useGoogle}
                    />
                    <span className="text-body-sm">Hunter.io (enrich with people)</span>
                  </label>

                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className="text-body-sm">Limit:</span>
                    <input
                      type="number"
                      min="1"
                      max="50"
                      value={limit}
                      onChange={(e) => setLimit(parseInt(e.target.value) || 10)}
                      disabled={ingesting}
                      className="input"
                      style={{ width: '80px' }}
                    />
                  </label>
                </div>

                <button
                  className={`btn ${ingesting || !searchQuery.trim() || !useGoogle ? 'btn-secondary' : 'btn-primary'}`}
                  onClick={handleIngest}
                  disabled={ingesting || !searchQuery.trim() || !useGoogle}
                  style={{ width: '100%' }}
                >
                  {ingesting ? 'Loading...' : 'Load Companies'}
                </button>

                {ingestStatus && (
                  <div className={`badge ${ingestStatus.includes('Loaded') ? 'badge-green' : ingestStatus.includes('Error') ? 'badge-red' : 'badge-amber'}`} style={{ marginTop: '16px', display: 'block', textAlign: 'center', padding: '12px' }}>
                    {ingestStatus}
                  </div>
                )}
              </div>
            </div>
          </div>
        )

      case 'pipeline':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Pipeline</h1>
                <p className="page-subtitle">Manage your sales pipeline and track deal progress.</p>
              </div>
              <div className="page-actions">
                <DarkModeToggle />
              </div>
            </div>
            <BowtieDashboard />
          </div>
        )

      case 'leads':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Leads</h1>
                <p className="page-subtitle">12 new leads requiring attention.</p>
              </div>
              <div className="page-actions">
                <button className="btn btn-primary">Add Lead</button>
                <DarkModeToggle />
              </div>
            </div>
            <LeadsDashboard />
          </div>
        )

      case 'deals':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Deals</h1>
                <p className="page-subtitle">47 active deals in your pipeline.</p>
              </div>
              <div className="page-actions">
                <button className="btn btn-primary">Add Deal</button>
                <button className="btn btn-secondary" onClick={() => handleViewDeal('demo')}>
                  View Demo Deal
                </button>
                <DarkModeToggle />
              </div>
            </div>
            <CompanyList />
          </div>
        )

      case 'deal-detail':
        return <DealDetail onBack={handleBackFromDeal} />

      case 'contacts':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Contacts</h1>
                <p className="page-subtitle">Manage your contacts and buying committees.</p>
              </div>
              <div className="page-actions">
                <button className="btn btn-primary">Add Contact</button>
                <DarkModeToggle />
              </div>
            </div>
            <PeopleList />
          </div>
        )

      case 'signals':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Signals Intelligence</h1>
                <p className="page-subtitle">Track buying signals and intent data across your accounts.</p>
              </div>
              <div className="page-actions">
                <DarkModeToggle />
              </div>
            </div>
            <SignalsDashboard />
          </div>
        )

      case 'intent':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Intent Data</h1>
                <p className="page-subtitle">Monitor buyer intent signals and engagement patterns.</p>
              </div>
              <div className="page-actions">
                <DarkModeToggle />
              </div>
            </div>
            <SignalsDashboard />
          </div>
        )

      case 'sequences':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Outreach Sequences</h1>
                <p className="page-subtitle">Create and manage automated outreach campaigns.</p>
              </div>
              <div className="page-actions">
                <button className="btn btn-primary">Create Sequence</button>
                <DarkModeToggle />
              </div>
            </div>
            <OutreachSequences />
          </div>
        )

      case 'analytics':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Analytics</h1>
                <p className="page-subtitle">Measure performance and track key metrics.</p>
              </div>
              <div className="page-actions">
                <DarkModeToggle />
              </div>
            </div>
            <LeadsDashboard />
          </div>
        )

      case 'settings':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Settings</h1>
                <p className="page-subtitle">Configure your account and preferences.</p>
              </div>
              <div className="page-actions">
                <DarkModeToggle />
              </div>
            </div>
            <div className="card">
              <div className="card-content">
                <h3 style={{ marginBottom: '16px' }}>API Status</h3>
                <HealthStatus />
              </div>
            </div>
            <div className="card" style={{ marginTop: '24px' }}>
              <div className="card-content">
                <h3 style={{ marginBottom: '16px' }}>Search</h3>
                <Search />
              </div>
            </div>
          </div>
        )

      case 'help':
        return (
          <div>
            <div className="page-header">
              <div>
                <h1 className="page-title">Help & Support</h1>
                <p className="page-subtitle">Get help with using Duinrell.</p>
              </div>
              <div className="page-actions">
                <DarkModeToggle />
              </div>
            </div>
            <div className="card">
              <div className="card-content">
                <h3 style={{ marginBottom: '16px' }}>Documentation</h3>
                <p>Contact support at support@duinrell.com</p>
              </div>
            </div>
          </div>
        )

      default:
        return <BowtieDashboard />
    }
  }

  const handleNavigate = (page: string) => {
    setCurrentPage(page as Page)
  }

  return (
    <div data-theme={isDarkMode ? 'dark' : 'light'}>
      <AppLayout currentPage={currentPage} onNavigate={handleNavigate}>
        {renderPageContent()}
      </AppLayout>
    </div>
  )
}

export default App
