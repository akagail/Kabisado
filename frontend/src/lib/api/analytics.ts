import { apiRequest } from "./client";
import type { SubjectProgress, TopicProgress } from "./types";

export function getSubjectProgress(): Promise<SubjectProgress> {
  return apiRequest<SubjectProgress>("/analytics/summary/");
}

export function getTopicProgress(): Promise<TopicProgress> {
  return apiRequest<TopicProgress>("/analytics/topics/");
}
