import React, { useEffect, useState } from 'react';
import { getFriends, deleteFriend } from '../../services/api';
import { formatINR } from '../../services/helpers';
import toast from 'react-hot-toast';
import AddFriendForm from './AddFriendForm';
import FriendDetail from './FriendDetail';

export default function LoanDashboard() {
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showAdd, setShowAdd] = useState(false);
  const [editFriend, setEditFriend] = useState(null);
  const [selectedFriend, setSelectedFriend] = useState(null);

  const load = () => {
    setLoading(true);
    getFriends().then(r => setFriends(r.data)).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleDelete = (f) => {
    if (!window.confirm(`Delete ${f.name} and all their transactions?`)) return;
    deleteFriend(f.id).then(() => { toast.success('Deleted'); load(); });
  };

  const totalOwedToMe = friends.filter(f => f.balance > 0).reduce((s, f) => s + f.balance, 0);
  const totalIOwe = friends.filter(f => f.balance < 0).reduce((s, f) => s + Math.abs(f.balance), 0);

  if (selectedFriend) {
    return <FriendDetail friend={selectedFriend} onBack={() => { setSelectedFriend(null); load(); }} />;
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">🤝 Loan Tracker</h2>
        <button className="btn-primary" onClick={() => { setEditFriend(null); setShowAdd(true); }}>+ Add Friend</button>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="card">
          <p className="text-sm text-gray-500 dark:text-gray-400">People owe you</p>
          <p className="text-xl font-bold text-green-500">{formatINR(totalOwedToMe)}</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-500 dark:text-gray-400">You owe others</p>
          <p className="text-xl font-bold text-red-500">{formatINR(totalIOwe)}</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-500 dark:text-gray-400">Net balance</p>
          <p className={`text-xl font-bold ${totalOwedToMe - totalIOwe >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {formatINR(totalOwedToMe - totalIOwe)}
          </p>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-10 text-gray-400">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {friends.length === 0 && <div className="col-span-full card text-center text-gray-400 py-12">No friends added yet</div>}
          {friends.map(f => (
            <div key={f.id} className="card hover:shadow-md transition-shadow cursor-pointer" onClick={() => setSelectedFriend(f)}>
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-gray-100">{f.name}</h3>
                  {f.phone && <p className="text-xs text-gray-500 dark:text-gray-400">{f.phone}</p>}
                </div>
                <div className="flex gap-1" onClick={e => e.stopPropagation()}>
                  <button className="text-xs btn-secondary px-2 py-1" onClick={() => { setEditFriend(f); setShowAdd(true); }}>Edit</button>
                  <button className="text-xs btn-danger px-2 py-1" onClick={() => handleDelete(f)}>Del</button>
                </div>
              </div>
              <div className={`text-lg font-bold ${f.balance > 0 ? 'text-green-500' : f.balance < 0 ? 'text-red-500' : 'text-gray-400'}`}>
                {f.balance > 0 ? `Owes you ${formatINR(f.balance)}` : f.balance < 0 ? `You owe ${formatINR(Math.abs(f.balance))}` : '✅ Settled'}
              </div>
              {f.last_transaction_date && <p className="text-xs text-gray-400 mt-1">Last: {f.last_transaction_date}</p>}
            </div>
          ))}
        </div>
      )}

      {showAdd && (
        <AddFriendForm
          friend={editFriend}
          onSave={() => { setShowAdd(false); setEditFriend(null); load(); }}
          onClose={() => { setShowAdd(false); setEditFriend(null); }}
        />
      )}
    </div>
  );
}
