"use client";
import { useState } from "react";
import { uploadFile } from "@/src/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { UploadCloud, FileText, Loader2, CheckCircle2, AlertCircle } from "lucide-react";

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    try {
      const result: any = await uploadFile(file);
      if (result.status === "success") {
        setStatus("success");
        setMessage(`${result.chunks_indexed} extraits indexés.`);
        setFile(null);
      }
    } catch (err) {
      setStatus("error");
      setMessage("Erreur d'upload.");
    }
  };

  return (
    <Card className="shadow-md">
      <CardHeader>
        <CardTitle className="text-md flex items-center gap-2">
          <FileText className="w-5 h-5 text-blue-600" />
          Documents
        </CardTitle>
        <CardDescription>Upload your PDF for the RAG</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="group relative border-2 border-dashed border-slate-200 rounded-xl p-8 flex flex-col items-center justify-center transition-colors hover:border-blue-400 hover:bg-blue-50/50">
          <input
            type="file"
            accept=".pdf"
            className="absolute inset-0 opacity-0 cursor-pointer"
            onChange={(e) => {
                setFile(e.target.files?.[0] || null);
                setStatus("idle");
            }}
          />
          <UploadCloud className="w-10 h-10 text-slate-400 mb-2 group-hover:text-blue-500 transition-colors" />
          <p className="text-xs font-medium text-slate-600 text-center">
            {file ? <span className="text-blue-600">{file.name}</span> : "Drag your PDF or click here"}
          </p>
        </div>

        <Button 
          onClick={handleUpload} 
          disabled={!file || status === "uploading"} 
          className="w-full bg-slate-900 hover:bg-slate-800"
        >
          {status === "uploading" ? (
            <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Indexation...</>
          ) : "Analyze the document "}
        </Button>

        {status !== "idle" && (
          <Badge variant={status === "success" ? "secondary" : "destructive"} className="w-full py-1 justify-center gap-2">
            {status === "success" ? <CheckCircle2 className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
            {message}
          </Badge>
        )}
      </CardContent>
    </Card>
  );
}