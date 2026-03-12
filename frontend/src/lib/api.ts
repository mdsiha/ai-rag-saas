const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const getAuthHeaders = (): Record<string, string> => {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const login = async (email: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Login failed.");

  return data;
};

export const register = async (email: string, password: string) => {
  const response = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Registration failed.");
  return data;
};

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: "POST",
      headers: { ...getAuthHeaders() },
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to index the file.");
    }

    return data;
  } catch (error: unknown) {
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
      headers: { "Content-Type": "application/json", ...getAuthHeaders() },
      body: JSON.stringify({ question }),
    });

    if (response.status === 401) {
      throw new Error("Session expired. Please log in again.");
    }

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
  } catch (error: unknown) {
    if (error instanceof Error) {
      onError(error.message);
    } else {
      onError("An error occurred.");
    }
  }
};
