export type TargetExam = "professional" | "subprofessional";

export interface User {
  id: string;
  email: string;
}

export interface StudyPreference {
  mode?: "untimed" | "timed";
  size?: number;
}

export interface Profile {
  id: string;
  display_name: string;
  target_exam: TargetExam | null;
  timezone: string;
  preference: StudyPreference;
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
  target_exam?: TargetExam | "";
  timezone?: string;
  preference?: StudyPreference;
}
