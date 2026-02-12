import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Link2, X, Search, CheckCircle } from 'lucide-react';
import type { Content, ContentType } from '../../../types/content';
import { CONTENT_COLORS, CONTENT_TYPE_CONFIG, formatContentDate } from '../../../constants/content';
import { SEQUENCE_CONTENT_MERGE_FIELDS } from '../../../constants/marketing';
import { api } from '../../../services/api';

interface ContentSequenceLinkerProps {
  sequenceId: string;
  stepId: string;
  onLinked: (contentId: string) => void;
  onClose: () => void;
}

const ContentSequenceLinker: React.FC<ContentSequenceLinkerProps> = ({
  sequenceId,
  stepId,
  onLinked,
  onClose,
}) => {
  const { t } = useTranslation('marketing');
  const [content, setContent] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<ContentType | ''>('');
  const [selectedContentId, setSelectedContentId] = useState<string | null>(null);
  const [linking, setLinking] = useState(false);

  useEffect(() => {
    loadContent();
  }, [selectedType]);

  const loadContent = async () => {
    setLoading(true);
    try {
      const result = await api.getContentForSequences(selectedType || undefined, 50);
      setContent(result.items as Content[]);
    } catch (error) {
      console.error('Failed to load content:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLink = async () => {
    if (!selectedContentId) return;

    setLinking(true);
    try {
      await api.linkContentToSequence(selectedContentId, sequenceId, stepId);
      onLinked(selectedContentId);
    } catch (error) {
      console.error('Failed to link content:', error);
    } finally {
      setLinking(false);
    }
  };

  const filteredContent = content.filter((item) => {
    if (searchQuery) {
      return item.title.toLowerCase().includes(searchQuery.toLowerCase());
    }
    return true;
  });

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '20px',
      }}
      onClick={onClose}
    >
      <div
        style={{
          backgroundColor: CONTENT_COLORS.cardBg,
          borderRadius: '12px',
          width: '100%',
          maxWidth: '600px',
          maxHeight: '80vh',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '16px 20px',
            borderBottom: `1px solid ${CONTENT_COLORS.border}`,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Link2 size={20} color={CONTENT_COLORS.primary} />
            <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 600, color: CONTENT_COLORS.primaryText }}>
              {t('sequenceIntegration.title')}
            </h3>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '4px',
              color: CONTENT_COLORS.secondaryText,
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Filters */}
        <div style={{ padding: '16px 20px', borderBottom: `1px solid ${CONTENT_COLORS.border}` }}>
          <div style={{ display: 'flex', gap: '12px' }}>
            {/* Search */}
            <div style={{ position: 'relative', flex: 1 }}>
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
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search content..."
                style={{
                  width: '100%',
                  padding: '8px 12px 8px 36px',
                  borderRadius: '6px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  fontSize: '0.875rem',
                }}
              />
            </div>

            {/* Type Filter */}
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value as ContentType | '')}
              style={{
                padding: '8px 12px',
                borderRadius: '6px',
                border: `1px solid ${CONTENT_COLORS.border}`,
                fontSize: '0.875rem',
                minWidth: '150px',
              }}
            >
              <option value="">All Types</option>
              {Object.entries(CONTENT_TYPE_CONFIG).map(([type, config]) => (
                <option key={type} value={type}>
                  {config.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Content List */}
        <div style={{ flex: 1, overflow: 'auto', padding: '8px 20px' }}>
          {loading ? (
            <div style={{ padding: '40px', textAlign: 'center', color: CONTENT_COLORS.secondaryText }}>
              Loading content...
            </div>
          ) : filteredContent.length === 0 ? (
            <div style={{ padding: '40px', textAlign: 'center', color: CONTENT_COLORS.secondaryText }}>
              No publishable content found
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '8px 0' }}>
              {filteredContent.map((item) => {
                const typeConfig = CONTENT_TYPE_CONFIG[item.content_type];
                const isSelected = selectedContentId === item.id;

                return (
                  <button
                    key={item.id}
                    onClick={() => setSelectedContentId(isSelected ? null : item.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '12px',
                      borderRadius: '8px',
                      border: `2px solid ${isSelected ? CONTENT_COLORS.primary : CONTENT_COLORS.border}`,
                      backgroundColor: isSelected ? `${CONTENT_COLORS.primary}08` : CONTENT_COLORS.cardBg,
                      cursor: 'pointer',
                      textAlign: 'left',
                      width: '100%',
                    }}
                  >
                    {/* Selection Indicator */}
                    <div
                      style={{
                        width: '20px',
                        height: '20px',
                        borderRadius: '50%',
                        border: `2px solid ${isSelected ? CONTENT_COLORS.primary : CONTENT_COLORS.border}`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        backgroundColor: isSelected ? CONTENT_COLORS.primary : 'transparent',
                        flexShrink: 0,
                      }}
                    >
                      {isSelected && <CheckCircle size={14} color="#fff" />}
                    </div>

                    {/* Content Info */}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                        <span
                          style={{
                            padding: '2px 6px',
                            borderRadius: '4px',
                            backgroundColor: `${typeConfig.color}15`,
                            color: typeConfig.color,
                            fontSize: '0.625rem',
                            fontWeight: 500,
                          }}
                        >
                          {typeConfig.label}
                        </span>
                      </div>
                      <div
                        style={{
                          fontSize: '0.875rem',
                          fontWeight: 500,
                          color: CONTENT_COLORS.primaryText,
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {item.title}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: CONTENT_COLORS.tertiaryText, marginTop: '2px' }}>
                        {formatContentDate(item.published_at || item.updated_at)}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Merge Fields Info */}
        <div
          style={{
            padding: '12px 20px',
            borderTop: `1px solid ${CONTENT_COLORS.border}`,
            backgroundColor: CONTENT_COLORS.background,
          }}
        >
          <div style={{ fontSize: '0.75rem', fontWeight: 500, color: CONTENT_COLORS.secondaryText, marginBottom: '8px' }}>
            {t('sequenceIntegration.mergeFields')}
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {SEQUENCE_CONTENT_MERGE_FIELDS.map((field) => (
              <code
                key={field.field}
                style={{
                  padding: '4px 8px',
                  borderRadius: '4px',
                  backgroundColor: CONTENT_COLORS.cardBg,
                  fontSize: '0.75rem',
                  color: CONTENT_COLORS.primary,
                  border: `1px solid ${CONTENT_COLORS.border}`,
                }}
              >
                {field.field}
              </code>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '12px',
            padding: '16px 20px',
            borderTop: `1px solid ${CONTENT_COLORS.border}`,
          }}
        >
          <button
            onClick={onClose}
            style={{
              padding: '10px 20px',
              borderRadius: '6px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              backgroundColor: CONTENT_COLORS.cardBg,
              color: CONTENT_COLORS.primaryText,
              fontSize: '0.875rem',
              cursor: 'pointer',
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleLink}
            disabled={!selectedContentId || linking}
            style={{
              padding: '10px 20px',
              borderRadius: '6px',
              border: 'none',
              backgroundColor: CONTENT_COLORS.primary,
              color: '#fff',
              fontSize: '0.875rem',
              fontWeight: 500,
              cursor: 'pointer',
              opacity: !selectedContentId || linking ? 0.5 : 1,
            }}
          >
            {linking ? 'Linking...' : t('sequenceIntegration.linkContent')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ContentSequenceLinker;
