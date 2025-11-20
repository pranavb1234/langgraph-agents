export default function ChatBubble({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div className={`w-full flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
      <div
        className={`px-4 py-2 max-w-[70%] rounded-lg text-white ${
          isUser ? "bg-blue-600" : "bg-gray-700"
        }`}
      >
        {text}
      </div>
    </div>
  );
}
