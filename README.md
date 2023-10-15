# Project Name: Psychologist Chatbot Game
### Project Description:

The **Psychologist Chatbot Game** is an interactive text-based game where players engage as a psychologist character to navigate through various scenarios and challenges. The game is designed to simulate conversations with AI. Players can interact with the chatbot, make choices, and progress through the game's story.

### Features:

1. **Interactive Conversations:** Engage in interactive conversations.

2. **Decision Making:** Make choices that impact the storyline and outcome of the game.

3. **Gender Selection:** Choose your character's gender at the beginning of the game.

4. **Game Progression:** Progress through the game by interacting with different characters and environments.

5. **Database Integration:** Store and retrieve game progress and character information using a database.

### Technologies Used:

- **Python:** The backend of the chatbot is implemented in Python, leveraging the Telebot library for Telegram bot development.

- **OpenAI GPT-3.5 Turbo:** Utilizes the OpenAI GPT-3.5 Turbo API for generating text-based responses and simulating conversations.

- **SQL Database:** Integrates SQL database to store and manage game data, including character information and chat history.

### How to Play:

1. **Start the Game:** Begin the game by selecting your character's gender using the provided options.

2. **Interactive Conversations:** Engage in conversations with the virtual psychologist by typing messages.

3. **Make Choices:** At certain points in the game, you will be presented with choices. Use the provided buttons to make your selection.

4. **Progress Through the Story:** Navigate through the game, interact with different characters, and explore various locations to progress the storyline.

5. **Save and Load:** Your progress is automatically saved. You can continue your game at any time by chatting with the bot.

### Setup and Installation:

To run the game locally, follow these steps:

1. **Clone the Repository:**
   ```
   git clone <repository-url>
   cd Game
   ```

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set Up API Keys:**
   - Obtain an OpenAI GPT-3.5 Turbo API and a telegram bot API with a SQL database keys and update the `api_key` variables in the code with your API keys.

4. **Run the Bot:**
   ```
   python main.py
   ```

5. **Play the Game:**
   - Open Telegram and search for your bot by its username.
   - Start a chat with the bot and enjoy playing the game!

### Game Screenshots:

![Game Screenshot 1](/screenshots/1.png)

![Game Screenshot 2](/screenshots/2.png)

### License:

This project is licensed under the [MIT License](/LICENSE).
---
