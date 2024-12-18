# Music Recommendation Chatbot

The Music Recommendation Chatbot helps users discover music effortlessly. Built using the Rasa framework and powered by the Last.fm API, it provides recommendations for similar artists, songs, and top tracks by genre. It also offers random song suggestions to keep users inspired.

## Features

- **Artist Recommendations**: Suggests similar artists to a user-specified artist.
- **Song Recommendations**: Provides songs similar to a given track and artist.
- **Genre Recommendations**: Lists top songs in a specified genre.
- **Random Song Suggestions**: Generates random music suggestions.
- **User-Friendly Web Interface**: Accessible via an HTML interface with options to learn more about the bot and contact support.

## Setup Instructions

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.8 or later
- pip (Python package manager)
- Node.js (for frontend dependencies if necessary)

### Steps to Clone and Run

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Train the Rasa Model**:
    ```bash
    rasa train
    ```

4. **Run the Chatbot Backend**:
    ```bash
    rasa run --enable-api
    ```

5. **Run the Action Server**:
    Open another terminal and execute:
    ```bash
    rasa run actions
    ```

6. **Serve the Frontend**:
    If using a simple HTTP server for the HTML files:
    ```bash
    python -m http.server
    ```

    Place the `index.html`, `about.html`, and `contact.html` files in the root directory or the desired folder.

7. **Access the Bot**:
   - Open the `index.html` file in your web browser or navigate to the hosted server URL.
   - Interact with the bot for music recommendations.

## File Structure

- `domain.yml`: Defines intents, entities, slots, responses, and actions for the chatbot.
- `nlu.yml`: Contains the NLU training data for intent and entity recognition.
- `stories.yml`: Holds the conversation flows for different scenarios.
- `rules.yml`: Contains rules for specific actions and conversations.
- `config.yml`: Rasa configuration file for pipeline and policies.
- `app.py`: Backend server script for serving HTML pages.
- `index.html`, `about.html`, `contact.html`: Frontend files for user interaction and additional information.

## Usage

- **Discover Artists**: Ask, "Can you recommend a similar artist like Adele?"
- **Find Similar Songs**: Say, "Can you recommend songs similar to 'Endzeit' by 'Heaven Shall Burn'?"
- **Explore Genres**: Query, "Show me top metal songs."
- **Get Inspired**: Ask, "Can you suggest a random song?"


