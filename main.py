from pathlib import Path

class Tool:
    def encrypt(self, game_path: str) -> None:
        with open(game_path) as f:
            game = f.read()

        game = " ".join(game.splitlines())

        game_space_splitted = game.split(" ")

        full_round_count = len(game_space_splitted) // 3

        game_rounds = []
        for move in range(full_round_count):
            game_rounds.append(f"{game_space_splitted[3*move+1]},{game_space_splitted[3*move+2]}")

        if len(game_space_splitted) % 3 != 0:
            game_rounds.append(f"{game_space_splitted[3*full_round_count+1]}")

        separator = "."
        game = separator.join(game_rounds)

        output_path = Path("crypted_game.txt")
        with output_path.open("w", encoding="utf-8") as f:
            f.write(game)



    def decrypt(self, crypted_game_path: str) -> None:
        with open(crypted_game_path) as f:
            game_crypted = f.read()

        game_rounds = game_crypted.split(".")

        game_space_splited = []
        for round in game_rounds:
            moves = round.split(",")
            game_space_splited.append(moves)

        full_round_count = len(game_space_splited)
        game = ""
        for move in range(full_round_count):
            separator = " "
            game += f"{move+1}. {separator.join(game_space_splited[move])} "

        game = game[:-1]

        output_path = Path("decrypted_game.txt")
        with output_path.open("w", encoding="utf-8") as f:
            f.write(game) 

tool = Tool()

tool.encrypt("game.txt")

tool.decrypt("crypted_game.txt")