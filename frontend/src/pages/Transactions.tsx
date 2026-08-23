import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

import {
  getTransactions
} from "@/api/transactions";


import type {
  Transaction
} from "@/types/investigation";


import PageTransition from "@/components/layout/PageTransition";
import RiskBadge from "@/components/ui/RiskBadge";



export default function Transactions(){


  const [
    transactions,
    setTransactions
  ] = useState<Transaction[]>([]);



  const [
    loading,
    setLoading
  ] = useState(true);



  const [
    search,
    setSearch
  ] = useState("");



  const [
    riskFilter,
    setRiskFilter
  ] = useState("ALL");



  const [
    sort,
    setSort
  ] = useState("NONE");



  const navigate = useNavigate();




  useEffect(()=>{


    async function load(){


      try{


        const data =
        await getTransactions();


        setTransactions(data);


      }
      catch(error){


        console.error(
          "Transaction loading failed",
          error
        );


      }
      finally{


        setLoading(false);


      }


    }


    load();


  },[]);






  let filtered =
  transactions.filter((item)=>{


    const matchesSearch =
    item.transaction_id
    .toLowerCase()
    .includes(
      search.toLowerCase()
    );



    const matchesRisk =
    riskFilter === "ALL"
    ||
    item.risk_level === riskFilter;



    return matchesSearch && matchesRisk;


  });





  if(sort==="HIGH"){


    filtered = [...filtered].sort(

      (a,b)=>

      (b.risk_score ?? 0)
      -
      (a.risk_score ?? 0)

    );


  }






  if(loading){


    return (

      <div className="
      text-slate-400
      ">

      Loading transactions...

      </div>

    );


  }






  return (


    <PageTransition>


    <div className="space-y-6">





      <div>


        <h1 className="
        text-3xl
        font-bold
        text-white
        ">

          Transactions

        </h1>



        <p className="
        text-slate-400
        mt-2
        ">

          Monitor financial transaction risk

        </p>


      </div>








      {/* Filters */}



      <div className="
      flex
      gap-4
      ">



        <input


        value={search}


        onChange={
          e=>setSearch(e.target.value)
        }


        placeholder="Search transaction ID"


        className="
        bg-slate-950
        border
        border-slate-800
        rounded-lg
        px-4
        py-2
        text-white
        w-80
        outline-none
        focus:border-cyan-500
        "


        />





        <select


        value={riskFilter}


        onChange={
          e=>setRiskFilter(e.target.value)
        }


        className="
        bg-slate-950
        border
        border-slate-800
        rounded-lg
        px-4
        text-white
        "


        >


          <option value="ALL">
            All Risk
          </option>


          <option value="HIGH">
            High
          </option>


          <option value="MEDIUM">
            Medium
          </option>


          <option value="LOW">
            Low
          </option>


        </select>







        <select


        value={sort}


        onChange={
          e=>setSort(e.target.value)
        }


        className="
        bg-slate-950
        border
        border-slate-800
        rounded-lg
        px-4
        text-white
        "


        >


          <option value="NONE">
            Sort
          </option>


          <option value="HIGH">
            Highest Risk Score
          </option>


        </select>



      </div>









      {/* Table */}



      <div className="
      bg-slate-950
      border
      border-slate-800
      rounded-xl
      overflow-hidden
      ">



      {
        filtered.length === 0

        ?

        (

          <div className="
          p-10
          text-center
          text-slate-500
          ">

          No transactions found

          </div>

        )


        :


        (

        <table className="w-full">



        <thead className="bg-slate-900">


        <tr className="
        text-slate-400
        text-sm
        text-left
        ">


        <th className="p-4">
          ID
        </th>


        <th className="p-4">
          Amount
        </th>


        <th className="p-4">
          Vendor
        </th>


        <th className="p-4">
          Employee
        </th>


        <th className="p-4">
          Timestamp
        </th>


        <th className="p-4">
          Risk
        </th>


        <th className="p-4">
          Score
        </th>


        <th className="p-4">
          Action
        </th>


        </tr>


        </thead>







        <tbody>



        {
          filtered.map((tx)=>(


          <motion.tr


          key={tx.transaction_id}


          initial={{
            opacity:0
          }}


          animate={{
            opacity:1
          }}


          transition={{
            duration:0.2
          }}



          className="
          border-t
          border-slate-800
          text-slate-300
          hover:bg-slate-900
          transition
          "


          >




          <td className="p-4">

            {tx.transaction_id}

          </td>




          <td className="p-4">


            ₹
            {tx.amount.toLocaleString()}


          </td>




          <td className="p-4">

            {tx.vendor_id}

          </td>




          <td className="p-4">

            {tx.employee_id}

          </td>




          <td className="p-4 text-sm">


          {
            new Date(
              tx.timestamp
            ).toLocaleString()
          }


          </td>





          <td className="p-4">


            <RiskBadge

              risk={tx.risk_level}

            />


          </td>






          <td className="p-4">


          {
            tx.risk_score ?? "-"
          }


          </td>







          <td className="p-4">



          <button


          onClick={()=>(
            navigate(
              `/investigation/${tx.transaction_id}`
            )
          )}



          className="
          px-3
          py-2
          rounded-md
          bg-cyan-500/10
          text-cyan-400
          hover:bg-cyan-500/20
          transition
          text-sm
          "


          >

          Investigate


          </button>



          </td>





          </motion.tr>


          ))

        }



        </tbody>



        </table>

        )


      }



      </div>




    </div>


    </PageTransition>


  );


}