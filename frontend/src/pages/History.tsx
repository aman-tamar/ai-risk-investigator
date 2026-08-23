import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

import {
  getInvestigations
} from "@/api/investigations";

import type {
  InvestigationHistory
} from "@/types/investigation";

import PageTransition from "@/components/layout/PageTransition";
import RiskBadge from "@/components/ui/RiskBadge";



export default function History(){


  const [
    investigations,
    setInvestigations
  ] = useState<InvestigationHistory[]>([]);



  const [
    loading,
    setLoading
  ] = useState(true);



  const navigate = useNavigate();




  useEffect(()=>{


    async function load(){


      try{


        const data =
          await getInvestigations();


        setInvestigations(data);


      }
      catch(error){


        console.error(
          "History loading failed",
          error
        );


      }
      finally{


        setLoading(false);


      }


    }


    load();


  },[]);






  if(loading){


    return (

      <div className="
        text-slate-400
      ">

        Loading investigation history...

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

            Investigation History

          </h1>



          <p className="
            text-slate-400
            mt-2
          ">

            Previous AI risk investigations

          </p>


        </div>







        <div className="
          bg-slate-950
          border
          border-slate-800
          rounded-xl
          overflow-hidden
        ">




        {
          investigations.length === 0

          ?

          (

            <div className="
              p-10
              text-center
              text-slate-500
            ">

              No investigations found

            </div>

          )


          :


          (

          <table className="w-full">


            <thead className="bg-slate-900">


              <tr className="
                text-left
                text-slate-400
                text-sm
              ">


                <th className="p-4">
                  ID
                </th>


                <th className="p-4">
                  Transaction ID
                </th>


                <th className="p-4">
                  Risk
                </th>


                <th className="p-4">
                  Score
                </th>


                <th className="p-4">
                  Confidence
                </th>


                <th className="p-4">
                  Created
                </th>


                <th className="p-4">
                  Action
                </th>


              </tr>


            </thead>





            <tbody>


            {
              investigations.map(
                (item)=>(


                <motion.tr

                  key={item.id}

                  initial={{
                    opacity:0,
                    y:10
                  }}

                  animate={{
                    opacity:1,
                    y:0
                  }}

                  transition={{
                    duration:0.25
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

                    {item.id}

                  </td>




                  <td className="p-4">

                    {item.transaction_id}

                  </td>





                  <td className="p-4">


                    <RiskBadge
                      risk={item.risk_level}
                    />


                  </td>





                  <td className="p-4">

                    {item.final_risk_score}

                  </td>





                  <td className="p-4">


                    {item.confidence}%


                  </td>





                  <td className="p-4 text-sm">


                    {
                      new Date(
                        item.created_at
                      ).toLocaleString()
                    }


                  </td>





                  <td className="p-4">



                    <button


                      onClick={()=>(
                        navigate(
                          `/investigation/${item.transaction_id}`
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

                      View

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