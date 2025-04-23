"use client";
import React, { useEffect, useState } from "react";
import ChatInput from "@/components/ChatInput";
import ChatMessageList from "@/components/ChatMessageList";
import { getSessionId } from "@/utils/session";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function HomePage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSending, setIsSending] = useState(false);

  const handleSendMessage = async (message: string) => {
    setIsSending(true);

    const userMessage = { role: "user", content: message } as const;
    setMessages((prev) => [...prev, userMessage]);

    const session_id = getSessionId();

    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id,
        ...userMessage,
      }),
    });

    // TODO: really fetch the response from the server
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `你輸入的是：「${message}」，我正在幫你查找資料中...`,
        },
      ]);
      setIsSending(false);
    }, 1500);
  };

  useEffect(() => {
    const loadMessages = async () => {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/messages?session_id=${getSessionId()}`
      );
      const data = await res.json();
      setMessages(data);
    };
    loadMessages();
  }, []);

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <div className="flex-1 overflow-auto">
        <ChatMessageList messages={messages} />
      </div>
      <ChatInput onSend={handleSendMessage} isLoading={isSending} />
    </div>
  );
}
