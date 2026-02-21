import { createContext, useState, useEffect, useContext } from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../api/constants"; // Point to your client constants

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    return !!token && token !== "undefined" && token !== "null";
  });

  // NEW: Add a user object to store the UUID or Username from the JWT later
  const [user, setUser] = useState(null);

  const login = (accessToken, refreshToken) => {
    if (accessToken) {
      localStorage.setItem(ACCESS_TOKEN, accessToken);
      if (refreshToken) localStorage.setItem(REFRESH_TOKEN, refreshToken);
      setIsLoggedIn(true);
    }
  };

  const logout = () => {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
    setIsLoggedIn(false);
    setUser(null);
  };

  useEffect(() => {
    const syncAuth = (event) => {
      if (event.key === ACCESS_TOKEN) {
        setIsLoggedIn(!!event.newValue && event.newValue !== "null");
      }
    };
    window.addEventListener("storage", syncAuth);
    return () => window.removeEventListener("storage", syncAuth);
  }, []);

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout, user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
