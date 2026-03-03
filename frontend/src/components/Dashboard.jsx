export default function Dashboard({ data, onBack }) {
  const items = data?.items || [];

  const totalImports = items.length;
  const cbamItems = items.filter((i) => i.cbam_covered);
  const totalCost = cbamItems.reduce(
    (sum, i) => sum + (i.estimated_cbam_cost || 0),
    0,
  );
  const readinessScore = Math.round(
    ((totalImports - cbamItems.length) / totalImports) * 100,
  );

  // Category breakdown
  const categoryMap = {};
  cbamItems.forEach((item) => {
    const cat = item.category || "Other";
    if (!categoryMap[cat]) categoryMap[cat] = { count: 0, cost: 0 };
    categoryMap[cat].count += 1;
    categoryMap[cat].cost += item.estimated_cbam_cost || 0;
  });

  const categories = Object.entries(categoryMap).sort(
    (a, b) => b[1].cost - a[1].cost,
  );

  const getReadinessColor = (score) => {
    if (score >= 70) return "text-green-400";
    if (score >= 40) return "text-yellow-400";
    return "text-red-400";
  };

  const getReadinessLabel = (score) => {
    if (score >= 70) return "Low Risk";
    if (score >= 40) return "Medium Risk";
    return "High Risk";
  };

  const categoryColors = [
    "bg-blue-500",
    "bg-yellow-500",
    "bg-red-500",
    "bg-green-500",
    "bg-purple-500",
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">CBAM Dashboard</h2>
          <p className="text-sm text-gray-400">
            Q{Math.ceil((new Date().getMonth() + 1) / 3)}{" "}
            {new Date().getFullYear()} — Compliance Overview
          </p>
        </div>
        <button
          onClick={onBack}
          className="text-sm text-gray-400 hover:text-white border border-gray-600 px-4 py-2 rounded-lg transition"
        >
          ← Back to Results
        </button>
      </div>

      {/* Top Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-800 rounded-xl p-5">
          <p className="text-sm text-gray-400 mb-1">CBAM Readiness</p>
          <p
            className={`text-4xl font-bold ${getReadinessColor(readinessScore)}`}
          >
            {readinessScore}%
          </p>
          <p
            className={`text-sm font-semibold mt-1 ${getReadinessColor(readinessScore)}`}
          >
            {getReadinessLabel(readinessScore)}
          </p>
        </div>

        <div className="bg-gray-800 rounded-xl p-5">
          <p className="text-sm text-gray-400 mb-1">Total Imports</p>
          <p className="text-4xl font-bold text-white">{totalImports}</p>
          <p className="text-sm text-gray-400 mt-1">products analyzed</p>
        </div>

        <div className="bg-gray-800 rounded-xl p-5">
          <p className="text-sm text-gray-400 mb-1">CBAM Covered</p>
          <p className="text-4xl font-bold text-red-400">{cbamItems.length}</p>
          <p className="text-sm text-gray-400 mt-1">
            {Math.round((cbamItems.length / totalImports) * 100)}% of imports
          </p>
        </div>

        <div className="bg-gray-800 rounded-xl p-5">
          <p className="text-sm text-gray-400 mb-1">Est. CBAM Cost</p>
          <p className="text-4xl font-bold text-yellow-400">
            €{(totalCost / 1000).toFixed(1)}k
          </p>
          <p className="text-sm text-gray-400 mt-1">this quarter</p>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Cost by Category */}
        <div className="bg-gray-800 rounded-xl p-5">
          <h3 className="text-md font-semibold mb-4">CBAM Cost by Category</h3>
          <div className="space-y-3">
            {categories.map(([cat, val], index) => (
              <div key={cat}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-300">{cat}</span>
                  <span className="text-yellow-400">
                    €
                    {val.cost.toLocaleString("de-DE", {
                      maximumFractionDigits: 0,
                    })}
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${categoryColors[index % categoryColors.length]}`}
                    style={{
                      width: `${Math.round((val.cost / totalCost) * 100)}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* CBAM Items List */}
        <div className="bg-gray-800 rounded-xl p-5">
          <h3 className="text-md font-semibold mb-4">
            Top CBAM Covered Imports
          </h3>
          <div className="space-y-2">
            {cbamItems
              .sort((a, b) => b.estimated_cbam_cost - a.estimated_cbam_cost)
              .slice(0, 5)
              .map((item, index) => (
                <div
                  key={index}
                  className="flex justify-between items-center text-sm py-2 border-b border-gray-700"
                >
                  <div>
                    <p className="text-white font-medium">
                      {item.product_description}
                    </p>
                    <p className="text-gray-400 text-xs">
                      {item.cn_code} · {item.country_of_origin}
                    </p>
                  </div>
                  <span className="text-yellow-400 font-semibold">
                    €
                    {(item.estimated_cbam_cost || 0).toLocaleString("de-DE", {
                      maximumFractionDigits: 0,
                    })}
                  </span>
                </div>
              ))}
          </div>
        </div>
      </div>

      {/* AI Compliance Summary */}
      {data?.compliance_summary && (
        <div className="bg-gray-800 rounded-xl p-5">
          <h3 className="text-md font-semibold mb-3">
            AI Compliance Assessment
          </h3>
          <p className="text-gray-300 text-sm whitespace-pre-line">
            {data.compliance_summary}
          </p>
        </div>
      )}

      {/* Export Button */}
      <button
        onClick={() => alert("Export feature coming soon!")}
        className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold transition"
      >
        Export CBAM Report (Q{Math.ceil((new Date().getMonth() + 1) / 3)}{" "}
        {new Date().getFullYear()})
      </button>
    </div>
  );
}
