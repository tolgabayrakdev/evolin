import { create } from "zustand";

interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

interface RegisterData {
  email: string;
  password: string;
}

interface AuthState {
  loading: boolean;
  isAuthenticated: boolean;
  user: User | null;
  checkAuth: () => Promise<boolean>;
  register: (data: RegisterData) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  setLoading: (loading: boolean) => void;
  setAuthenticated: (authenticated: boolean, user?: User | null) => void;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const useAuthStore = create<AuthState>((set) => ({
  loading: true,
  isAuthenticated: false,
  user: null,

  setLoading: (loading: boolean) => set({ loading }),

  setAuthenticated: (authenticated: boolean, user: User | null = null) =>
    set({ isAuthenticated: authenticated, user }),

  checkAuth: async (): Promise<boolean> => {
    set({ loading: true });

    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: "GET",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const user: User = await response.json();
        set({
          isAuthenticated: true,
          user,
          loading: false,
        });
        return true;
      } else {
        set({
          isAuthenticated: false,
          user: null,
          loading: false,
        });
        return false;
      }
    } catch {
      set({
        isAuthenticated: false,
        user: null,
        loading: false,
      });
      return false;
    }
  },

  register: async (data: RegisterData): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        await response.json();
        return { success: true };
      } else {
        const errorData = await response.json().catch(() => ({ detail: "Registration failed" }));
        return { success: false, error: errorData.detail || "Registration failed" };
      }
    } catch {
      return { success: false, error: "Network error. Please try again." };
    }
  },

  logout: async (): Promise<void> => {
    try {
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });
    } catch {
      // Ignore errors on logout
    } finally {
      set({
        isAuthenticated: false,
        user: null,
      });
    }
  },
}));

// Selector hook for isAuthenticated
export const useIsAuthenticated = () => useAuthStore((state) => state.isAuthenticated);
