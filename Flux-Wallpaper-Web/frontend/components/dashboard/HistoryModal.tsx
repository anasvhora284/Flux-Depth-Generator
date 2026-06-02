import { JobHistoryItem } from '@/hooks/useJobHistory';
import { Button } from '@/components/ui/button';
import { Download, Clock, XCircle, RotateCw, FileImage, History, Layers } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import api from '@/lib/api';

interface HistoryModalProps {
    history: JobHistoryItem[];
    isOpen: boolean;
    onClose: () => void;
}

export function HistoryModal({ history, isOpen, onClose }: HistoryModalProps) {
    const [downloading, setDownloading] = useState<string | null>(null);

    const now = Date.now();
    const oneHour = 60 * 60 * 1000;
    const recentHistory = history.filter(item => (now - item.timestamp) < oneHour);

    const handleDownload = async (jobId: string, filename: string) => {
        try {
            setDownloading(jobId);
            const res = await api.get(`/depth/download/${jobId}`, {
                responseType: 'blob'
            });

            if (res.data.type === 'application/json' || res.headers['content-type']?.includes('application/json')) {
                const text = await res.data.text();
                throw new Error(JSON.parse(text).detail || "Download failed");
            }

            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement('a');
            link.href = url;
            
            const contentDisposition = res.headers['content-disposition'];
            let downloadName = filename.includes('.') ? filename : `flux_depth.zip`;
            if (contentDisposition) {
                const match = contentDisposition.match(/filename=(.+)/);
                if (match && match[1]) downloadName = match[1].replace(/['"]/g, '');
            }

            link.setAttribute('download', downloadName);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (e: any) {
            console.error(e);
            alert(`Download failed: ${e.message}`);
        } finally {
            setDownloading(null);
        }
    };

    const formatTime = (ms: number) => {
        return new Date(ms).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    <motion.div 
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 overflow-y-auto overflow-x-hidden flex items-center justify-center p-4"
                    >
                        <motion.div
                            initial={{ scale: 0.95, opacity: 0, y: 20 }}
                            animate={{ scale: 1, opacity: 1, y: 0 }}
                            exit={{ scale: 0.95, opacity: 0, y: 20 }}
                            onClick={(e) => e.stopPropagation()}
                            className="relative w-full max-w-2xl rounded-2xl bg-black/80 border border-white/10 shadow-2xl overflow-hidden flex flex-col max-h-[85vh]"
                        >
                            <div className="flex items-center justify-between p-6 border-b border-white/10 bg-white/5">
                                <div>
                                    <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                                        Your History
                                    </h2>
                                    <p className="text-sm text-muted-foreground mt-1">
                                        Generations from the last hour are stored here.
                                    </p>
                                </div>
                                <Button variant="ghost" size="icon" onClick={onClose} className="rounded-full hover:bg-white/10">
                                    <XCircle className="h-6 w-6 opacity-70" />
                                </Button>
                            </div>

                            <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
                                {recentHistory.length === 0 ? (
                                    <div className="text-center py-12 flex flex-col items-center">
                                        <div className="h-16 w-16 rounded-full bg-white/5 flex items-center justify-center mb-4">
                                            <History className="h-8 w-8 text-blue-400" />
                                        </div>
                                        <h3 className="text-lg font-medium text-white">No history yet</h3>
                                        <p className="text-muted-foreground max-w-xs mx-auto mt-2">
                                            Generate some depth maps and they will appear here.
                                        </p>
                                    </div>
                                ) : (
                                    <div className="grid gap-4">
                                        {recentHistory.map((item) => (
                                            <div key={item.jobId} className="group relative bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl p-4 transition-all flex items-center gap-4 px-2">
                                                <div className="relative shrink-0 h-14 w-14 rounded-lg overflow-hidden border border-white/10 bg-black/40">
                                                    <img 
                                                        src={`${resolveApiBaseUrl()}/depth/thumbnail/${item.jobId}`} 
                                                        alt="preview"
                                                        className="h-full w-full object-cover"
                                                        onError={(e) => {
                                                            e.currentTarget.style.display = 'none';
                                                            e.currentTarget.nextElementSibling?.classList.remove('hidden');
                                                        }}
                                                    />
                                                    
                                                    <div className="hidden h-full w-full flex items-center justify-center bg-white/5">
                                                        <FileImage className="h-6 w-6 text-blue-400" />
                                                    </div>

                                                    <div className="absolute top-0 right-0 bg-blue-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-bl-lg">
                                                        {item.totalFiles}
                                                    </div>
                                                </div>
                                                
                                                <div className="flex-1 min-w-0 flex flex-col justify-center gap-1.5">
                                                    <div className="flex items-center gap-2">
                                                        <Layers className="h-4 w-4 text-blue-400" />
                                                        <span className="font-semibold text-white text-sm truncate">
                                                            {item.fileName.replace(/\d+ images/, 'Generated Batch')}
                                                        </span>
                                                    </div>

                                                    <div className="flex items-center gap-3 text-xs text-muted-foreground">
                                                        <span className="flex items-center gap-1">
                                                            <Clock className="h-3 w-3" />
                                                            {formatTime(item.timestamp)}
                                                        </span>
                                                        <span className={`px-2 py-0.5 rounded-full text-[10px] uppercase font-bold tracking-wider ${
                                                            item.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                                                            item.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                                                            'bg-blue-500/20 text-blue-400'
                                                        }`}>
                                                            {item.status}
                                                        </span>
                                                    </div>
                                                </div>

                                                {item.status === 'completed' && (
                                                    <Button
                                                        onClick={() => handleDownload(item.jobId, item.fileName)}
                                                        disabled={!!downloading}
                                                        className="shrink-0 bg-blue-600/10 text-blue-400 hover:bg-blue-600 hover:text-white border border-blue-500/20 transition-all font-medium"
                                                    >
                                                        {downloading === item.jobId ? (
                                                            <RotateCw className="h-4 w-4 animate-spin" />
                                                        ) : (
                                                            <Download className="h-4 w-4" />
                                                        )}
                                                        <span className="ml-2 hidden sm:inline">Download</span>
                                                    </Button>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
