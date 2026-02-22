import axios from 'axios';

const BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({ baseURL: BASE });

// Expenses
export const getExpenses = (params) => api.get('/expenses', { params });
export const getExpense = (id) => api.get(`/expenses/${id}`);
export const createExpense = (data) => api.post('/expenses', data);
export const updateExpense = (id, data) => api.put(`/expenses/${id}`, data);
export const deleteExpense = (id) => api.delete(`/expenses/${id}`);

// Income
export const getIncomes = (params) => api.get('/income', { params });
export const createIncome = (data) => api.post('/income', data);
export const updateIncome = (id, data) => api.put(`/income/${id}`, data);
export const deleteIncome = (id) => api.delete(`/income/${id}`);
export const getIncomeSources = () => api.get('/income/sources');

// Categories
export const getCategories = () => api.get('/categories');
export const createCategory = (data) => api.post('/categories', data);
export const updateCategory = (id, data) => api.put(`/categories/${id}`, data);
export const deleteCategory = (id) => api.delete(`/categories/${id}`);

// Loans / Friends
export const getFriends = () => api.get('/friends');
export const createFriend = (data) => api.post('/friends', data);
export const updateFriend = (id, data) => api.put(`/friends/${id}`, data);
export const deleteFriend = (id) => api.delete(`/friends/${id}`);
export const getFriendTransactions = (id) => api.get(`/friends/${id}/transactions`);
export const addTransaction = (id, data) => api.post(`/friends/${id}/transactions`, data);
export const settleBalance = (id, data) => api.post(`/friends/${id}/settle`, data);

// Budgets
export const getBudgets = (params) => api.get('/budgets', { params });
export const setBudget = (data) => api.post('/budgets', data);
export const deleteBudget = (id) => api.delete(`/budgets/${id}`);

// Analytics
export const getSummary = (params) => api.get('/analytics/summary', { params });
export const getCategoryBreakdown = (params) => api.get('/analytics/category-breakdown', { params });
export const getTrends = (params) => api.get('/analytics/trends', { params });
export const getIncomeVsExpense = (params) => api.get('/analytics/income-vs-expense', { params });

// Export
export const exportExpenses = (params) => `${BASE}/export/expenses?${new URLSearchParams(params)}`;
export const exportIncome = (params) => `${BASE}/export/income?${new URLSearchParams(params)}`;
export const exportLoans = () => `${BASE}/export/loans`;
export const exportReport = (params) => `${BASE}/export/report?${new URLSearchParams(params)}`;

// Settings
export const getSettings = () => api.get('/settings');
export const updateSettings = (data) => api.put('/settings', data);

export default api;
