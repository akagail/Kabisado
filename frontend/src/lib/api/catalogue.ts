import { apiRequest } from "./client";
import type { ExamFamily, Subject, Topic } from "./types";

export function getExamFamilies(): Promise<{ exam_families: ExamFamily[] }> {
  return apiRequest<{ exam_families: ExamFamily[] }>("/exams/");
}

export function getSubjects(versionId: string): Promise<Subject[]> {
  return apiRequest<Subject[]>(`/exam-versions/${versionId}/subjects/`);
}

export function getTopics(subjectId: string): Promise<Topic[]> {
  return apiRequest<Topic[]>(`/subjects/${subjectId}/topics/`);
}

export function getTopic(topicId: string): Promise<Topic> {
  return apiRequest<Topic>(`/topics/${topicId}/`);
}
