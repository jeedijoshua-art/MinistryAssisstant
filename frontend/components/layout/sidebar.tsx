import { LayoutDashboard, Settings } from "lucide-react";

const navigation = [{ label: "Dashboard", icon: LayoutDashboard }, { label: "Settings", icon: Settings }];
export function Sidebar() {
  return <aside className="hidden w-64 shrink-0 border-r border-white/10 bg-slate-950/30 p-5 md:block">
    <p className="text-xs font-semibold tracking-[0.24em] text-gold">ZION PRAYER TOWER</p>
    <h1 className="mt-2 text-xl font-semibold">ZTP Assistant</h1>
    <nav className="mt-10 space-y-2">{navigation.map(({ label, icon: Icon }) => <div key={label} className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-300"><Icon size={18} />{label}</div>)}</nav>
  </aside>;
}
