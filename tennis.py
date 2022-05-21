class Tennis:
    def __init__(self):
        self.first_player_score_times = 0

    def score(self):
        if self.first_player_score_times == 1:
            return 'fifteen love'
        if self.first_player_score_times == 2:
            return 'thirty love'

    def first_player_score(self):
        self.first_player_score_times += 1


def greeting(name: str):
    return 'Hello ' + name


if __name__ == '__main__':
    greeting('World')
