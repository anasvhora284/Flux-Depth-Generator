"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Navbar } from '@/components/ui/navbar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch'; // Need to create Switch or use checkbox for now
import { User, Shield, Key, Mail, CheckCircle } from 'lucide-react';
import api from '@/lib/api';

export default function SettingsPage() {
    const router = useRouter();
    const [user, setUser] = useState<any>(null);
    const [fullName, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [is2FAEnabled, setIs2FAEnabled] = useState(false);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchUser();
    }, []);

    const fetchUser = async () => {
        try {
            const res = await api.get('/users/me');
            setUser(res.data);
            setFullName(res.data.full_name || '');
            setEmail(res.data.email || '');
            setIs2FAEnabled(res.data.is_2fa_enabled || false);
        } catch (err) {
            console.error(err);
            // router.push('/login');
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateProfile = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        setSaving(true);
        setMessage('');

        try {
            const updateData: any = { full_name: fullName, email };
            if (newPassword) updateData.password = newPassword;

            await api.put('/users/me', updateData);
            setMessage('Profile updated successfully!');
            setTimeout(() => setMessage(''), 3000);
        } catch (err: any) {
            console.error(err);
            setMessage('Failed to update profile.');
        } finally {
            setSaving(false);
        }
    };

    const toggle2FA = async (enabled: boolean) => {
        try {
            await api.post('/users/me/2fa', { enable: enabled });
            setIs2FAEnabled(enabled);
            setMessage(`2FA ${enabled ? 'Enabled' : 'Disabled'}`);
            setTimeout(() => setMessage(''), 3000);
        } catch (err) {
            console.error(err);
            setMessage('Failed to toggle 2FA.');
        }
    };

    if (loading) return <div className="min-h-screen flex items-center justify-center text-white">Loading...</div>;

    return (
        <div className="min-h-screen flex flex-col">
            <Navbar />

            <main className="flex-1 container mx-auto px-4 py-8 pt-32">
                <div className="max-w-3xl mx-auto space-y-8">
                    <div>
                        <h1 className="text-3xl font-bold font-heading">Settings</h1>
                        <p className="text-muted-foreground">Manage your account preferences and security.</p>
                    </div>

                    {message && (
                        <div className="bg-green-500/10 border border-green-500/20 text-green-400 p-4 rounded-xl flex items-center gap-2">
                            <CheckCircle className="h-5 w-5" />
                            {message}
                        </div>
                    )}

                    <div className="grid gap-8">
                        {/* Profile Section */}
                        <Card className="glass-card border-white/10">
                            <CardHeader>
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400">
                                        <User className="h-5 w-5" />
                                    </div>
                                    <div>
                                        <CardTitle>Profile Information</CardTitle>
                                        <CardDescription>Update your personal details</CardDescription>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <form onSubmit={handleUpdateProfile} className="space-y-4">
                                    <div className="grid md:grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label>Full Name</Label>
                                            <Input
                                                value={fullName}
                                                onChange={(e) => setFullName(e.target.value)}
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <Label>Email</Label>
                                            <Input
                                                value={email}
                                                onChange={(e) => setEmail(e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <Label>New Password (Optional)</Label>
                                        <Input
                                            type="password"
                                            placeholder="Leave blank to keep current"
                                            value={newPassword}
                                            onChange={(e) => setNewPassword(e.target.value)}
                                        />
                                    </div>
                                </form>
                            </CardContent>
                        </Card>

                        {/* Security Section */}
                        <Card className="glass-card border-white/10">
                            <CardHeader>
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-purple-500/20 rounded-lg text-purple-400">
                                        <Shield className="h-5 w-5" />
                                    </div>
                                    <div>
                                        <CardTitle>Security</CardTitle>
                                        <CardDescription>Manage your 2-Factor Authentication</CardDescription>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 p-4 rounded-xl bg-white/5 border border-white/5">
                                    <div className="space-y-1 flex-1">
                                        <h4 className="font-medium flex items-center gap-2 flex-wrap">
                                            Two-Factor Authentication
                                            {is2FAEnabled && <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full">Enabled</span>}
                                        </h4>
                                        <p className="text-sm text-muted-foreground">
                                            Secure your account by requiring an OTP sent to your email upon login.
                                        </p>
                                    </div>
                                    <div className="flex items-center gap-3 flex-shrink-0">
                                        <span className="text-sm font-medium text-muted-foreground">{is2FAEnabled ? 'On' : 'Off'}</span>
                                        <Switch
                                            checked={is2FAEnabled}
                                            onCheckedChange={toggle2FA}
                                            className="data-[state=checked]:bg-green-500"
                                        />
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        <div className="flex justify-end pt-4">
                            <Button onClick={() => handleUpdateProfile()} disabled={saving} variant="premium" className="w-full md:w-auto">
                                {saving ? 'Saving...' : 'Save Changes'}
                            </Button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
