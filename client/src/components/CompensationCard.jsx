import { ArrowDown, TrendingUp } from "lucide-react";

const CompensationCard = ({ berBefore, berAfter, improvement }) => {
  // Convert BER values to numbers
  const before = Number(berBefore) || 0;
  const after = Number(berAfter) || 0;

  // Scale the bars so small BER values are still visible
  const beforeHeight = Math.min(before * 1000, 100);
  const afterHeight = Math.min(after * 1000, 100);

  return (
    <section className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">

      {/* ================================== */}
      {/* HEADER */}
      {/* ================================== */}

      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Crosstalk Compensation
          </h2>

          <p className="text-sm text-slate-500 mt-1">
            Comparing signal quality before and after compensation
          </p>
        </div>

        <div className="p-2.5 bg-emerald-50 rounded-xl">
          <TrendingUp className="w-6 h-6 text-emerald-600" />
        </div>
      </div>

      

      {/* ================================== */}
      {/* BER VALUES */}
      {/* ================================== */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

        {/* BEFORE */}

        <div className="bg-red-50 border border-red-100 rounded-xl p-5">

          <p className="text-sm text-red-700 font-medium">
            BER Before Compensation
          </p>

          <p className="text-3xl font-bold text-slate-900 mt-2">
            {before.toFixed(4)}
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Signal contains crosstalk interference
          </p>

        </div>

        {/* AFTER */}

        <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-5">

          <p className="text-sm text-emerald-700 font-medium">
            BER After Compensation
          </p>

          <p className="text-3xl font-bold text-slate-900 mt-2">
            {after.toFixed(4)}
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Interference reduced from the received signal
          </p>

        </div>

      </div>

      {/* ================================== */}
      {/* BER GRAPH */}
      {/* ================================== */}

      <div className="mt-6 border border-slate-200 rounded-xl p-5">

        {/* Graph heading */}

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-5">

          <div>
            <h3 className="font-semibold text-slate-900">
              BER Comparison
            </h3>

            <p className="text-xs text-slate-500 mt-1">
              Visual comparison of bit error rate
            </p>
          </div>

          <div className="text-xs text-slate-400">
            Lower is better
          </div>

        </div>

        {/* Graph */}

        <div className="flex items-end justify-center gap-16 h-52 border-b border-slate-200 px-8">

          {/* BEFORE BAR */}

          <div className="flex flex-col items-center justify-end h-full">

            <p className="text-xs font-semibold text-red-600 mb-2">
              {before.toFixed(4)}
            </p>

            <div
              className="w-16 bg-red-400 rounded-t-lg transition-all duration-700"
              style={{
                height: `${Math.max(beforeHeight, before > 0 ? 10 : 0)}%`,
              }}
            />

          </div>

          {/* AFTER BAR */}

          <div className="flex flex-col items-center justify-end h-full">

            <p className="text-xs font-semibold text-emerald-600 mb-2">
              {after.toFixed(4)}
            </p>

            <div
              className="w-16 bg-emerald-400 rounded-t-lg transition-all duration-700"
              style={{
                height: `${Math.max(afterHeight, after > 0 ? 10 : 0)}%`,
              }}
            />

          </div>

        </div>

        {/* Graph labels */}

        <div className="flex justify-center gap-14 mt-3 my-6">

          <div className="flex items-center gap-2">

            <div className="w-3 h-3 rounded-sm bg-red-400" />

            <span className="text-xs text-slate-500">
              Before Compensation
            </span>

          </div>

          <div className="flex items-center gap-2">

            <div className="w-3 h-3 rounded-sm bg-emerald-400" />

            <span className="text-xs text-slate-500">
              After Compensation
            </span>

          </div>

        </div>

      {/* ================================== */}
      {/* IMPROVEMENT */}
      {/* ================================== */}

      <div className="bg-slate-900 rounded-xl p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">

        <div>
          <p className="text-sm text-slate-400">
            BER Improvement
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Lower BER means fewer transmission errors
          </p>
        </div>

        <p className="text-3xl font-bold text-emerald-400">
          {Number(improvement).toFixed(2)}%
        </p>

      </div>

      

        {/* Explanation */}

        <div className="mt-5 bg-slate-50 border border-slate-100 rounded-lg p-4">

          <p className="text-xs text-slate-600 leading-5">

            <span className="font-semibold text-slate-900">
              How to read this graph:
            </span>{" "}

            The red bar represents the Bit Error Rate before crosstalk
            compensation. The green bar represents the BER after the
            interference has been reduced. A shorter green bar means
            fewer errors and therefore better signal quality.

          </p>

        </div>

      </div>

    </section>
  );
};

export default CompensationCard;