export async function postMessage(session_id: string, content: string) {
  return await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id, role: "user", content }),
  });
}

export async function fetchMessages(session_id: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/messages?session_id=${session_id}`
  );
  return await res.json();
}
