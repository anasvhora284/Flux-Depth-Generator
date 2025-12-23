import { useState, useEffect } from 'react';
import api from '@/lib/api';

export interface JobHistoryItem {
    jobId: string;
    timestamp: number;
    status: 'pending' | 'processing' | 'completed' | 'failed' | 'expired';
    fileName: string;
    totalFiles?: number;
}

const STORAGE_KEY = 'flux_depth_job_history';
const EXPIRATION_MS = 60 * 60 * 1000;

export function useJobHistory() {
    const [history, setHistory] = useState<JobHistoryItem[]>([]);

    useEffect(() => {
        const syncHistory = async () => {
            try {
                const response = await api.get('/depth/jobs');
                const serverJobs: any[] = response.data;

                const mappedJobs: JobHistoryItem[] = serverJobs.map((job: any) => {
                    let dateStr = job.created_at;
                    if (dateStr && !dateStr.endsWith('Z')) {
                        dateStr += 'Z';
                    }
                    
                    return {
                        jobId: job.id,
                        timestamp: new Date(dateStr).getTime(),
                        status: job.status,
                        fileName: `${job.total} images`,
                        totalFiles: job.total
                    };
                });

                const now = Date.now();
                const valid = mappedJobs.filter(item => (now - item.timestamp) < EXPIRATION_MS);

                setHistory(valid);
                localStorage.setItem(STORAGE_KEY, JSON.stringify(valid));

            } catch (e) {
                console.error("Failed to sync job history from server", e);
                try {
                    const stored = localStorage.getItem(STORAGE_KEY);
                    if (stored) {
                        const parsed = JSON.parse(stored);
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
