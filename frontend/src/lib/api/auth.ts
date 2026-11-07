import { apiRequest } from "./client";
import type {
  ExportRequest,
  Profile,
  ProfileUpdate,
  SessionPayload,
} from "./types";

export function register(email: string, password: string): Promise<SessionPayload> {
  return apiRequest<SessionPayload>("/auth/register/", {
    method: "POST",
    body: { email, password },
  });
}

export function login(email: string, password: string): Promise<SessionPayload> {
  return apiRequest<SessionPayload>("/auth/login/", {
    method: "POST",
    body: { email, password },
  });
}

export function logout(): Promise<void> {
  return apiRequest<void>("/auth/logout/", { method: "POST" });
}

export function requestPasswordReset(email: string): Promise<{ message: string }> {
  return apiRequest<{ message: string }>("/auth/password-reset/", {
    method: "POST",
    body: { email },
  });
}

export function confirmPasswordReset(
  token: string,
  password: string,
): Promise<SessionPayload> {
  return apiRequest<SessionPayload>("/auth/password-reset/confirm/", {
    method: "POST",
    body: { token, password },
  });
}

export function getMe(): Promise<SessionPayload> {
  return apiRequest<SessionPayload>("/me/");
}

export function updateMe(update: ProfileUpdate): Promise<{ profile: Profile }> {
  return apiRequest<{ profile: Profile }>("/me/", {
    method: "PATCH",
    body: update,
  });
}

export function deleteMe(password: string): Promise<void> {
  return apiRequest<void>("/me/", { method: "DELETE", body: { password } });
}

export function requestExport(): Promise<ExportRequest> {
  return apiRequest<ExportRequest>("/me/export/", { method: "POST" });
}

export function getExport(exportId: string): Promise<ExportRequest> {
  return apiRequest<ExportRequest>(`/me/export/${exportId}/`);
}
