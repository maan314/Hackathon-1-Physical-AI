import React, { useState, useRef, useEffect } from 'react';
import { apiClient } from '../../utils/api';
import RobotIcon from './RobotIcon';
import styles from './styles.module.css';

interface Message {
  id: string | number;
  text: string;
  sender: 'user' | 'bot';
  sources?: Array<{
    id: string;
    content: string;
    metadata: Record<string, any>;
    score: number;
  }>;
}

export default function RagChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize chat session when component mounts
  useEffect(() => {
    const initializeSession = async () => {
      try {
        const session = await apiClient.createChatSession();
        setSessionId(session.session_id);
        setMessages([{
          id: 'welcome',
          text: "Hello! I'm your textbook assistant. Ask me questions about the Physical AI & Humanoid Robotics content.",
          sender: 'bot'
        }]);
      } catch (err) {
        console.error('Error initializing session:', err);
        // Set a default message even if session creation fails
        setMessages([{
          id: 'welcome',
          text: "Hello! I'm your textbook assistant. Note: There was an issue connecting to the backend.",
          sender: 'bot'
        }]);
      }
    };

    initializeSession();
  }, []); // Empty dependency array is correct here

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || !sessionId) return;

    // Add user message
    const userMessage: Message = { id: Date.now().toString(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await apiClient.sendChatMessage(sessionId, inputValue);

      // Add bot response
      const botMessage: Message = {
        id: Date.now().toString(),
        text: response.response,
        sender: 'bot',
        sources: response.sources
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: "Sorry, I encountered an error processing your request. Please make sure the backend is running.",
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.floatingChatbot}>
      <div className={styles.chatbotIconContainer} onClick={() => setIsOpen(!isOpen)}>
        <div className={`${styles.chatbotIcon} ${isOpen ? styles.open : ''}`}>
          <RobotIcon size={isOpen ? 32 : 28} />
        </div>
        {isOpen && (
          <div className={styles.chatbotExpanded} onClick={(e) => e.stopPropagation()}>
            <div className={styles.chatbotHeader}>
              <h4>Textbook Assistant</h4>
              <span className={styles.toggleButton} onClick={(e) => { e.stopPropagation(); setIsOpen(false); }}>×</span>
            </div>

            <div className={styles.chatbotMessages}>
              {messages.length === 0 && (
                <div className={styles.welcomeMessage}>
                  Hello! I'm your textbook assistant. Ask me questions about the Physical AI & Humanoid Robotics content.
                </div>
              )}

              {messages.map((message) => (
                <div key={message.id} className={`${styles.message} ${styles[message.sender]}`} onClick={(e) => e.stopPropagation()}>
                  {message.text}
                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.sources} onClick={(e) => e.stopPropagation()}>
                      <details className={styles.sourcesDetails}>
                        <summary>Sources</summary>
                        {message.sources.map((source, idx) => (
                          <div key={idx} className={styles.source} onClick={(e) => e.stopPropagation()}>
                            <p>{source.content.substring(0, 100)}...</p>
                          </div>
                        ))}
                      </details>
                    </div>
                  )}
                </div>
              ))}

              {isLoading && (
                <div className={`${styles.message} ${styles.bot}`} onClick={(e) => e.stopPropagation()}>
                  <div className={styles.typingIndicator}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <form className={styles.chatbotInputForm} onSubmit={(e) => { e.preventDefault(); handleSendMessage(e); }} onClick={(e) => e.stopPropagation()}>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => { e.stopPropagation(); setInputValue(e.target.value); }}
                placeholder="Ask a question about the textbook..."
                disabled={isLoading}
                onClick={(e) => e.stopPropagation()}
              />
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim() || !sessionId}
                onClick={(e) => e.stopPropagation()}
              >
                Send
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}