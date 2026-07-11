// services/auth.ts
// Service untuk autentikasi admin

import { api } from "@/lib/api";
import { AdminInfo, TokenResponse } from "@/types";

export interface LoginCredentials {
  username: string;
  password: string;
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await fetch(
      `/api/backend/api/v1/auth/login`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      }
    );

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Login gagal. Periksa username dan password.");
    }

    const data: TokenResponse = await response.json();

    // Simpan tokens
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);

    return data;
  },

  async getMe(): Promise<AdminInfo> {
    return api.get<AdminInfo>("/api/v1/auth/me");
  },

  async refreshToken(): Promise<TokenResponse | null> {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) return null;

    try {
      const response = await fetch(
        `/api/backend/api/v1/auth/refresh`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: refreshToken }),
        }
      );

      if (!response.ok) return null;

      const data: TokenResponse = await response.json();
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      return data;
    } catch {
      return null;
    }
  },

  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "/login";
  },

  isAuthenticated(): boolean {
    if (typeof window === "undefined") return false;
    return !!localStorage.getItem("access_token");
  },
};
