"use client";
import ChatBox from "@/src/components/chat/ChatBox";

export default function Home() {
  return (
    <div className="max-w-5xl mx-auto p-6 space-y-8">
      {/* Section En-tête */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-extrabold tracking-tight">
          Discuss with your documents
        </h2>
        <p className="text-gray-500">
          Upload a PDF and ask your questions to the AI.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Colonne de gauche : Upload (On ajoutera le composant après) */}
        <div className="md:col-span-1 space-y-4">
          <div className="bg-white p-6 rounded-xl border shadow-sm">
            <h3 className="font-semibold mb-4">Documents Base</h3>
            <div className="border-2 border-dashed border-gray-200 rounded-lg p-8 text-center hover:border-blue-400 transition cursor-pointer">
              <p className="text-sm text-gray-400">Upload a PDF</p>
            </div>
          </div>
        </div>

        {/* Colonne de droite : Chat */}
        <div className="md:col-span-2">
          <ChatBox />
        </div>
      </div>
    </div>
  );
}