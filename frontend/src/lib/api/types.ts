/** The DRF pagination envelope every list endpoint returns. */
export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export type ExamLevel = "professional" | "subprofessional";

export interface User {
  id: string;
  email: string;
}

export interface StudyPreference {
  mode?: "untimed" | "timed";
  size?: number;
}

export interface ExamVersion {
  id: string;
  slug: string;
  label: string;
  source_url: string;
  published_at: string;
  passing_rate: number | null;
}

export interface Exam {
  id: string;
  slug: string;
  name: string;
  level: ExamLevel;
  current_version: ExamVersion | null;
}

export interface ExamFamily {
  id: string;
  slug: string;
  name: string;
  exams: Exam[];
}

/** The profile's target exam: the catalogue object without version details. */
export interface ExamSummary {
  id: string;
  slug: string;
  name: string;
}

export interface Subject {
  id: string;
  slug: string;
  name: string;
  display_order: number;
}

export interface Topic {
  id: string;
  slug: string;
  name: string;
  display_order: number;
  accuracy: number | null;
  attempts: number;
  weak_topic: boolean;
}

export interface Profile {
  id: string;
  display_name: string;
  target_exam: ExamSummary | null;
  timezone: string;
  preference: StudyPreference;
  /** Opaque version echoed on update; a mismatch means another tab edited. */
  updated_at: string;
}

export interface SessionPayload {
  user: User;
  profile: Profile;
}

export type ExportStatus = "pending" | "ready" | "expired";

export interface ExportRequest {
  export_id: string;
  status: ExportStatus;
  requested_at: string;
  completed_at: string | null;
  download_url: string | null;
}

export interface ProfileUpdate {
  display_name?: string;
  /** Exam slug (e.g. `cse-professional`). */
  target_exam?: string;
  timezone?: string;
  preference?: StudyPreference;
  updated_at?: string;
}

export type PracticeMode = "untimed" | "timed";
export type PracticeStatus = "in_progress" | "submitted" | "expired" | "abandoned";

export interface PracticeOption {
  id: string;
  text: string;
  /** Only present after the session is submitted. */
  is_correct?: boolean;
}

export interface PracticeItem {
  position: number;
  question: {
    id: string;
    stem: string;
    options: PracticeOption[];
  };
  saved_answer: { selected_option_id: string } | null;
}

export interface PracticeSession {
  id: string;
  mode: PracticeMode;
  status: PracticeStatus;
  time_limit_seconds: number | null;
  started_at: string;
  expires_at: string | null;
  submitted_at: string | null;
  score_correct: number | null;
  score_total: number | null;
  items: PracticeItem[];
}

export interface PracticeResultItem {
  position: number;
  question: {
    id: string;
    stem: string;
    options: PracticeOption[];
    explanation: string;
    provenance: string;
    difficulty: string;
  };
  selected_option_id: string | null;
  is_correct: boolean | null;
  explanation: string;
  provenance: string;
}

export interface PracticeResults {
  session_id: string;
  score_correct: number;
  score_total: number;
  items: PracticeResultItem[];
}

export interface PracticeSubmitResult {
  id: string;
  status: PracticeStatus;
  submitted_at: string | null;
  score_correct: number | null;
  score_total: number | null;
}

export interface PracticeHistoryEntry {
  id: string;
  status: PracticeStatus;
  mode: PracticeMode;
  started_at: string;
  submitted_at: string | null;
  score_correct: number | null;
  score_total: number | null;
}

export interface SubjectAccuracy {
  subject: { id: string; slug: string; name: string };
  accuracy: number;
  attempts: number;
}

export interface TopicAccuracy {
  topic: { id: string; slug: string; name: string };
  accuracy: number;
  attempts: number;
  weak_topic: boolean;
  weak_reason: string | null;
}

export interface SubjectProgress {
  subjects: SubjectAccuracy[];
}

export interface TopicProgress {
  topics: TopicAccuracy[];
}
