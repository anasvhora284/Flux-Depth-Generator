import { useState, useEffect } from 'react';

export interface JobHistoryItem {
    jobId: string;
    timestamp: number;
    status: 'processing' | 'completed' | 'failed' | 'expired';
    fileName: string; // Display name (e.g., "3 images (vits)")
    totalFiles?: number;
}

const STORAGE_KEY = 'flux_depth_job_history';
const EXPIRATION_MS = 60 * 60 * 1000; // 1 Hour

export function useJobHistory() {
    const [history, setHistory] = useState<JobHistoryItem[]>([]);

    // Load from LocalStorage on mount
    useEffect(() => {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                const parsed: JobHistoryItem[] = JSON.parse(stored);

                // Filter expired
                const now = Date.now();
                const valid = parsed.filter(item => (now - item.timestamp) < EXPIRATION_MS);

                setHistory(valid);

                // Update storage if items were removed
                if (valid.length !== parsed.length) {
                    localStorage.setItem(STORAGE_KEY, JSON.stringify(valid));
                }
            }
        } catch (e) {
            console.error("Failed to load job history", e);
        }
    }, []);

    const saveToStorage = (items: JobHistoryItem[]) => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
        setHistory(items);
    };

    const addJob = (jobId: string, fileName: string, totalFiles: number = 1) => {
        const newItem: JobHistoryItem = {
            jobId,
            timestamp: Date.now(),
            status: 'processing',
            fileName,
            totalFiles
        };

        // Add to beginning
        const newHistory = [newItem, ...history];
        saveToStorage(newHistory);
    };

    const updateJobStatus = (jobId: string, status: JobHistoryItem['status']) => {
        const newHistory = history.map(item =>
            item.jobId === jobId ? { ...item, status } : item
        );
        saveToStorage(newHistory);
    };

    const clearHistory = () => {
        saveToStorage([]);
    };

    return { history, addJob, updateJobStatus, clearHistory };
}
