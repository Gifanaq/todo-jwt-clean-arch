import { api } from './axios';

export type Todo = {
  id: string;
  user_id: string;
  title: string;
  is_done: boolean;
  created_at: string;
  updated_at: string;
};

export type TodoUpdate = Partial<Pick<Todo, 'title' | 'is_done'>>;

export async function getTodos(): Promise<Todo[]> {
  const { data } = await api.get<Todo[]>('/todos');
  return data;
}

export async function createTodo(title: string): Promise<Todo> {
  const { data } = await api.post<Todo>('/todos', { title });
  return data;
}

export async function updateTodo(
  todoId: string,
  changes: TodoUpdate,
): Promise<Todo> {
  const { data } = await api.patch<Todo>(`/todos/${todoId}`, changes);
  return data;
}

export async function deleteTodo(todoId: string): Promise<void> {
  await api.delete(`/todos/${todoId}`);
}
