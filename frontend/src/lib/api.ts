const API_URL = "http://localhost:8000";

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  });
  return response;
};

export const chatStream = async (
  question: string,
  onChunk: (chunk: string) => void
) => {
  const response = await fetch(`${API_URL}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

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
        onChunk(line.replace("data: ", ""));
      }
    });
  }
};
