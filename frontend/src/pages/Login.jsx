// src/pages/Login.jsx
import AuthForm from "../features/auth/AuthForm";
import { Zap } from "lucide-react";

function Login() {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-6 selection:bg-hybrid-neon selection:text-black">
      {/* Optional: Branding floating above the form */}
      <div className="mb-8 flex items-center gap-2 group">
        <Zap className="w-6 h-6 text-hybrid-neon group-hover:scale-110 transition-transform" />
        <span className="text-xl font-black tracking-tighter text-white uppercase">
          Hybrid <span className="text-hybrid-neon">Hour</span>
        </span>
      </div>

      {/* The Centralized Form */}
      <AuthForm method="login" />

      {/* Footer / Legal Links */}
      <footer className="mt-12 text-[10px] text-zinc-700 uppercase tracking-[0.2em] font-bold">
        Engineered for Performance • v1.0
      </footer>
    </div>
  );
}

export default Login;
