import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ArrowLeft, Save, Send, Calendar, Sparkles, Hash, Image, Link2, AtSign, X } from 'lucide-react';
import type { LinkedInPost, LinkedInPostContent, ContentCategory } from '../../../types/content';
import { CONTENT_COLORS, CONTENT_CATEGORY_CONFIG } from '../../../constants/content';
import { AI_TONE_OPTIONS } from '../../../constants/marketing';
import { api } from '../../../services/api';
import LinkedInPreview from './LinkedInPreview';
import LinkedInScheduler from './LinkedInScheduler';

interface LinkedInPostEditorProps {
  post?: LinkedInPost;
  onSave: () => void;
  onCancel: () => void;
}

const LINKEDIN_MAX_CHARS = 3000;
const LINKEDIN_MAX_HASHTAGS = 10;

const LinkedInPostEditor: React.FC<LinkedInPostEditorProps> = ({ post, onSave, onCancel }) => {
  const { t } = useTranslation('marketing');
  const [saving, setSaving] = useState(false);
  const [showScheduler, setShowScheduler] = useState(false);
  const [showAIGenerator, setShowAIGenerator] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [suggestedHashtags, setSuggestedHashtags] = useState<string[]>([]);

  // Form state
  const [title, setTitle] = useState(post?.title || '');
  const [body, setBody] = useState(post?.linkedin?.body || '');
  const [hashtags, setHashtags] = useState<string[]>(post?.linkedin?.hashtags || []);
  const [hashtagInput, setHashtagInput] = useState('');
  const [imageUrl, setImageUrl] = useState(post?.linkedin?.image_url || '');
  const [linkUrl, setLinkUrl] = useState(post?.linkedin?.link_url || '');
  const [callToAction, setCallToAction] = useState(post?.linkedin?.call_to_action || '');
  const [category, setCategory] = useState<ContentCategory | ''>(post?.category || '');

  // AI generation state
  const [aiPrompt, setAiPrompt] = useState('');
  const [aiTone, setAiTone] = useState<'professional' | 'casual' | 'formal' | 'friendly'>('professional');
  const [aiKeyPoints, setAiKeyPoints] = useState('');

  const charCount = body.length;
  const isOverLimit = charCount > LINKEDIN_MAX_CHARS;
  const hashtagCount = hashtags.length;

  useEffect(() => {
    // Suggest hashtags based on content
    if (body.length > 50) {
      const timer = setTimeout(() => {
        suggestHashtags();
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [body]);

  const suggestHashtags = async () => {
    try {
      const result = await api.suggestHashtags(body);
      setSuggestedHashtags(result.hashtags.filter(h => !hashtags.includes(h)));
    } catch (error) {
      console.error('Failed to suggest hashtags:', error);
    }
  };

  const handleAddHashtag = (tag: string) => {
    const cleanTag = tag.replace(/^#/, '').trim();
    if (cleanTag && !hashtags.includes(cleanTag) && hashtags.length < LINKEDIN_MAX_HASHTAGS) {
      setHashtags([...hashtags, cleanTag]);
      setHashtagInput('');
      setSuggestedHashtags(suggestedHashtags.filter(h => h !== cleanTag));
    }
  };

  const handleRemoveHashtag = (tag: string) => {
    setHashtags(hashtags.filter(h => h !== tag));
  };

  const handleHashtagKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      handleAddHashtag(hashtagInput);
    }
  };

  const handleGenerateContent = async () => {
    if (!aiPrompt.trim()) return;

    setGenerating(true);
    try {
      const result = await api.generateContent({
        content_type: 'linkedin_post',
        prompt: aiPrompt,
        tone: aiTone,
        key_points: aiKeyPoints ? aiKeyPoints.split('\n').filter(p => p.trim()) : undefined,
      });

      if (result.linkedin?.body) {
        setBody(result.linkedin.body);
      }
      if (result.linkedin?.hashtags) {
        setHashtags(result.linkedin.hashtags);
      }
      if (result.linkedin?.call_to_action) {
        setCallToAction(result.linkedin.call_to_action);
      }
      if (result.title) {
        setTitle(result.title);
      }

      setShowAIGenerator(false);
    } catch (error) {
      console.error('Failed to generate content:', error);
    } finally {
      setGenerating(false);
    }
  };

  const handleSave = async (asDraft = true) => {
    setSaving(true);
    try {
      const linkedinContent: Partial<LinkedInPostContent> = {
        body,
        hashtags,
        image_url: imageUrl || undefined,
        link_url: linkUrl || undefined,
        call_to_action: callToAction || undefined,
      };

      if (post?.id) {
        await api.updateContent(post.id, {
          title: title || 'Untitled Post',
          category: category || undefined,
          linkedin: linkedinContent,
          status: asDraft ? 'draft' : 'review',
        });
      } else {
        await api.createContent({
          content_type: 'linkedin_post',
          title: title || 'Untitled Post',
          category: category || undefined,
          linkedin: linkedinContent,
        });
      }

      onSave();
    } catch (error) {
      console.error('Failed to save post:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleSchedule = async (scheduledTime: string, timezone: string) => {
    if (!post?.id) {
      // Save first, then schedule
      await handleSave(true);
    }

    try {
      await api.scheduleLinkedInPost(post?.id || '', scheduledTime, timezone);
      setShowScheduler(false);
      onSave();
    } catch (error) {
      console.error('Failed to schedule post:', error);
    }
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button
            onClick={onCancel}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '8px 12px',
              borderRadius: '6px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              backgroundColor: CONTENT_COLORS.cardBg,
              color: CONTENT_COLORS.primaryText,
              cursor: 'pointer',
            }}
          >
            <ArrowLeft size={18} />
            {t('common.back')}
          </button>
          <div>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: CONTENT_COLORS.primaryText, margin: 0 }}>
              {post ? t('linkedin.editPost') : t('linkedin.createPost')}
            </h1>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={() => setShowAIGenerator(true)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '10px 16px',
              borderRadius: '8px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              backgroundColor: CONTENT_COLORS.cardBg,
              color: CONTENT_COLORS.primary,
              fontSize: '0.875rem',
              fontWeight: 500,
              cursor: 'pointer',
            }}
          >
            <Sparkles size={18} />
            {t('linkedin.aiGenerate')}
          </button>
          <button
            onClick={() => setShowScheduler(true)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '10px 16px',
              borderRadius: '8px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              backgroundColor: CONTENT_COLORS.cardBg,
              color: CONTENT_COLORS.primaryText,
              fontSize: '0.875rem',
              fontWeight: 500,
              cursor: 'pointer',
            }}
          >
            <Calendar size={18} />
            {t('linkedin.schedule')}
          </button>
          <button
            onClick={() => handleSave(true)}
            disabled={saving}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '10px 16px',
              borderRadius: '8px',
              border: `1px solid ${CONTENT_COLORS.border}`,
              backgroundColor: CONTENT_COLORS.cardBg,
              color: CONTENT_COLORS.primaryText,
              fontSize: '0.875rem',
              fontWeight: 500,
              cursor: 'pointer',
              opacity: saving ? 0.5 : 1,
            }}
          >
            <Save size={18} />
            {t('common.saveDraft')}
          </button>
          <button
            onClick={() => handleSave(false)}
            disabled={saving || isOverLimit}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '10px 20px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: CONTENT_COLORS.linkedinPost,
              color: '#fff',
              fontSize: '0.875rem',
              fontWeight: 600,
              cursor: 'pointer',
              opacity: saving || isOverLimit ? 0.5 : 1,
            }}
          >
            <Send size={18} />
            {t('linkedin.submitForReview')}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: '24px' }}>
        {/* Editor Panel */}
        <div
          style={{
            backgroundColor: CONTENT_COLORS.cardBg,
            borderRadius: '12px',
            border: `1px solid ${CONTENT_COLORS.border}`,
            padding: '24px',
          }}
        >
          {/* Title */}
          <div style={{ marginBottom: '20px' }}>
            <label
              style={{
                display: 'block',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: CONTENT_COLORS.primaryText,
                marginBottom: '8px',
              }}
            >
              {t('linkedin.postTitle')}
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder={t('linkedin.postTitlePlaceholder')}
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '8px',
                border: `1px solid ${CONTENT_COLORS.border}`,
                fontSize: '0.875rem',
              }}
            />
          </div>

          {/* Category */}
          <div style={{ marginBottom: '20px' }}>
            <label
              style={{
                display: 'block',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: CONTENT_COLORS.primaryText,
                marginBottom: '8px',
              }}
            >
              {t('linkedin.category')}
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value as ContentCategory | '')}
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '8px',
                border: `1px solid ${CONTENT_COLORS.border}`,
                fontSize: '0.875rem',
              }}
            >
              <option value="">Select category...</option>
              {Object.entries(CONTENT_CATEGORY_CONFIG).map(([key, config]) => (
                <option key={key} value={key}>
                  {config.label}
                </option>
              ))}
            </select>
          </div>

          {/* Body */}
          <div style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <label
                style={{
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  color: CONTENT_COLORS.primaryText,
                }}
              >
                {t('linkedin.postContent')}
              </label>
              <span
                style={{
                  fontSize: '0.75rem',
                  color: isOverLimit ? CONTENT_COLORS.error : CONTENT_COLORS.secondaryText,
                }}
              >
                {charCount} / {LINKEDIN_MAX_CHARS}
              </span>
            </div>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder={t('linkedin.postContentPlaceholder')}
              style={{
                width: '100%',
                minHeight: '200px',
                padding: '12px',
                borderRadius: '8px',
                border: `1px solid ${isOverLimit ? CONTENT_COLORS.error : CONTENT_COLORS.border}`,
                fontSize: '0.875rem',
                fontFamily: 'inherit',
                resize: 'vertical',
              }}
            />
          </div>

          {/* Hashtags */}
          <div style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <label
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  color: CONTENT_COLORS.primaryText,
                }}
              >
                <Hash size={16} />
                {t('linkedin.hashtags')}
              </label>
              <span style={{ fontSize: '0.75rem', color: CONTENT_COLORS.secondaryText }}>
                {hashtagCount} / {LINKEDIN_MAX_HASHTAGS}
              </span>
            </div>

            {/* Current hashtags */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '12px' }}>
              {hashtags.map((tag) => (
                <span
                  key={tag}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '4px 10px',
                    borderRadius: '16px',
                    backgroundColor: `${CONTENT_COLORS.linkedinPost}15`,
                    color: CONTENT_COLORS.linkedinPost,
                    fontSize: '0.875rem',
                  }}
                >
                  #{tag}
                  <button
                    onClick={() => handleRemoveHashtag(tag)}
                    style={{
                      background: 'none',
                      border: 'none',
                      padding: '0',
                      cursor: 'pointer',
                      color: CONTENT_COLORS.linkedinPost,
                      display: 'flex',
                    }}
                  >
                    <X size={14} />
                  </button>
                </span>
              ))}
            </div>

            {/* Hashtag input */}
            <input
              type="text"
              value={hashtagInput}
              onChange={(e) => setHashtagInput(e.target.value)}
              onKeyDown={handleHashtagKeyDown}
              placeholder={t('linkedin.addHashtag')}
              disabled={hashtagCount >= LINKEDIN_MAX_HASHTAGS}
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                border: `1px solid ${CONTENT_COLORS.border}`,
                fontSize: '0.875rem',
              }}
            />

            {/* Suggested hashtags */}
            {suggestedHashtags.length > 0 && (
              <div style={{ marginTop: '12px' }}>
                <span style={{ fontSize: '0.75rem', color: CONTENT_COLORS.secondaryText, marginBottom: '8px', display: 'block' }}>
                  {t('linkedin.suggestedHashtags')}
                </span>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {suggestedHashtags.slice(0, 5).map((tag) => (
                    <button
                      key={tag}
                      onClick={() => handleAddHashtag(tag)}
                      style={{
                        padding: '4px 10px',
                        borderRadius: '16px',
                        border: `1px dashed ${CONTENT_COLORS.border}`,
                        backgroundColor: 'transparent',
                        color: CONTENT_COLORS.secondaryText,
                        fontSize: '0.875rem',
                        cursor: 'pointer',
                      }}
                    >
                      #{tag}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Image URL */}
          <div style={{ marginBottom: '20px' }}>
            <label
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: CONTENT_COLORS.primaryText,
                marginBottom: '8px',
              }}
            >
              <Image size={16} />
              {t('linkedin.imageUrl')}
            </label>
            <input
              type="url"
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
              placeholder="https://..."
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                border: `1px solid ${CONTENT_COLORS.border}`,
                fontSize: '0.875rem',
              }}
            />
          </div>

          {/* Link URL */}
          <div style={{ marginBottom: '20px' }}>
            <label
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: CONTENT_COLORS.primaryText,
                marginBottom: '8px',
              }}
            >
              <Link2 size={16} />
              {t('linkedin.linkUrl')}
            </label>
            <input
              type="url"
              value={linkUrl}
              onChange={(e) => setLinkUrl(e.target.value)}
              placeholder="https://..."
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                border: `1px solid ${CONTENT_COLORS.border}`,
                fontSize: '0.875rem',
              }}
            />
          </div>

          {/* Call to Action */}
          <div>
            <label
              style={{
                display: 'block',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: CONTENT_COLORS.primaryText,
                marginBottom: '8px',
              }}
            >
              {t('linkedin.callToAction')}
            </label>
            <input
              type="text"
              value={callToAction}
              onChange={(e) => setCallToAction(e.target.value)}
              placeholder={t('linkedin.callToActionPlaceholder')}
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                border: `1px solid ${CONTENT_COLORS.border}`,
                fontSize: '0.875rem',
              }}
            />
          </div>
        </div>

        {/* Preview Panel */}
        <div>
          <LinkedInPreview
            body={body}
            hashtags={hashtags}
            imageUrl={imageUrl}
            linkUrl={linkUrl}
          />
        </div>
      </div>

      {/* AI Generator Modal */}
      {showAIGenerator && (
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
          onClick={() => setShowAIGenerator(false)}
        >
          <div
            style={{
              backgroundColor: CONTENT_COLORS.cardBg,
              borderRadius: '12px',
              width: '100%',
              maxWidth: '500px',
              padding: '24px',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
              <h3 style={{ margin: 0, fontSize: '1.125rem', fontWeight: 600, color: CONTENT_COLORS.primaryText }}>
                {t('linkedin.aiGenerate')}
              </h3>
              <button
                onClick={() => setShowAIGenerator(false)}
                style={{ background: 'none', border: 'none', cursor: 'pointer', color: CONTENT_COLORS.secondaryText }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 500, marginBottom: '8px' }}>
                {t('aiGenerator.prompt')}
              </label>
              <textarea
                value={aiPrompt}
                onChange={(e) => setAiPrompt(e.target.value)}
                placeholder={t('aiGenerator.promptPlaceholder')}
                style={{
                  width: '100%',
                  minHeight: '100px',
                  padding: '12px',
                  borderRadius: '8px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  fontSize: '0.875rem',
                  fontFamily: 'inherit',
                  resize: 'vertical',
                }}
              />
            </div>

            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 500, marginBottom: '8px' }}>
                {t('aiGenerator.tone')}
              </label>
              <select
                value={aiTone}
                onChange={(e) => setAiTone(e.target.value as typeof aiTone)}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  borderRadius: '8px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  fontSize: '0.875rem',
                }}
              >
                {AI_TONE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 500, marginBottom: '8px' }}>
                {t('aiGenerator.keyPoints')}
              </label>
              <textarea
                value={aiKeyPoints}
                onChange={(e) => setAiKeyPoints(e.target.value)}
                placeholder={t('aiGenerator.keyPointsPlaceholder')}
                style={{
                  width: '100%',
                  minHeight: '80px',
                  padding: '12px',
                  borderRadius: '8px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  fontSize: '0.875rem',
                  fontFamily: 'inherit',
                  resize: 'vertical',
                }}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
              <button
                onClick={() => setShowAIGenerator(false)}
                style={{
                  padding: '10px 20px',
                  borderRadius: '8px',
                  border: `1px solid ${CONTENT_COLORS.border}`,
                  backgroundColor: CONTENT_COLORS.cardBg,
                  color: CONTENT_COLORS.primaryText,
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                }}
              >
                {t('common.cancel')}
              </button>
              <button
                onClick={handleGenerateContent}
                disabled={generating || !aiPrompt.trim()}
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
                  fontWeight: 500,
                  cursor: 'pointer',
                  opacity: generating || !aiPrompt.trim() ? 0.5 : 1,
                }}
              >
                <Sparkles size={16} />
                {generating ? t('aiGenerator.generating') : t('aiGenerator.generate')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Scheduler Modal */}
      {showScheduler && (
        <LinkedInScheduler
          post={post}
          onSchedule={handleSchedule}
          onClose={() => setShowScheduler(false)}
        />
      )}
    </div>
  );
};

export default LinkedInPostEditor;
