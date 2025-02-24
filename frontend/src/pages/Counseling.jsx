import { useState, useEffect } from "react";
import elon from "../assets/elon.png";
import donald from "../assets/donald.png";
import ted from "../assets/ted.png";
import ChatMessage from "../components/ChatMessage";

const Counseling = () => {
  const [mostRecentImage, setMostRecentImage] = useState(null);
  const [mostRecentUserMessage, setMostRecentUserMessage] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState("");
  const [transcription, setTranscription] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [ragDocuments, setRagDocuments] = useState([]);
  const [healthRecord, setHealthRecord] = useState({
    physiologicalFunctions: {
      bowelMovement: false,
      urination: false,
      hydration: false,
      nutrition: false,
      sleepCycle: false,
      oralHygiene: false,
      personalHygiene: false,
      fatigue: false,
      gastrointestinalDiscomfort: false,
      cephalgia: false,
    },
    psychologicalStatus: {
      positiveAffect: false,
      anxietyDepression: false,
      concentrationDeficit: false,
      phobicSymptoms: false,
      psychomotorRetardation: false,
    },
    physicalActivity: {
      outdoorActivity: false,
      sedentaryBehavior: false,
      muscularFlexibility: false,
      physicalTrauma: false,
      mobilityImpairment: false,
    },
    nutritionalIntake: {
      morningNutrition: false,
      excessiveSugarIntake: false,
      carbonatedBeverages: false,
      appetiteChanges: false,
      hyperphagia: false,
    },
    academicPerformance: {
      cognitiveEngagement: false,
      learningDifficulties: false,
      academicFatigue: false,
      socialInteraction: false,
      academicAnxiety: false,
    },
    clinicalStatus: {
      medicationAdherence: false,
      bronchodilatorUsage: false,
      allergicResponse: false,
      respiratoryDistress: false,
      dermatologicalSymptoms: false,
    },
  });

  const avatars = [
    { name: "Ted", img: ted },
    { name: "Donald", img: donald },
    { name: "Elon", img: elon },
  ];

  useEffect(() => {
    const interval = setInterval(runFinalFunction, 1000); // 로봇 데이터 주기적 GET 요청
    return () => clearInterval(interval);
  });

  const runEhrFunction = async () => {
    try {
      const response = await fetch("http://localhost:8000/ehr/check", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          checklist: healthRecord,
          conversation: mostRecentUserMessage,
        }),
      });

      const data = await response.json();

      if (data.status === 200) {
        setHealthRecord(data.response);
      }
    } catch (error) {
      console.error("Error fetching EHR function:", error);
    }
  };

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

      if (response.ok) {
        const data = await response.json();
        console.log(data);

        if (data.transcribed_text != null) {
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
          setMostRecentUserMessage(data.transcribed_text);
          if (data.rag_context && data.rag_context.length > 0) {
            setRagDocuments(data.rag_context);
          }
          runEhrFunction();
        }
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
        if (data.rag_context && data.rag_context.length > 0) {
          setRagDocuments(data.rag_context);
        }
        setMostRecentUserMessage(newMessage);
        runEhrFunction();
        setNewMessage("");
      }
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchLatestImage, 1000);
    return () => clearInterval(interval);
  }, []);

  const fetchLatestImage = async () => {
    try {
      const response = await fetch("http://localhost:8000/image/latest");
      const data = await response.json();

      if (data.status === 200) {
        if (data.image_url != null) {
          setMostRecentImage(data.image_url);
        }
      }
    } catch (error) {
      console.error("Error fetching latest image:", error);
    }
  };

  const handleEhrRequest = async () => {
    try {
      let prompt = "Now you need to ask the user sound like ted the bear in the movie regarding whether the paitient did"+ selectedItem+"kindly. Please generate a response. Only return the response not adding any additional words like sure I can do that.";
      const response = await fetch("http://localhost:8000/ehr/request", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: prompt,
          character: "ted the bear",
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const new_transcription = {
          role: "assistant",
          content: data.characterized_response,
        };
        setTranscription((prev) => [...prev, new_transcription]);
      }
    } catch (error) {
      console.error("Error requesting EHR:", error);
    }
  };

  return (
    <div className="relative flex h-screen overflow-hidden bg-gray-50">
      {/* Chat Section */}
      <div className="flex-1 h-full flex flex-col justify-between bg-gray-100 border-2 border-gray-100 shadow-lg">
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {transcription.map((msg, index) => (
            <ChatMessage
              key={index}
              message={msg.content}
              isAI={msg.role === "assistant"}
            />
          ))}
        </div>

        {/* Chat Input */}
        <div className="border-t border-gray-200 bg-white p-4">
          <div className="flex items-center space-x-4">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-6 py-3 border-2 rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
            <button
              onClick={handleSendMessage}
              className="px-8 py-3 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 transition-all transform hover:scale-105"
            >
              Send
            </button>
          </div>
        </div>
        <div className="h-16 bg-white"></div>
      </div>

      {/* Avatar and Health Section */}
      <div className="flex-1 h-screen overflow-y-auto bg-gray-50 px-6 py-4">
        <img
          src={mostRecentImage || avatars[0].img}
          alt="Avatar"
          className="w-full h-96 object-cover rounded-2xl shadow-lg mb-6"
        />

        {/* Modal */}
        {isModalOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-lg shadow-xl max-w-md w-full">
              <h3 className="text-lg font-semibold mb-4">
                Do you want to ask Ted to ask your patient about &quot;
                {selectedItem}&quot;?
              </h3>
              <div className="flex justify-end space-x-4">
                <button
                  onClick={() => {
                    handleEhrRequest();
                    setIsModalOpen(false);
                  }}
                  className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                >
                  Yes
                </button>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                >
                  No
                </button>
              </div>
            </div>
          </div>
        )}

        <h3 className="text-2xl font-bold text-center mb-2 text-indigo-600">
          Electronic Health Record (EHR)
        </h3>

        <div className="grid grid-cols-2 gap-6">
          {Object.entries(healthRecord).map(([category, items]) => (
            <div
              key={category}
              className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all"
            >
              <h4 className="text-xl font-bold mb-4 text-indigo-600 capitalize">
                {category.replace(/([A-Z])/g, " $1").trim()}
              </h4>
              <div className="space-y-3">
                {Object.entries(items).map(([item, value]) => (
                  <div
                    key={item}
                    className="flex items-center justify-between py-1"
                  >
                    <span
                      className="text-sm text-gray-700 capitalize cursor-pointer hover:text-indigo-600"
                      onClick={() => {
                        setSelectedItem(item);
                        setIsModalOpen(true);
                      }}
                    >
                      {item.replace(/([A-Z])/g, " $1").trim()}
                    </span>
                    <span
                      className={`text-sm font-medium ${
                        value ? "text-emerald-500" : "text-rose-500"
                      }`}
                    >
                      {value ? "✓" : "✗"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* RAG Section */}
      <div className="flex-1 h-screen overflow-y-auto bg-gray-50 px-6 pt-4">
        {/* <div className="mb-4">
          <HappinessChart dataSource={dataSource} />
        </div> */}

        <h3 className="text-2xl font-bold text-center mb-2 text-indigo-600">
          Top 3 Most Relevant Documents
        </h3>
        <div className="space-y-6">
          {ragDocuments.map((doc, index) => (
            <div
              key={index}
              className={`bg-white rounded-xl p-6 transition-all hover:shadow-lg
                ${
                  index === 0
                    ? "border-2 border-indigo-500 shadow-md"
                    : "shadow-sm"
                }`}
            >
              <div className="flex items-center justify-between mb-4">
                <span className="text-lg font-semibold text-indigo-600">
                  {index === 0
                    ? "🥇 Most Relevant"
                    : index === 1
                    ? "🥈 Second Most Relevant"
                    : "🥉 Third Most Relevant"}
                </span>
                <span className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                  Score: {doc.score.toFixed(2)}
                </span>
              </div>
              <div className="text-gray-700 max-h-48 overflow-y-auto prose">
                {doc.content.split("\n").map((paragraph, i) => (
                  <p key={i} className="mb-3">
                    {paragraph}
                  </p>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Counseling;
