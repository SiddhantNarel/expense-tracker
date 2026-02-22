import React, { useEffect, useState } from 'react';
import { getIncomes, deleteIncome } from '../../services/api';
import { formatINR } from '../../services/helpers';
import toast from 'react-hot-toast';
import AddIncomeForm from './AddIncomeForm';

export default function IncomeList() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [search, setSearch] = useState('');

  const load = () => {
    setLoading(true);
    getIncomes({ page, per_page: 15, search })
      .then(r => { setItems(r.data.data); setTotal(r.data.total); setPages(r.data.pages); })
      .finally(() => setLoading(false));
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { load(); }, [page, search]);

  const handleDelete = (id) => {
    if (!window.confirm('Delete this income entry?')) return;
    deleteIncome(id).then(() => { toast.success('Deleted'); load(); });
  };

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Income</h2>
        <button className="btn-primary" onClick={() => { setEditing(null); setShowForm(true); }}>+ Add Income</button>
      </div>
      <div className="card">
        <input placeholder="Search description..." className="input" value={search} onChange={e => setSearch(e.target.value)} />
      </div>
      <div className="text-sm text-gray-500 dark:text-gray-400">{total} entries</div>
      {loading ? <div className="text-center py-10 text-gray-400">Loading...</div> : (
        <div className="space-y-2">
          {items.length === 0 && <div className="card text-center text-gray-400 py-12">No income entries yet</div>}
          {items.map(item => (
            <div key={item.id} className="card flex items-center justify-between gap-4 p-4">
              <div>
                <p className="font-medium text-gray-900 dark:text-gray-100">{item.source}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">{item.date} {item.description && `· ${item.description}`}</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="font-bold text-green-500 text-lg">{formatINR(item.amount)}</span>
                <button className="btn-secondary text-xs px-3 py-1.5" onClick={() => { setEditing(item); setShowForm(true); }}>Edit</button>
                <button className="btn-danger text-xs px-3 py-1.5" onClick={() => handleDelete(item.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
      {pages > 1 && (
        <div className="flex gap-2 justify-center">
          <button className="btn-secondary px-3 py-1" disabled={page === 1} onClick={() => setPage(p => p - 1)}>←</button>
          <span className="py-1 text-sm text-gray-600 dark:text-gray-400">Page {page} of {pages}</span>
          <button className="btn-secondary px-3 py-1" disabled={page === pages} onClick={() => setPage(p => p + 1)}>→</button>
        </div>
      )}
      {showForm && (
        <AddIncomeForm
          income={editing}
          onSave={() => { setShowForm(false); setEditing(null); load(); }}
          onClose={() => { setShowForm(false); setEditing(null); }}
        />
      )}
    </div>
  );
}
