import React, { useState } from 'react';
import { settleBalance } from '../../services/api';
import { formatINR, getToday } from '../../services/helpers';
import toast from 'react-hot-toast';

export default function SettleModal({ friendId, balance, onSave, onClose }) {
  const [amount, setAmount] = useState(Math.abs(balance));
  const [date, setDate] = useState(getToday());
  const [description, setDescription] = useState('Settlement');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await settleBalance(friendId, { amount: parseFloat(amount), date, description });
      toast.success('Settled!');
      onSave();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Error');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6">
        <h3 className="text-lg font-bold mb-2 text-gray-900 dark:text-gray-100">Settle Tab</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
          Current balance: <span className="font-semibold">{formatINR(Math.abs(balance))}</span>
          {balance > 0 ? ' (they owe you)' : ' (you owe them)'}
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Amount (₹)</label>
            <input type="number" min="0.01" step="0.01" required className="input" value={amount} onChange={e => setAmount(e.target.value)} />
          </div>
          <div>
            <label className="label">Date</label>
            <input type="date" required className="input" value={date} onChange={e => setDate(e.target.value)} />
          </div>
          <div>
            <label className="label">Note</label>
            <input type="text" className="input" value={description} onChange={e => setDescription(e.target.value)} />
          </div>
          <div className="flex gap-3 pt-2">
            <button type="submit" className="btn-primary flex-1">Settle</button>
            <button type="button" className="btn-secondary flex-1" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
