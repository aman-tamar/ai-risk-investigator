interface Props {
  risk: "LOW" | "MEDIUM" | "HIGH" | null;
}


export default function RiskBadge({
  risk
}: Props) {


  if (!risk) {

    return (

      <span
        className="
        px-3
        py-1
        rounded-full
        text-xs
        bg-slate-800
        text-slate-400
        "
      >

        NOT ASSESSED

      </span>

    );

  }



  const styles = {

    HIGH:
      "bg-red-500/10 text-red-400 border-red-500/20",

    MEDIUM:
      "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",

    LOW:
      "bg-green-500/10 text-green-400 border-green-500/20"

  };



  return (

    <span
      className={`
      px-3
      py-1
      rounded-full
      text-xs
      border
      ${styles[risk]}
      `}
    >

      {risk}

    </span>

  );

}