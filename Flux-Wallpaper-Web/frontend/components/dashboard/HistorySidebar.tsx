import { JobHistoryItem } from '@/hooks/useJobHistory';
import { Button } from '@/components/ui/button';
import { Download, Clock, CheckCircle, XCircle, RotateCw } from 'lucide-react';
import api from '@/lib/api';
import { cn } from '@/lib/utils';
import { useState } from 'react';

interface HistorySidebarProps {
    history: JobHistoryItem[];
    isOpen: boolean;
    onClose: () => void;
}

export function HistorySidebar({ history, isOpen, onClose }: HistorySidebarProps) {
    const [downloading, setDownloading] = useState<string | null>(null);

    const handleDownload = async (jobId: string, filename: string) => {
        try {
            setDownloading(jobId);
            const res = await api.get(`/depth/download/${jobId}`, {
                responseType: 'blob'
            });

            // Create download link
            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement('a');
            link.href = url;
            // Use original filename or default zip
            link.setAttribute('download', filename.includes('.') ? filename : `flux_depth_${jobId.slice(0, 6)}.zip`);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (e) {
            console.error("Download failed", e);
            alert("Download failed. Link may have expired (1 hour limit).");
        } finally {
            setDownloading(null);
        }
    };

    const formatTime = (ms: number) => {
        return new Date(ms).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-y-0 right-0 w-80 bg-black/90 backdrop-blur-xl border-l border-white/10 shadow-2xl z-50 transform transition-transform duration-300 ease-in-out p-6 flex flex-col">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold flex items-center gap-2">
                    <Clock className="w-5 h-5 text-blue-400" />
                    History
                </h2>
                <Button variant="ghost" size="icon" onClick={onClose} className="h-8 w-8 rounded-full hover:bg-white/10">
                    <XCircle className="w-5 h-5 text-muted-foreground" />
                </Button>
            </div>

            <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
                {history.length === 0 ? (
                    <div className="text-center text-muted-foreground py-10">
                        <p>No recent jobs found.</p>
                        <p className="text-xs opacity-60 mt-1">Files expire after 1 hour</p>
                    </div>
                ) : (
                    history.map((item) => (
                        <div key={item.jobId} className="bg-white/5 border border-white/10 rounded-lg p-4 transition-all hover:bg-white/10">
                            <div className="flex justify-between items-start mb-2">
                                <div>
                                    <h3 className="font-semibold text-sm text-gray-200">{item.fileName}</h3>
                                    <span className="text-xs text-muted-foreground">{formatTime(item.timestamp)}</span>
                                </div>
                                {item.status === 'completed' && <CheckCircle className="w-4 h-4 text-green-400" />}
                                {item.status === 'processing' && <RotateCw className="w-4 h-4 text-blue-400 animate-spin" />}
                                {item.status === 'failed' && <XCircle className="w-4 h-4 text-red-400" />}
                            </div>

                            {item.status === 'completed' && (
                                <Button
                                    size="sm"
                                    variant="outline"
                                    className="w-full mt-2 h-8 text-xs bg-blue-500/10 hover:bg-blue-500/20 text-blue-300 border-blue-500/30"
                                    onClick={() => handleDownload(item.jobId, item.fileName)}
                                    disabled={!!downloading}
                                >
                                    {downloading === item.jobId ? (
                                        <span className="animate-spin mr-2">⏳</span>
                                    ) : (
                                        <Download className="w-3 h-3 mr-2" />
                                    )}
                                    {downloading === item.jobId ? 'Downloading...' : 'Download Zip'}
                                </Button>
                            )}
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
