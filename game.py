class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.active = False


class Game:
    def __init__(self):
        self.players = {}
        self.program = ''
        self._cur_turn = 0
        self.started = False
        self.done = False


    def start(self):
        for player in self.players.values():
            player.active = True

        self.program = ''
        self._cur_turn = 0
        self.started = True


    def go(self, sid, message):

        print("current turn:", self.cur_turn)
        print("current player:", self.players[sid].player_id)
        print("num players:", self.num_players)
        print("num active players:", self.num_active_players)
        print(self.program)

        if not self.started:
            return 'Game has not yet started'
        elif self.done:
            return 'Game is over!'
        elif not self.players[sid].active:
            return 'Wait for the next game'
        elif self.players[sid].player_id != self.cur_turn:
            return 'It is not your turn!'
        elif len(message) != 1:
            return 'Did not send 1 char'
        else:
            self.program += message
            self._cur_turn += 1
            return "" # no errors


    def state(self):
        d = {
                'cur_turn'  :  self.cur_turn,
                'program'   :  self.program,
                'players'   :  [p.__dict__ for p in self.players.values()],
                'started'   :  self.started,
                'done'      :  self.done
        }
        return d


    @property
    def cur_turn(self):
        if self.num_active_players == 0:
            return -1
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
