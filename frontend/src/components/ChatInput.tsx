"use client";

import React, { useRef, useState, useEffect } from "react";
import { SendIcon } from "@/components/icons";
import { TextField, TextArea, Label } from "react-aria-components";
import BeatLoader from "react-spinners/BeatLoader";

type ChatInputProps = {
  onSend: (message: string) => Promise<void>;
  onPlanStart: () => Promise<void>; // Click to fetch trip plan
  isLoading?: boolean;
};

const ChatInput: React.FC<ChatInputProps> = ({ onSend, onPlanStart, isLoading }) => {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = textareaRef.current.scrollHeight + "px";
    }
  }, [message]);

  const handleSend = async () => {
    if (!message.trim()) return;

    await onSend(message);  
    await onPlanStart();    
    setMessage("");         
  };

  return (
    <div className="w-full border-t border-gray-200 p-4 bg-white">
      <div className="flex items-end gap-2">
        <TextField className="flex w-full">
          <Label className="sr-only">Message</Label>
          <TextArea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Enter your travel plan here..."
            className="w-full max-h-40 resize-none overflow-y-auto rounded-md border border-gray-300 p-3 text-sm text-amber-800 shadow-sm focus:border-emerald-500 focus:outline-none"
            rows={1}
          />
        </TextField>
        <button
          onClick={handleSend}
          disabled={isLoading || !message}
          className="rounded-md bg-primary-500 p-3 transition hover:bg-primary-600 disabled:opacity-50"
          aria-label="Submit message"
        >
          {isLoading ? (
            <div className="size-6 flex items-center justify-center">
              <BeatLoader color="#D1FAE5" />
            </div>
          ) : (
            <SendIcon className="size-6 -rotate-30 text-emerald-200 hover:text-emerald-600 transition" />
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
