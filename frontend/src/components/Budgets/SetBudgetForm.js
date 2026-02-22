import React, { useState } from 'react';
import { setBudget } from '../../services/api';
import toast from 'react-hot-toast';

export default function SetBudgetForm({ categories, month, year, onSave, onClose }) {
  const [form, setForm] = useState({ category_id: '', amount: '', month, year });
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await setBudget({ ...form, amount: parseFloat(form.amount), category_id: form.category_id || null });
      toast.success('Budget saved!');
      onSave();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Error');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-gray-100">Set Budget</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Category (leave blank for overall)</label>
            <select className="input" value={form.category_id} onChange={e => set('category_id', e.target.value)}>
              <option value="">Overall Budget</option>
              {categories.map(c => <option key={c.id} value={c.id}>{c.emoji} {c.name}</option>)}
            </select>
          </div>
          <div>
            <label className="label">Amount (₹) *</label>
            <input type="number" min="1" step="1" required className="input" value={form.amount} onChange={e => set('amount', e.target.value)} />
          </div>
          <div className="flex gap-3 pt-2">
            <button type="submit" className="btn-primary flex-1">Save Budget</button>
            <button type="button" className="btn-secondary flex-1" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
