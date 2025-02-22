import { useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

const Chatbox = () => {
  const [isRightPanelOpen, setIsRightPanelOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Function to handle sending a message
  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    // Add the user's message to the chat
    setMessages((prev) => [...prev, { text: inputText, isUser: true }]);
    setInputText("");

    // Simulate a response from the RAG system
    const response = await fetchRAGResponse(inputText);
    setMessages((prev) => [...prev, { text: response, isUser: false }]);
		setIsLoading(false);
  };

  // Simulate fetching a response from the RAG system
  const fetchRAGResponse = async (query) => {
    setIsLoading(true);
    const body = {
      question: query,
    };

    console.log("Body:", body);
    try {
      // Fetch the result and await the response
      const response = await fetch(import.meta.env.VITE_RAG_API_URL + "/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      // Parse the JSON response
      const result = await response.json();

      // Set the response state or do something with the result
      console.log("response", result.response);

      return result.response;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div
      className={`absolute z-50 right-0 top-0 w-[50%] h-full bg-gray-100 shadow-md p-4 transition-transform transform ${
        isRightPanelOpen ? "translate-x-0" : "translate-x-full"
      }`}
    >
      {/* Toggle Button */}
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

      {/* Chatbox Header */}
      <h3 className="text-lg font-semibold mb-4">Chat with RAG</h3>

      {/* Chat Messages */}
      <div className="flex flex-col justify-start overflow-y-auto mb-4">
        {messages.map((message, index) => (
          <div
            key={index}
						readOnly
            className={`mb-2 p-2 rounded-lg ${
              message.isUser ? "bg-indigo-600 text-white self-end w-fit" : "bg-white text-gray-800 self-start w-fit"
            }`}
          >
            {message.text}
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div className="flex gap-2">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
          className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
          placeholder="Type your question..."
        />
        <button
          onClick={handleSendMessage}
          className="p-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
					disabled={isLoading ? true : false}
        >
					{
						isLoading ? (
							<div className="animate-spin inline-block size-6 border-[3px] border-current border-t-transparent text-white rounded-full dark:text-blue-500" role="status" aria-label="loading">
								<span className="sr-only text-white">Loading...</span>
							</div>
						) : (
							"Send"
						)
					}
        </button>
      </div>
    </div>
  );
};

export default Chatbox;
