"use client";
import ChatBox from "@/src/components/chat/ChatBox";
import FileUpload from "@/src/components/chat/FileUpload";

export default function Home() {
  return (
    <div className="max-w-5xl mx-auto p-6 space-y-8">
      <div className="text-center space-y-2">
        <h2 className="text-4xl font-black text-gray-900 tracking-tight">
          AI Knowledge Base
        </h2>
        <p className="text-gray-500 text-lg">
          Votre cerveau numérique personnel.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <FileUpload />
        </div>

        <div className="md:col-span-2">
          <ChatBox />
        </div>
      </div>
    </div>
  );
}