import { TripPlan } from "@/types";

export async function postMessage(session_id: string, content: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id, role: "user", content }),
  });

  if (!res.ok) {
    console.error("postMessage failed:", res.status, res.statusText);
    throw new Error("Failed to post message");
  } 

  return await res.json();
}

export async function fetchMessages(session_id: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/messages/${session_id}`
  );

  if (!res.ok) {
    console.error("fetchMessages failed:", res.status, res.statusText);
    throw new Error("Failed to fetch messages");
  }

  return await res.json();
}


export async function fetchTripPlan(): Promise<TripPlan> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/plan`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch trip plan");
  }

  const data = await res.json();
  return data as TripPlan;
}

// export async function fetchTripPlan(userInput: string, startDate: string) {
//   const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/plan`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       user_input: userInput,
//       start_date: startDate,
//     }),
//   });
//   if (!res.ok) throw new Error("Failed to fetch trip plan");
//   return res.json();
// }
