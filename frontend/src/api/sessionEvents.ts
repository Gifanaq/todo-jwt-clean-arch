type SessionExpiredListener = () => void;

const sessionExpiredListeners = new Set<SessionExpiredListener>();

export function subscribeToSessionExpiry(
  listener: SessionExpiredListener,
): () => void {
  sessionExpiredListeners.add(listener);
  return () => {
    sessionExpiredListeners.delete(listener);
  };
}

export function notifySessionExpired(): void {
  sessionExpiredListeners.forEach((listener) => listener());
}
