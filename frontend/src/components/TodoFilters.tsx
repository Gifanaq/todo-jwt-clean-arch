export type TodoFilter = 'all' | 'active' | 'completed';

type TodoFiltersProps = {
  filter: TodoFilter;
  onChange: (filter: TodoFilter) => void;
};

export function TodoFilters({ filter, onChange }: TodoFiltersProps) {
  return (
    <div className="todo-filters" aria-label="Фильтр задач" role="group">
      <button
        type="button"
        className={filter === 'all' ? 'filter-active' : ''}
        aria-pressed={filter === 'all'}
        onClick={() => onChange('all')}
      >
        Все
      </button>
      <button
        type="button"
        className={filter === 'active' ? 'filter-active' : ''}
        aria-pressed={filter === 'active'}
        onClick={() => onChange('active')}
      >
        Активные
      </button>
      <button
        type="button"
        className={filter === 'completed' ? 'filter-active' : ''}
        aria-pressed={filter === 'completed'}
        onClick={() => onChange('completed')}
      >
        Выполненные
      </button>
    </div>
  );
}
