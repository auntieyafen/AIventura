import React from "react";

type ChatMessageListProps = {
  messages: { role: "user" | "assistant"; content: string }[];
};

const ChatMessageList: React.FC<ChatMessageListProps> = ({ messages }) => {
  return (
    <div className="flex flex-col gap-4 p-6 overflow-y-auto max-h-[70vh]">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`max-w-[80%] px-4 py-2 text-sm rounded-md shadow-sm ${
            msg.role === "user"
              ? "self-end bg-emerald-100 text-gray-800"
              : "self-start bg-gray-200 text-gray-700"
          }`}
        >
          {msg.content}
        </div>
      ))}
    </div>
  );
};

export default ChatMessageList;