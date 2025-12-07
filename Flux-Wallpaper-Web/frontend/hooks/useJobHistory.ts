import { useState, useEffect } from 'react';
import api from '@/lib/api';

export interface JobHistoryItem {
    jobId: string;
    timestamp: number;
    status: 'pending' | 'processing' | 'completed' | 'failed' | 'expired';
    fileName: string; // Display name (e.g., "3 images (vits)")
    totalFiles?: number;
}

const STORAGE_KEY = 'flux_depth_job_history';
const EXPIRATION_MS = 60 * 60 * 1000; // 1 Hour

export function useJobHistory() {
    const [history, setHistory] = useState<JobHistoryItem[]>([]);

    // Load from API + LocalStorage on mount
    useEffect(() => {
        const syncHistory = async () => {
            try {
                // 1. Fetch from Server (Primary Source of Truth)
                const response = await api.get('/depth/jobs');
                const serverJobs: any[] = response.data;

                const mappedJobs: JobHistoryItem[] = serverJobs.map((job: any) => ({
                    jobId: job.id,
                    timestamp: new Date(job.created_at).getTime(),
                    status: job.status,
                    fileName: `${job.total} files`, // Or some better description
                    totalFiles: job.total
                }));

                // 2. Filter expired (client side double check)
                const now = Date.now();
                const valid = mappedJobs.filter(item => (now - item.timestamp) < EXPIRATION_MS);

                setHistory(valid);
                localStorage.setItem(STORAGE_KEY, JSON.stringify(valid));

            } catch (e) {
                console.error("Failed to sync job history from server", e);
                // Fallback to local storage if server fails
                try {
                    const stored = localStorage.getItem(STORAGE_KEY);
                    if (stored) {
                        const parsed = JSON.parse(stored);
                        // Filter expired locally
                        const now = Date.now();
                        const valid = parsed.filter((item: JobHistoryItem) => (now - item.timestamp) < EXPIRATION_MS);
                        setHistory(valid);
                    }
                } catch (localErr) {
                    console.error("Local storage error", localErr);
                }
            }
        };

        syncHistory();
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
