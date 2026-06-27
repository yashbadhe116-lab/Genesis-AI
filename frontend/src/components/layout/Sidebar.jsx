import { LayoutDashboard, FolderOpen, History, CreditCard, Settings } from "lucide-react";

const menu = [
    { icon: LayoutDashboard, label: "Dashboard" },
    { icon: FolderOpen, label: "Projects" },
    { icon: History, label: "History" },
    { icon: CreditCard, label: "Billing" },
    { icon: Settings, label: "Settings" },
];

export default function Sidebar() {
    return (
        <aside className="w-64 bg-slate-900 text-white min-h-screen border-r border-slate-800">
            <div className="p-6">
                <h1 className="text-2xl font-bold">Genesis AI</h1>
            </div>

            <nav className="space-y-2 px-3">
                {menu.map((item) => {
                    const Icon = item.icon;

                    return (
                        <button
                            key={item.label}
                            className="flex items-center gap-3 w-full rounded-lg px-4 py-3 hover:bg-slate-800 transition"
                        >
                            <Icon size={20} />
                            <span>{item.label}</span>
                        </button>
                    );
                })}
            </nav>
        </aside>
    );
}