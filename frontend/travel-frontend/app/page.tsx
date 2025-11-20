"use client";

import { useState } from "react";
import axios from "axios";
import ChatBubble from "../components/ChatB";

export default function Home() {
  const [messages, setMessages] = useState([
    { sender: "assistant", text: "Hello! How can I help with your travel plan?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const backendURL = "http://127.0.0.1:8000/chat"; // Your FastAPI backend

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post(backendURL, {
        session_id: "demo_user_1",
        message: input
      });

      const { reply } = response.data;

      setMessages((prev) => [
        ...prev,
        { sender: "assistant", text: reply }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "assistant", text: "⚠️ Error connecting to backend" }
      ]);
    }

    setLoading(false);
  };

  const handleKeyPress = (e : any) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="w-full min-h-screen bg-gray-900 text-white flex flex-col items-center py-10 px-4">
      <div className="w-full max-w-2xl bg-gray-800 rounded-xl p-4 shadow-xl border border-gray-700">
        <h1 className="text-xl font-bold text-center mb-4">✈️ Travel Planning Assistant</h1>

        <div className="h-[60vh] overflow-y-auto p-3 bg-gray-700 rounded-lg">
          {messages.map((msg, idx) => (
            <ChatBubble key={idx} sender={msg.sender} text={msg.text} />
          ))}

          {loading && (
            <div className="text-gray-300 italic text-sm mt-2">
              Searching… (agents working)
            </div>
          )}
        </div>

        <div className="flex mt-4">
          <input
            className="flex-1 px-4 py-2 bg-gray-600 rounded-lg outline-none"
            placeholder="Ask something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
          />

          <button
            onClick={sendMessage}
            className="ml-2 px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
