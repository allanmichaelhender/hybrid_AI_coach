import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { ReactNode, ButtonHTMLAttributes, ReactElement } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "outline" | "ghost";
}

function Button({
  className,
  variant = "primary",
  children,
  ...props
}: ButtonProps): ReactElement {
  const baseStyles =
    "px-6 py-2.5 rounded-xl font-bold transition-all active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2 text-sm uppercase tracking-tight";

  const variants = {
    primary:
      "bg-hybrid-neon text-black hover:brightness-110 shadow-lg shadow-hybrid-neon/10",
    outline:
      "bg-transparent border border-zinc-800 text-zinc-400 hover:text-white hover:border-zinc-600",
    ghost: "bg-zinc-900/50 text-zinc-500 hover:text-white",
  };

  return (
    <button
      className={twMerge(clsx(baseStyles, variants[variant], className))}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;
