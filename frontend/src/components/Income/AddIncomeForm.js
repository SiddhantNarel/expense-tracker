import React, { useState, useEffect } from 'react';
import { createIncome, updateIncome } from '../../services/api';
import { getToday } from '../../services/helpers';
import toast from 'react-hot-toast';

const SOURCES = ['Family', 'Pocket Money', 'Freelance', 'Part-time Job', 'Stipend', 'Other'];

export default function AddIncomeForm({ income, onSave, onClose }) {
  const [form, setForm] = useState({ amount: '', source: 'Other', date: getToday(), description: '' });

  useEffect(() => {
    if (income) setForm({ amount: income.amount, source: income.source, date: income.date, description: income.description || '' });
  }, [income]);

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...form, amount: parseFloat(form.amount) };
      if (income?.id) { await updateIncome(income.id, payload); toast.success('Income updated!'); }
      else { await createIncome(payload); toast.success('Income added!'); }
      onSave();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Something went wrong');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-gray-100">{income ? 'Edit Income' : 'Add Income'}</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Amount (₹) *</label>
            <input type="number" min="0.01" step="0.01" required className="input" value={form.amount} onChange={e => set('amount', e.target.value)} />
          </div>
          <div>
            <label className="label">Source</label>
            <select className="input" value={form.source} onChange={e => set('source', e.target.value)}>
              {SOURCES.map(s => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="label">Date *</label>
            <input type="date" required className="input" value={form.date} onChange={e => set('date', e.target.value)} />
          </div>
          <div>
            <label className="label">Description</label>
            <input type="text" className="input" value={form.description} onChange={e => set('description', e.target.value)} />
          </div>
          <div className="flex gap-3 pt-2">
            <button type="submit" className="btn-primary flex-1">{income ? 'Update' : 'Add'} Income</button>
            <button type="button" className="btn-secondary flex-1" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
