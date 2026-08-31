import { Info } from "lucide-react";

const InfoSection = ({ dispersion, receivedPower, bitErrors }) => {
  const measurements = [
    {
      title: "Dispersion",
      value: `${Number(dispersion).toFixed(2)} ps`,
      description: "Pulse spreading inside the optical fiber",
    },
    {
      title: "Received Power",
      value: `${Number(receivedPower).toExponential(3)} W`,
      description: "Optical power reaching the receiver",
    },
    {
      title: "Bit Errors",
      value: bitErrors,
      description: "Number of incorrectly detected bits",
    },
  ];

  return (
    <section className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 bg-blue-50 rounded-xl">
          <Info className="w-5 h-5 text-blue-600" />
        </div>

        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Additional Measurements
          </h2>

          <p className="text-sm text-slate-500">
            Other parameters monitored by the simulation
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {measurements.map((item) => (
          <div
            key={item.title}
            className="bg-slate-50 border border-slate-100 rounded-xl p-5"
          >
            <p className="text-sm text-slate-500">{item.title}</p>

            <p className="text-xl font-bold text-slate-900 mt-2">
              {item.value}
            </p>

            <p className="text-xs text-slate-400 mt-2">{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default InfoSection;
