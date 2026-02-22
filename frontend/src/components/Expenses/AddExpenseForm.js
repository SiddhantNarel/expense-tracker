import React, { useState, useEffect } from 'react';
import { createExpense, updateExpense } from '../../services/api';
import { getToday } from '../../services/helpers';
import toast from 'react-hot-toast';

const PAYMENT_METHODS = ['Cash', 'GPay', 'Credit Card', 'Debit Card', 'Wallet'];

export default function AddExpenseForm({ expense, categories, onSave, onClose }) {
  const [form, setForm] = useState({
    amount: '',
    category_id: '',
    date: getToday(),
    description: '',
    payment_method: 'Cash',
  });

  useEffect(() => {
    if (expense) {
      setForm({
        amount: expense.amount || '',
        category_id: expense.category_id || '',
        date: expense.date || getToday(),
        description: expense.description || '',
        payment_method: expense.payment_method || 'Cash',
      });
    }
  }, [expense]);

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...form, amount: parseFloat(form.amount), category_id: form.category_id || null };
      if (expense?.id) {
        await updateExpense(expense.id, payload);
        toast.success('Expense updated!');
      } else {
        await createExpense(payload);
        toast.success('Expense added!');
      }
      onSave();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Something went wrong');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-gray-100">
          {expense ? 'Edit Expense' : 'Add Expense'}
        </h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Amount (₹) *</label>
            <input type="number" min="0.01" step="0.01" required className="input" value={form.amount} onChange={e => set('amount', e.target.value)} placeholder="0.00" />
          </div>
          <div>
            <label className="label">Category</label>
            <select className="input" value={form.category_id} onChange={e => set('category_id', e.target.value)}>
              <option value="">Select category</option>
              {categories.map(c => <option key={c.id} value={c.id}>{c.emoji} {c.name}</option>)}
            </select>
          </div>
          <div>
            <label className="label">Date *</label>
            <input type="date" required className="input" value={form.date} onChange={e => set('date', e.target.value)} />
          </div>
          <div>
            <label className="label">Description</label>
            <input type="text" className="input" value={form.description} onChange={e => set('description', e.target.value)} placeholder="e.g. Lunch at restaurant" />
          </div>
          <div>
            <label className="label">Payment Method</label>
            <select className="input" value={form.payment_method} onChange={e => set('payment_method', e.target.value)}>
              {PAYMENT_METHODS.map(m => <option key={m}>{m}</option>)}
            </select>
          </div>
          <div className="flex gap-3 pt-2">
            <button type="submit" className="btn-primary flex-1">{expense ? 'Update' : 'Add'} Expense</button>
            <button type="button" className="btn-secondary flex-1" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
