"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatBox from "@/src/components/chat/ChatBox";
import FileUpload from "@/src/components/chat/FileUpload";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { LogOut, FileText, Database } from "lucide-react";
import { getStats } from "@/src/lib/api";

export default function Home() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  const [files, setFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
      } else {
        setIsAuthenticated(true);
        try {
          const stats = await getStats();
          setFiles(stats.files);
        } catch (error) {
          console.error("Error fetching stats:", error);
        }
      }
    };
    
    checkAuth();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  if (isAuthenticated !== true) return null;

  return (
    <div className="max-w-6xl mx-auto min-h-screen p-4 md:p-8 space-y-8">
      <header className="flex justify-between items-end">
        <div className="space-y-2">
          <h2 className="text-3xl font-extrabold text-slate-900 sm:text-4xl">
            Knowledge Base <span className="text-blue-600">IA</span>
          </h2>
          <p className="text-slate-500 text-lg max-w-2xl">
            Use your local data safely. Ask questions to your documents with the RAG.
          </p>
        </div>
        <Button variant="outline" onClick={handleLogout} className="text-slate-500 hover:text-red-600">
          <LogOut className="w-4 h-4 mr-2" />
          Déconnexion
        </Button>
      </header>
      
      <Separator className="bg-slate-200" />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <aside className="lg:col-span-1 space-y-6">
          <FileUpload />
          
          <div className="bg-white rounded-lg border shadow-sm overflow-hidden">
            <div className="p-3 bg-slate-50 border-b font-bold text-sm flex items-center gap-2">
              <Database className="w-4 h-4 text-blue-600" />
              Ma Bibliothèque
            </div>
            <div className="p-2 space-y-1">
              <button
                onClick={() => setSelectedFile(null)}
                className={`w-full text-left px-3 py-2 rounded-md text-sm transition ${
                  !selectedFile ? "bg-blue-600 text-white" : "hover:bg-slate-100 text-slate-600"
                }`}
              >
                Tous les documents
              </button>
              {files.map((file) => (
                <button
                  key={file}
                  onClick={() => setSelectedFile(file)}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm truncate transition ${
                    selectedFile === file ? "bg-blue-600 text-white" : "hover:bg-slate-100 text-slate-600"
                  }`}
                  title={file.split("/").pop()}
                >
                  <FileText className="inline w-3 h-3 mr-2 opacity-70" />
                  {file.split("/").pop()}
                </button>
              ))}
            </div>
          </div>
        </aside>

        <main className="lg:col-span-3">
          <ChatBox selectedFile={selectedFile}/>
        </main>
      </div>
    </div>
  );
}