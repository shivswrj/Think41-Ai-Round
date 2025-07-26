import React, { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ApiService from '../services/api';

const ChatWindow = ({ currentConversationId, onNewConversation }) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (currentConversationId) {
      loadConversationHistory(currentConversationId);
    } else {
      setMessages([]);
    }
  }, [currentConversationId]);

  const loadConversationHistory = async (conversationId) => {
    try {
      setIsLoading(true);
      const history = await ApiService.getConversationHistory(conversationId);
      setMessages(history.messages || []);
    } catch (error) {
      console.error('Failed to load conversation history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await ApiService.sendMessage(messageText, currentConversationId);
      
      const aiMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'ai',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);

      // If this is a new conversation, notify parent component
      if (!currentConversationId && response.conversation_id) {
        onNewConversation(response.conversation_id);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h2>Customer Support Chat</h2>
      </div>
      
      <MessageList 
        messages={messages} 
        isLoading={isLoading}
      />
      
      <UserInput 
        onSendMessage={handleSendMessage} 
        disabled={isLoading}
      />
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;