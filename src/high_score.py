from dataclasses import dataclass
from typing import List
from datetime import datetime
from pathlib import Path
from os import getcwd
from bisect import insort
from rich.console import Console
from rich.table import Table


FILE_NAME = "data.bin"
ENCODING = 'utf-8'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

@dataclass
class PlayerScore:
    '''PlayerScore is dataclass. It mainly stores name, score and data for each high scores
    '''
    name: str = ""
    score: int = 0
    date: datetime = datetime.now().strftime(DATE_FORMAT)

    def __str__(self):
        return f"{self.date} - {self.name} - {self.score}"

    def __le__(self, other):
        if isinstance(other, PlayerScore):
            return self.score >= other.score

    def __lt__(self, other):
        if isinstance(other, PlayerScore):
            return self.score > other.score

class ScoreBoard:
    '''ScoreBoard is class which store all highscores throughout (Only Top 10)
    '''
    def __init__(self) -> None:
        self.players = []
        self.min_score = self.max_score = 0
        current_path = Path(getcwd())
        self.file_path = current_path / "data/data.bin"
        self.load_data()

    def load_data(self):
        '''load data from disk
        '''
        if self.file_path.exists():
            with open(self.file_path, "rb") as file:
                try:
                    for line in file:
                        date, name, score = line.decode(
                            ENCODING).strip().split(" - ")
                        player = PlayerScore(
                            name=name,
                            score=score,
                            date=date,
                            )
                        self.players.append(player)
                        self.max_score = max(self.max_score, player.score)
                        self.min_score = min(self.min_score, player.score)
                except Exception as e:
                    raise Exception("ParseError\nUnable to Parse Data.\nTry to delete data/data.bin")


    def save_data(self):
        '''save data to disk
        '''
        with open(self.file_path, "wb") as file:
            for player in self.players:
                msg = str(player) + "\n"
                file.write(msg.encode(ENCODING))

    def add_score(self, name: str, score: int):
        '''adding new score into table
        '''
        if score < self.min_score:
            return

        player = PlayerScore(name, score)
        insort(self.players, player)
        self.players.pop()

        self.max_score = max(self.max_score, score)
        self.min_score = min(self.min_score, score)
        self.save_data()

    def display_board(self, console: Console):
        '''displaying high score table
        '''
        if len(self.players) == 0:
            console.print("[bold red]No Highest Score available")
            return

        console.print()
        table = Table(title="🔥 TOP 10 SCORES!! 🔥")
        table.add_column("Date", justify="left", style="cyan")
        table.add_column("Name", justify="left", style="cyan")
        table.add_column("Score", justify="left", style="cyan")

        for player in self.players:
            table.add_row(player.date, player.name, str(player.score))

        console.print(table)
        console.print()
