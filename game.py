class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.active = True #change to False

class Game:
    def __init__(self):
        self.players = {}
        self._cur_player_id = 0

    def start(self):
        for player in self.players:
            player.active = True

        self.program = ''
        self._cur_player_id = 0

    def turn(self, sid, message):
        print("current player:", self.cur_player_id)
        if self.players[sid].player_id == self.cur_player_id:
            if len(message) == 1:
                self.program += message
                self._cur_player_id += 1
        print(self.program)

    @property
    def cur_player_id(self):
        if self._cur_player_id >= self.num_active_players:
            self._cur_player_id %= self.num_active_players
        return self._cur_player_id
    
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
