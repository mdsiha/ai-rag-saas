const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to index the file.");
    }

    return data;
  } catch (error: any) {
    console.error("Upload API Error:", error);
    throw error;
  }
};

export const chatStream = async (
  question: string,
  onChunk: (chunk: string) => void,
  onError: (error: string) => void
) => {
  try {
    const response = await fetch(`${API_URL}/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || "Chat connection failed.");
    }

    if (!response.body) return;

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      lines.forEach((line) => {
        if (line.startsWith("data: ")) {
          const content = line.substring(6);

          if (content === "[SERVER_ERROR]") {
            onError("The server encountered an issue during generation.");
          } else {
            onChunk(content);
          }
        }
      });
    }
  } catch (error: any) {
    onError(error.message);
  }
};
