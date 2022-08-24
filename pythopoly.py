# Author: Amar Jilani
# GitHub username: amarjilani
# Date: 2022-08-02
# Description:
import pythopolyapi
import sys, pygame
import random

# initialize game
pygame.init()
game = pythopolyapi.RealEstateGame()
rents = [30, 30, 30, 30, 30, 30, 50, 50, 50, 50, 50, 75, 75, 75, 100, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150,
         150, 200, 200, 200, 200, 200, 300, 300, 300, 400, 400, 400, 500, 1000]
game.create_spaces(200, rents)
p1 = game.create_player("Black", 1500)
p2 = game.create_player("Red", 1500)
p3 = game.create_player("Blue", 1500)
p4 = game.create_player("Green", 1500)
players = [p1, p2, p3, p4]

main_font = pygame.font.SysFont("Segoe UI", 70, True)
scoreboard_font = pygame.font.SysFont("Segoe UI", 30, True)
buy_font = pygame.font.SysFont("Segoe UI", 40, True)

# create screen
screen = pygame.display.set_mode((1024, 1024))
gameover_surf = main_font.render("Winner is: " + game.check_game_over(), False, "Black")
gameover_rect = gameover_surf.get_rect(center=(400,100))

# title and icon
pygame.display.set_caption("Pythopoly")
icon = pygame.image.load("graphics/snakeicon2.png")
pygame.display.set_icon(icon)

# board
bg = pygame.image.load("graphics/board-final.png")

# player
player1 = pygame.image.load("graphics/pawn.png")
player1_rect = player1.get_rect(center=(945, 960))
p1.set_image(player1)
p1.set_rect(player1_rect)

player2 = pygame.image.load("graphics/pawn2.png")
player2_rect = player2.get_rect(center=(950, 960))
p2.set_image(player2)
p2.set_rect(player2_rect)

player3 = pygame.image.load("graphics/pawn3.png")
player3_rect = player3.get_rect(center=(955, 960))
p3.set_image(player3)
p3.set_rect(player3_rect)

player4 = pygame.image.load("graphics/pawn4.png")
player4_rect = player4.get_rect(center=(960, 960))
p4.set_image(player4)
p4.set_rect(player4_rect)

# dice
turn = 0
dice = pygame.image.load("graphics/dice.png")
dice_rect = dice.get_rect(midbottom=(760, 800))
whos_turn = main_font.render(players[turn].get_name() + " turn", False, "Black")
player_bank = main_font.render("Balance = $" + str(players[turn].get_balance()), False, "Black")
rolled_num = main_font.render(str(0), False, "Black")

# purchase property
buy = buy_font.render("Buy", False, "Black")
buy_rect = buy.get_rect(center=(400, 800))
border = pygame.draw.rect(bg, "Green", buy_rect, 0, 20)
notbuy = buy_font.render("Pass", False, "Black")
notbuy_rect = notbuy.get_rect(center=(600, 800))
border2 = pygame.draw.rect(bg, "Red", notbuy_rect, 0, 20)


def roll_dice():
    return random.randint(1, 6)

running = True

board_space_pos = [(954, 960), (846, 960), (768, 960), (679, 960), (596, 960), (518, 960), (430, 960), (350, 960),
                   (260, 960), (170, 960), (54, 960), (54, 850), (54, 760), (54, 680), (54, 593), (54, 505), (54, 424)
                   , (54, 342), (54, 258), (54, 174), (54, 68), (170, 68), (260, 68), (350, 68), (430, 68), (518, 68),
                   (596, 68), (679, 68), (768, 68), (846, 68), (954, 68), (954, 174), (954, 258), (954, 342), (954, 424)
                    ,(954, 505), (954, 593), (954, 680), (954, 760), (954, 850)]
print(len(board_space_pos))
clock = 0
# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if dice_rect.collidepoint(pos):
                print(turn)
                num = roll_dice()
                rolled_num = main_font.render(str(num), False, "Black")
                print(num)
                player = players[turn]
                game.move_player(player.get_name(), num)
                rect = player.get_rect()
                rect.center = board_space_pos[player.get_position()]
                for player in players:
                    other_rect = player.get_rect()
                    if other_rect.collidepoint(rect.center) and turn != 0:
                        rect.x += 5

            # purchase?
            if buy_rect.collidepoint(pos):
                player = players[turn]
                game.buy_space(player.get_name())
                turn = (turn + 1) % 4

            if notbuy_rect.collidepoint(pos):
                turn = (turn + 1) % 4






    if game.check_game_over() == "":
        screen.blit(bg, (0,0))
        screen.blit(dice, dice_rect)
        screen.blit(rolled_num, (750, 800))
        screen.blit(p1.get_image(), p1.get_rect())
        screen.blit(p2.get_image(), p2.get_rect())
        screen.blit(p3.get_image(), p3.get_rect())
        screen.blit(p4.get_image(), p4.get_rect())
        whos_turn = main_font.render(players[turn].get_name() + "'s turn", False, "Black")
        player1_bank = scoreboard_font.render("Black: $" + str(players[0].get_balance()), False, "Black")
        player2_bank = scoreboard_font.render("Red: $" + str(players[1].get_balance()), False, "Red")
        player3_bank = scoreboard_font.render("Blue: $" + str(players[2].get_balance()), False, "Blue")
        player4_bank = scoreboard_font.render("Green: $" + str(players[3].get_balance()), False, "DarkGreen")
        screen.blit(whos_turn, (330, 200))
        screen.blit(player1_bank, (150, 600))
        screen.blit(player2_bank, (150, 630))
        screen.blit(player3_bank, (150, 660))
        screen.blit(player4_bank, (150, 690))
        screen.blit(buy, buy_rect)
        screen.blit(notbuy, notbuy_rect)
        pygame.display.update()

    else:
        screen.fill("DarkRed")
        screen.blit(gameover_surf, gameover_rect)









