import { TripPlan } from "@/types";

function convertTripFromBackend(raw: unknown): TripPlan {
  const data = raw as {
    daily_itinerary: {
      [day: string]: {
        date: string;
        activities: { time: string; description: string; location: string }[];
      };
    };
  };

  const days = Object.entries(data.daily_itinerary).map(([_, value]) => ({
    date: value.date,
    places: value.activities.map((act) => ({
      time: act.time,
      name: act.description,
      transport: "walk",
      lat: 0,
      lng: 0,
    })),
  }));

  return { days };
}


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

  const data = await res.json();

  if (data.trip) {
    return {
      status: "ok",
      trip: convertTripFromBackend(data.trip),
    };
  }

  return { status: "ok" };
}


export async function fetchMessages(session_id: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/messages/${session_id}`
  );

  if (!res.ok) {
    console.error("fetchMessages failed:", res.status, res.statusText);
    throw new Error("Failed to fetch messages");
  }

  console.log("🔍 session_id in fetchMessages:", session_id);

  return await res.json();
}


export async function fetchTripPlan(): Promise<TripPlan> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/plan`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch trip plan");
  }

  console.log(res);

  const data = await res.json();
  return convertTripFromBackend(data) as TripPlan;
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
