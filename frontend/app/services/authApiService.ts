export const AuthApiService = {
  async register(
    data: any,
    onMessage: (payload: {
      message: string;
      progress: number;
      done: boolean;
    }) => void,
  ): Promise<void> {
    const config = useRuntimeConfig();
    const baseUrl = config.public.apiBase;

    const response = await fetch(`${baseUrl}/registro/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      throw new ApiError("Error en el registro", errorData, response.status);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) return;

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);

      // SSE puede enviar varios mensajes en un solo "chunk"
      const lines = chunk.split("\n\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const jsonStr = line.replace("data: ", "");
          try {
            const payload = JSON.parse(jsonStr);
            onMessage(payload);
          } catch (e) {
            console.error("Error parseando SSE:", e);
          }
        }
      }
    }
  },
};
