import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";

import {
  runInvestigation
} from "@/api/investigations";

import type {
  InvestigationResult
} from "@/types/investigation";


import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";


import PageTransition from "@/components/layout/PageTransition";
import RiskBadge from "@/components/ui/RiskBadge";



export default function InvestigationDetail(){


  const {
    transaction_id
  } = useParams();



  const [
    investigation,
    setInvestigation
  ] = useState<InvestigationResult | null>(null);



  const [
    loading,
    setLoading
  ] = useState(true);




  useEffect(()=>{


    async function load(){


      if(!transaction_id)
        return;



      try{


        const data =
        await runInvestigation(
          transaction_id
        );


        setInvestigation(data);


      }
      catch(error){


        console.error(
          "Investigation failed",
          error
        );


      }
      finally{


        setLoading(false);


      }


    }


    load();


  },[transaction_id]);






  if(loading){

    return (

      <div className="text-slate-400">

        Running AI Investigation...

      </div>

    );

  }





  if(!investigation){

    return (

      <div className="text-red-400">

        Investigation unavailable

      </div>

    );

  }





  return (

    <PageTransition>


    <div className="space-y-6">





      {/* Header */}


      <Card className="
      bg-slate-950
      border-slate-800
      ">


        <CardHeader>

          <CardTitle className="text-white">

            Transaction Investigation

          </CardTitle>

        </CardHeader>




        <CardContent>


        <div className="
        grid
        grid-cols-3
        gap-6
        ">


          <Info
          label="Transaction ID"
          value={
            investigation.transaction_id
          }
          />


          <div>

          <p className="text-slate-400 text-sm">
          Risk Level
          </p>


          <div className="mt-2">

          <RiskBadge
          risk={
            investigation
            .risk_assessment
            .risk_level
          }
          />

          </div>

          </div>




          <Info

          label="Final Risk Score"

          value={
            investigation
            .risk_assessment
            .final_risk_score
          }

          />


        </div>


        </CardContent>


      </Card>







      {/* Risk Scores */}


      <Card className="
      bg-slate-950
      border-slate-800
      ">


      <CardHeader>

      <CardTitle className="text-white">

      Risk Assessment

      </CardTitle>

      </CardHeader>




      <CardContent>


      <div className="
      grid
      grid-cols-3
      gap-5
      ">


      <ScoreCard

      title="ML Score"

      value={
        investigation
        .risk_assessment
        .ml_score
      }

      />



      <ScoreCard

      title="Rule Score"

      value={
        investigation
        .risk_assessment
        .rule_score
      }

      />



      <ScoreCard

      title="Final Score"

      value={
        investigation
        .risk_assessment
        .final_risk_score
      }

      />


      </div>


      </CardContent>


      </Card>







      {/* Signals */}


      <ListSection

      title="Risk Signals"

      items={
        investigation.risk_signals
      }

      danger

      />







      {/* AI Report */}


      <Card className="
      bg-slate-950
      border-slate-800
      ">


      <CardHeader>

      <CardTitle className="text-white">

      AI Investigation Report

      </CardTitle>

      </CardHeader>




      <CardContent>


      <div className="space-y-6">



      <div>


      <h3 className="text-slate-400">

      Conclusion

      </h3>



      <p className="
      text-white
      mt-2
      leading-relaxed
      ">

      {
        investigation
        .investigation
        .conclusion
      }

      </p>


      </div>







      <div>


      <h3 className="text-slate-400">

      Confidence

      </h3>



      <div className="
      mt-3
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
        `${investigation
        .investigation
        .confidence}%`

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
      text-sm
      text-slate-400
      mt-2
      ">

      Confidence:
      {
        investigation
        .investigation
        .confidence
      }%

      </p>


      </div>


      </div>


      </CardContent>


      </Card>







      <ListSection

      title="Key Findings"

      items={
        investigation
        .investigation
        .key_findings
      }

      />







      <ListSection

      title="Evidence Assessment"

      items={
        investigation
        .investigation
        .evidence_assessment
      }

      />







      <ListSection

      title="Contradictory Evidence"

      items={
        investigation
        .investigation
        .contradictory_evidence
      }

      />







      <ListSection

      title="Recommended Actions"

      items={
        investigation
        .investigation
        .recommended_actions
      }

      />


    </div>


    </PageTransition>


  );

}









function Info(
{
label,
value
}
:
{
label:string;
value:any;
}

){

return (

<div>


<p className="text-slate-400 text-sm">

{label}

</p>


<p className="
text-white
mt-1
">

{value ?? "-"}

</p>


</div>

);

}










function ScoreCard(
{
title,
value
}
:
{
title:string;
value:number;
}

){


return (

<motion.div

initial={{
opacity:0,
y:10
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
bg-slate-900
border-slate-800
">


<CardContent className="p-5">


<p className="text-slate-400">

{title}

</p>



<p className="
text-3xl
font-bold
text-cyan-400
mt-2
">

{value ?? "-"}

</p>


</CardContent>


</Card>


</motion.div>

);

}









function ListSection(
{
title,
items,
danger
}
:
{
title:string;
items:string[];
danger?:boolean;
}

){


return (

<Card className="
bg-slate-950
border-slate-800
">


<CardHeader>

<CardTitle className="text-white">

{title}

</CardTitle>

</CardHeader>




<CardContent>


<div className="space-y-3">


{
items?.map(

(item,index)=>(


<motion.div

key={index}

initial={{
opacity:0,
x:-10
}}

animate={{
opacity:1,
x:0
}}

transition={{
duration:0.2
}}

className={`
p-4
rounded-lg
border
text-slate-300

${
danger
?
"bg-red-500/10 border-red-500/20"
:
"bg-slate-900 border-slate-800"
}

`}

>


{danger && "⚠ "}

{item}


</motion.div>


)

)

}



</div>


</CardContent>


</Card>


);

}