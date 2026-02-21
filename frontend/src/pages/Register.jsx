// src/pages/Register.jsx
import AuthForm from "../features/auth/AuthForm";
import { Zap } from "lucide-react";
import { Link } from "react-router-dom";

function Register() {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-6 selection:bg-hybrid-neon selection:text-black">
      {/* Small Branding Header */}
      <Link to="/login" className="mb-8 flex items-center gap-2 group hover:opacity-80 transition-opacity">
        <Zap className="w-6 h-6 text-hybrid-neon group-hover:scale-110 transition-transform" />
        <span className="text-xl font-black tracking-tighter text-white uppercase">
          Hybrid <span className="text-hybrid-neon">Hour</span>
        </span>
      </Link>

      {/* Reusing the AuthForm with the "register" logic */}
      <AuthForm method="register" />

      {/* Contextual help link if they already have an account */}
      <footer className="mt-8">
        <p className="text-zinc-600 text-xs font-bold uppercase tracking-widest">
          Join the <span className="text-white">Hybrid Hour</span> Community
        </p>
      </footer>
    </div>
  );
}

export default Register;
