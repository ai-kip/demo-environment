import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Plus, Calendar, Eye, FileText } from 'lucide-react';
import type { LinkedInPost } from '../../../types/content';
import { CONTENT_COLORS } from '../../../constants/content';
import { api } from '../../../services/api';
import { ContentCard } from '../shared';
import LinkedInPostEditor from './LinkedInPostEditor';

interface LinkedInPageProps {
  onNavigate?: (page: string) => void;
}

type TabType = 'all' | 'scheduled' | 'published' | 'drafts';

const LinkedInPage: React.FC<LinkedInPageProps> = ({ onNavigate }) => {
  const { t } = useTranslation('marketing');
  const [posts, setPosts] = useState<LinkedInPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<TabType>('all');
  const [showEditor, setShowEditor] = useState(false);
  const [editingPost, setEditingPost] = useState<LinkedInPost | null>(null);

  useEffect(() => {
    loadPosts();
  }, [activeTab]);

  const loadPosts = async () => {
    setLoading(true);
    try {
      const status = activeTab === 'all' ? undefined : activeTab === 'drafts' ? 'draft' : activeTab;
      const result = await api.getContentList({
        content_type: 'linkedin_post',
        status,
        page_size: 50,
      });
      setPosts(result.items as LinkedInPost[]);
    } catch (error) {
      console.error('Failed to load posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNew = () => {
    setEditingPost(null);
    setShowEditor(true);
  };

  const handleEdit = (post: LinkedInPost) => {
    setEditingPost(post);
    setShowEditor(true);
  };

  const handleSave = () => {
    setShowEditor(false);
    setEditingPost(null);
    loadPosts();
  };

  const tabs: { key: TabType; label: string; icon: React.ReactNode }[] = [
    { key: 'all', label: 'All Posts', icon: <FileText size={16} /> },
    { key: 'scheduled', label: t('linkedin.scheduledPosts'), icon: <Calendar size={16} /> },
    { key: 'published', label: t('linkedin.publishedPosts'), icon: <Eye size={16} /> },
    { key: 'drafts', label: t('linkedin.drafts'), icon: <FileText size={16} /> },
  ];

  if (showEditor) {
    return (
      <LinkedInPostEditor
        post={editingPost || undefined}
        onSave={handleSave}
        onCancel={() => {
          setShowEditor(false);
          setEditingPost(null);
        }}
      />
    );
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: CONTENT_COLORS.primaryText, margin: 0 }}>
            {t('linkedin.title')}
          </h1>
          <p style={{ fontSize: '0.875rem', color: CONTENT_COLORS.secondaryText, marginTop: '4px' }}>
            {t('linkedin.subtitle')}
          </p>
        </div>
        <button
          onClick={handleCreateNew}
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
          }}
        >
          <Plus size={18} />
          {t('linkedin.newPost')}
        </button>
      </div>

      {/* Tabs */}
      <div
        style={{
          display: 'flex',
          gap: '4px',
          marginBottom: '24px',
          borderBottom: `1px solid ${CONTENT_COLORS.border}`,
          paddingBottom: '4px',
        }}
      >
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '10px 16px',
              borderRadius: '6px 6px 0 0',
              border: 'none',
              backgroundColor: activeTab === tab.key ? CONTENT_COLORS.cardBg : 'transparent',
              color: activeTab === tab.key ? CONTENT_COLORS.primary : CONTENT_COLORS.secondaryText,
              fontSize: '0.875rem',
              fontWeight: activeTab === tab.key ? 600 : 400,
              cursor: 'pointer',
              borderBottom: activeTab === tab.key ? `2px solid ${CONTENT_COLORS.primary}` : '2px solid transparent',
            }}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Posts Grid */}
      {loading ? (
        <div style={{ padding: '60px', textAlign: 'center', color: CONTENT_COLORS.secondaryText }}>
          Loading...
        </div>
      ) : posts.length === 0 ? (
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
            No posts found
          </h3>
          <p style={{ margin: 0, marginBottom: '20px', color: CONTENT_COLORS.secondaryText }}>
            Create your first LinkedIn post to get started.
          </p>
          <button
            onClick={handleCreateNew}
            style={{
              padding: '10px 20px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: CONTENT_COLORS.linkedinPost,
              color: '#fff',
              fontSize: '0.875rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Create Post
          </button>
        </div>
      ) : (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '16px',
          }}
        >
          {posts.map((post) => (
            <ContentCard
              key={post.id}
              content={post}
              onClick={() => handleEdit(post)}
              onEdit={() => handleEdit(post)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default LinkedInPage;
