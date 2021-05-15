from game import *
import glob


def check_moves(c_moves, winner):
    if c_moves < 9:  # too short game someone has resign
        return False
    if winner == 0:  # draw
        return False
    if winner == 1 and c_moves % 2 == 0:  # wrong number of moves
        return False
    if winner == -1 and c_moves % 2 == 1:  # wrong number of moves
        return False
    return True


def interpret_moves(moves):
    return tuple((int(moves[m], 16) - 1, int(moves[m+1], 16) - 1) for m in range(0,len(moves),2))


def load_file(path):
    data = ''
    with open(path, 'r') as f:
        data = f.read()
    lines = data.splitlines()
    game = Game()
    states = []
    ok = 0
    bad_moves = 0
    bad_unfinished = 0
    for line in data.splitlines():
        winner_str, moves = line.split(',')[3:5]

        winner = 0
        if winner_str == '-':
            winner = -1
        elif winner_str == '+':
            winner = 1

        # we dont want to store these games
        c_moves = len(moves) // 2
        if not check_moves(c_moves, winner):
            bad_moves += 1
            continue

        moves = interpret_moves(moves)

        s = GameState(moves[:-1], on_turn=winner)
        s = game.move(s, moves[-1])
        if not s.terminal:
            bad_unfinished += 1
            continue
        ok += 1
        states.append(s.__dict__)
    print(f'Total games {len(data.splitlines())}, OK: {ok}, BAD:{bad_moves, bad_unfinished}')
    return states

if __name__ == '__main__':
    states = []
    for path in glob.iglob("game_databases/*.bdt"):
        print(path)
        states += load_file(path)

    with open('games_history.json', 'w') as f:
        json.dump(states, fp=f)
