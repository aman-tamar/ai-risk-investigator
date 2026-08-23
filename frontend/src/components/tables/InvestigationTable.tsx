import { useNavigate } from "react-router-dom";

import type {
  InvestigationHistory
} from "@/types/investigation";


interface Props {
  investigations: InvestigationHistory[];
}



export default function InvestigationTable({
  investigations
}: Props) {


  const navigate = useNavigate();



  function getRiskStyle(
    level: string
  ){

    if(level === "HIGH")
      return "text-red-400 bg-red-400/10";


    if(level === "MEDIUM")
      return "text-yellow-400 bg-yellow-400/10";


    return "text-green-400 bg-green-400/10";

  }



  return (

    <div className="
      rounded-xl
      border
      border-slate-800
      overflow-hidden
      bg-slate-950
    ">


      <table className="w-full">


        <thead className="bg-slate-900">


          <tr className="text-left text-slate-400 text-sm">


            <th className="p-4">
              Transaction ID
            </th>


            <th className="p-4">
              Risk Level
            </th>


            <th className="p-4">
              Score
            </th>


            <th className="p-4">
              Confidence
            </th>


            <th className="p-4">
              Date
            </th>


            <th className="p-4">
              Action
            </th>


          </tr>


        </thead>



        <tbody>


        {
          investigations.map((item)=>(


            <tr
              key={item.id}
              className="
              border-t
              border-slate-800
              text-slate-300
              "
            >


              <td className="p-4">
                {item.transaction_id}
              </td>



              <td className="p-4">

                <span
                className={`
                  px-3
                  py-1
                  rounded-full
                  text-xs
                  ${getRiskStyle(
                    item.risk_level
                  )}
                `}
                >

                  {item.risk_level}

                </span>

              </td>



              <td className="p-4">

                {item.score ?? "-"}

              </td>



              <td className="p-4">

                {
                  item.confidence
                  ?
                  `${item.confidence}%`
                  :
                  "-"
                }

              </td>



              <td className="p-4">

                {
                  new Date(
                    item.created_date
                  ).toLocaleDateString()
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
                py-1
                rounded-md
                bg-cyan-500/10
                text-cyan-400
                hover:bg-cyan-500/20
                text-sm
                "

                >

                View

                </button>


              </td>


            </tr>


          ))
        }


        </tbody>


      </table>


      {
        investigations.length===0 &&

        <div className="
        p-8
        text-center
        text-slate-500
        ">

          No investigations available

        </div>

      }


    </div>

  );

}