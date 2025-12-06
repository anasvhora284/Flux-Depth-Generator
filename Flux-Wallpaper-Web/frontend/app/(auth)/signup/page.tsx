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

const MAX_RESEND_ATTEMPTS = 5;

export default function SignupPage() {
    const router = useRouter();
    const [step, setStep] = useState<'details' | 'otp'>('details');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [otp, setOtp] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [resendCount, setResendCount] = useState(0);
    const [resending, setResending] = useState(false);
    const [resendSuccess, setResendSuccess] = useState(false);

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await api.post('/auth/signup', {
                email,
                password,
                full_name: fullName
            });
            setStep('otp');
            setResendCount(0); // Reset resend count on new signup
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Signup failed');
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOtp = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await api.post('/auth/verify-signup', {
                email,
                otp
            });

            // Store token
            localStorage.setItem('token', response.data.access_token);
            router.push('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Verification failed');
        } finally {
            setLoading(false);
        }
    };

    const handleResendOtp = async () => {
        if (resendCount >= MAX_RESEND_ATTEMPTS) {
            setError('Maximum resend attempts reached. Please start over.');
            setTimeout(() => {
                router.push('/signup');
                setStep('details');
                setEmail('');
                setPassword('');
                setFullName('');
                setOtp('');
                setResendCount(0);
            }, 2000);
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

    return (
        <Card className="w-full glass-card border-white/10 shadow-2xl">
            <CardHeader className="space-y-1 text-center">
                <CardTitle className="text-2xl font-bold tracking-tight">
                    {step === 'details' ? 'Create your account' : 'Verify Email'}
                </CardTitle>
                <CardDescription>
                    {step === 'details'
                        ? 'Enter your details below to create your account'
                        : `We sent a code to ${email}. Please enter it below.`}
                </CardDescription>
            </CardHeader>
            <CardContent>
                {step === 'details' ? (
                    <form onSubmit={handleSignup} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="fullName">Full Name</Label>
                            <Input
                                id="fullName"
                                placeholder="John Doe"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="m@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>

                        {error && (
                            <div className="flex items-center gap-2 text-red-400 text-sm bg-red-500/10 p-3 rounded-lg border border-red-500/20">
                                <AlertCircle className="h-4 w-4" />
                                {error}
                            </div>
                        )}

                        <Button type="submit" className="w-full" disabled={loading} variant="premium">
                            {loading ? 'Creating Account...' : 'Sign Up'}
                        </Button>
                    </form>
                ) : (
                    <form onSubmit={handleVerifyOtp} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="otp">One-Time Password</Label>
                            <Input
                                id="otp"
                                placeholder="123456"
                                value={otp}
                                onChange={(e) => setOtp(e.target.value)}
                                required
                                className="text-center text-lg tracking-widest"
                                maxLength={6}
                            />
                        </div>

                        {error && (
                            <div className="flex items-center gap-2 text-red-400 text-sm bg-red-500/10 p-3 rounded-lg border border-red-500/20">
                                <AlertCircle className="h-4 w-4" />
                                {error}
                            </div>
                        )}

                        {resendSuccess && (
                            <div className="flex items-center gap-2 text-green-400 text-sm bg-green-500/10 p-3 rounded-lg border border-green-500/20">
                                New code sent! Check your email.
                            </div>
                        )}

                        <Button type="submit" className="w-full" disabled={loading} variant="premium">
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
                    </form>
                )}
            </CardContent>
            <CardFooter className="flex justify-center">
                {step === 'details' ? (
                    <div className="text-sm text-muted-foreground">
                        Already have an account?{' '}
                        <Link href="/login" className="text-blue-400 hover:text-blue-300 font-medium">
                            Sign in
                        </Link>
                    </div>
                ) : (
                    <Button variant="link" onClick={() => setStep('details')} className="text-muted-foreground">
                        Back to Signup
                    </Button>
                )}
            </CardFooter>
        </Card>
    );
}

