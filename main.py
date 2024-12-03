from src.controller import Controller

def main():
    """
    Entry point of the program. Initializes the Controller and starts the game loop.
    """
    # Create an instance of the Controller class
    controller = Controller()
    
    # Start the main game loop
    controller.mainloop()

if __name__ == "__main__":
    main()