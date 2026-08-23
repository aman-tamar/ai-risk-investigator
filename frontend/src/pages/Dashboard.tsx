import { useEffect, useState } from "react";
import { motion } from "framer-motion";

import { getTransactions } from "@/api/transactions";
import { getInvestigations } from "@/api/investigations";

import type {
  Transaction,
  InvestigationHistory,
} from "@/types/investigation";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

import InvestigationTable from "@/components/tables/InvestigationTable";
import PageTransition from "@/components/layout/PageTransition";



export default function Dashboard() {


  const [transactions, setTransactions] =
    useState<Transaction[]>([]);


  const [investigations, setInvestigations] =
    useState<InvestigationHistory[]>([]);



  const [loading, setLoading] =
    useState(true);



  useEffect(() => {


    async function loadData() {


      try {


        const tx =
          await getTransactions();


        const inv =
          await getInvestigations();



        setTransactions(tx);

        setInvestigations(inv);


      }
      catch(error) {


        console.error(
          "Dashboard loading failed",
          error
        );


      }
      finally {


        setLoading(false);


      }


    }


    loadData();


  }, []);





  if (loading) {


    return (

      <div className="
        flex
        items-center
        justify-center
        h-full
        text-slate-400
      ">

        Loading dashboard...


      </div>

    );


  }






  const highRisk =
    transactions.filter(
      t => t.risk_level === "HIGH"
    ).length;



  const mediumRisk =
    transactions.filter(
      t => t.risk_level === "MEDIUM"
    ).length;



  const lowRisk =
    transactions.filter(
      t => t.risk_level === "LOW"
    ).length;



  const assessedTransactions =
    transactions.filter(
      t => t.risk_level !== null
    ).length;



  const notAssessed =
    transactions.filter(
      t => t.risk_level === null
    ).length;





  const riskData = [

    {
      name: "LOW",
      value: lowRisk
    },

    {
      name: "MEDIUM",
      value: mediumRisk
    },

    {
      name: "HIGH",
      value: highRisk
    },

    {
      name: "NOT ASSESSED",
      value: notAssessed
    }

  ];





  const chartColors = [

    "#22c55e",
    "#eab308",
    "#ef4444",
    "#64748b"

  ];





  return (

    <PageTransition>


      <div className="space-y-8">


        <div>


          <h1 className="
            text-3xl
            font-bold
            text-white
          ">

            Risk Overview

          </h1>


          <p className="
            text-slate-400
            mt-2
          ">

            AI powered financial fraud monitoring

          </p>


        </div>






        {/* Summary Cards */}


        <div className="
          grid
          grid-cols-5
          gap-6
        ">


          <SummaryCard
            title="Total Transactions"
            value={transactions.length}
          />


          <SummaryCard
            title="High Risk"
            value={highRisk}
            danger
          />


          <SummaryCard
            title="Medium Risk"
            value={mediumRisk}
            warning
          />



          <SummaryCard
            title="Investigated"
            value={assessedTransactions}
          />



          <SummaryCard
            title="Not Assessed"
            value={notAssessed}
          />



        </div>







        {/* Investigation Coverage */}



        <Card className="
          bg-slate-950
          border-slate-800
        ">


          <CardHeader>


            <CardTitle className="text-white">

              Investigation Coverage

            </CardTitle>


          </CardHeader>



          <CardContent>


            <div className="
              flex
              justify-between
              text-sm
              text-slate-400
              mb-2
            ">


              <span>
                Analyzed Transactions
              </span>


              <span>

                {assessedTransactions}
                /
                {transactions.length}

              </span>


            </div>




            <div className="
              h-3
              bg-slate-800
              rounded-full
              overflow-hidden
            ">


              <motion.div

                initial={{
                  width:0
                }}

                animate={{

                  width:
                  `${
                    transactions.length===0
                    ?
                    0
                    :
                    (
                      assessedTransactions /
                      transactions.length
                    ) * 100
                  }%`

                }}

                transition={{
                  duration:0.8
                }}

                className="
                  h-full
                  bg-cyan-400
                "

              />


            </div>




            <p className="
              text-xs
              text-slate-500
              mt-2
            ">


              {
                transactions.length===0
                ?
                "0"
                :
                (
                  (
                    assessedTransactions /
                    transactions.length
                  ) * 100
                ).toFixed(2)

              }

              % transactions analyzed


            </p>


          </CardContent>


        </Card>







        {/* Risk Chart */}


        <Card className="
          bg-slate-950
          border-slate-800
        ">


          <CardHeader>


            <CardTitle className="text-white">

              Risk Distribution

            </CardTitle>


          </CardHeader>




          <CardContent className="h-[350px]">


            {
              transactions.length === 0

              ?

              <div className="
                h-full
                flex
                items-center
                justify-center
                text-slate-500
              ">

                No transaction data available

              </div>


              :


              <ResponsiveContainer>


                <PieChart>


                  <Pie

                    data={riskData}

                    dataKey="value"

                    nameKey="name"

                    outerRadius={120}

                  >


                    {
                      riskData.map(
                        (_,index)=>(

                          <Cell
                            key={index}
                            fill={
                              chartColors[index]
                            }
                          />

                        )
                      )
                    }


                  </Pie>



                  <Tooltip />

                  <Legend />


                </PieChart>


              </ResponsiveContainer>


            }


          </CardContent>


        </Card>







        {/* Recent Investigations */}



        <Card className="
          bg-slate-950
          border-slate-800
        ">


          <CardHeader>


            <CardTitle className="text-white">

              Recent Investigations

            </CardTitle>


          </CardHeader>




          <CardContent>


            <InvestigationTable

              investigations={
                investigations
              }

            />


          </CardContent>


        </Card>




      </div>


    </PageTransition>


  );


}









function SummaryCard(
{
 title,
 value,
 danger,
 warning
}
:
{
 title:string;
 value:number;
 danger?:boolean;
 warning?:boolean;
}

){



return (


<motion.div

initial={{
opacity:0,
y:15
}}

animate={{
opacity:1,
y:0
}}

transition={{
duration:0.3
}}

>


<Card className="
bg-slate-950
border-slate-800
hover:border-slate-700
transition
">


<CardHeader>


<CardTitle className="
text-sm
text-slate-400
">

{title}


</CardTitle>


</CardHeader>




<CardContent>


<p
className={`
text-3xl
font-bold

${
danger
?
"text-red-400"
:
warning
?
"text-yellow-400"
:
"text-cyan-400"
}

`}
>

{value}


</p>


</CardContent>


</Card>


</motion.div>


);

}