import React, { useState, useEffect, useRef } from 'react';
import { Send, MessageCircle, History, User, Bot } from 'lucide-react';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI assistant. How can I help you today?", sender: 'ai', timestamp: new Date() }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([
    { id: 1, title: "Getting Started", messages: 5, timestamp: new Date(Date.now() - 86400000) },
    { id: 2, title: "Project Discussion", messages: 12, timestamp: new Date(Date.now() - 172800000) },
    { id: 3, title: "Code Review", messages: 8, timestamp: new Date(Date.now() - 259200000) }
  ]);
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        text: generateAIResponse(inputValue),
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1000 + Math.random() * 2000);
  };

  const generateAIResponse = (userInput) => {
    const responses = [
      "That's an interesting question! Let me help you with that.",
      "I understand what you're looking for. Here's my suggestion:",
      "Based on your input, I can provide the following insights:",
      "Great question! Let me break this down for you:",
      "I'd be happy to assist you with that. Here's what I think:",
      "That's a complex topic. Let me explain it step by step:",
    ];
    return responses[Math.floor(Math.random() * responses.length)] + " " + 
           "This is a simulated response to demonstrate the chat functionality. In a real implementation, this would connect to your AI backend service.";
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const loadConversation = (conversation) => {
    const simulatedMessages = [
      { id: 1, text: `Loading conversation: ${conversation.title}`, sender: 'ai', timestamp: conversation.timestamp },
      { id: 2, text: "This is a previously saved conversation.", sender: 'user', timestamp: new Date(conversation.timestamp.getTime() + 60000) },
      { id: 3, text: "Conversation history loaded successfully!", sender: 'ai', timestamp: new Date(conversation.timestamp.getTime() + 120000) }
    ];
    setMessages(simulatedMessages);
    setShowHistory(false);
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (timestamp) => {
    const today = new Date();
    const messageDate = new Date(timestamp);
    const diffTime = Math.abs(today - messageDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return 'Yesterday';
    if (diffDays <= 7) return `${diffDays} days ago`;
    return messageDate.toLocaleDateString();
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Conversation History Panel */}
      <div className={`${showHistory ? 'w-80' : 'w-0'} transition-all duration-300 overflow-hidden bg-gray-800 border-r border-gray-700`}>
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <History size={20} />
            Conversation History
          </h2>
        </div>
        <div className="overflow-y-auto h-full pb-20">
          {conversationHistory.map((conversation) => (
            <div
              key={conversation.id}
              onClick={() => loadConversation(conversation)}
              className="p-4 hover:bg-gray-700 cursor-pointer border-b border-gray-700 transition-colors"
            >
              <div className="font-medium text-white">{conversation.title}</div>
              <div className="text-sm text-gray-400 mt-1">
                {conversation.messages} messages • {formatDate(conversation.timestamp)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-gray-800 p-4 border-b border-gray-700 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              <History size={20} />
            </button>
            <div className="flex items-center gap-2">
              <Bot size={24} className="text-blue-400" />
              <h1 className="text-xl font-semibold">AI Assistant</h1>
            </div>
          </div>
          <div className="text-sm text-gray-400">
            {isLoading ? 'AI is thinking...' : 'Online'}
          </div>
        </div>

        {/* Message List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-3 ${
                message.sender === 'user' ? 'flex-row-reverse' : ''
              }`}
            >
              <div className={`p-2 rounded-full ${
                message.sender === 'user' 
                  ? 'bg-blue-600' 
                  : 'bg-gray-600'
              }`}>
                {message.sender === 'user' ? (
                  <User size={16} />
                ) : (
                  <Bot size={16} />
                )}
              </div>
              <div className={`max-w-xs lg:max-w-md xl:max-w-lg ${
                message.sender === 'user' ? 'text-right' : ''
              }`}>
                <div className={`p-3 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-white'
                }`}>
                  {message.text}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-full bg-gray-600">
                <Bot size={16} />
              </div>
              <div className="max-w-xs lg:max-w-md xl:max-w-lg">
                <div className="p-3 rounded-lg bg-gray-700 text-white">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* User Input */}
        <div className="p-4 border-t border-gray-700 bg-gray-800">
          <div className="flex gap-2">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              className="flex-1 bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows="1"
              style={{
                minHeight: '40px',
                maxHeight: '120px',
                overflowY: 'auto'
              }}
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition-colors flex items-center justify-center min-w-[50px]"
            >
              <Send size={20} />
            </button>
          </div>
          <div className="text-xs text-gray-400 mt-2">
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;