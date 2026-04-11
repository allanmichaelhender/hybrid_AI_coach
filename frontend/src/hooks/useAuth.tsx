import {
  createContext,
  useState,
  useEffect,
  useContext,
  type ReactNode,
  type ReactElement,
} from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../api/constants";
import type { AuthContextType, User } from "@/types";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

function AuthProvider({ children }: AuthProviderProps): ReactElement {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(() => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    return !!token && token !== "undefined" && token !== "null";
  });

  const [user, setUser] = useState<User | null>(null);

  const login = (accessToken: string, refreshToken?: string): void => {
    if (accessToken) {
      localStorage.setItem(ACCESS_TOKEN, accessToken);
      if (refreshToken) localStorage.setItem(REFRESH_TOKEN, refreshToken);
      setIsLoggedIn(true);
    }
  };

  const logout = (): void => {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
    setIsLoggedIn(false);
    setUser(null);
  };

  useEffect(() => {
    const syncAuth = (event: StorageEvent): void => {
      if (event.key === ACCESS_TOKEN) {
        setIsLoggedIn(!!event.newValue && event.newValue !== "null");
      }
    };
    window.addEventListener("storage", syncAuth);
    return () => window.removeEventListener("storage", syncAuth);
  }, []);

  const contextValue: AuthContextType = {
    isLoggedIn,
    user,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
}

export { AuthProvider };

function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export { useAuth };
