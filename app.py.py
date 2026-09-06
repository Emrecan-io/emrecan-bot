import requests, json, chess, chess.engine, chess.pgn, os, threading, time
TOKEN = "lip_X3GvF7X563QU5wR5dz6L"
HEADERS = {"Authorization": "Bearer " + TOKEN}
print("Bot baslatiliyor...")
try: BOT_ID = requests.get("https://lichess.org/api/account", headers=HEADERS).json().get("id", "").lower()
except: BOT_ID = "emrecan_bot1"
print("Lichess baglantisi basarili. Bot ID:", BOT_ID)
try:
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    print("Stockfish Dengeli Insan Modu (Derinlik 12) Aktif!")
except Exception as e: print("Stockfish HATA:", e)

white_book = {}
black_book = {}

def load_pgns():
    global white_book, black_book
    files = ["Emrecan_l-white.pgn", "Emrecan_w-white.pgn", "Emrecan_l-black.pgn", "Emrecan_w-black.pgn"]
    for fn in files:
        if os.path.exists(fn):
            count = 0
            try:
                with open(fn, "r", encoding="utf-8", errors="ignore") as f:
                    while True:
                        g = chess.pgn.read_game(f)
                        if not g: break
                        count += 1
                        b = g.board()
                        moves = []
                        for node in g.mainline():
                            mv = node.move
                            if "-white" in fn and b.turn == chess.WHITE:
                                key = tuple(moves)
                                if key not in white_book: white_book[key] = {}
                                white_book[key][mv] = white_book[key].get(mv, 0) + 1
                            elif "-black" in fn and b.turn == chess.BLACK:
                                key = tuple(moves)
                                if key not in black_book: black_book[key] = {}
                                black_book[key][mv] = black_book[key].get(mv, 0) + 1
                            b.push(mv)
                            moves.append(mv)
            except: pass

load_pgns()

def hamle_sec(board, bot_white):
    legal = list(board.legal_moves)
    if not legal: return None
    moves = tuple(board.move_stack)
    
    if bot_white:
        if moves in white_book and white_book[moves]:
            best_mv = max(white_book[moves], key=white_book[moves].get)
            if best_mv in legal: return best_mv
    else:
        if moves in black_book and black_book[moves]:
            best_mv = max(black_book[moves], key=black_book[moves].get)
            if best_mv in legal: return best_mv
            
    try:
        # Derinligi 12 hamle ile sinirliyoruz: Taktikleri kacirmaz ama insan gibi mantikli oynar
        res = engine.play(board, chess.engine.Limit(depth=12))
        if res.move: return res.move
    except: pass
    return legal[0]

def play_game(g_id):
    print("OYUN BASLADI, ID:", g_id)
    bot_white = None
    try:
        for l in requests.get("https://lichess.org/api/bot/game/stream/" + g_id, headers=HEADERS, stream=True).iter_lines():
            if l:
                d = json.loads(l.decode("utf-8"))
                t = d.get("type")
                if t == "gameFull":
                    white_id = d.get("white", {}).get("id", "").lower()
                    bot_white = (white_id == BOT_ID)
                    moves = d.get("state", {}).get("moves", "")
                elif t == "gameState": moves = d.get("moves", "")
                else: continue
                board = chess.Board()
                if moves:
                    for m in moves.split():
                        if m: board.push(chess.Move.from_uci(m))
                if board.is_game_over(): print("Oyun bitti."); break
                sirasi_bizde = (board.turn == chess.WHITE and bot_white) or (board.turn == chess.BLACK and not bot_white)
                if sirasi_bizde:
                    mv = hamle_sec(board, bot_white)
                    if mv:
                        requests.post("https://lichess.org/api/bot/game/" + g_id + "/move/" + mv.uci(), headers=HEADERS)
    except Exception as e: print("Oyun hatasi:", e)
while True:
    try:
        print("Mac bekleniyor...")
        for l in requests.get("https://lichess.org/api/stream/event", headers=HEADERS, stream=True).iter_lines():
            if l:
                ev = json.loads(l.decode("utf-8"))
                if ev.get("type") == "challenge":
                    c_id = ev["challenge"]["id"]
                    print("Meydan okuma kabul ediliyor:", c_id)
                    requests.post("https://lichess.org/api/challenge/" + c_id + "/accept", headers=HEADERS)
                elif ev.get("type") == "gameStart":
                    threading.Thread(target=play_game, args=(ev["game"]["id"],)).start()
    except Exception as e: time.sleep(3)
