import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Sparkles, Loader2, Copy, Check } from 'lucide-react';
import type { ContentType } from '../../../types/content';
import { CONTENT_COLORS, CONTENT_TYPE_CONFIG } from '../../../constants/content';
import { AI_TONE_OPTIONS } from '../../../constants/marketing';
import { api } from '../../../services/api';

interface AIContentGeneratorProps {
  contentType: ContentType;
  onGenerated: (content: Record<string, unknown>) => void;
  onClose?: () => void;
}

const AIContentGenerator: React.FC<AIContentGeneratorProps> = ({
  contentType,
  onGenerated,
  onClose,
}) => {
  const { t } = useTranslation('marketing');
  const [prompt, setPrompt] = useState('');
  const [tone, setTone] = useState<string>('professional');
  const [targetAudience, setTargetAudience] = useState('');
  const [keyPoints, setKeyPoints] = useState<string[]>([]);
  const [newKeyPoint, setNewKeyPoint] = useState('');
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState<Record<string, unknown> | null>(null);
  const [copied, setCopied] = useState(false);

  const typeConfig = CONTENT_TYPE_CONFIG[contentType];

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    try {
      const result = await api.generateContent({
        content_type: contentType,
        prompt: prompt.trim(),
        tone,
        target_audience: targetAudience || undefined,
        key_points: keyPoints.length > 0 ? keyPoints : undefined,
      });

      if (result.success) {
        setGeneratedContent(result.content);
      }
    } catch (error) {
      console.error('Failed to generate content:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddKeyPoint = () => {
    if (newKeyPoint.trim() && keyPoints.length < 5) {
      setKeyPoints([...keyPoints, newKeyPoint.trim()]);
      setNewKeyPoint('');
    }
  };

  const handleRemoveKeyPoint = (index: number) => {
    setKeyPoints(keyPoints.filter((_, i) => i !== index));
  };

  const handleUseContent = () => {
    if (generatedContent) {
      onGenerated(generatedContent);
    }
  };

  const handleCopy = () => {
    if (generatedContent) {
      const contentStr = JSON.stringify(generatedContent, null, 2);
      navigator.clipboard.writeText(contentStr);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div
      style={{
        backgroundColor: CONTENT_COLORS.cardBg,
        borderRadius: '12px',
        border: `1px solid ${CONTENT_COLORS.border}`,
        overflow: 'hidden',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '16px 20px',
          borderBottom: `1px solid ${CONTENT_COLORS.border}`,
          background: `linear-gradient(135deg, ${CONTENT_COLORS.primary}10 0%, ${CONTENT_COLORS.cardBg} 100%)`,
        }}
      >
        <Sparkles size={20} color={CONTENT_COLORS.primary} />
        <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 600, color: CONTENT_COLORS.primaryText }}>
          {t('ai.title')}
        </h3>
        <span
          style={{
            marginLeft: 'auto',
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
      </div>

      <div style={{ padding: '20px' }}>
        {!generatedContent ? (
          <>
            {/* Prompt Input */}
            <div style={{ marginBottom: '16px' }}>
              <label
                style={{
                  display: 'block',
                  marginBottom: '8px',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  color: CONTENT_COLORS.primaryText,
                }}
              >
                {t('ai.prompt')}
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder={t('ai.promptPlaceholder')}
                rows={3}
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  fontSize: '0.875rem',
                  resize: 'vertical',
                  fontFamily: 'inherit',
                }}
              />
            </div>

            {/* Tone Selection */}
            <div style={{ marginBottom: '16px' }}>
              <label
                style={{
                  display: 'block',
                  marginBottom: '8px',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  color: CONTENT_COLORS.primaryText,
                }}
              >
                {t('ai.tone')}
              </label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {AI_TONE_OPTIONS.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setTone(option.value)}
                    style={{
                      padding: '8px 16px',
                      borderRadius: '6px',
                      border: `1px solid ${tone === option.value ? CONTENT_COLORS.primary : CONTENT_COLORS.border}`,
                      backgroundColor: tone === option.value ? `${CONTENT_COLORS.primary}10` : CONTENT_COLORS.cardBg,
                      color: tone === option.value ? CONTENT_COLORS.primary : CONTENT_COLORS.secondaryText,
                      fontSize: '0.875rem',
                      cursor: 'pointer',
                    }}
                  >
                    {t(option.labelKey)}
                  </button>
                ))}
              </div>
            </div>

            {/* Target Audience */}
            <div style={{ marginBottom: '16px' }}>
              <label
                style={{
                  display: 'block',
                  marginBottom: '8px',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  color: CONTENT_COLORS.primaryText,
                }}
              >
                Target Audience (optional)
              </label>
              <input
                type="text"
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
                placeholder="e.g., Marketing managers at B2B SaaS companies"
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  borderRadius: '6px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  fontSize: '0.875rem',
                }}
              />
            </div>

            {/* Key Points */}
            <div style={{ marginBottom: '20px' }}>
              <label
                style={{
                  display: 'block',
                  marginBottom: '8px',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  color: CONTENT_COLORS.primaryText,
                }}
              >
                Key Points to Include (optional)
              </label>
              <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
                <input
                  type="text"
                  value={newKeyPoint}
                  onChange={(e) => setNewKeyPoint(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAddKeyPoint()}
                  placeholder="Add a key point..."
                  style={{
                    flex: 1,
                    padding: '8px 12px',
                    borderRadius: '6px',
                    border: `1px solid ${CONTENT_COLORS.border}`,
                    fontSize: '0.875rem',
                  }}
                />
                <button
                  onClick={handleAddKeyPoint}
                  disabled={!newKeyPoint.trim() || keyPoints.length >= 5}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: CONTENT_COLORS.primary,
                    color: '#fff',
                    fontSize: '0.875rem',
                    cursor: 'pointer',
                    opacity: !newKeyPoint.trim() || keyPoints.length >= 5 ? 0.5 : 1,
                  }}
                >
                  Add
                </button>
              </div>
              {keyPoints.length > 0 && (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {keyPoints.map((point, index) => (
                    <span
                      key={index}
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '4px 10px',
                        borderRadius: '4px',
                        backgroundColor: CONTENT_COLORS.background,
                        fontSize: '0.75rem',
                        color: CONTENT_COLORS.primaryText,
                      }}
                    >
                      {point}
                      <button
                        onClick={() => handleRemoveKeyPoint(index)}
                        style={{
                          background: 'none',
                          border: 'none',
                          cursor: 'pointer',
                          color: CONTENT_COLORS.secondaryText,
                          padding: 0,
                          fontSize: '1rem',
                          lineHeight: 1,
                        }}
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={!prompt.trim() || loading}
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                padding: '12px 24px',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: CONTENT_COLORS.primary,
                color: '#fff',
                fontSize: '0.875rem',
                fontWeight: 600,
                cursor: 'pointer',
                opacity: !prompt.trim() || loading ? 0.5 : 1,
              }}
            >
              {loading ? (
                <>
                  <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} />
                  {t('ai.generating')}
                </>
              ) : (
                <>
                  <Sparkles size={18} />
                  {t('ai.generateContent')}
                </>
              )}
            </button>
          </>
        ) : (
          <>
            {/* Generated Content Preview */}
            <div
              style={{
                marginBottom: '16px',
                padding: '16px',
                borderRadius: '8px',
                backgroundColor: CONTENT_COLORS.background,
                maxHeight: '300px',
                overflow: 'auto',
              }}
            >
              <pre
                style={{
                  margin: 0,
                  fontSize: '0.75rem',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                  color: CONTENT_COLORS.primaryText,
                }}
              >
                {JSON.stringify(generatedContent, null, 2)}
              </pre>
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                onClick={handleUseContent}
                style={{
                  flex: 1,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  border: 'none',
                  backgroundColor: CONTENT_COLORS.primary,
                  color: '#fff',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Use This Content
              </button>
              <button
                onClick={handleCopy}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  padding: '12px 16px',
                  borderRadius: '8px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  backgroundColor: CONTENT_COLORS.cardBg,
                  color: CONTENT_COLORS.primaryText,
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                }}
              >
                {copied ? <Check size={16} color={CONTENT_COLORS.success} /> : <Copy size={16} />}
              </button>
              <button
                onClick={() => setGeneratedContent(null)}
                style={{
                  padding: '12px 16px',
                  borderRadius: '8px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  backgroundColor: CONTENT_COLORS.cardBg,
                  color: CONTENT_COLORS.secondaryText,
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                }}
              >
                Try Again
              </button>
            </div>
          </>
        )}
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default AIContentGenerator;
