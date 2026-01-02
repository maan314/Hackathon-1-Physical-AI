# Physical AI & Humanoid Robotics Textbook - Backend API

This is the backend API for the Physical AI & Humanoid Robotics Textbook, providing authentication, content management, personalization, translation, and RAG chatbot functionality.

## Features

- **Authentication**: User registration, login, and profile management with JWT tokens
- **Content Management**: API for textbook content, modules, and chapters
- **Personalization**: User profile-based content personalization and recommendations
- **Urdu Translation**: AI-based translation with formatting preservation
- **RAG Chatbot**: Context-aware chatbot with textbook content retrieval
- **Progress Tracking**: User progress, quiz attempts, and learning paths
- **Hardware Appendix**: Cloud vs on-prem lab configurations with sim-to-real warnings

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Content
- `POST /api/` - Create content
- `GET /api/{content_id}` - Get content by ID
- `GET /api/module/{module_type}` - Get content by module type
- `PUT /api/{content_id}` - Update content
- `DELETE /api/{content_id}` - Delete content
- `GET /api/modules/` - Get all modules
- `GET /api/modules/{module_id}/chapters` - Get chapters by module

### Progress Tracking
- `POST /api/progress` - Create or update progress
- `GET /api/progress/{content_id}` - Get user progress for content
- `GET /api/progress/` - Get all user progress
- `PUT /api/progress/{content_id}` - Update progress
- `GET /api/stats/` - Get user completion stats
- `POST /api/quiz-attempts` - Create quiz attempt
- `GET /api/quiz-attempts/{content_id}` - Get quiz attempts
- `POST /api/learning-paths` - Create learning path
- `GET /api/learning-paths/` - Get user learning paths
- `GET /api/learning-paths/{path_id}` - Get specific learning path
- `PUT /api/learning-paths/{path_id}` - Update learning path
- `DELETE /api/learning-paths/{path_id}` - Delete learning path

### Personalization
- `POST /api/personalization/profiles` - Create or update profile
- `GET /api/personalization/profiles` - Get user profile
- `PUT /api/personalization/profiles` - Update profile
- `GET /api/personalization/content/{content_id}/personalized` - Get personalized content
- `GET /api/personalization/recommendations` - Get recommendations
- `GET /api/personalization/learning-path` - Get personalized learning path

### Translation
- `POST /api/translation/requests` - Request translation
- `GET /api/translation/requests/{request_id}` - Get translation request
- `GET /api/translation/languages` - Get supported languages
- `POST /api/translation/translate` - Direct translation

### Chatbot
- `POST /api/chatbot/sessions` - Create chat session
- `GET /api/chatbot/sessions/{session_id}` - Get chat session
- `PUT /api/chatbot/sessions/{session_id}` - Update chat session
- `POST /api/chatbot/sessions/{session_id}/query` - Process query with RAG
- `POST /api/chatbot/enforce-selected-text` - Enforce selected text response
- `GET /api/chatbot/sessions/{session_id}/history` - Get chat history
- `GET /api/chatbot/sessions/` - Get all user sessions

### Hardware Appendix
- `GET /api/hardware/components` - Get hardware components
- `GET /api/hardware/setups` - Get hardware setups
- `GET /api/hardware/labs` - Get hardware labs
- `GET /api/hardware/recommendations` - Get hardware recommendations
- `GET /api/hardware/cloud-vs-on-prem` - Get cloud vs on-prem comparison
- `GET /api/hardware/latency-considerations` - Get latency considerations
- `GET /api/hardware/sim-to-real-warnings` - Get sim-to-real warnings

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
   SECRET_KEY=your-secret-key
   OPENAI_API_KEY=your-openai-api-key
   ```
3. Run the application: `uvicorn src.main:app --reload`

## Author

This project was created and is maintained by:
- **Muhammad Usman**
- GitHub: https://github.com/maan314
- LinkedIn: https://www.linkedin.com/feed/

## License

This project is provided for educational purposes as part of the Physical AI & Humanoid Robotics Textbook.