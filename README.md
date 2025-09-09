# PGN Crypt

![Python](https://img.shields.io/badge/python-3.13-blue)
![Chess](https://img.shields.io/badge/chess-PGN-brown)

---

## Overview

**PGN Crypt** was a small contest I had with some friends.
The goal was to take a PGN file as input (we stripped the opening metadata for simplicity) and make the game content **as small as possible**.

We could use any language, so I naturally chose Python. We had one week to come up with our solution.

---

## My solution

Instead of trying to actually encrypt the move notation like `Qxa4+`, I decided to focus on **optimizing the format**.

---

### Step 1: Clean the PGN

Chess.com exports PGN with lots of line breaks.
First, I just removed all the `\n` characters:

```python
game = " ".join(game.splitlines())
```

---

### Step 2: Split into tokens

After cleaning, I was left with something like this:

```pgn
1. e4 e5 2. Nf3 Nc6 3. Bc4 d5 4. exd5 Nb4 5. Nxe5 Bd6 ...
```

It’s basically repeating this pattern:

```
<index>. <white move> <black move>
```

So I split everything on spaces:

```python
game_space_splitted = game.split(" ")
```

And then calculated the number of **full rounds** (both white and black moves) using floor division:

```python
full_round_count = len(game_space_splitted) // 3
```

---

### Step 3: Compact each round

Each round has 3 tokens (`index`, `white move`, `black move`).
Since the index is redundant, I only kept the moves and joined them with a comma:

```python
for move in range(full_round_count):
    game_rounds.append(f"{game_space_splitted[3*move+1]},{game_space_splitted[3*move+2]}")
```

Example:

```
"1. e4 e5 2. Nf3 Nc6"
```

becomes:

```
["e4,e5", "Nf3,Nc6"]
```

---

### Step 4: Handle unfinished games

Sometimes the last round only contains a white move (for example if Black resigned).
In that case, I store the last move separately:

```python
if len(game_space_splitted) % 3 != 0:
    game_rounds.append(f"{game_space_splitted[3*full_round_count+1]}")
```

---

### Step 5: Use a compact separator

Finally, I joined all rounds with `"."` instead of spaces + numbers:

```python
separator = "."
game = separator.join(game_rounds)
```

Example:

```
e4,e5.Nf3,Nc6.Bc4,d5.exd5,Nb4
```

This is then written into `crypted_game.txt`.

---

## Decryption

The **`decrypt`** function does the exact reverse process:

1. **Read and split** the compact format by `"."`:

```python
game_rounds = game_crypted.split(".")
```

2. **Split white/black moves** (by `,`):

```python
for round in game_rounds:
    moves = round.split(",")
    game_space_splited.append(moves)
```

3. **Rebuild the PGN-like format** with proper indices:

```python
for move in range(full_round_count):
    game += f"{move+1}. {' '.join(game_space_splited[move])} "
```

---

## Example

* **Input (`game.txt`)**:

```
1. e4 e5
2. Nf3 Nc6
3. Bc4 d5
```

* **Encrypted (`crypted_game.txt`)**:

```
e4,e5.Nf3,Nc6.Bc4,d5
```

* **Decrypted (`decrypted_game.txt`)**:

```
1. e4 e5 2. Nf3 Nc6 3. Bc4 d5
```

---

## Summary

* **encrypt** = takes a PGN, removes round numbers, and compresses moves into `white,black` pairs separated by `"."`.
* **decrypt** = reverses the process and restores a human-readable PGN.