"use client";
import React, { useState } from "react";
import { SendIcon } from "@/components/icons";
import {
  TextField,
  TextArea,
  Label,
} from "react-aria-components";

type ChatInputProps = {
  onSend: (message: string) => void;
};

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (message.trim() !== "") {
      onSend(message.trim());
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full border-t border-gray-200 p-4 bg-white">
      <div className="flex items-center gap-2">
        <TextField className="flex w-full">
          <Label className="sr-only">訊息</Label>
          <TextArea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="輸入你的旅遊計畫..."
            className="w-full resize-none rounded-md border border-gray-300 p-3 text-sm shadow-sm focus:border-emerald-500 focus:outline-none"
            rows={1}
          />
        </TextField>
        <button
          onClick={handleSend}
          disabled={message.trim() === ""}
          className="rounded-md bg-primary-500 p-3"
          aria-label="送出訊息"
        >
          <SendIcon className="size-6 -rotate-30 text-emerald-200 hover:text-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transition hover:cursor-pointer" />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
