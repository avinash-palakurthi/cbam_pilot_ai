import { useState } from "react";
const API_BASE = import.meta.env.VITE_API_URL;

export default function UploadForm({ onSuccess, onClassifying }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a CSV or Excel file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      onClassifying(); // move to step 2

      const response = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const err = await response.json();
        console.error("Error:", err);
        alert("Classification failed. Check console.");
        return;
      }

      const data = await response.json();
      onSuccess(data);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center">
      <div className="bg-gray-800 p-8 rounded-xl shadow-lg w-full max-w-xl space-y-6">
        <div>
          <h2 className="text-xl font-semibold text-white mb-1">
            Required Documents
          </h2>
          <p className="text-sm text-gray-400">
            Upload your imports CSV or Excel file to begin CBAM classification.
          </p>
        </div>

        {/* File Upload */}
        <div className="space-y-2">
          <label className="block text-white font-medium">
            Imports File <span className="text-red-400">*</span>
          </label>
          <p className="text-xs text-gray-400">
            Required columns: product_description, country_of_origin,
            volume_tonnes, supplier
          </p>

          <input
            type="file"
            accept=".csv,.xlsx,.xls"
            id="imports-file"
            onChange={(e) => setFile(e.target.files[0])}
            className="hidden"
          />

          <label
            htmlFor="imports-file"
            className="cursor-pointer inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition"
          >
            {file ? "Change File" : "Choose File"}
          </label>

          {file && (
            <p className="text-sm text-green-400">Selected: {file.name}</p>
          )}
        </div>

        {/* Sample CSV hint */}
        <div className="bg-gray-700 rounded-lg p-4 text-xs text-gray-300 space-y-1">
          <p className="font-semibold text-gray-200 mb-2">
            📄 Sample CSV format:
          </p>
          <p>product_description, country_of_origin, volume_tonnes, supplier</p>
          <p>Hot rolled steel coils, China, 50, Beijing Steel Co</p>
          <p>Portland cement, India, 120, Mumbai Cement Ltd</p>
          <p>Aluminium ingots, Russia, 30, Rusal</p>
        </div>

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={loading || !file}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white py-3 rounded-lg font-semibold transition"
        >
          {loading ? "Classifying..." : "Upload & Classify"}
        </button>
      </div>
    </div>
  );
}
