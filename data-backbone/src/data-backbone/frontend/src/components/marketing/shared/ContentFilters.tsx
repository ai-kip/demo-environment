import React from 'react';
import { useTranslation } from 'react-i18next';
import { Search, Filter, X } from 'lucide-react';
import type { ContentType, ContentStatus, ContentCategory } from '../../../types/content';
import {
  CONTENT_COLORS,
  CONTENT_TYPE_CONFIG,
  CONTENT_STATUS_CONFIG,
  CONTENT_CATEGORY_CONFIG,
} from '../../../constants/content';

interface ContentFiltersProps {
  filters: {
    contentType?: ContentType;
    status?: ContentStatus;
    category?: ContentCategory;
    search?: string;
  };
  onChange: (filters: {
    contentType?: ContentType;
    status?: ContentStatus;
    category?: ContentCategory;
    search?: string;
  }) => void;
  showSearch?: boolean;
  showTypeFilter?: boolean;
  showStatusFilter?: boolean;
  showCategoryFilter?: boolean;
}

const ContentFilters: React.FC<ContentFiltersProps> = ({
  filters,
  onChange,
  showSearch = true,
  showTypeFilter = true,
  showStatusFilter = true,
  showCategoryFilter = true,
}) => {
  const { t } = useTranslation('marketing');

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange({ ...filters, search: e.target.value || undefined });
  };

  const handleTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange({ ...filters, contentType: e.target.value as ContentType || undefined });
  };

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange({ ...filters, status: e.target.value as ContentStatus || undefined });
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange({ ...filters, category: e.target.value as ContentCategory || undefined });
  };

  const clearFilters = () => {
    onChange({});
  };

  const hasActiveFilters = filters.contentType || filters.status || filters.category || filters.search;

  const selectStyle: React.CSSProperties = {
    padding: '8px 12px',
    borderRadius: '6px',
    border: `1px solid ${CONTENT_COLORS.border}`,
    backgroundColor: CONTENT_COLORS.cardBg,
    fontSize: '0.875rem',
    color: CONTENT_COLORS.primaryText,
    cursor: 'pointer',
    minWidth: '140px',
  };

  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        gap: '12px',
        padding: '16px',
        backgroundColor: CONTENT_COLORS.cardBg,
        borderRadius: '8px',
        border: `1px solid ${CONTENT_COLORS.border}`,
      }}
    >
      {/* Search */}
      {showSearch && (
        <div style={{ position: 'relative', flex: '1 1 200px', maxWidth: '300px' }}>
          <Search
            size={16}
            style={{
              position: 'absolute',
              left: '12px',
              top: '50%',
              transform: 'translateY(-50%)',
              color: CONTENT_COLORS.tertiaryText,
            }}
          />
          <input
            type="text"
            placeholder={t('contentLibrary.filters.search', 'Search content...')}
            value={filters.search || ''}
            onChange={handleSearchChange}
            style={{
              width: '100%',
              padding: '8px 12px 8px 36px',
              borderRadius: '6px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              backgroundColor: CONTENT_COLORS.cardBg,
              fontSize: '0.875rem',
              color: CONTENT_COLORS.primaryText,
            }}
          />
        </div>
      )}

      {/* Type Filter */}
      {showTypeFilter && (
        <select
          value={filters.contentType || ''}
          onChange={handleTypeChange}
          style={selectStyle}
        >
          <option value="">{t('contentLibrary.filters.allTypes')}</option>
          {Object.entries(CONTENT_TYPE_CONFIG).map(([type, config]) => (
            <option key={type} value={type}>
              {config.label}
            </option>
          ))}
        </select>
      )}

      {/* Status Filter */}
      {showStatusFilter && (
        <select
          value={filters.status || ''}
          onChange={handleStatusChange}
          style={selectStyle}
        >
          <option value="">{t('contentLibrary.filters.allStatuses')}</option>
          {Object.entries(CONTENT_STATUS_CONFIG).map(([status, config]) => (
            <option key={status} value={status}>
              {config.label}
            </option>
          ))}
        </select>
      )}

      {/* Category Filter */}
      {showCategoryFilter && (
        <select
          value={filters.category || ''}
          onChange={handleCategoryChange}
          style={selectStyle}
        >
          <option value="">{t('contentLibrary.filters.allCategories')}</option>
          {Object.entries(CONTENT_CATEGORY_CONFIG).map(([category, config]) => (
            <option key={category} value={category}>
              {config.label}
            </option>
          ))}
        </select>
      )}

      {/* Clear Filters */}
      {hasActiveFilters && (
        <button
          onClick={clearFilters}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            padding: '8px 12px',
            borderRadius: '6px',
            border: 'none',
            backgroundColor: CONTENT_COLORS.background,
            color: CONTENT_COLORS.secondaryText,
            fontSize: '0.875rem',
            cursor: 'pointer',
          }}
        >
          <X size={14} />
          Clear
        </button>
      )}
    </div>
  );
};

export default ContentFilters;
