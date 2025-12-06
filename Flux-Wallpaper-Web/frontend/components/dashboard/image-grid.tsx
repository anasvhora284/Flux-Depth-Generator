"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { File as FileIcon, X, ChevronLeft, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ImageGridProps {
    files: File[];
    onRemove: (index: number) => void;
}

export function ImageGrid({ files, onRemove }: ImageGridProps) {
    const ITEMS_PER_PAGE = 9;
    const [currentPage, setCurrentPage] = useState(0);
    const [previews, setPreviews] = useState<Record<string, string>>({});

    const totalPages = Math.ceil(files.length / ITEMS_PER_PAGE);

    // Reset to last page if current page becomes empty
    if (currentPage >= totalPages && totalPages > 0) {
        setCurrentPage(totalPages - 1);
    }

    // Generate previews
    useEffect(() => {
        const newPreviews: Record<string, string> = {};
        const currentFileNames = new Set(files.map(f => f.name));

        files.forEach(file => {
            if (!previews[file.name]) {
                newPreviews[file.name] = URL.createObjectURL(file);
            }
        });

        const previewsToRevoke: string[] = [];
        for (const fileName in previews) {
            if (!currentFileNames.has(fileName)) {
                URL.revokeObjectURL(previews[fileName]);
                previewsToRevoke.push(fileName);
            }
        }

        if (Object.keys(newPreviews).length > 0 || previewsToRevoke.length > 0) {
            setPreviews(prev => {
                const updatedPreviews = { ...prev, ...newPreviews };
                previewsToRevoke.forEach(fileName => delete updatedPreviews[fileName]);
                return updatedPreviews;
            });
        }

        return () => {
            Object.values(previews).forEach(url => URL.revokeObjectURL(url));
        };
    }, [files]);

    const currentFiles = files.slice(
        currentPage * ITEMS_PER_PAGE,
        (currentPage + 1) * ITEMS_PER_PAGE
    );

    const nextPage = () => setCurrentPage(p => Math.min(p + 1, totalPages - 1));
    const prevPage = () => setCurrentPage(p => Math.max(p - 1, 0));

    // Determine grid columns based on file count
    const getGridCols = () => {
        const count = currentFiles.length;
        if (count === 1) return 'grid-cols-1';
        if (count === 2) return 'grid-cols-2';
        if (count <= 4) return 'grid-cols-2 sm:grid-cols-2';
        return 'grid-cols-2 sm:grid-cols-3';
    };

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between">
                <h3 className="font-semibold text-lg">Selected Images <span className="text-muted-foreground text-sm ml-2">({files.length})</span></h3>
                <div className="flex gap-2">
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={prevPage}
                        disabled={currentPage === 0}
                        className="h-8 w-8 hover:bg-white/10 hover:text-white disabled:opacity-30"
                    >
                        <ChevronLeft className="h-4 w-4" />
                    </Button>
                    <span className="text-sm self-center text-muted-foreground w-12 text-center font-mono">
                        {totalPages === 0 ? '0/0' : `${currentPage + 1}/${totalPages}`}
                    </span>
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={nextPage}
                        disabled={currentPage >= totalPages - 1}
                        className="h-8 w-8 hover:bg-white/10 hover:text-white disabled:opacity-30"
                    >
                        <ChevronRight className="h-4 w-4" />
                    </Button>
                </div>
            </div>

            <div className={`grid ${getGridCols()} gap-2 sm:gap-3`}>
                <AnimatePresence mode="popLayout">
                    {currentFiles.map((file, i) => {
                        const globalIndex = currentPage * ITEMS_PER_PAGE + i;
                        const preview = previews[file.name];

                        return (
                            <motion.div
                                key={`${file.name}-${globalIndex}`}
                                layout
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.8 }}
                                className="relative group bg-black/40 border border-white/10 rounded-lg overflow-hidden aspect-square"
                            >
                                <div className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 sm:group-hover:opacity-100 transition-opacity z-20">
                                    <button
                                        onClick={() => onRemove(globalIndex)}
                                        className="p-1.5 bg-red-500 hover:bg-red-600 text-white rounded-full transition-colors shadow-lg"
                                    >
                                        <X className="h-3 w-3" />
                                    </button>
                                </div>

                                {/* Mobile: Always show delete button */}
                                <div className="sm:hidden absolute top-1 right-1 z-20">
                                    <button
                                        onClick={() => onRemove(globalIndex)}
                                        className="p-1.5 bg-red-500/80 text-white rounded-full shadow-lg"
                                    >
                                        <X className="h-3 w-3" />
                                    </button>
                                </div>

                                {preview ? (
                                    <div className="absolute inset-0 z-0">
                                        <img
                                            src={preview}
                                            alt={file.name}
                                            className="w-full h-full object-cover"
                                        />
                                        <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors" />
                                    </div>
                                ) : (
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <div className="p-3 bg-blue-500/20 rounded-full">
                                            <FileIcon className="h-6 w-6 text-blue-400" />
                                        </div>
                                    </div>
                                )}

                                <div className="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/90 via-black/60 to-transparent z-10">
                                    <p className="text-[10px] sm:text-xs font-medium truncate w-full text-white/90">
                                        {file.name}
                                    </p>
                                </div>
                            </motion.div>
                        );
                    })}
                </AnimatePresence>
            </div>
        </div>
    );
}


