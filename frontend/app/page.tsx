"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatBox from "@/src/components/chat/ChatBox";
import FileUpload from "@/src/components/chat/FileUpload";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

export default function Home() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
      } else {
        setIsAuthenticated(true);
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
        <aside className="lg:col-span-1">
          <FileUpload />
          <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100">
            <h4 className="text-sm font-bold text-blue-800 mb-1">System Status</h4>
            <div className="flex items-center gap-2 text-xs text-blue-600">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              Cloud LLM Connected
            </div>
          </div>
        </aside>

        <main className="lg:col-span-3">
          <ChatBox />
        </main>
      </div>
    </div>
  );
}