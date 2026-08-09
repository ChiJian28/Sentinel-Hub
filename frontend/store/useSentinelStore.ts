import { create } from 'zustand';

interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  title: string;
  message: string;
}

interface SentinelState {
  targetWallet: string;
  setTargetWallet: (wallet: string) => void;
  
  forceCritical: boolean;
  setForceCritical: (force: boolean) => void;
  
  activeTab: 'overview' | 'keepers' | 'sentry' | 'wallet' | 'audit';
  setActiveTab: (tab: 'overview' | 'keepers' | 'sentry' | 'wallet' | 'audit') => void;
  
  selectedRunId: string | null;
  setSelectedRunId: (runId: string | null) => void;
  
  toasts: ToastMessage[];
  addToast: (toast: Omit<ToastMessage, 'id'>) => void;
  removeToast: (id: string) => void;
}

export const useSentinelStore = create<SentinelState>((set) => ({
  targetWallet: '0x29fdB176C316982Da6876425c7ec2b75041a8552',
  setTargetWallet: (targetWallet) => set({ targetWallet }),
  
  forceCritical: false,
  setForceCritical: (forceCritical) => set({ forceCritical }),
  
  activeTab: 'overview',
  setActiveTab: (activeTab) => set({ activeTab }),
  
  selectedRunId: null,
  setSelectedRunId: (selectedRunId) => set({ selectedRunId }),
  
  toasts: [],
  addToast: (toast) =>
    set((state) => ({
      toasts: [...state.toasts, { ...toast, id: Math.random().toString(36).substring(2, 9) }],
    })),
  removeToast: (id) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),
}));
