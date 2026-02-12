import React from 'react';
import { Edit3, Eye, CheckCircle, Clock, Globe, Archive } from 'lucide-react';
import type { ContentStatus } from '../../../types/content';
import { CONTENT_STATUS_CONFIG } from '../../../constants/content';

interface ContentStatusBadgeProps {
  status: ContentStatus;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
}

const statusIcons: Record<ContentStatus, React.ReactNode> = {
  draft: <Edit3 size={12} />,
  review: <Eye size={12} />,
  approved: <CheckCircle size={12} />,
  scheduled: <Clock size={12} />,
  published: <Globe size={12} />,
  archived: <Archive size={12} />,
};

const ContentStatusBadge: React.FC<ContentStatusBadgeProps> = ({
  status,
  size = 'md',
  showIcon = true,
}) => {
  const config = CONTENT_STATUS_CONFIG[status];

  const sizeStyles = {
    sm: { padding: '2px 6px', fontSize: '0.625rem', iconSize: 10 },
    md: { padding: '4px 8px', fontSize: '0.75rem', iconSize: 12 },
    lg: { padding: '6px 12px', fontSize: '0.875rem', iconSize: 14 },
  };

  const styles = sizeStyles[size];

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '4px',
        padding: styles.padding,
        borderRadius: '4px',
        backgroundColor: config.bgColor,
        color: config.color,
        fontSize: styles.fontSize,
        fontWeight: 500,
        lineHeight: 1,
      }}
    >
      {showIcon && statusIcons[status]}
      <span>{config.label}</span>
    </span>
  );
};

export default ContentStatusBadge;
