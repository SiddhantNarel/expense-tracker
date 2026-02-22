import React, { useState } from 'react';
import { addTransaction } from '../../services/api';
import { getToday } from '../../services/helpers';
import toast from 'react-hot-toast';

export default function AddLoanEntry({ friendId, onSave, onClose }) {
  const [form, setForm] = useState({ type: 'gave', amount: '', date: getToday(), description: '' });
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addTransaction(friendId, { ...form, amount: parseFloat(form.amount) });
      toast.success('Entry added!');
      onSave();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Error');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-gray-100">Add Loan Entry</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex gap-3">
            <button type="button" className={`flex-1 py-2 rounded-lg border-2 font-medium transition-colors ${form.type === 'gave' ? 'border-red-400 bg-red-50 dark:bg-red-900/20 text-red-600' : 'border-gray-200 dark:border-gray-600'}`} onClick={() => set('type', 'gave')}>
              🔴 I gave
            </button>
            <button type="button" className={`flex-1 py-2 rounded-lg border-2 font-medium transition-colors ${form.type === 'received' ? 'border-green-400 bg-green-50 dark:bg-green-900/20 text-green-600' : 'border-gray-200 dark:border-gray-600'}`} onClick={() => set('type', 'received')}>
              🟢 They paid
            </button>
          </div>
          <div>
            <label className="label">Amount (₹) *</label>
            <input type="number" min="0.01" step="0.01" required className="input" value={form.amount} onChange={e => set('amount', e.target.value)} />
          </div>
          <div>
            <label className="label">Date *</label>
            <input type="date" required className="input" value={form.date} onChange={e => set('date', e.target.value)} />
          </div>
          <div>
            <label className="label">Description</label>
            <input type="text" className="input" value={form.description} onChange={e => set('description', e.target.value)} placeholder="e.g. Dinner, Movie tickets" />
          </div>
          <div className="flex gap-3 pt-2">
            <button type="submit" className="btn-primary flex-1">Add Entry</button>
            <button type="button" className="btn-secondary flex-1" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
