"use client";

import React, { useEffect, useState } from "react";
import ChatInput from "@/components/ChatInput";
import ChatMessageList from "@/components/ChatMessageList";
import PlaceSearchMap from "@/components/PlaceSearchMap";
import { getSessionId } from "@/utils/session";
import { fetchMessages, postMessage, fetchTripPlan } from "@/libs/api";
import { useLoadScript } from "@react-google-maps/api";
import { ChatMessage, TripPlan } from "@/types";

const libraries: ("places" | "drawing" | "geometry" | "visualization")[] = ["places"];

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function HomePage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSending, setIsSending] = useState(false);
  const [tripPlan, setTripPlan] = useState<TripPlan | null>(null);

  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_KEY!,
    libraries,
  });

  const handleSendMessage = async (message: string) => {
    setIsSending(true);
    const session_id = getSessionId();
    const userMessage: Message = { role: "user", content: message };
    
    try {
      const res = await postMessage(session_id, userMessage.content);
      if (res.status === 'ok' && res.trip) {
        setTripPlan(res.trip);
      } else {
        console.error("API response error:", res);
      }
    } catch (error) {
      console.error("Error posting message:", error);
    } finally {
      setIsSending(false);
    }
  };

  // Load messages when the component mounts
  useEffect(() => {
    const load = async () => {
      const data = await fetchMessages(getSessionId());
      setMessages(data);
    };
    load();
  }, []);

  const handlePlanStart = async () => {
    try {
      const plan = await fetchTripPlan();
      setTripPlan(plan);
    } catch (error) {
      console.error("Failed to fetch trip plan:", error);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-auto">
        <ChatMessageList messages={messages} />
        {isLoaded ? (
          <PlaceSearchMap tripPlan={tripPlan} />
        ) : (
          <div className="text-center py-4">Loading map...</div>
        )}
      </div>
      <ChatInput onSend={handleSendMessage} onPlanStart={handlePlanStart} isLoading={isSending} />
    </div>
  );
}
