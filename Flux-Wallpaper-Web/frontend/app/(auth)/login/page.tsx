"use client";

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle, RefreshCw } from 'lucide-react';
import api from '@/lib/api';
import { motion, AnimatePresence } from 'framer-motion';

const MAX_RESEND_ATTEMPTS = 5;

export default function LoginPage() {
    const router = useRouter();
    const [step, setStep] = useState<'login' | '2fa' | 'verify-email'>('login');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [otp, setOtp] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [resendCount, setResendCount] = useState(0);
    const [resending, setResending] = useState(false);
    const [resendSuccess, setResendSuccess] = useState(false);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const res = await api.post('/auth/login', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            if (res.data.message === "2FA_REQUIRED") {
                setStep('2fa');
            } else {
                localStorage.setItem('token', res.data.access_token);
                router.push('/dashboard');
            }
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Login failed';
            if (errorMsg.includes('verify your email')) {
                // Trigger resend OTP and show verification screen
                try {
                    await api.post('/auth/resend-otp', { email });
                    setStep('verify-email');
                    setResendCount(1);
                } catch {
                    setError('Failed to send verification email. Please sign up again.');
                }
            } else {
                setError(errorMsg);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleVerify2FA = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const res = await api.post('/auth/verify-2fa', {
                email,
                otp
            });

            localStorage.setItem('token', res.data.access_token);
            router.push('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.detail || '2FA Verification failed');
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyEmail = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const res = await api.post('/auth/verify-signup', {
                email,
                otp
            });

            localStorage.setItem('token', res.data.access_token);
            router.push('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Verification failed');
        } finally {
            setLoading(false);
        }
    };

    const handleResendOtp = async () => {
        if (resendCount >= MAX_RESEND_ATTEMPTS) {
            setError('Maximum resend attempts reached.');
            return;
        }

        setResending(true);
        setError('');
        setResendSuccess(false);

        try {
            await api.post('/auth/resend-otp', { email });
            setResendCount(prev => prev + 1);
            setResendSuccess(true);
            setTimeout(() => setResendSuccess(false), 3000);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to resend OTP');
        } finally {
            setResending(false);
        }
    };

    const getTitle = () => {
        if (step === 'login') return 'Welcome back';
        if (step === '2fa') return 'Two-Factor Authentication';
        return 'Verify Your Email';
    };

    const getDescription = () => {
        if (step === 'login') return 'Enter your credentials to access your account';
        if (step === '2fa') return `Enter the code sent to ${email}`;
        return `A verification code has been sent to ${email}`;
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <Card className="w-full glass-card border-white/10 shadow-2xl backdrop-blur-xl bg-black/40">
                <CardHeader className="space-y-1 text-center">
                    <CardTitle className="text-2xl font-bold tracking-tight">
                        {getTitle()}
                    </CardTitle>
                    <CardDescription>
                        {getDescription()}
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <AnimatePresence mode="wait">
                        {step === 'login' && (
                            <motion.form
                                key="login" 
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }} 
                                onSubmit={handleLogin} 
                                className="space-y-4"
                            >
                                <div className="space-y-2">
                                    <Label htmlFor="email">Email</Label>
                                    <Input
                                        id="email"
                                        type="email"
                                        placeholder="m@example.com"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                        className="bg-white/5 border-white/10 focus:border-blue-500/50"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <div className="flex items-center justify-between">
                                        <Label htmlFor="password">Password</Label>
                                        <Link href="#" className="text-xs text-blue-400 hover:text-blue-300 hover:underline transition-all">
                                            Forgot password?
                                        </Link>
                                    </div>
                                    <Input
                                        id="password"
                                        type="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                        className="bg-white/5 border-white/10 focus:border-blue-500/50"
                                    />
                                </div>

                                {error && (
                                    <div className="flex items-center gap-2 text-red-400 text-sm bg-red-500/10 p-3 rounded-lg border border-red-500/20 animate-in fade-in slide-in-from-top-1">
                                        <AlertCircle className="h-4 w-4 flex-shrink-0" />
                                        {error}
                                    </div>
                                )}

                                <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 transition-colors" disabled={loading} variant="default">
                                    {loading ? 'Signing in...' : 'Sign In'}
                                </Button>
                            </motion.form>
                        )}

                        {step === '2fa' && (
                            <motion.form 
                                key="2fa"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                onSubmit={handleVerify2FA} 
                                className="space-y-4"
                            >
                                <div className="space-y-2">
                                    <Label htmlFor="otp">Security Code</Label>
                                    <Input
                                        id="otp"
                                        placeholder="123456"
                                        value={otp}
                                        onChange={(e) => setOtp(e.target.value)}
                                        required
                                        className="text-center text-lg tracking-widest bg-white/5 border-white/10 focus:border-blue-500/50"
                                        maxLength={6}
                                    />
                                </div>

                                {error && (
                                    <div className="flex items-center gap-2 text-red-400 text-sm bg-red-500/10 p-3 rounded-lg border border-red-500/20 animate-in fade-in slide-in-from-top-1">
                                        <AlertCircle className="h-4 w-4" />
                                        {error}
                                    </div>
                                )}

                                <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 transition-colors" disabled={loading} variant="default">
                                    {loading ? 'Verifying...' : 'Authenticate'}
                                </Button>
                            </motion.form>
                        )}

                        {step === 'verify-email' && (
                            <motion.form 
                                key="verify-email"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                onSubmit={handleVerifyEmail} 
                                className="space-y-4"
                            >
                                <div className="space-y-2">
                                    <Label htmlFor="otp">Verification Code</Label>
                                    <Input
                                        id="otp"
                                        placeholder="123456"
                                        value={otp}
                                        onChange={(e) => setOtp(e.target.value)}
                                        required
                                        className="text-center text-lg tracking-widest bg-white/5 border-white/10 focus:border-blue-500/50"
                                        maxLength={6}
                                    />
                                </div>

                                {error && (
                                    <div className="flex items-center gap-2 text-red-400 text-sm bg-red-500/10 p-3 rounded-lg border border-red-500/20 animate-in fade-in slide-in-from-top-1">
                                        <AlertCircle className="h-4 w-4" />
                                        {error}
                                    </div>
                                )}

                                {resendSuccess && (
                                    <div className="flex items-center gap-2 text-green-400 text-sm bg-green-500/10 p-3 rounded-lg border border-green-500/20 animate-in fade-in slide-in-from-top-1">
                                        New code sent! Check your email.
                                    </div>
                                )}

                                <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 transition-colors" disabled={loading} variant="default">
                                    {loading ? 'Verifying...' : 'Verify & Login'}
                                </Button>

                                <div className="flex items-center justify-between text-sm">
                                    <span className="text-muted-foreground">
                                        Didn't receive code?
                                    </span>
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        size="sm"
                                        onClick={handleResendOtp}
                                        disabled={resending || resendCount >= MAX_RESEND_ATTEMPTS}
                                        className="gap-1 text-blue-400 hover:text-blue-300"
                                    >
                                        <RefreshCw className={`h-3 w-3 ${resending ? 'animate-spin' : ''}`} />
                                        {resending ? 'Sending...' : `Resend (${MAX_RESEND_ATTEMPTS - resendCount} left)`}
                                    </Button>
                                </div>
                            </motion.form>
                        )}
                    </AnimatePresence>
                </CardContent>
                <CardFooter className="flex justify-center border-t border-white/5 pt-6">
                    {step === 'login' ? (
                        <div className="text-sm text-muted-foreground">
                            Don't have an account?{' '}
                            <Link href="/signup" className="text-blue-400 hover:text-blue-300 font-medium hover:underline transition-all">
                                Sign up
                            </Link>
                        </div>
                    ) : (
                        <Button variant="link" onClick={() => { setStep('login'); setOtp(''); setError(''); }} className="text-muted-foreground hover:text-white transition-colors">
                            Back to Login
                        </Button>
                    )}
                </CardFooter>
            </Card>
        </motion.div>
    );
}
