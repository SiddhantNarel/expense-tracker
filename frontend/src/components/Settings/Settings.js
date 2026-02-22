import React, { useEffect, useState } from 'react';
import { getCategories, createCategory, updateCategory, deleteCategory } from '../../services/api';
import { useTheme } from '../../context/ThemeContext';
import toast from 'react-hot-toast';

export default function Settings() {
  const { darkMode, toggleDarkMode } = useTheme();
  const [categories, setCategories] = useState([]);
  const [showCatForm, setShowCatForm] = useState(false);
  const [catForm, setCatForm] = useState({ name: '', emoji: '', color: '#6366f1' });
  const [editCat, setEditCat] = useState(null);

  const loadCats = () => getCategories().then(r => setCategories(r.data));
  useEffect(() => { loadCats(); }, []);

  const handleSaveCat = async (e) => {
    e.preventDefault();
    try {
      if (editCat) { await updateCategory(editCat.id, catForm); toast.success('Category updated!'); }
      else { await createCategory(catForm); toast.success('Category added!'); }
      setShowCatForm(false); setEditCat(null); setCatForm({ name: '', emoji: '', color: '#6366f1' });
      loadCats();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Error');
    }
  };

  const handleDeleteCat = async (cat) => {
    if (!window.confirm(`Delete "${cat.name}"?`)) return;
    try {
      await deleteCategory(cat.id); toast.success('Deleted'); loadCats();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Error');
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">⚙️ Settings</h2>

      {/* Dark Mode */}
      <div className="card flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">Dark Mode</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Switch between light and dark theme</p>
        </div>
        <button
          onClick={toggleDarkMode}
          className={`relative inline-flex h-7 w-12 items-center rounded-full transition-colors ${darkMode ? 'bg-blue-500' : 'bg-gray-300'}`}
        >
          <span className={`inline-block h-5 w-5 transform rounded-full bg-white shadow transition-transform ${darkMode ? 'translate-x-6' : 'translate-x-1'}`} />
        </button>
      </div>

      {/* Categories */}
      <div className="card space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">Categories</h3>
          <button className="btn-primary text-sm" onClick={() => { setEditCat(null); setCatForm({ name: '', emoji: '', color: '#6366f1' }); setShowCatForm(true); }}>
            + Add Category
          </button>
        </div>
        {showCatForm && (
          <form onSubmit={handleSaveCat} className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="label">Name *</label>
                <input required className="input" value={catForm.name} onChange={e => setCatForm(f => ({ ...f, name: e.target.value }))} />
              </div>
              <div>
                <label className="label">Emoji</label>
                <input className="input" value={catForm.emoji} onChange={e => setCatForm(f => ({ ...f, emoji: e.target.value }))} placeholder="🎯" />
              </div>
              <div>
                <label className="label">Color</label>
                <input type="color" className="input h-10 p-1 cursor-pointer" value={catForm.color} onChange={e => setCatForm(f => ({ ...f, color: e.target.value }))} />
              </div>
            </div>
            <div className="flex gap-2">
              <button type="submit" className="btn-primary text-sm px-4 py-1.5">{editCat ? 'Update' : 'Add'}</button>
              <button type="button" className="btn-secondary text-sm px-4 py-1.5" onClick={() => { setShowCatForm(false); setEditCat(null); }}>Cancel</button>
            </div>
          </form>
        )}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {categories.map(c => (
            <div key={c.id} className="flex items-center justify-between p-2 rounded-lg bg-gray-50 dark:bg-gray-700/50">
              <span className="text-sm" style={{ color: c.color }}>{c.emoji} {c.name}</span>
              {c.is_custom ? (
                <div className="flex gap-1">
                  <button className="text-xs text-blue-500 hover:underline" onClick={() => { setEditCat(c); setCatForm({ name: c.name, emoji: c.emoji, color: c.color }); setShowCatForm(true); }}>Edit</button>
                  <button className="text-xs text-red-500 hover:underline" onClick={() => handleDeleteCat(c)}>Del</button>
                </div>
              ) : <span className="text-xs text-gray-400">Built-in</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
