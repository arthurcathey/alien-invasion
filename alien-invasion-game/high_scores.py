"""
High score management for Alien Invasion.

This module contains the HighScores class which handles persistent storage
of the top 5 scores to a file.

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""

import os


class HighScores:
    """
    Manage high scores persistence.
    
    Loads and saves the top 5 scores to a file so they persist between
    game sessions. Provides methods to check if a new score is high enough
    to be added to the list.
    """

    def __init__(self):
        """Initialize high scores."""
        self.score_file = 'highscores.txt'
        self.scores = self.load_scores()

    def load_scores(self):
        """Load high scores from file."""
        scores = []
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    for line in f:
                        try:
                            score = int(line.strip())
                            scores.append(score)
                        except ValueError:
                            pass
            except IOError:
                pass
        
        # Sort scores in descending order and keep top 5
        scores.sort(reverse=True)
        return scores[:5]

    def add_score(self, score):
        """Add a new score and save if it's in top 5."""
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.scores = self.scores[:5]
        self.save_scores()
        return self.is_high_score(score)

    def is_high_score(self, score):
        """Check if score is in top 5."""
        if len(self.scores) < 5:
            return True
        return score > self.scores[-1]

    def save_scores(self):
        """Save scores to file."""
        try:
            with open(self.score_file, 'w') as f:
                for score in self.scores:
                    f.write(f"{score}\n")
        except IOError:
            pass

    def get_high_score(self):
        """Get the highest score."""
        return self.scores[0] if self.scores else 0

    def get_all_scores(self):
        """Get all top 5 scores."""
        return self.scores
