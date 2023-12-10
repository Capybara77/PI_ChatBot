import { useState } from 'react';
import { AppStore } from './store/AppStore';
import { observer } from 'mobx-react';
import './App.css';

export const FindPage = observer(() => {
  const [store] = useState(() => new AppStore());
  const [value, setValue] = useState('');

  const handleSearchClick = () => {
    store.getData(value);
    setValue('');
  };

  const handleClearClick = () => {
    store.clearContext();
    setValue('');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSearchClick();
  };

  return (
    <div>
      <h1>Программная инженерия</h1>
      <div>
        <div>
          {store.fetchedData && store.fetchedData.messages
            ? store.fetchedData.messages.map((item) => (
                <div key={item.content}>
                  {item.role} - {item.content}
                </div>
              ))
            : ''}
        </div>
        {store.isLoading ? <div>Загрузка...</div> : ''}
        <form onSubmit={handleSubmit}>
          <input
            placeholder='Введите запрос'
            value={value}
            onChange={(e) => setValue(e.target.value)}
            ref={(el) => {
              if (el) el.focus();
            }}
          />
          <button type='button' onClick={handleSearchClick}>
            Поиск
          </button>
          <button type='button' onClick={handleClearClick}>
            Сброс
          </button>
        </form>
      </div>
    </div>
  );
});
