import player
import game
import pygame
from argparse import ArgumentParser

import pystk


class DummyPlayer:
    def __init__(self, team=0):
        self.team = team

    @property
    def config(self):
        return pystk.PlayerConfig(
            controller=pystk.PlayerConfig.Controller.AI_CONTROL,
            team=self.team)

    def __call__(self, image, player_info):
        return dict()


if __name__ == '__main__':
    parser = ArgumentParser("Play some Ice Hockey. List any number of players, odd players are in team 1, even players team 2.")
    parser.add_argument('-s', '--save_loc', help="Do you want to record?")
    parser.add_argument('-f', '--num_frames', default=1000, type=int, help="How many steps should we play for?")
    parser.add_argument('players', nargs='+', help="Add any number of players. List python module names or `AI` for AI players). Teams alternate.")
    args = parser.parse_args()

    graphics_config = pystk.GraphicsConfig.hd()
    graphics_config.screen_width = 400
    graphics_config.screen_height = 300
    pystk.init(graphics_config)
    pygame.init()
    screen = pygame.display.set_mode((graphics_config.screen_width, graphics_config.screen_height))

    players = []
    for i, player in range(args.players):
        if i == 0:
            players.append(game.Player(player.HockeyPlayer(i), i % 2))
        else:
            players.append(DummyPlayer(i % 2))

    tournament = game.Tournament(players, screen)
    score = tournament.play(save=args.save_loc, max_frames=args.num_frames)
    tournament.close()
    print('Final score', score)
