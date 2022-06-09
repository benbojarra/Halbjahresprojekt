import pygame
from pygame.version import PygameVersion
import os
from pygame.draw import *
import math

class Settings():
    window = {'width':1000, 'height':600, 'border':10}
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    inner_rect = pygame.Rect(20, 20, window['width'] - 40, window['height'] - 40)
    fps = 60
    caption = "Tank"
    punktestandgegner = 0
    punktestandspieler = 0

class Background(object):
    def __init__(self, filename) -> None:
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window['width'], Settings.window['height']))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Tank(pygame.sprite.Sprite):
    def __init__(self, picturefile, wall) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (50, 50))
        self.image_ = pygame.transform.scale(self.image_orig, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window['width'] / 8
        self.rect.centery = Settings.window['height'] / 2
        self.directionx = 0
        self.directiony = 1
        self.speed = 0
        self.rotate_angle = 0
        self.directionxy = 0
        self.right()
        self.right()
        self.wall = wall

    def update(self):
        self.direction()
        newrect = self.rect.move(self.directionx * self.speed, self.directiony * self.speed)
        self.newrect = newrect
        if newrect.right >= Settings.window['width']:
            self.stop()
        if newrect.left <= Settings.window['border']:
            self.stop()
        if newrect.bottom >= Settings.window['height']:
            self.stop()
        if newrect.top <= Settings.window['border']:
            self.stop()
        self.rect.move_ip((self.directionx * self.speed, self.directiony * self.speed))
        if pygame.sprite.collide_mask(self, self.wall):
            self.stop()

    def draw(self, screen):        
        screen.blit(self.image, self.rect)

    def direction(self):
        if self.directionxy == 0:
            self.directionx = 0
            self.directiony = 1.5
        if self.directionxy == 1:
            self.directionx = 1
            self.directiony = 1
        if self.directionxy == 2:
            self.directionx = 1.5
            self.directiony = 0
        if self.directionxy == 3:
            self.directionx = 1
            self.directiony = -1
        if self.directionxy == 4:
            self.directionx = 0
            self.directiony = -1.5
        if self.directionxy == 5:
            self.directionx = -1
            self.directiony = -1
        if self.directionxy == 6:
            self.directionx = -1.5
            self.directiony = 0
        if self.directionxy == 7:
            self.directionx = -1
            self.directiony = 1

    def stop(self):
        self.speed = 0

    def back(self):
        self.speed = 2

    def front(self):
        self.speed = -2

    def left(self):
        self.old_center = self.rect.center
        self.rotate_angle += 45
        self.image_rotate = pygame.transform.rotate(self.image_, self.rotate_angle)
        self.image = self.image_rotate
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
        if self.directionxy <= 6:
            self.directionxy += 1
        else :
            self.directionxy = 0

    def right(self):
        self.old_center = self.rect.center
        self.rotate_angle -= 45
        self.image_rotate = pygame.transform.rotate(self.image_, self.rotate_angle)
        self.image = self.image_rotate
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
        if self.directionxy >= 1:
            self.directionxy -= 1
        else :
            self.directionxy = 7

class Tankhead(pygame.sprite.Sprite):
    def __init__(self, picturefile, tank, wall) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (50, 50))
        self.image_ = pygame.transform.scale(self.image_orig, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.rect.centerx
        self.rect.centery = tank.rect.centery
        self.directionx = 0
        self.directiony = 1
        self.speed = 0
        self.rotate_angle = 0
        self.directionxy = 0
        self.right()
        self.right()
        self.wall = wall
        self.tank = tank

    def update(self):
        self.direction()
        self.rotate()
        newrect = self.tank.newrect
        if newrect.right >= Settings.window['width']:
            self.stop()
        if newrect.left <= Settings.window['border']:
            self.stop()
        if newrect.bottom >= Settings.window['height']:
            self.stop()
        if newrect.top <= Settings.window['border']:
            self.stop()
        self.rect.move_ip((self.directionx * self.speed, self.directiony * self.speed))
        if pygame.sprite.collide_mask(self.tank, self.wall):
            self.stop()

    def draw(self, screen):        
        screen.blit(self.image, self.rect)

    def direction(self):
        if self.directionxy == 0:
            self.directionx = 0
            self.directiony = 1.5
        if self.directionxy == 1:
            self.directionx = 1
            self.directiony = 1
        if self.directionxy == 2:
            self.directionx = 1.5
            self.directiony = 0
        if self.directionxy == 3:
            self.directionx = 1
            self.directiony = -1
        if self.directionxy == 4:
            self.directionx = 0
            self.directiony = -1.5
        if self.directionxy == 5:
            self.directionx = -1
            self.directiony = -1
        if self.directionxy == 6:
            self.directionx = -1.5
            self.directiony = 0
        if self.directionxy == 7:
            self.directionx = -1
            self.directiony = 1

    def stop(self):
        self.speed = 0

    def back(self):
        self.speed = 2

    def front(self):
        self.speed = -2

    def left(self):
        if self.directionxy <= 6:
            self.directionxy += 1
        else :
            self.directionxy = 0

    def right(self):
        if self.directionxy >= 1:
            self.directionxy -= 1
        else :
            self.directionxy = 7

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        old_center = self.rect.center
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_, int(angle))
        self.rect = self.image.get_rect()
        self.rect.center = old_center

