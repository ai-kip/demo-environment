import React from 'react';
import { useTranslation } from 'react-i18next';
import { Calendar, Eye, MoreVertical, Edit, Trash2, Archive, Copy } from 'lucide-react';
import type { Content, ContentType, ContentStatus } from '../../../types/content';
import {
  CONTENT_COLORS,
  CONTENT_TYPE_CONFIG,
  CONTENT_STATUS_CONFIG,
  formatContentDate,
} from '../../../constants/content';

interface ContentCardProps {
  content: Content;
  onClick?: () => void;
  onEdit?: () => void;
  onDelete?: () => void;
  onArchive?: () => void;
  onDuplicate?: () => void;
  compact?: boolean;
}

const ContentCard: React.FC<ContentCardProps> = ({
  content,
  onClick,
  onEdit,
  onDelete,
  onArchive,
  onDuplicate,
  compact = false,
}) => {
  const { t } = useTranslation('marketing');
  const [showMenu, setShowMenu] = React.useState(false);

  const typeConfig = CONTENT_TYPE_CONFIG[content.content_type];
  const statusConfig = CONTENT_STATUS_CONFIG[content.status];

  const handleMenuClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowMenu(!showMenu);
  };

  const handleAction = (action: () => void | undefined) => {
    return (e: React.MouseEvent) => {
      e.stopPropagation();
      setShowMenu(false);
      if (action) action();
    };
  };

  return (
    <div
      style={{
        backgroundColor: CONTENT_COLORS.cardBg,
        borderRadius: '8px',
        border: `1px solid ${CONTENT_COLORS.border}`,
        padding: compact ? '12px' : '16px',
        cursor: onClick ? 'pointer' : 'default',
        transition: 'all 0.2s ease',
        position: 'relative',
      }}
      onClick={onClick}
      onMouseEnter={(e) => {
        (e.currentTarget as HTMLElement).style.boxShadow = '0 4px 12px rgba(0,0,0,0.08)';
        (e.currentTarget as HTMLElement).style.borderColor = CONTENT_COLORS.primary;
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLElement).style.boxShadow = 'none';
        (e.currentTarget as HTMLElement).style.borderColor = CONTENT_COLORS.border;
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Content Type Badge */}
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              padding: '4px 8px',
              borderRadius: '4px',
              backgroundColor: `${typeConfig.color}15`,
              color: typeConfig.color,
              fontSize: '0.75rem',
              fontWeight: 500,
            }}
          >
            {typeConfig.label}
          </span>

          {/* Status Badge */}
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              padding: '4px 8px',
              borderRadius: '4px',
              backgroundColor: statusConfig.bgColor,
              color: statusConfig.color,
              fontSize: '0.75rem',
              fontWeight: 500,
            }}
          >
            {statusConfig.label}
          </span>
        </div>

        {/* Actions Menu */}
        {(onEdit || onDelete || onArchive || onDuplicate) && (
          <div style={{ position: 'relative' }}>
            <button
              onClick={handleMenuClick}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '4px',
                borderRadius: '4px',
                color: CONTENT_COLORS.secondaryText,
              }}
            >
              <MoreVertical size={16} />
            </button>

            {showMenu && (
              <div
                style={{
                  position: 'absolute',
                  right: 0,
                  top: '100%',
                  backgroundColor: CONTENT_COLORS.cardBg,
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  borderRadius: '6px',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                  minWidth: '140px',
                  zIndex: 10,
                }}
              >
                {onEdit && (
                  <button
                    onClick={handleAction(onEdit)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      width: '100%',
                      padding: '8px 12px',
                      border: 'none',
                      background: 'none',
                      cursor: 'pointer',
                      fontSize: '0.875rem',
                      color: CONTENT_COLORS.primaryText,
                      textAlign: 'left',
                    }}
                  >
                    <Edit size={14} />
                    {t('actions.edit')}
                  </button>
                )}
                {onDuplicate && (
                  <button
                    onClick={handleAction(onDuplicate)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      width: '100%',
                      padding: '8px 12px',
                      border: 'none',
                      background: 'none',
                      cursor: 'pointer',
                      fontSize: '0.875rem',
                      color: CONTENT_COLORS.primaryText,
                      textAlign: 'left',
                    }}
                  >
                    <Copy size={14} />
                    {t('actions.duplicate')}
                  </button>
                )}
                {onArchive && (
                  <button
                    onClick={handleAction(onArchive)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      width: '100%',
                      padding: '8px 12px',
                      border: 'none',
                      background: 'none',
                      cursor: 'pointer',
                      fontSize: '0.875rem',
                      color: CONTENT_COLORS.primaryText,
                      textAlign: 'left',
                    }}
                  >
                    <Archive size={14} />
                    {t('actions.archive')}
                  </button>
                )}
                {onDelete && (
                  <button
                    onClick={handleAction(onDelete)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      width: '100%',
                      padding: '8px 12px',
                      border: 'none',
                      background: 'none',
                      cursor: 'pointer',
                      fontSize: '0.875rem',
                      color: CONTENT_COLORS.danger,
                      textAlign: 'left',
                    }}
                  >
                    <Trash2 size={14} />
                    {t('actions.delete')}
                  </button>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Title */}
      <h3
        style={{
          margin: 0,
          marginBottom: compact ? '8px' : '12px',
          fontSize: compact ? '0.875rem' : '1rem',
          fontWeight: 600,
          color: CONTENT_COLORS.primaryText,
          lineHeight: 1.4,
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          display: '-webkit-box',
          WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical',
        }}
      >
        {content.title}
      </h3>

      {/* Tags */}
      {!compact && content.tags && content.tags.length > 0 && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginBottom: '12px' }}>
          {content.tags.slice(0, 3).map((tag, index) => (
            <span
              key={index}
              style={{
                padding: '2px 8px',
                borderRadius: '4px',
                backgroundColor: CONTENT_COLORS.background,
                color: CONTENT_COLORS.secondaryText,
                fontSize: '0.75rem',
              }}
            >
              {tag}
            </span>
          ))}
          {content.tags.length > 3 && (
            <span
              style={{
                padding: '2px 8px',
                borderRadius: '4px',
                backgroundColor: CONTENT_COLORS.background,
                color: CONTENT_COLORS.tertiaryText,
                fontSize: '0.75rem',
              }}
            >
              +{content.tags.length - 3}
            </span>
          )}
        </div>
      )}

      {/* Footer */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginTop: 'auto',
          paddingTop: compact ? '8px' : '12px',
          borderTop: `1px solid ${CONTENT_COLORS.border}`,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: CONTENT_COLORS.tertiaryText, fontSize: '0.75rem' }}>
          <Calendar size={12} />
          <span>{formatContentDate(content.updated_at)}</span>
        </div>

        {content.author_name && (
          <span style={{ color: CONTENT_COLORS.tertiaryText, fontSize: '0.75rem' }}>
            {content.author_name}
          </span>
        )}
      </div>
    </div>
  );
};

export default ContentCard;
