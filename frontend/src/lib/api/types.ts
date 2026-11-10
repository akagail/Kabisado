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
