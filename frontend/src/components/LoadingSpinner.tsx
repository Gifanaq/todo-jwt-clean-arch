type LoadingSpinnerProps = {
  label?: string;
  className?: string;
};

export function LoadingSpinner({ label, className = '' }: LoadingSpinnerProps) {
  return (
    <span
      className={`loading-spinner ${className}`.trim()}
      role={label ? 'status' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
    />
  );
}
