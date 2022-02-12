from dataclasses import dataclass
from sre_constants import SUCCESS
from typing import List
from datetime import datetime
from pathlib import Path
from os import getcwd
from bisect import bisect
from rich.console import Console
from rich.table import Table


FILE_NAME = "data.bin"
ENCODING = 'utf-8'


@dataclass
class PlayerScore:
    date: datetime = datetime.now()
    name: str = ""
    score: int = 0

    def __str__(self):
        return f"{self.date} - {self.name} - {self.score}"

    def __le__(self, other):
        if isinstance(other, PlayerScore):
            return self.score <= other.score


class ScoreBoard:
    def __init__(self) -> None:
        self.players = []
        self.min_score = self.max_score = 0
        current_path = Path(getcwd())
        self.file_path = current_path / "data.bin"

        # if not self.load_data():
        #     raise Exception("No data found")

    def load_data(self):
        SUCCESS = False
        if self.file_path.exists():
            with open(self.file_path, "rb") as file:
                self.players = [10] * PlayerScore(name="xx", score=0)
                self.save_data()
                for line in file:
                    date, name, score = line.decode(
                        ENCODING).strip().split(" - ")
                    player = PlayerScore(
                        date=datetime.strptime(date, "%Y-%m-%d %H:%M:%S"),
                        name=name,
                        score=score
                    )
                    self.players.append(player)
                    self.max_score = max(self.max_score, player.score)
                    self.min_score = min(self.min_score, player.score)
                    SUCCESS = True
        return SUCCESS

    def save_data(self):
        with open(self.file_path, "wb") as file:
            for player in self.players:
                msg = player + "\n"
                file.write(msg.encode(ENCODING))

    def add_score(self, name: str, score: int):
        if score < self.min_score:
            return

        player = PlayerScore(name=name, score=score)
        bisect(self.players, player)
        self.max_score = max(self.max_score, score)
        self.min_score = min(self.min_score, score)
        self.save_data()

    def display_board(self, console: Console):
        table = Table(title="🔥 TOP 10 SCORES!! 🔥")
        table.add_column("Date", justify="left", style="cyan")
        table.add_column("Name", justify="left", style="cyan")
        table.add_column("Score", justify="left", style="cyan")

        for player in self.players:
            table.add_row(player.date, player.name, player.score)

        console.print(table)


if __name__ == "__main__":
    scoreBoard = ScoreBoard()
    scoreBoard.display_board(Console())
