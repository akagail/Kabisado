import { apiRequest } from "./client";
import type {
  Paginated,
  PracticeHistoryEntry,
  PracticeMode,
  PracticeResults,
  PracticeSession,
  PracticeSubmitResult,
} from "./types";

export function startSession(input: {
  topic: string;
  mode: PracticeMode;
  size: number;
}): Promise<PracticeSession> {
  return apiRequest<PracticeSession>("/practice-sessions/", {
    method: "POST",
    body: input,
  });
}

export function getSession(sessionId: string): Promise<PracticeSession> {
  return apiRequest<PracticeSession>(`/practice-sessions/${sessionId}/`);
}

export function saveAnswer(
  sessionId: string,
  position: number,
  selectedOptionId: string,
): Promise<void> {
  return apiRequest<void>(`/practice-sessions/${sessionId}/answers/${position}/`, {
    method: "PUT",
    body: { selected_option_id: selectedOptionId },
  });
}

export function submitSession(sessionId: string): Promise<PracticeSubmitResult> {
  return apiRequest<PracticeSubmitResult>(`/practice-sessions/${sessionId}/submit/`, {
    method: "POST",
  });
}

export function getResults(sessionId: string): Promise<PracticeResults> {
  return apiRequest<PracticeResults>(`/practice-sessions/${sessionId}/results/`);
}

export function getHistory(): Promise<Paginated<PracticeHistoryEntry>> {
  return apiRequest<Paginated<PracticeHistoryEntry>>("/practice-sessions/");
}
