class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.active = True #change to False


class Game:
    def __init__(self):
        self.players = {}
        self._cur_turn = 0


    def start(self):
        for player in self.players:
            player.active = True

        self.program = ''
        self._cur_turn = 0


    def go(self, sid, message):
        print("current turn:", self.cur_turn)
        print("current player:", self.players[sid].player_id)
        print("num players:", self.num_players)
        print("num active players:", self.num_active_players)
        if self.players[sid].player_id == self.cur_turn:
            if len(message) == 1:
                self.program += message
                self._cur_turn += 1
        print(self.program)


    def state(self):
        d = {
                'cur_turn'  :  self.cur_turn,
                'program'   :  self.program,
                'players'   :  [p.__dict__ for p in self.players.values()]
        }
        return d


    @property
    def cur_turn(self):
        if self._cur_turn >= self.num_active_players:
            self._cur_turn %= self.num_active_players
        return self._cur_turn
    

    def add_player(self, sid):
        if not self.players.get(sid):
            self.players[sid] = Player(self.num_players)


    def remove_player(self, sid):
        player = self.players.pop(sid, None)
        if player:
            for p in self.players.values():
                if p.player_id > player.player_id:
                    p.player_id -= 1


    @property
    def num_players(self):
        return len(self.players)


    @property
    def num_active_players(self):
        return sum(1 for player in self.players.values() if player.active)
