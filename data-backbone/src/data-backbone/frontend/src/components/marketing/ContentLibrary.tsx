import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Plus, Grid, List, FileText } from 'lucide-react';
import type { Content, ContentType, ContentStatus, ContentCategory } from '../../types/content';
import { CONTENT_COLORS } from '../../constants/content';
import { api } from '../../services/api';
import { ContentCard, ContentFilters } from './shared';

interface ContentLibraryProps {
  onNavigate?: (page: string) => void;
}

const ContentLibrary: React.FC<ContentLibraryProps> = ({ onNavigate }) => {
  const { t } = useTranslation('marketing');
  const [content, setContent] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [filters, setFilters] = useState<{
    contentType?: ContentType;
    status?: ContentStatus;
    category?: ContentCategory;
    search?: string;
  }>({});
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const pageSize = 20;

  useEffect(() => {
    loadContent();
  }, [filters, page]);

  const loadContent = async () => {
    setLoading(true);
    try {
      const result = await api.getContentList({
        content_type: filters.contentType,
        status: filters.status,
        category: filters.category,
        search: filters.search,
        page,
        page_size: pageSize,
      });
      setContent(result.items as Content[]);
      setTotal(result.total);
    } catch (error) {
      console.error('Failed to load content:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (contentId: string) => {
    // Navigate to edit page based on content type
    console.log('Edit content:', contentId);
  };

  const handleDelete = async (contentId: string) => {
    if (window.confirm(t('confirmations.delete'))) {
      try {
        await api.deleteContent(contentId);
        loadContent();
      } catch (error) {
        console.error('Failed to delete content:', error);
      }
    }
  };

  const handleArchive = async (contentId: string) => {
    try {
      await api.archiveContent(contentId);
      loadContent();
    } catch (error) {
      console.error('Failed to archive content:', error);
    }
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: CONTENT_COLORS.primaryText, margin: 0 }}>
            {t('contentLibrary.title')}
          </h1>
          <p style={{ fontSize: '0.875rem', color: CONTENT_COLORS.secondaryText, marginTop: '4px' }}>
            {t('contentLibrary.subtitle')}
          </p>
        </div>
        <button
          onClick={() => onNavigate && onNavigate('linkedin')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '10px 20px',
            borderRadius: '8px',
            border: 'none',
            backgroundColor: CONTENT_COLORS.primary,
            color: '#fff',
            fontSize: '0.875rem',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          <Plus size={18} />
          {t('contentLibrary.createContent')}
        </button>
      </div>

      {/* Filters */}
      <div style={{ marginBottom: '20px' }}>
        <ContentFilters filters={filters} onChange={setFilters} />
      </div>

      {/* View Toggle & Results Count */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <span style={{ fontSize: '0.875rem', color: CONTENT_COLORS.secondaryText }}>
          {total} {total === 1 ? 'item' : 'items'}
        </span>
        <div style={{ display: 'flex', gap: '4px' }}>
          <button
            onClick={() => setViewMode('grid')}
            style={{
              padding: '8px',
              borderRadius: '6px',
              border: `1px solid ${viewMode === 'grid' ? CONTENT_COLORS.primary : CONTENT_COLORS.border}`,
              backgroundColor: viewMode === 'grid' ? `${CONTENT_COLORS.primary}10` : CONTENT_COLORS.cardBg,
              color: viewMode === 'grid' ? CONTENT_COLORS.primary : CONTENT_COLORS.secondaryText,
              cursor: 'pointer',
            }}
          >
            <Grid size={18} />
          </button>
          <button
            onClick={() => setViewMode('list')}
            style={{
              padding: '8px',
              borderRadius: '6px',
              border: `1px solid ${viewMode === 'list' ? CONTENT_COLORS.primary : CONTENT_COLORS.border}`,
              backgroundColor: viewMode === 'list' ? `${CONTENT_COLORS.primary}10` : CONTENT_COLORS.cardBg,
              color: viewMode === 'list' ? CONTENT_COLORS.primary : CONTENT_COLORS.secondaryText,
              cursor: 'pointer',
            }}
          >
            <List size={18} />
          </button>
        </div>
      </div>

      {/* Content Grid/List */}
      {loading ? (
        <div
          style={{
            padding: '60px',
            textAlign: 'center',
            color: CONTENT_COLORS.secondaryText,
          }}
        >
          Loading...
        </div>
      ) : content.length === 0 ? (
        <div
          style={{
            padding: '60px',
            textAlign: 'center',
            backgroundColor: CONTENT_COLORS.cardBg,
            borderRadius: '12px',
            border: `1px solid ${CONTENT_COLORS.border}`,
          }}
        >
          <FileText size={48} color={CONTENT_COLORS.tertiaryText} style={{ marginBottom: '16px' }} />
          <h3 style={{ margin: 0, marginBottom: '8px', color: CONTENT_COLORS.primaryText }}>
            {t('contentLibrary.emptyState.title')}
          </h3>
          <p style={{ margin: 0, marginBottom: '20px', color: CONTENT_COLORS.secondaryText }}>
            {t('contentLibrary.emptyState.description')}
          </p>
          <button
            onClick={() => onNavigate && onNavigate('linkedin')}
            style={{
              padding: '10px 20px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: CONTENT_COLORS.primary,
              color: '#fff',
              fontSize: '0.875rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            {t('contentLibrary.emptyState.action')}
          </button>
        </div>
      ) : viewMode === 'grid' ? (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '16px',
          }}
        >
          {content.map((item) => (
            <ContentCard
              key={item.id}
              content={item}
              onClick={() => handleEdit(item.id)}
              onEdit={() => handleEdit(item.id)}
              onDelete={() => handleDelete(item.id)}
              onArchive={() => handleArchive(item.id)}
            />
          ))}
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {content.map((item) => (
            <ContentCard
              key={item.id}
              content={item}
              onClick={() => handleEdit(item.id)}
              onEdit={() => handleEdit(item.id)}
              onDelete={() => handleDelete(item.id)}
              onArchive={() => handleArchive(item.id)}
              compact
            />
          ))}
        </div>
      )}

      {/* Pagination */}
      {total > pageSize && (
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '8px',
            marginTop: '24px',
          }}
        >
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 1}
            style={{
              padding: '8px 16px',
              borderRadius: '6px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              backgroundColor: CONTENT_COLORS.cardBg,
              color: page === 1 ? CONTENT_COLORS.tertiaryText : CONTENT_COLORS.primaryText,
              cursor: page === 1 ? 'not-allowed' : 'pointer',
            }}
          >
            Previous
          </button>
          <span
            style={{
              padding: '8px 16px',
              color: CONTENT_COLORS.secondaryText,
            }}
          >
            Page {page} of {Math.ceil(total / pageSize)}
          </span>
          <button
            onClick={() => setPage(page + 1)}
            disabled={page >= Math.ceil(total / pageSize)}
            style={{
              padding: '8px 16px',
              borderRadius: '6px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              backgroundColor: CONTENT_COLORS.cardBg,
              color: page >= Math.ceil(total / pageSize) ? CONTENT_COLORS.tertiaryText : CONTENT_COLORS.primaryText,
              cursor: page >= Math.ceil(total / pageSize) ? 'not-allowed' : 'pointer',
            }}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default ContentLibrary;
