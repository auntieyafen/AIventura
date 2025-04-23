"use client";
import React, { useState } from "react";
import ChatInput from "@/components/ChatInput";
import ChatMessageList from "@/components/ChatMessageList";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function HomePage() {
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSendMessage = async (message: string) => {
    // 加入使用者訊息
    setMessages((prev) => [...prev, { role: "user", content: message }]);

    // 模擬 AI 回覆（2 秒後出現）
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `你輸入的是：「${message}」，我正在幫你查找資料中...` },
      ]);
    }, 2000);

    console.log("使用者輸入：", message); // ✅ 檢查是否有內容
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <div className="flex-1 overflow-auto">
        <ChatMessageList messages={messages} />
      </div>
      <ChatInput onSend={handleSendMessage} />
    </div>
  );
}