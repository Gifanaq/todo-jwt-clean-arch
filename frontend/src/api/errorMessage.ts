import axios from 'axios';

function getValidationMessages(detail: unknown): string | null {
  if (!Array.isArray(detail)) {
    return null;
  }

  const messages = detail.flatMap((item: unknown) => {
    if (
      typeof item === 'object' &&
      item !== null &&
      'msg' in item &&
      typeof item.msg === 'string'
    ) {
      return [item.msg];
    }

    return [];
  });

  return messages.length > 0 ? messages.join(' ') : null;
}

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError<{ detail?: unknown }>(error)) {
    const detail = error.response?.data?.detail;

    if (typeof detail === 'string') {
      return detail;
    }

    return getValidationMessages(detail) ?? error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'Не удалось выполнить запрос.';
}
