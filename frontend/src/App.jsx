import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ClassificationResult from "./components/ClassificationResult";
import Dashboard from "./components/Dashboard";

const steps = ["Upload", "Classifying", "Results", "Dashboard"];

function App() {
  const [step, setStep] = useState(1);
  const [classificationData, setClassificationData] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);

  const handleUploadSuccess = (data) => {
    setClassificationData(data);
    setStep(3);
  };

  const handleViewDashboard = (data) => {
    setDashboardData(data);
    setStep(4);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      {/* Header */}
      <h1 className="text-3xl font-bold mb-8 tracking-wide">CBAM PILOT AI</h1>

      {/* Progress Steps */}
      <div className="flex justify-between mb-10">
        {steps.map((label, index) => {
          const stepNumber = index + 1;
          return (
            <div key={label} className="flex flex-col items-center flex-1">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all
                  ${
                    stepNumber < step
                      ? "bg-green-500 text-black"
                      : stepNumber === step
                        ? "bg-blue-500 text-white"
                        : "bg-gray-600 text-gray-400"
                  }`}
              >
                {stepNumber}
              </div>
              <p className="text-xs mt-2 text-center text-gray-400">{label}</p>
            </div>
          );
        })}
      </div>

      {/* Step 1 — Upload */}
      {step === 1 && (
        <UploadForm
          onSuccess={handleUploadSuccess}
          onClassifying={() => setStep(2)}
        />
      )}

      {/* Step 2 — Classifying (loading) */}
      {step === 2 && (
        <div className="flex flex-col items-center justify-center py-24 space-y-6">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-xl text-gray-300 font-semibold">
            AI is classifying your imports...
          </p>
          <p className="text-sm text-gray-500">
            Checking CN codes, CBAM coverage, and estimating costs
          </p>
        </div>
      )}

      {/* Step 3 — Results */}
      {step === 3 && classificationData && (
        <ClassificationResult
          data={classificationData}
          onViewDashboard={handleViewDashboard}
        />
      )}

      {/* Step 4 — Dashboard */}
      {step === 4 && dashboardData && (
        <Dashboard data={dashboardData} onBack={() => setStep(3)} />
      )}
    </div>
  );
}

export default App;
