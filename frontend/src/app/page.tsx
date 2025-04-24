"use client";

import React, { useEffect, useState } from "react";
import ChatInput from "@/components/ChatInput";
import ChatMessageList from "@/components/ChatMessageList";
import PlaceSearchMap from "@/components/PlaceSearchMap";
import { getSessionId } from "@/utils/session";
import { fetchMessages, postMessage } from "@/libs/api";
import { useLoadScript } from "@react-google-maps/api";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function HomePage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSending, setIsSending] = useState(false);

  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_KEY!,
    libraries: ["places"], // <- 確保這有加！
  });

  const handleSendMessage = async (message: string) => {
    setIsSending(true);
    const session_id = getSessionId();
    const userMessage: Message = { role: "user", content: message };
    
    setMessages((prev) => [...prev, userMessage]);
    await postMessage(session_id, message);

    // 模擬 AI 回覆
    setTimeout(() => {
      const reply = `你輸入的是：「${message}」，我正在幫你查找資料中...`;
      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);
      setIsSending(false);
    }, 1500);
  };

  useEffect(() => {
    const load = async () => {
      const data = await fetchMessages(getSessionId());
      setMessages(data);
    };
    load();
  }, []);

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-auto">
        <ChatMessageList messages={messages} />
        {isLoaded ? <PlaceSearchMap /> : <div>Loading map...</div>}
      </div>
      <ChatInput onSend={handleSendMessage} isLoading={isSending} />
    </div>
  );
}
