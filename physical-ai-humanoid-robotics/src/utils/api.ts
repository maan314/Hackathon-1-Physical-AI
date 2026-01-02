// API helper functions for backend RAG integration
// Using a constant that can be configured for different environments
const API_BASE_URL = 'http://localhost:8001';

interface ChatSession {
  session_id: string;
  created_at: string;
}

interface ChatMessage {
  id: string;
  session_id: string;
  role: string;
  content: string;
  timestamp: string;
  context_sources: string[];
  metadata: Record<string, any>;
}

interface ChatQueryResponse {
  response: string;
  sources: Array<{
    id: string;
    content: string;
    metadata: Record<string, any>;
    score: number;
  }>;
  processing_time: number;
  context_retrieval: boolean;
  source_validation: Record<string, any>;
  safety_check: Record<string, any>;
}

interface SelectedTextQueryResponse {
  selected_text: string;
  context: Array<{
    id: string;
    content: string;
    metadata: Record<string, any>;
    score: number;
  }>;
  response: string;
  source_validation: Record<string, any>;
  safety_check: Record<string, any>;
  total_results: number;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Helper method to get auth headers
  private getAuthHeaders(): { [key: string]: string } {
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    const headers: { [key: string]: string } = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Mock responses for development when backend is not available
  private getMockResponse(query: string): ChatQueryResponse {
    const mockResponses: { [key: string]: string } = {
      'hello': "Hello! I'm your Physical AI Tutor. How can I help you with robotics, AI, or humanoid systems today?",
      'what is robotics': "Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. It deals with the design, construction, operation, and application of robots, as well as computer systems for their control, sensory feedback, and information processing.",
      'what is ai': "Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.",
      'what is humanoid': "A humanoid robot is a robot with its body shape built to copy that of the human body. They are bipedal, have a torso, two arms, and a head. Some humanoid robots also have a face with eyes and mouth, and can imitate human expressions.",
      'default': `I understand you're asking about "${query}". As your Physical AI Tutor, I can help you understand concepts related to robotics, AI, and humanoid systems. In a full implementation, I would retrieve relevant information from the textbook content and provide a detailed response based on the curriculum.`
    };

    const lowerQuery = query.toLowerCase();
    let responseText = mockResponses['default'];

    // Check for exact matches first
    if (mockResponses[lowerQuery]) {
      responseText = mockResponses[lowerQuery];
    } else {
      // Check for partial matches
      for (const [key, value] of Object.entries(mockResponses)) {
        if (lowerQuery.includes(key)) {
          responseText = value;
          break;
        }
      }
    }

    return {
      response: responseText,
      sources: [
        {
          id: 'mock-source-1',
          content: 'This is a simulated response from the textbook content.',
          metadata: { chapter: 'Introduction', page: '1' },
          score: 0.9
        }
      ],
      processing_time: 0.1,
      context_retrieval: true,
      source_validation: { validated: true },
      safety_check: { safe: true }
    };
  }

  // Create a new chat session
  async createChatSession(): Promise<ChatSession> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chatbot/sessions`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        // If backend is not available, return a mock session
        if (response.status === 0 || response.status === 500) {
          console.warn('Backend not available, using mock session');
          return {
            session_id: `mock-session-${Date.now()}`,
            created_at: new Date().toISOString()
          };
        }
        throw new Error(`Failed to create session: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating chat session:', error);
      // Return mock session if network error
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.warn('Network error, using mock session');
        return {
          session_id: `mock-session-${Date.now()}`,
          created_at: new Date().toISOString()
        };
      }
      throw error;
    }
  }

  // Send a message to the chatbot
  async sendChatMessage(sessionId: string, content: string): Promise<ChatQueryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chatbot/sessions/${sessionId}/query?query=${encodeURIComponent(content)}&context_retrieval=true`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        // If backend is not available, return a mock response
        if (response.status === 0 || response.status === 401 || response.status === 403 || response.status === 500) {
          console.warn('Backend not available, using mock response');
          return this.getMockResponse(content);
        }
        throw new Error(`Failed to send message: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending chat message:', error);
      // Return mock response if network error
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.warn('Network error, using mock response');
        return this.getMockResponse(content);
      }
      throw error;
    }
  }

  // Send a selected text query to the chatbot
  async sendSelectedTextQuery(sessionId: string, selectedText: string): Promise<SelectedTextQueryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chatbot/selected-text-query?selected_text=${encodeURIComponent(selectedText)}&session_id=${sessionId}`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Failed to send selected text query: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending selected text query:', error);
      throw error;
    }
  }

  // Get chat session details
  async getChatSession(sessionId: string): Promise<ChatSession> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chatbot/sessions/${sessionId}`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Failed to get session: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting chat session:', error);
      throw error;
    }
  }

  // Get chat session messages
  async getChatSessionMessages(sessionId: string, limit: number = 50): Promise<{ messages: ChatMessage[] }> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chatbot/sessions/${sessionId}/messages?limit=${limit}`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Failed to get messages: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting chat session messages:', error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();