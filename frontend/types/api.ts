export interface BibleVerse {
  id: string;
  book_id: string;
  chapter_number: number;
  verse_number: number;
  text: string;
  reference?: string;
}

export interface Sermon {
  id: string;
  title: string;
  theme?: string;
  main_verse?: string;
  bible_version: string;
  audience?: string;
  occasion?: string;
  estimated_duration?: number;
  date_preached?: string;
  content?: string;
  status: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Conversation {
  id: string;
  title: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface CreativeProject {
  id: string;
  title: string;
  media_type: string;
  status: string;
  ai_prompt?: string;
  created_at: string;
  updated_at: string;
}

export interface CommunicationProject {
  id: string;
  title: string;
  campaign_type: string;
  status: string;
  created_at: string;
  updated_at: string;
}
