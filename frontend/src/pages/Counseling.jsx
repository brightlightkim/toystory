import { useState, useEffect } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Maximize,
  Minimize,
  ChevronDown,
} from "lucide-react";
import VideoCapture from "../components/VideoCapture";
import HappinessChart from "../components/HappinessChart";
import elon from "../assets/elon.png";
import donald from "../assets/donald.png";
import ted from "../assets/ted.png";
import ChatMessage from '../components/ChatMessage';

const Counseling = () => {
  const [emotion, setEmotion] = useState("neutral");
  const [happinessScore, setHappinessScore] = useState(0); // 행복지수 추가
  const [counselingResponse, setCounselingResponse] = useState(
    "Hello! How can I assist you today?"
  );
  const [transcription, setTranscription] = useState([]);
  const [isLeftPanelOpen, setIsLeftPanelOpen] = useState(false);
  const [isRightPanelOpen, setIsRightPanelOpen] = useState(false);
  const [isMyVideoLarge, setIsMyVideoLarge] = useState(false);
  const [selectedAvatar, setSelectedAvatar] = useState(ted); // 기본 아바타 설정
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [newMessage, setNewMessage] = useState('');

  const avatars = [
    { name: "Ted", img: ted },
    { name: "Donald", img: donald },
    { name: "Elon", img: elon },
  ];

  // 🌟 데이터 소스 선택 상태 (웹캠 또는 로봇)
  const [dataSource, setDataSource] = useState("robot"); // 'webcam' 또는 'robot'

  // useEffect(() => {
  //   if (dataSource === "robot") {
  //     const interval = setInterval(fetchRobotEmotion, 10000); // 로봇 데이터 주기적 GET 요청
  //     return () => clearInterval(interval);
  //   }
  // }, [dataSource]);

  const fetchRobotEmotion = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/emotion/analyze_robot/"
      );
      const data = await response.json();
      // console.log(data);
      setEmotion(data.emotion.dominant_emotion);
      setHappinessScore(data.happiness_score);
    } catch (error) {
      console.error("Error fetching robot emotion:", error);
    }
  };

  const fetchChatHistory = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/chat/history/736d02e0-376a-425a-b76d-78967be66ba0"
      );
      const data = await response.json();
      console.log("Full Response:", data); // 전체 데이터 확인용

      // content만 추출 후 JSON 파싱
      const parsedMessages = data.map((item) => {
        const parsedContent = JSON.parse(item.content); // 문자열 파싱
        return {
          role: parsedContent.role, // 'assistant' 또는 'user'
          content: parsedContent.content, // 메시지 내용
        };
      });

      console.log("Parsed Messages:", parsedMessages);

      // 상태 업데이트 (Transcription)
      if (parsedMessages.length) {
        setTranscription(parsedMessages); // 여기서 parsedMessages로 업데이트
      }
    } catch (error) {
      console.error("Error fetching chat history:", error);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim()) return;
    
    try {
      const response = await fetch('http://localhost:8000/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sessionid: '736d02e0-376a-425a-b76d-78967be66ba0',
          message: newMessage,
        }),
      });
      
      if (response.ok) {
        setNewMessage('');
        fetchChatHistory();
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="relative flex h-screen overflow-hidden">
      {/* Left Sliding Panel (Chat) */}
      <div
        className={`fixed z-[100] left-0 top-0 h-full bg-gray-100 shadow-md transition-transform transform ${
          isLeftPanelOpen ? "translate-x-0" : "-translate-x-full"
        } w-1/4 flex flex-col`}
      >
        {/* Panel Toggle Button */}
        <button
          onClick={() => setIsLeftPanelOpen(!isLeftPanelOpen)}
          className="absolute right-[-20px] top-1/2 transform -translate-y-1/2 bg-indigo-600 text-white p-2 rounded-full shadow-md z-[101]"
        >
          {isLeftPanelOpen ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
        </button> 

        <div className="p-4 bg-white">
          <h3 className="text-lg font-semibold">Chat with Robot</h3>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {transcription.map((msg, index) => (
            <ChatMessage
              key={index}
              message={msg.content}
              isAI={msg.role === 'assistant'}
            />
          ))}
        </div>

        {/* Chat Input - Fixed at bottom */}
        <div className="p-4 border-t bg-white shadow-up">
          <div className="flex space-x-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
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
      </div>

      {/* Main Content */}
      <div className="flex-1 ml-0">
        {/* Main Counseling UI */}
        <div className="flex flex-col justify-center items-center bg-white p-8 min-h-screen">
          <h2 className="text-xl font-semibold mb-4">AI Counseling Session</h2>

          {/* 🌟 비디오 컴포넌트: 웹캠만 표시
          {dataSource === "webcam" && (
            <div className=" bg-gray-800 border-2 border-white shadow-lg rounded-lg transition-all duration-300 w-96">
              <VideoCapture />
              <button
                onClick={() => setIsMyVideoLarge(!isMyVideoLarge)}
                className="absolute top-2 right-2 bg-white text-gray-800 p-1 rounded-full shadow-md"
              >
                {isMyVideoLarge ? (
                  <Minimize className="w-5 h-5" />
                ) : (
                  <Maximize className="w-5 h-5" />
                )}
              </button>
            </div>
          )} */}

          {/* Avatar Dropdown */}
          <div className="absolute top-16 right-16">
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="bg-white text-gray-800 p-2 rounded-full shadow-md flex items-center space-x-2"
            >
              <img
                src={selectedAvatar}
                alt="Selected Avatar"
                className="w-8 h-8 rounded-full"
              />
              <ChevronDown className="w-4 h-4" />
            </button>
            {isDropdownOpen && (
              <div className="absolute right-0 mt-2 bg-white shadow-lg rounded-lg w-40">
                <ul className="space-y-2 p-2">
                  {avatars.map((avatar) => (
                    <li
                      key={avatar.name}
                      className="flex items-center space-x-2 cursor-pointer hover:bg-indigo-100 p-2 rounded"
                      onClick={() => {
                        setSelectedAvatar(avatar.img);
                        setIsDropdownOpen(false);
                      }}
                    >
                      <img
                        src={avatar.img}
                        alt={avatar.name}
                        className="w-8 h-8 rounded-full"
                      />
                      <span>{avatar.name}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* 행복지수 그래프 */}
          <div className="mt-6 w-full flex justify-center">
            <HappinessChart dataSource={dataSource} />
          </div>
        </div>
      </div>

      {/* Right Sliding Panel */}
      <div
        className={`absolute z-50 right-0 top-0 h-full bg-gray-100 shadow-md p-4 transition-transform transform ${
          isRightPanelOpen ? "translate-x-0" : "translate-x-full"
        } w-1/4`}
      >
        <button
          onClick={() => setIsRightPanelOpen(!isRightPanelOpen)}
          className="absolute left-[-20px] top-1/2 transform -translate-y-1/2 bg-indigo-600 text-white p-2 rounded-full shadow-md"
        >
          {isRightPanelOpen ? (
            <ChevronRight className="w-5 h-5" />
          ) : (
            <ChevronLeft className="w-5 h-5" />
          )}
        </button>

        <h3 className="text-lg font-semibold mb-4">RAG with Finetuned Embedding Model</h3>
        <h3 className="text-lg font-semibold mb-4">EHR (Electronic Health Record)</h3>
      </div>
    </div>
  );
};

export default Counseling;