class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, picturefile) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (50, 50))
        self.image_ = pygame.transform.scale(self.image_orig, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window['width'] * 0.875
        self.rect.centery = Settings.window['height'] / 2

    def update(self):
        pass

    def draw(self, screen):        
        screen.blit(self.image, self.rect)


class EnemyTankhead(pygame.sprite.Sprite):
    def __init__(self, picturefile, enemytank, wall, tank) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (50, 50))
        self.image_ = pygame.transform.scale(self.image_orig, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = enemytank.rect.centerx
        self.rect.centery = enemytank.rect.centery
        self.rotate_angle = 0
        self.directionxy = 0
        self.wall = wall
        self.enemytank = enemytank
        self.tank = tank

    def update(self):
        self.rotate()

    def draw(self, screen):        
        screen.blit(self.image, self.rect)

    def rotate(self):
        mouse_x, mouse_y = self.tank.rect.centerx, self.tank.rect.centery
        old_center = self.rect.center
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_, int(angle))
        self.rect = self.image.get_rect()
        self.rect.center = old_center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, picturefile, tank, enemytank, wall):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.rect.centerx
        self.rect.centery = tank.rect.centery
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.speed = 0.05
        self.directionx = mouse_x - tank.rect.centerx
        self.directiony = mouse_y - tank.rect.centery
        self.rotate()
        self.wall = wall
        self.enemytank = enemytank
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.cos, self.sin = (math.cos(self.angle * math.pi / 180), math.sin(self.angle * math.pi / 180))
        #self.y = math.acos((mouse_x - tank.rect.centerx, mouse_y - tank.rect.centery) * (self.cos, self.sin) / (mouse_x - tank.rect.centerx, mouse_y - tank.rect.centery))
        #print(self.cos, self.sin)
        #print(self.angle)

    def update(self):
        newrect = self.rect.move(self.directionx * self.speed, self.directiony * self.speed)
        if newrect.right >= Settings.window['width']:
            self.kill()
        if newrect.left <= Settings.window['border']:
            self.kill()
        if newrect.bottom >= Settings.window['height']:
            self.kill()
        if newrect.top <= Settings.window['border']:
            self.kill()
        self.rect.move_ip((self.directionx * self.speed, self.directiony * self.speed))
        if pygame.sprite.collide_mask(self, self.wall):
            self.kill()
        if pygame.sprite.collide_mask(self, self.enemytank):
            Settings.punktestandspieler = Settings.punktestandspieler + 1
            self.kill()
        
    def draw(self, screen):        
        screen.blit(self.image, self.rect)

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        old_center = self.rect.center
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_orig, int(angle))
        self.rect = self.image.get_rect()
        self.rect.center = old_center

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, picturefile, enemytank, tank, wall):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = enemytank.rect.centerx
        self.rect.centery = enemytank.rect.centery
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.speed = 0.05
        self.directionx = tank.rect.centerx - enemytank.rect.centerx
        self.directiony = tank.rect.centery - enemytank.rect.centery
        self.wall = wall
        self.tankx = tank.rect.centerx
        self.tanky = tank.rect.centery
        self.tank = tank
        self.rotate()

    def update(self):
        newrect = self.rect.move(self.directionx * self.speed, self.directiony * self.speed)
        if newrect.right >= Settings.window['width']:
            self.kill()
        if newrect.left <= Settings.window['border']:
            self.kill()
        if newrect.bottom >= Settings.window['height']:
            self.kill()
        if newrect.top <= Settings.window['border']:
            self.kill()
        self.rect.move_ip((self.directionx * self.speed, self.directiony * self.speed))
        if pygame.sprite.collide_mask(self, self.wall):
            self.kill()
        if pygame.sprite.collide_mask(self, self.tank):
            Settings.punktestandgegner = Settings.punktestandgegner + 1
            self.kill()

    def draw(self, screen):        
        screen.blit(self.image, self.rect)

    def rotate(self):
        old_center = self.rect.center
        rel_x, rel_y = self.tankx- self.rect.centerx, self.tanky - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_orig, int(angle))
        self.rect = self.image.get_rect()
        self.rect.center = old_center

