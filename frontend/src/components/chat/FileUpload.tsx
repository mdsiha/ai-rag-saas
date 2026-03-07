"use client";
import { useState } from "react";
import { uploadFile } from "@/src/lib/api";

export default function FileUpload() {
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
    const [message, setMessage] = useState<string>("");

    const handleUpload = async () => {
        if (!file) return;

        setStatus("uploading");
        try {
            const result: any = await uploadFile(file);
            if (result.status === "success") {
                setStatus("success");
                setMessage(`File uploaded successfully. Chunks indexed: ${result.chunks_indexed}`);
                setFile(null);
            } else {
                throw new Error(result.detail || "Unknown error");
            }
        } catch (err) {
            setStatus("error");
            setMessage("Error uploading file.");
            console.error(err);
        }
    };

    return (
    <div className="bg-white p-6 rounded-xl border shadow-sm space-y-4">
      <h3 className="font-semibold text-gray-700">Knowledge Base</h3>
      
      <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-lg p-6 hover:border-blue-400 transition bg-gray-50">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="hidden"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="cursor-pointer text-center">
          <span className="text-blue-600 font-medium">Choose a file</span>
          <p className="text-xs text-gray-400 mt-1">Only PDF (Max 10Mo)</p>
        </label>
        {file && <p className="mt-2 text-sm font-bold text-gray-600">{file.name}</p>}
      </div>

      <button
        onClick={handleUpload}
        disabled={!file || status === "uploading"}
        className={`w-full py-2 rounded-lg font-medium transition ${
          status === "uploading" ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700 text-white"
        }`}
      >
        {status === "uploading" ? "Uploading..." : "Upload"}
      </button>

      {message && (
        <p className={`text-xs text-center ${status === "success" ? "text-green-600" : "text-red-500"}`}>
          {message}
        </p>
      )}
    </div>
  );
}