export type ChatMessage = {
    role: "user" | "assistant";
    content: string;
};

export type TripPlan = {
    date: string;
    activities: string[];
};
