import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/client"; // Use your configured axios client
import { useAuth } from "../../hooks/useAuth"; // Use your context!
import { Loader2, Zap } from "lucide-react";

function AuthForm({ method }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const { login } = useAuth(); // Destructure the login function

  const isLogin = method === "login";
  const title = isLogin ? "Welcome Back" : "Create Account";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isLogin) {
        // FastAPI OAuth2 expects form-data for the token endpoint
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const res = await api.post("/auth/login/access-token", formData);
        
        // Use the context's login to set tokens and update global state
        login(res.data.access_token, res.data.refresh_token);
        navigate("/");
      } else {
        // Registration uses standard JSON
        await api.post("/auth/register", { username, password });
        alert("Registration successful! Now, let's get you logged in.");
        navigate("/login");
      }
    } catch (error) {
      const detail = error.response?.data?.detail || "Something went wrong";
      alert(typeof detail === 'string' ? detail : JSON.stringify(detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md p-8 bg-zinc-900 border border-zinc-800 rounded-3xl shadow-2xl">
      <div className="flex flex-col items-center mb-8">
        <div className="p-3 bg-hybrid-neon/10 rounded-2xl mb-4">
          <Zap className="w-8 h-8 text-hybrid-neon fill-current" />
        </div>
        <h1 className="text-2xl font-black text-white">{title}</h1>
        <p className="text-zinc-500 text-sm mt-2">Adaptive 60-Minute Programming</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            className="w-full bg-black border border-zinc-800 rounded-xl px-4 py-3 focus:outline-none focus:border-hybrid-neon transition-all placeholder:text-zinc-700"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            required
          />
        </div>
        <div>
          <input
            className="w-full bg-black border border-zinc-800 rounded-xl px-4 py-3 focus:outline-none focus:border-hybrid-neon transition-all placeholder:text-zinc-700"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
        </div>

        <button 
          className="w-full bg-hybrid-neon text-black font-black py-4 rounded-xl hover:brightness-110 active:scale-[0.98] transition-all flex justify-center items-center gap-2" 
          type="submit"
          disabled={loading}
        >
          {loading ? <Loader2 className="animate-spin w-5 h-5" /> : (isLogin ? "LOG IN" : "REGISTER")}
        </button>
      </form>

      <div className="mt-8 text-center">
        <button 
          onClick={() => navigate(isLogin ? "/register" : "/login")}
          className="text-zinc-500 text-sm hover:text-white transition-colors"
        >
          {isLogin ? "New to Hybrid Hour? Create an account" : "Already have an account? Log in"}
        </button>
      </div>
    </div>
  );
}

export default AuthForm;
