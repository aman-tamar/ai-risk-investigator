import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import DashboardLayout from "@/layouts/DashboardLayout";

import Dashboard from "@/pages/Dashboard";

import Transactions from "@/pages/Transactions";

import InvestigationDetail from "@/pages/InvestigationDetail";

import History from "@/pages/History";


function Placeholder(){

  return (
    <div className="text-white text-2xl">
      Coming Soon
    </div>
  );

}


export default function App(){

  return (

    <BrowserRouter>

      <Routes>


        <Route element={<DashboardLayout/>}>


          {/* Dashboard Page */}
          <Route
            path="/"
            element={<Dashboard/>}
          />


          {/* Still placeholders for now */}
          <Route
            path="/transactions"
            element={<Transactions/>}
          />


          <Route
            path="/history"
            element={<History/>}
          />

          <Route
          path="/investigation/:transaction_id"
          element={<InvestigationDetail/>}
          />


        </Route>


      </Routes>


    </BrowserRouter>

  );

}