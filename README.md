# PyBomb  
*A Python implementation of JKLM Bombparty*.
![image](https://github.com/user-attachments/assets/3ed929b3-d5b6-4e03-a7e3-18ed31e45101)




## Description  
PyBomb is a syllable-based word game designed for fast-paced, turn-based multiplayer gameplay.  

## How to Play  
1. **Install Dependencies**  
   Ensure you have Python installed. Install the required libraries by running:  
   ```bash  ![Uploading arrow.png…]()

   pip install pygame
   pip install tweener
   pip install pillow
   pip install git+https://github.com/robtandy/randomdict.git
   ```  

2. **Launch the Game**  
   Run the `game_manager.py` file to start the game:  
   ```bash  
   python game_manager.py  
   ```  

3. **Game Setup**  
   - The main menu allows you to select the number of players (2–8).  
   - Once players are set up, the game begins with a random syllable prompt.  

4. **Gameplay**  
   - Players take turns typing words containing the given syllable.  
   - Words must be valid, unused, and include the syllable in the correct character order.  
   - Be quick! Running out of time costs a life.  

5. **Winning the Game**  
   The last player standing with remaining lives is the winner.  

