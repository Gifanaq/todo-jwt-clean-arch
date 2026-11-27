const MINIMUM_LOADING_DURATION_MS = 300;

export async function withMinimumLoading<T>(
  operation: () => Promise<T>,
): Promise<T> {
  const startedAt = Date.now();

  try {
    return await operation();
  } finally {
    const remaining = MINIMUM_LOADING_DURATION_MS - (Date.now() - startedAt);
    if (remaining > 0) {
      await new Promise((resolve) => setTimeout(resolve, remaining));
    }
  }
}
