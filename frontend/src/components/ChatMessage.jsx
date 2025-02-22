// eslint-disable-next-line react/prop-types
const ChatMessage = ({ message, isAI }) => {
  return (
    <div className={`flex ${isAI ? 'justify-start' : 'justify-end'} mb-4`}>
      <div
        className={`max-w-[70%] rounded-lg px-4 py-2 ${
          isAI
            ? 'bg-gray-200 text-gray-800 rounded-tl-none'
            : 'bg-indigo-600 text-white rounded-tr-none'
        }`}
      >
        <p className="text-sm">{message}</p>
      </div>
    </div>
  );
};

export default ChatMessage;
