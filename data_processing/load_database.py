from game import *
import glob

def check_moves_short(c_moves, winner):
    return c_moves < 9  # too short game someone has resign

def check_moves_draw(c_moves, winner):
    return winner == 0

def check_moves_unfinished(c_moves, winner):
    if winner == 1 and c_moves % 2 == 0:  # wrong number of moves
        return True
    if winner == -1 and c_moves % 2 == 1:  # wrong number of moves
        return True
    return False

def check_moves(c_moves, winner):
    if c_moves < 9:
        return False
    if winner == 0:  # draw
        return False
    if winner == 1 and c_moves % 2 == 0:  # wrong number of moves
        return False
    if winner == -1 and c_moves % 2 == 1:  # wrong number of moves
        return False
    return True


def interpret_moves(moves):
    return tuple((int(moves[m], 16) - 1, int(moves[m + 1], 16) - 1) for m in range(0, len(moves), 2))


def load_file(path):
    data = ''
    with open(path, 'r') as f:
        data = f.read()
    lines = data.splitlines()
    game = Game()
    ok_games = []
    unfinished_games = []

    stats = {'ok':0, 'draw':0, 'unfinished':0, 'short':0}

    for line in data.splitlines():
        winner_str, moves = line.split(',')[3:5]

        winner = 0
        if winner_str == '-':
            winner = -1
        elif winner_str == '+':
            winner = 1

        # we dont want to store these games
        c_moves = len(moves) // 2

        if check_moves_short(c_moves, winner):
            stats['short'] += 1

        elif check_moves_draw(c_moves, winner):
            stats['draw'] += 1

        elif check_moves_unfinished(c_moves, winner):
            stats['unfinished'] += 1
            unfinished_games.append(s.__dict__)
        else:
            moves = interpret_moves(moves)
            s = GameState(moves[:-1], on_turn=winner)
            s = game.move(s, moves[-1])
            if not s.terminal:
                stats['unfinished'] += 1
                unfinished_games.append(s.__dict__)
            else:
                stats['ok'] += 1
                ok_games.append(s.__dict__)

    print(f'Total games {len(data.splitlines())}, {stats}')
    return ok_games, unfinished_games


if __name__ == '__main__':
    ok, unfinished = [], []
    for path in glob.iglob("game_databases/*.bdt"):
        print(path)
        tmp = load_file(path)
        ok += tmp[0]
        unfinished += tmp[1]

    with open('ok.json', 'w') as f:
        json.dump(ok, fp=f)

    with open('unfinished.json', 'w') as f:
        json.dump(unfinished, fp=f)
