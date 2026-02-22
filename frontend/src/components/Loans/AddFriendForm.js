import React, { useState, useEffect } from 'react';
import { createFriend, updateFriend } from '../../services/api';
import toast from 'react-hot-toast';

export default function AddFriendForm({ friend, onSave, onClose }) {
  const [form, setForm] = useState({ name: '', phone: '', notes: '' });

  useEffect(() => {
    if (friend) setForm({ name: friend.name || '', phone: friend.phone || '', notes: friend.notes || '' });
  }, [friend]);

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (friend?.id) { await updateFriend(friend.id, form); toast.success('Friend updated!'); }
      else { await createFriend(form); toast.success('Friend added!'); }
      onSave();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Something went wrong');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-gray-100">{friend ? 'Edit Friend' : 'Add Friend'}</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Name *</label>
            <input required className="input" value={form.name} onChange={e => set('name', e.target.value)} placeholder="Friend's name" />
          </div>
          <div>
            <label className="label">Phone (optional)</label>
            <input className="input" value={form.phone} onChange={e => set('phone', e.target.value)} placeholder="+91 9999999999" />
          </div>
          <div>
            <label className="label">Notes</label>
            <textarea className="input" rows={2} value={form.notes} onChange={e => set('notes', e.target.value)} placeholder="Any notes..." />
          </div>
          <div className="flex gap-3 pt-2">
            <button type="submit" className="btn-primary flex-1">{friend ? 'Update' : 'Add'} Friend</button>
            <button type="button" className="btn-secondary flex-1" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
