export default function ClassificationResult({ data, onViewDashboard }) {
  const items = data?.items || [];

  const totalCost = items.reduce(
    (sum, item) => sum + (item.estimated_cbam_cost || 0),
    0,
  );
  const cbamCount = items.filter((i) => i.cbam_covered).length;

  const getStatusColor = (covered) =>
    covered ? "text-red-400" : "text-green-400";

  const getConfidenceColor = (score) => {
    if (score >= 0.8) return "text-green-400";
    if (score >= 0.5) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="space-y-6">
      {/* Summary Bar */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gray-800 rounded-xl p-4 text-center">
          <p className="text-3xl font-bold text-white">{items.length}</p>
          <p className="text-sm text-gray-400 mt-1">Total Imports</p>
        </div>
        <div className="bg-gray-800 rounded-xl p-4 text-center">
          <p className="text-3xl font-bold text-red-400">{cbamCount}</p>
          <p className="text-sm text-gray-400 mt-1">CBAM Covered</p>
        </div>
        <div className="bg-gray-800 rounded-xl p-4 text-center">
          <p className="text-3xl font-bold text-yellow-400">
            €{totalCost.toLocaleString("de-DE", { maximumFractionDigits: 0 })}
          </p>
          <p className="text-sm text-gray-400 mt-1">Est. CBAM Cost</p>
        </div>
      </div>

      {/* Results Table */}
      <div className="bg-gray-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-lg font-semibold">Classification Results</h2>
          <p className="text-sm text-gray-400">
            AI-classified imports with CBAM coverage and cost estimates
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-700 text-gray-300">
                <th className="text-left p-3">Product Description</th>
                <th className="text-left p-3">CN Code</th>
                <th className="text-left p-3">Category</th>
                <th className="text-left p-3">Country</th>
                <th className="text-left p-3">Volume (t)</th>
                <th className="text-left p-3">CBAM Covered</th>
                <th className="text-left p-3">Est. Cost (€)</th>
                <th className="text-left p-3">Confidence</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item, index) => (
                <tr
                  key={index}
                  className="border-t border-gray-700 hover:bg-gray-750 transition"
                >
                  <td className="p-3 text-white font-medium">
                    {item.product_description}
                  </td>
                  <td className="p-3 text-blue-400 font-mono">
                    {item.cn_code || "—"}
                  </td>
                  <td className="p-3 text-gray-300">{item.category || "—"}</td>
                  <td className="p-3 text-gray-300">
                    {item.country_of_origin}
                  </td>
                  <td className="p-3 text-gray-300">{item.volume_tonnes}</td>
                  <td
                    className={`p-3 font-semibold ${getStatusColor(item.cbam_covered)}`}
                  >
                    {item.cbam_covered ? "✓ Yes" : "✗ No"}
                  </td>
                  <td className="p-3 text-yellow-400">
                    {item.cbam_covered
                      ? `€${(item.estimated_cbam_cost || 0).toLocaleString("de-DE", { maximumFractionDigits: 0 })}`
                      : "—"}
                  </td>
                  <td
                    className={`p-3 font-semibold ${getConfidenceColor(item.confidence)}`}
                  >
                    {item.confidence
                      ? `${(item.confidence * 100).toFixed(0)}%`
                      : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* AI Notes */}
      {items.some((i) => i.ai_note) && (
        <div className="bg-gray-800 rounded-xl p-4 space-y-2">
          <h3 className="text-md font-semibold text-white mb-2">
            AI Classification Notes
          </h3>
          {items
            .filter((i) => i.ai_note)
            .map((item, index) => (
              <div key={index} className="text-sm text-gray-300">
                <span className="text-blue-400 font-medium">
                  {item.product_description}:
                </span>{" "}
                {item.ai_note}
              </div>
            ))}
        </div>
      )}

      {/* View Dashboard Button */}
      <button
        onClick={() => onViewDashboard(data)}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition"
      >
        View CBAM Dashboard →
      </button>
    </div>
  );
}
