import React, { useEffect, useState } from 'react';
import { getFriendTransactions } from '../../services/api';
import { formatINR } from '../../services/helpers';
import AddLoanEntry from './AddLoanEntry';
import SettleModal from './SettleModal';

export default function FriendDetail({ friend, onBack }) {
  const [data, setData] = useState(null);
  const [showAdd, setShowAdd] = useState(false);
  const [showSettle, setShowSettle] = useState(false);

  const load = () => {
    getFriendTransactions(friend.id).then(r => setData(r.data));
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { load(); }, [friend.id]);

  const balance = data?.balance ?? 0;

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center gap-3">
        <button className="btn-secondary px-3 py-1.5 text-sm" onClick={onBack}>← Back</button>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{friend.name}</h2>
      </div>

      <div className="card flex items-center justify-between flex-wrap gap-4">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">Current Balance</p>
          <p className={`text-2xl font-bold ${balance > 0 ? 'text-green-500' : balance < 0 ? 'text-red-500' : 'text-gray-400'}`}>
            {balance > 0 ? `Owes you ${formatINR(balance)}` : balance < 0 ? `You owe ${formatINR(Math.abs(balance))}` : '✅ Settled'}
          </p>
        </div>
        <div className="flex gap-2">
          <button className="btn-primary" onClick={() => setShowAdd(true)}>+ Add Entry</button>
          {balance !== 0 && <button className="btn-secondary" onClick={() => setShowSettle(true)}>Settle Tab</button>}
        </div>
      </div>

      <div className="space-y-2">
        {(!data?.transactions || data.transactions.length === 0) && (
          <div className="card text-center text-gray-400 py-12">No transactions yet</div>
        )}
        {(data?.transactions || []).map(tx => (
          <div key={tx.id} className={`card p-4 border-l-4 ${tx.type === 'gave' ? 'border-l-red-400' : tx.type === 'received' ? 'border-l-green-400' : 'border-l-blue-400'}`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900 dark:text-gray-100">
                  {tx.type === 'gave' ? '🔴 You gave' : tx.type === 'received' ? '🟢 They paid' : '✅ Settlement'}
                  {tx.description && ` — ${tx.description}`}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">{tx.date}</p>
              </div>
              <span className={`font-bold text-lg ${tx.type === 'gave' ? 'text-red-500' : 'text-green-500'}`}>
                {formatINR(tx.amount)}
              </span>
            </div>
          </div>
        ))}
      </div>

      {showAdd && <AddLoanEntry friendId={friend.id} onSave={() => { setShowAdd(false); load(); }} onClose={() => setShowAdd(false)} />}
      {showSettle && <SettleModal friendId={friend.id} balance={balance} onSave={() => { setShowSettle(false); load(); }} onClose={() => setShowSettle(false)} />}
    </div>
  );
}
