# Turkish Flashcards Game
## CS110 Final Project Fall 2024

## Team Members

Mert Kanibir

***

## Project Description

The Turkish Language Flashcard Game is an interactive and dynamic educational tool designed to enhance Turkish vocabulary learning. With a focus on engagement and ease of use, the game offers a quiz-style interface where users match English words with their corresponding Turkish translations. The game tracks progress through a scoring system, offers feedback on responses, and includes features like a username-based leaderboard, a lives system, and smooth animations for a modern user experience. Ideal for learners of all levels, this application combines learning and fun in a visually appealing and intuitive environment.

***    

## GUI Design

### Initial Design

![initial gui](assets/gui.jpg)

### Final Design

![final gui](assets/finalgui.jpg)

## Program Design

## Features

1. Flashcards
2. Score Tracking
3. Multiple Choice
4. Usernames
5. Welcome Screen

### Classes

### Classes

- **Controller**: Manages the user interface, game state, and user interactions such as button clicks and hover effects. Handles the main game logic and transitions between screens.  
- **GameBoard**: Manages the flashcards, scoring system, and game progression. Responsible for generating multiple-choice options and validating user answers.  
- **Card**: Represents a single flashcard with an English word and its Turkish (or other language) translation. Provides the data structure for individual flashcards.  

## ATP

| Step | Procedure                                      | Expected Results                                                                 |
|------|-----------------------------------------------|---------------------------------------------------------------------------------|
| 1    | Launch the program                            | The application window appears, displaying the "Enter Your Username" screen.   |
| 2    | Enter a username and press Enter        | Transition to the "Start Screen" with the "Start Game" button visible.         |
| 3    | Click "Start Game" on the start screen        | Transition to the game screen, showing the first word to translate and options.|
| 4    | Select the correct translation option         | The score increases, and the next word appears with updated options.           |
| 5    | Enter an incorrect translation option         | A feedback message "Wrong!" appears, and the next word appears with new options.|
| 6    | Exit the application during any screen        | The application closes gracefully without errors.                              |