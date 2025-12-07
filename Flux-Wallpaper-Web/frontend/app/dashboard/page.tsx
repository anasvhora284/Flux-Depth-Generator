"use client";

import { useCallback, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useDropzone } from 'react-dropzone';
import { Navbar } from '@/components/ui/navbar';
import { Button } from '@/components/ui/button';
import { Upload, File, CheckCircle, AlertCircle, Settings, History } from 'lucide-react';
import api from '@/lib/api';
import { ImageGrid } from '@/components/dashboard/image-grid';
import { HistorySidebar } from '@/components/dashboard/HistorySidebar';
import { useJobHistory } from '@/hooks/useJobHistory';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Slider } from "@/components/ui/slider"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"

export default function Dashboard() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(true);

    // History Hook
    const { history, addJob, updateJobStatus } = useJobHistory();
    const [isHistoryOpen, setIsHistoryOpen] = useState(false);

    // Auth check - redirect to login if not authenticated
    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/login');
        } else {
            setIsLoading(false);
        }
    }, [router]);

    const [files, setFiles] = useState<File[]>([]);
    const [uploading, setUploading] = useState(false);
    const [processedUrl, setProcessedUrl] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [modelType, setModelType] = useState('vits');

    // Advanced Settings State
    const [outputMode, setOutputMode] = useState<'embedded' | 'depth'>('embedded');
    const [colormap, setColormap] = useState('grayscale');
    const [invert, setInvert] = useState(false);
    const [near, setNear] = useState(0);
    const [far, setFar] = useState(100);
    const [includeOriginals, setIncludeOriginals] = useState(false);
    const [isConfigOpen, setIsConfigOpen] = useState(false);

    const [jobId, setJobId] = useState<string | null>(null);
    const [progress, setProgress] = useState(0);

    const checkJobStatus = useCallback(async (id: string) => {
        try {
            const res = await api.get(`/depth/status/${id}`);
            if (res.data.status === 'completed') {
                setJobId(null);
                setProgress(100);

                // Update History
                updateJobStatus(id, 'completed');

                // Fetch the zip file from the backend via API
                const downloadRes = await api.get(res.data.download_url, {
                    responseType: 'blob',
                });

                // Get filename from header or use default
                const contentDisposition = downloadRes.headers['content-disposition'];
                let filename = 'depth_results.zip';
                if (contentDisposition) {
                    const match = contentDisposition.match(/filename=(.+)/);
                    if (match && match[1]) {
                        filename = match[1].replace(/['"]/g, '');
                    }
                }

                // Create blob URL and trigger download
                const url = window.URL.createObjectURL(new Blob([downloadRes.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', filename);
                document.body.appendChild(link);
                link.click();
                link.remove();
                window.URL.revokeObjectURL(url);

                setProcessedUrl(url);
                setUploading(false);
            } else if (res.data.status === 'failed') {
                setJobId(null);
                setUploading(false);
                setError(`Processing failed: ${res.data.error || 'Unknown error'}`);
                updateJobStatus(id, 'failed');
            } else {
                setProgress(res.data.progress || 0);
                setTimeout(() => checkJobStatus(id), 2000);
            }
        } catch (err) {
            console.error(err);
            setJobId(null);
            setUploading(false);
            setError("Failed to check job status.");
            updateJobStatus(id, 'failed');
        }
    }, [updateJobStatus]);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        setFiles(prev => [...prev, ...acceptedFiles]);
        setError(null);
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.png', '.jpg', '.jpeg', '.webp']
        },
        maxFiles: 200
    });

    const handleProcess = async () => {
        if (files.length === 0) return;

        setUploading(true);
        setProcessedUrl(null);
        setError(null);
        setJobId(null);
        setProgress(0);

        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });
        formData.append('model_type', modelType);
        formData.append('output_mode', outputMode);
        formData.append('colormap', colormap);
        formData.append('invert', String(invert));
        formData.append('near', String(near));
        formData.append('far', String(far));
        formData.append('include_originals', String(includeOriginals));


        try {
            // Always expect JSON because backend forces async for everything now
            const response = await api.post('/depth/generate', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            if (response.data.job_id) {
                // Async Job Started (Standard Flow)
                const data = response.data;
                setJobId(data.job_id);

                // Add to History
                const desc = files.length > 1 ? `${files.length} images (${modelType})` : `${files[0].name} (${modelType})`;
                addJob(data.job_id, desc, files.length);

                checkJobStatus(data.job_id);
            } else {
                // Should not happen with current backend logic, but safe fallback
                setUploading(false);
                setError("Unexpected response format from server");
            }

        } catch (err: unknown) {
            console.error(err);
            setError("Failed to process images. Please try again.");
            setUploading(false);
        }
    };

    const removeFile = (index: number) => {
        setFiles(prev => prev.filter((_, i) => i !== index));
    };

    // Show loading while checking auth
    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen flex flex-col relative overflow-x-hidden">
            <Navbar />

            <HistorySidebar history={history} isOpen={isHistoryOpen} onClose={() => setIsHistoryOpen(false)} />

            <main className={`flex-1 container mx-auto px-4 py-8 pt-24 transition-all duration-300 ${isHistoryOpen ? 'mr-80' : ''}`}>
                <div className="max-w-4xl mx-auto space-y-8">
                    <div className="flex items-center justify-between">
                        <div className="text-left space-y-2">
                            <h1 className="text-3xl font-bold font-heading">Depth Tool</h1>
                            <p className="text-muted-foreground">Generate high-quality depth maps from your images.</p>
                        </div>

                        <div className="flex items-center gap-2">
                            <Button
                                variant="outline"
                                className="gap-2 cursor-pointer"
                                onClick={() => setIsHistoryOpen(!isHistoryOpen)}
                            >
                                <History className="h-4 w-4" />
                                {isHistoryOpen ? 'Hide History' : 'History'}
                            </Button>

                            <Dialog open={isConfigOpen} onOpenChange={setIsConfigOpen}>
                                <DialogTrigger asChild>
                                    <Button variant="outline" className="gap-2 cursor-pointer">
                                        <Settings className="h-4 w-4" />
                                        Advanced Config
                                    </Button>
                                </DialogTrigger>
                                <DialogContent className="sm:max-w-[425px] max-h-[85vh] overflow-y-auto">
                                    <DialogHeader>
                                        <DialogTitle>Processing Configuration</DialogTitle>
                                        <DialogDescription>
                                            Choose output type and visualization settings.
                                        </DialogDescription>
                                    </DialogHeader>
                                    <div className="grid gap-6 py-4">
                                        {/* Mode Radio Buttons */}
                                        <div className="space-y-3">
                                            <Label className="text-base font-semibold">Output Type</Label>
                                            <div className="grid grid-cols-2 gap-3">
                                                <div
                                                    onClick={() => setOutputMode('embedded')}
                                                    className={`cursor-pointer p-4 rounded-xl border transition-all ${outputMode === 'embedded'
                                                        ? 'border-blue-500 bg-blue-500/10 ring-2 ring-blue-500/30'
                                                        : 'border-white/10 hover:border-white/30 bg-white/5'
                                                        }`}
                                                >
                                                    <span className="font-semibold block">Embedded Image</span>
                                                    <span className="text-xs text-muted-foreground">Original + Depth in Alpha</span>
                                                </div>
                                                <div
                                                    onClick={() => setOutputMode('depth')}
                                                    className={`cursor-pointer p-4 rounded-xl border transition-all ${outputMode === 'depth'
                                                        ? 'border-blue-500 bg-blue-500/10 ring-2 ring-blue-500/30'
                                                        : 'border-white/10 hover:border-white/30 bg-white/5'
                                                        }`}
                                                >
                                                    <span className="font-semibold block">Depth Map</span>
                                                    <span className="text-xs text-muted-foreground">Visualized depth only</span>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Depth Map Mode Options */}
                                        {outputMode === 'depth' && (
                                            <div className="space-y-4 animate-in fade-in slide-in-from-top-2">
                                                <div className="space-y-3">
                                                    <Label className="text-base font-semibold">Colormap Style</Label>
                                                    <div className="grid grid-cols-2 gap-3">
                                                        {[
                                                            { id: 'grayscale', name: 'Grayscale', gradient: 'from-gray-900 to-gray-100' },
                                                            { id: 'viridis', name: 'Viridis', gradient: 'from-[#440154] via-[#21918c] to-[#fde725]' },
                                                            { id: 'plasma', name: 'Plasma', gradient: 'from-[#0d0887] via-[#cc4778] to-[#f0f921]' },
                                                            { id: 'inferno', name: 'Inferno', gradient: 'from-[#000004] via-[#bb3754] to-[#fcffa4]' },
                                                            { id: 'turbo', name: 'Turbo', gradient: 'from-[#30123b] via-[#a2fc3c] to-[#7a0403]' },
                                                            { id: 'jet', name: 'Jet', gradient: 'from-[#00008f] via-[#fff100] to-[#7f0000]' },
                                                            { id: 'heatmap', name: 'Heatmap', gradient: 'from-blue-600 via-yellow-400 to-red-600' },
                                                            { id: 'edges', name: 'Edges', gradient: 'from-black to-white ring-1 ring-white/20' },
                                                        ].map((cm) => (
                                                            <div
                                                                key={cm.id}
                                                                onClick={() => setColormap(cm.id)}
                                                                className={`cursor-pointer group relative overflow-hidden rounded-lg border transition-all duration-200 ${colormap === cm.id
                                                                    ? 'border-blue-500 ring-2 ring-blue-500/30'
                                                                    : 'border-white/10 hover:border-white/30'
                                                                    }`}
                                                            >
                                                                <div className={`h-12 w-full bg-gradient-to-r ${cm.gradient} opacity-80 group-hover:opacity-100 transition-opacity`} />
                                                                <div className="absolute inset-0 flex items-center justify-center bg-black/40 group-hover:bg-black/20 transition-colors">
                                                                    <span className="text-xs font-medium text-white shadow-sm drop-shadow-md">{cm.name}</span>
                                                                </div>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </div>

                                                <div className="flex items-center justify-between space-x-2 border border-white/10 p-4 rounded-xl bg-white/5">
                                                    <Label htmlFor="invert-mode" className="flex flex-col space-y-1">
                                                        <span className="font-semibold">Invert Depth</span>
                                                        <span className="font-normal text-xs text-muted-foreground">Swap near (white) and far (black)</span>
                                                    </Label>
                                                    <Switch id="invert-mode" checked={invert} onCheckedChange={setInvert} className="data-[state=checked]:bg-blue-600" />
                                                </div>

                                                <div className="flex items-center justify-between space-x-2 border border-white/10 p-4 rounded-xl bg-white/5">
                                                    <Label htmlFor="include-originals" className="flex flex-col space-y-1">
                                                        <span className="font-semibold">Include Original Images</span>
                                                        <span className="font-normal text-xs text-muted-foreground">Also download untouched originals</span>
                                                    </Label>
                                                    <Switch id="include-originals" checked={includeOriginals} onCheckedChange={setIncludeOriginals} className="data-[state=checked]:bg-blue-600" />
                                                </div>

                                                <div className="space-y-6 pt-2">
                                                    <div className="space-y-3">
                                                        <div className="flex justify-between items-center text-sm">
                                                            <Label className="font-semibold">Near Clip Distance</Label>
                                                            <span className="px-2 py-0.5 rounded bg-white/10 text-xs font-mono">{near}%</span>
                                                        </div>
                                                        <Slider value={[near]} min={0} max={100} step={1} onValueChange={(vals: number[]) => setNear(vals[0])} className="py-1" />
                                                    </div>
                                                    <div className="space-y-3">
                                                        <div className="flex justify-between items-center text-sm">
                                                            <Label className="font-semibold">Far Clip Distance</Label>
                                                            <span className="px-2 py-0.5 rounded bg-white/10 text-xs font-mono">{far}%</span>
                                                        </div>
                                                        <Slider value={[far]} min={0} max={100} step={1} onValueChange={(vals: number[]) => setFar(vals[0])} className="py-1" />
                                                    </div>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                    <DialogFooter>
                                        <Button onClick={() => setIsConfigOpen(false)} type="button" className="w-full bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-500/20 cursor-pointer">Save Configuration</Button>
                                    </DialogFooter>
                                </DialogContent>
                            </Dialog>
                        </div>
                    </div>

                    {/* Model Selection */}
                    <div className="bg-white/5 border border-white/10 rounded-xl p-6 backdrop-blur-sm">
                        <label className="block text-sm font-medium mb-3">Select Model Capability</label>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {[
                                { id: 'vits', name: 'ViT-Small', desc: 'Fastest • Good Details' },
                                { id: 'vitb', name: 'ViT-Base', desc: 'Balanced • Better Accuracy' },
                                { id: 'vitl', name: 'ViT-Large', desc: 'Slowest • Maximum Quality' }
                            ].map((model) => (
                                <div
                                    key={model.id}
                                    onClick={() => setModelType(model.id)}
                                    className={`cursor-pointer rounded-xl p-5 border transition-all duration-200 relative overflow-hidden group ${modelType === model.id
                                        ? 'bg-blue-600/10 border-blue-500/50 shadow-[0_0_20px_rgba(37,99,235,0.15)] ring-1 ring-blue-500/50'
                                        : 'bg-white/5 border-white/5 hover:border-white/20 hover:bg-white/10'
                                        }`}
                                >
                                    {modelType === model.id && (
                                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-transparent pointer-events-none" />
                                    )}
                                    <div className="flex items-center justify-between mb-2 relative z-10">
                                        <span className={`font-bold text-lg ${modelType === model.id ? 'text-blue-400' : 'text-white group-hover:text-white/90'}`}>{model.name}</span>
                                        {modelType === model.id ? (
                                            <CheckCircle className="h-5 w-5 text-blue-400 drop-shadow-md" />
                                        ) : (
                                            <div className="h-5 w-5 rounded-full border border-white/20 group-hover:border-white/40" />
                                        )}
                                    </div>
                                    <p className="text-xs text-muted-foreground relative z-10">{model.desc}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div
                        {...getRootProps()}
                        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300
              ${isDragActive ? 'border-blue-500 bg-blue-500/10 scale-[1.02]' : 'border-border/50 hover:border-blue-500/50 hover:bg-white/5 glass-card'}
            `}
                    >
                        <input {...getInputProps()} />
                        <div className="flex flex-col items-center gap-4">
                            <div className="p-5 rounded-full bg-blue-500/10 ring-1 ring-blue-500/20">
                                <Upload className="h-10 w-10 text-blue-500" />
                            </div>
                            <div className="space-y-2">
                                <p className="text-xl font-medium bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                                    Drag & drop images here
                                </p>
                                <p className="text-sm text-muted-foreground">or click to select (Max 200)</p>
                            </div>
                        </div>
                    </div>

                    {files.length > 0 && (
                        <div className="glass-card rounded-xl border border-border/50 p-6 space-y-4 animate-in fade-in slide-in-from-bottom-4">
                            <div className="flex items-center justify-between mb-4">
                                <div className="space-x-2">
                                    <Button size="sm" onClick={() => setFiles([])} className="hover:text-red-400 hover:bg-red-400/10 bg-transparent text-muted-foreground h-8 px-2">Clear All</Button>
                                </div>
                            </div>

                            <ImageGrid files={files} onRemove={removeFile} />

                            <div className="pt-4 border-t border-white/10 flex justify-end gap-3 items-center mt-4">
                                {processedUrl && jobId === null && (
                                    <a
                                        href={processedUrl}
                                        download={processedUrl.includes('api/v1') ? undefined : "depth_results.zip"}
                                        className="flex items-center text-green-400 text-sm mr-auto bg-green-500/10 px-4 py-2 rounded-full border border-green-500/20 hover:bg-green-500/20 transition-colors"
                                    >
                                        <CheckCircle className="h-4 w-4 mr-2" />
                                        Download Ready (Zip)
                                    </a>
                                )}
                                {error && (
                                    <div className="flex items-center text-red-400 text-sm mr-auto bg-red-500/10 px-3 py-1.5 rounded-full border border-red-500/20">
                                        <AlertCircle className="h-4 w-4 mr-2" />
                                        {error}
                                    </div>
                                )}

                                <Button onClick={handleProcess} disabled={uploading} className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg shadow-blue-500/20 border-0 text-ellipsis overflow-hidden h-11 px-8">
                                    {uploading ? (
                                        <>
                                            <span className="animate-spin mr-2">⏳</span>
                                            {jobId ? `Processing Bulk (${progress}%)` : 'Processing...'}
                                        </>
                                    ) : (
                                        `Generate Depth Maps (${files.length})`
                                    )}
                                </Button>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}