class EnemyAim(pygame.sprite.Sprite):
    def __init__(self, picturefile, enemytank, tank, wall):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = enemytank.rect.centerx
        self.rect.centery = enemytank.rect.centery
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.speed = 0.05
        self.directionx = tank.rect.centerx - enemytank.rect.centerx
        self.directiony = tank.rect.centery - enemytank.rect.centery
        self.wall = wall
        self.tank = tank
        self.tankx = tank.rect.centerx
        self.tanky = tank.rect.centery

    def update(self):
        newrect = self.rect.move(self.directionx * self.speed, self.directiony * self.speed)
        if newrect.right >= Settings.window['width']:
            self.kill()
        if newrect.left <= Settings.window['border']:
            self.kill()
        if newrect.bottom >= Settings.window['height']:
            self.kill()
        if newrect.top <= Settings.window['border']:
            self.kill()
        self.rect.move_ip((self.directionx * self.speed, self.directiony * self.speed))
        if pygame.sprite.collide_mask(self, self.wall):
            self.kill()

    def draw(self, screen):        
        screen.blit(self.image, self.rect)

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "Cursor.png")).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.scale = {'width':self.rect.width, 'height':self.rect.height}

    def update(self):
        if self.rect.left < Settings.inner_rect.left:
            self.rect.left = Settings.inner_rect.left
        if self.rect.right > Settings.inner_rect.right:
            self.rect.right = Settings.inner_rect.right
        if self.rect.top < Settings.inner_rect.top:
            self.rect.top = Settings.inner_rect.top
        if self.rect.bottom > Settings.inner_rect.bottom:
            self.rect.bottom = Settings.inner_rect.bottom
        cx = self.rect.centerx
        cy = self.rect.centery
        self.image = pygame.transform.scale(self.image_orig,(self.scale['width'], self.scale['height']))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, picturefile):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, (1000, 600))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = Settings.window['width'] / 2
        self.rect.centery = Settings.window['height'] / 2

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,30"
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window['width'],Settings.window['height']))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.running = False
        self.background = Background("Hintergrund.png")
        self.wall = Wall("Wand.png")
        self.tank = Tank("tankkörper.png", self.wall)
        self.tankhead = Tankhead("tankkopf.png", self.tank, self.wall)
        self.enemytank = EnemyTank("tankkörper.png")
        self.enemytankhead = EnemyTankhead("tankkopf.png", self.enemytank, self.wall, self.tank)
        self.cursor = pygame.sprite.GroupSingle(Cursor())
        self.all_bullets = pygame.sprite.Group()
        self.all_enemybullets = pygame.sprite.Group()
        self.all_enemyaimbullets = pygame.sprite.Group()

    def run(self):
        self.running = True
        while self.running:
            self.watch_for_events()
            self.playing = True
            while self.playing:
                self.clock.tick(Settings.fps)
                self.cursor.sprite.rect.centerx, self.cursor.sprite.rect.centery = pygame.mouse.get_pos()
                pygame.mouse.set_visible(not Settings.inner_rect.collidepoint(self.cursor.sprite.rect.centerx, self.cursor.sprite.rect.centery))
                self.update()
                self.draw()
                self.enemyshot()
            self.running = False

        pygame.quit()

    def draw(self):
        self.background.draw(self.screen)
        self.tank.draw(self.screen)
        self.tankhead.draw(self.screen)
        self.enemytank.draw(self.screen)
        self.enemytankhead.draw(self.screen)
        self.cursor.draw(self.screen)
        self.all_bullets.draw(self.screen)
        self.all_enemybullets.draw(self.screen)
        self.wall.draw(self.screen)
        text_surface_punktestand = self.font.render("Punktestand Spieler: {0}".format(Settings.punktestandspieler), True, (0, 0, 0))
        self.screen.blit(text_surface_punktestand, dest=(10, 10))
        text_surface_punktestand = self.font.render("Punktestand Gegner: {0}".format(Settings.punktestandgegner), True, (0, 0, 0))
        self.screen.blit(text_surface_punktestand, dest=(700, 10)) 
        pygame.display.flip()

    def update(self):
        self.tank.update()
        self.tankhead.update()
        self.enemytank.update()
        self.enemytankhead.update()
        self.cursor.update()
        self.all_bullets.update()
        self.all_enemybullets.update()
        self.all_enemyaimbullets.update()
    
    def enemyshot(self):
        if len(self.all_enemybullets) < 1:
            self.enemyaimbullet = EnemyAim("bullet.png", self.enemytank, self.tank, self.wall)
            self.all_enemyaimbullets.add(self.enemyaimbullet)
            for s in self.all_enemyaimbullets:
                if pygame.sprite.collide_rect(s, self.tank):
                    self.enemybullet = EnemyBullet("bullet.png", self.enemytank, self.tank, self.wall)
                    self.all_enemybullets.add(self.enemybullet)
                    self.enemyaimbullet.kill()


    def watch_for_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing = False

                    elif event.key == pygame.K_DOWN:
                        self.tank.back()
                        self.tankhead.back()
                    elif event.key == pygame.K_UP:
                        self.tank.front()
                        self.tankhead.front()
                    elif event.key == pygame.K_LEFT:
                        self.tank.left()
                        self.tankhead.left()
                    elif event.key == pygame.K_RIGHT:
                        self.tank.right()
                        self.tankhead.right()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.tank.stop()
                        self.tankhead.stop()
                    elif event.key == pygame.K_UP:
                        self.tank.stop()
                        self.tankhead.stop()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if len(self.all_bullets) < 1:
                            self.bullet = Bullet("bullet.png", self.tank, self.enemytank, self.wall)
                            self.all_bullets.add(self.bullet)


if __name__ == "__main__":

    game = Game()
    game.run()