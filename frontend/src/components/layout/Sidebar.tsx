import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  CreditCard,
  FileSearch,
} from "lucide-react";


const navigation = [
  {
    name: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Transactions",
    path: "/transactions",
    icon: CreditCard,
  },
  {
    name: "Investigation History",
    path: "/history",
    icon: FileSearch,
  },
];


export default function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-slate-950 border-r border-slate-800 text-slate-200">

      <div className="p-6 border-b border-slate-800">

        <h1 className="text-xl font-bold text-cyan-400">
          AI Risk
        </h1>

        <p className="text-sm text-slate-400 mt-1">
          Investigator
        </p>

      </div>


      <nav className="p-4 space-y-2">

        {navigation.map((item) => {

          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({isActive}) =>
                `
                flex items-center gap-3 px-4 py-3 rounded-lg
                transition
                ${
                  isActive
                  ? "bg-cyan-500/10 text-cyan-400"
                  : "text-slate-400 hover:bg-slate-900 hover:text-white"
                }
                `
              }
            >

              <Icon size={20}/>

              <span>
                {item.name}
              </span>

            </NavLink>
          );

        })}

      </nav>


      <div className="absolute bottom-6 left-6 text-xs text-slate-500">

        System:
        <span className="text-green-400 ml-1">
          Online
        </span>

      </div>


    </aside>
  );
}