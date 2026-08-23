import { Outlet } from "react-router-dom";
import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";


export default function DashboardLayout(){

  return (

    <div className="flex min-h-screen bg-slate-900">


      <Sidebar/>


      <div className="flex-1 flex flex-col">


        <Header/>


        <main className="flex-1 p-8 overflow-auto">

          <Outlet/>

        </main>


      </div>


    </div>

  );

}