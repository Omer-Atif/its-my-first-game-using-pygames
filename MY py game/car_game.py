import pygame
from pygame.locals import *
import random
import sys

pygame.init()


width, height = 500,800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Car Game')


gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)


road_width = 300
marker_width = 10
marker_height = 50


left_lane, center_lane, right_lane = 150, 250, 350
lanes = [left_lane, center_lane, right_lane]


road = pygame.Rect(100, 0, road_width, height)
left_edge_marker = pygame.Rect(95, 0, marker_width, height)
right_edge_marker = pygame.Rect(395, 0, marker_width, height)


lane_marker_move_y = 0


player_x, player_y = 250, 400


clock = pygame.time.Clock()
fps = 120


speed = 2
score = 0


car_image = pygame.image.load('images/car.png')
vehicle_images = [pygame.image.load('images/' + filename) for filename in ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']]
crash_image = pygame.image.load('images/crash.png')


player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()


class PlayerVehicle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(car_image, (45, 90))
        self.rect = self.image.get_rect(center=(x, y))

player = PlayerVehicle(player_x, player_y)
player_group.add(player)


running = True
gameover = False

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and not gameover:
            if event.key == K_LEFT and player.rect.centerx > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.centerx < right_lane:
                player.rect.x += 100

    
    screen.fill(green)

    
    pygame.draw.rect(screen, gray, road)

    
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    
    player_group.draw(screen)

    
    if len(vehicle_group) < 2 and not gameover:
        add_vehicle = all(vehicle.rect.top > vehicle.rect.height * 1.5 for vehicle in vehicle_group)
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = pygame.sprite.Sprite()
            vehicle.image = pygame.transform.scale(image, (45, 90))
            vehicle.rect = vehicle.image.get_rect(center=(lane, -90))
            vehicle_group.add(vehicle)

    
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            if score > 0 and score % 5 == 0:
                speed += 1

    
    vehicle_group.draw(screen)

    
    font = pygame.font.Font(None, 36)
    score_text = font.render('Score: ' + str(score), True, white)
    screen.blit(score_text, (10, 10))

    
    if pygame.sprite.spritecollide(player, vehicle_group, False):
        gameover = True

    
    if gameover:
        screen.blit(crash_image, (player.rect.centerx - 45, player.rect.top - 90))
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(None, 36)
        text = font.render('''Game over. Play again? (Press P or Q )''', True, white)
        print("P = play and Q = quit")
        text_rect = text.get_rect(center=(width / 2, 100))
        screen.blit(text, text_rect)

    pygame.display.flip()

    while gameover:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = (player_x, player_y)
                elif event.key == K_q:
                    gameover = False
                    running = False

pygame.quit()
sys.exit()
