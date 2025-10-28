// Common types used across the application

export interface User {
  id: string
  username: string
  email: string
  full_name?: string
  organization?: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at?: string
  last_login?: string
}

export interface Dataset {
  id: string
  user_id: string
  name: string
  description?: string
  file_name: string
  file_size: number
  mime_type: string
  total_rows: number
  processed_rows: number
  failed_rows: number
  processing_status: ProcessingStatus
  processing_started_at?: string
  processing_completed_at?: string
  error_message?: string
  metadata: Record<string, any>
  settings: Record<string, any>
  is_public: boolean
  created_at: string
  updated_at?: string
}

export interface Tweet {
  id: string
  dataset_id: string
  original_id?: string
  text: string
  cleaned_text?: string
  language: string
  character_count?: number
  word_count?: number
  hashtag_count: number
  mention_count: number
  url_count: number
  created_at?: string
  processed_at: string
  metadata: Record<string, any>
  is_valid: boolean
  validation_errors?: string[]
  processing_errors?: string[]
  qdrant_id?: string
  analysis_result?: AnalysisResult
}

export interface AnalysisResult {
  id: string
  tweet_id: string
  model_version: string
  sentiment: SentimentLabel
  sentiment_confidence: number
  sentiment_scores: Record<string, number>
  emotion: EmotionLabel
  emotion_confidence: number
  emotion_scores: Record<string, number>
  offensive_language: boolean
  offensive_confidence: number
  offensive_scores: Record<string, number>
  hate_speech?: HateSpeechLabel
  hate_confidence?: number
  hate_scores?: Record<string, number>
  irony?: boolean
  irony_confidence?: number
  processing_time_ms?: number
  model_used?: string
  analyzed_at: string
  confidence_threshold: number
  is_high_confidence: boolean
}

export interface SearchResult {
  tweet_id: string
  text: string
  similarity_score: number
  analysis?: AnalysisResult
  metadata: Record<string, any>
}

export interface SearchResponse {
  results: SearchResult[]
  total_count: number
  query_time_ms: number
  max_similarity: number
  avg_similarity: number
}

export interface ExportJob {
  id: string
  user_id: string
  dataset_id: string
  export_type: ExportType
  format_options: Record<string, any>
  filters: Record<string, any>
  status: ProcessingStatus
  progress_percentage: number
  file_path?: string
  file_name?: string
  file_size?: number
  download_url?: string
  expires_at?: string
  total_records?: number
  processed_records: number
  processing_time_ms?: number
  error_message?: string
  created_at: string
  updated_at?: string
  completed_at?: string
}

// Enums
export enum ProcessingStatus {
  PENDING = 'pending',
  UPLOADING = 'uploading',
  VALIDATING = 'validating',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export enum SentimentLabel {
  POSITIVE = 'positive',
  NEGATIVE = 'negative',
  NEUTRAL = 'neutral'
}

export enum EmotionLabel {
  JOY = 'joy',
  SADNESS = 'sadness',
  ANGER = 'anger',
  FEAR = 'fear',
  SURPRISE = 'surprise',
  DISGUST = 'disgust',
  OTHERS = 'others'
}

export enum HateSpeechLabel {
  HATEFUL = 'hateful',
  TARGETED = 'targeted',
  AGGRESSIVE = 'aggressive',
  NONE = 'none'
}

export enum ExportType {
  CSV = 'csv',
  JSON = 'json',
  PDF = 'pdf',
  EXCEL = 'excel'
}

// API Response types
export interface ApiResponse<T = any> {
  data?: T
  error?: {
    code: number
    message: string
    type: string
  }
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// Form types
export interface LoginFormData {
  email: string
  password: string
  remember?: boolean
}

export interface RegisterFormData {
  username: string
  email: string
  password: string
  confirm_password: string
  full_name?: string
  organization?: string
}

export interface DatasetUploadFormData {
  name: string
  description?: string
  file: File
  is_public: boolean
  settings: Record<string, any>
}

export interface SearchFormData {
  query: string
  filters: Record<string, any>
  limit: number
  offset: number
  similarity_threshold: number
}