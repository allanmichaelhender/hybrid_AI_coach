// src/components/ui/Button.jsx
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export const Button = ({ className, variant = 'primary', ...props }) => {
  const baseStyles = "px-6 py-2.5 rounded-xl font-bold transition-all active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2 text-sm uppercase tracking-tight";
  
  const variants = {
    primary: "bg-hybrid-neon text-black hover:brightness-110 shadow-lg shadow-hybrid-neon/10",
    outline: "bg-transparent border border-zinc-800 text-zinc-400 hover:text-white hover:border-zinc-600",
    ghost: "bg-zinc-900/50 text-zinc-500 hover:text-white"
  };

  return (
    <button 
      className={twMerge(baseStyles, variants[variant], className)} 
      {...props} 
    />
  );
};
