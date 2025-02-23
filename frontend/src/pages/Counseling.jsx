import { useState, useEffect } from "react";
import HappinessChart from "../components/HappinessChart";
import elon from "../assets/elon.png";
import donald from "../assets/donald.png";
import ted from "../assets/ted.png";
import ChatMessage from "../components/ChatMessage";

const Counseling = () => {
  const [emotion, setEmotion] = useState("neutral");
  const [happinessScore, setHappinessScore] = useState(0); // 행복지수 추가
  const [transcription, setTranscription] = useState([]);
  const [newMessage, setNewMessage] = useState("");

  const avatars = [
    { name: "Ted", img: ted },
    { name: "Donald", img: donald },
    { name: "Elon", img: elon },
  ];

  // 🌟 데이터 소스 선택 상태 (웹캠 또는 로봇)
  const [dataSource, setDataSource] = useState("robot"); // 'webcam' 또는 'robot'

  // useEffect(() => {
  //   const interval = setInterval(runFinalFunction, 1000); // 로봇 데이터 주기적 GET 요청
  //   return () => clearInterval(interval);
  // }, [dataSource]);

  const runFinalFunction = async () => {
    try {
      const response = await fetch("http://localhost:8000/final/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          character: "ted the bear",
        }),
      });

      const data = await response.json();

      if (data.status === 200) {
        // Add user's transcribed text to chat
        const userMessage = {
          role: "user",
          content: data.transcribed_text,
        };

        // Add robot's response to chat
        const robotMessage = {
          role: "assistant",
          content: data.characterized_response,
        };

        // Update transcription with new messages
        setTranscription((prev) => [...prev, userMessage, robotMessage]);
      }
    } catch (error) {
      console.error("Error fetching final function:", error);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      const response = await fetch("http://localhost:8000/final", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          character: "ted the bear",
          text_input: newMessage.length > 0 ? newMessage : null,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setTranscription((prev) => [
          ...prev,
          { role: "user", content: newMessage },
          {
            role: "assistant",
            content: data.characterized_response,
          },
        ]);

        setNewMessage("");
      }
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="relative flex h-screen overflow-hidden">
      {/* Chat Section */}
      <div
        className={`flex-1 h-full bg-gray-100 shadow-md flex flex-col justify-between`}
      >
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {transcription.map((msg, index) => (
            <ChatMessage
              key={index}
              message={msg.content}
              isAI={msg.role === "assistant"}
            />
          ))}
        </div>

        {/* Chat Input - removed margin/padding bottom */}
        <div className="border-t bg-white shadow-up">
          <div className="flex space-x-2 p-3">
            {" "}
            {/* Reduced padding */}
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              onClick={handleSendMessage}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Send
            </button>
          </div>
        </div>
        <div className="h-16 bg-white"></div>
      </div>

      {/* Main Content */}
      <div className="flex-1 ml-0">
        {/* Main Counseling UI */}
        <div className="flex flex-col justify-center items-center bg-white p-8 min-h-screen">
          <h2 className="text-xl font-semibold mb-4">AI Counseling Session</h2>
        </div>

        <h3 className="text-lg font-semibold mb-4">
          EHR (Electronic Health Record)
        </h3>
      </div>

      <div className="flex-1 ml-0">
        <div className="mt-6 w-full flex justify-center">
          <HappinessChart dataSource={dataSource} />
        </div>

        <h3 className="text-lg font-semibold mb-4">
          RAG with Finetuned Embedding Model
        </h3>
      </div>
    </div>
  );
};

export default Counseling;
