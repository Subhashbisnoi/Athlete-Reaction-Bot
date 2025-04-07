import pygame
import math
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800     
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Improved Agility Testing Bot Simulation")

# Colors
COLORS = {
    'background': (240, 240, 240),
    'floor': (210, 180, 140),
    'bot_base': (100, 100, 100),
    'laser': (255, 50, 50),
    'target': (200, 0, 0),
    'footprint': (0, 150, 0),
    'text': (40, 40, 40),
    'status': (30, 30, 30)
}

# Simulation parameters
LASER_HEIGHT = 15  # cm
PIXELS_PER_CM = 6
MIN_DISTANCE_FROM_BOT = 30  # cm
MIN_DISTANCE_FROM_PREVIOUS = 40  # cm
SERVO_SPEED = 30  # degrees per second
HUMAN_REACTION = 0.2  # seconds minimum reaction time

# Servo limits
HORIZONTAL_RANGE = (-30, 30)
VERTICAL_RANGE = (-25, -5)  # Keeps targets further away

# Fonts
font_large = pygame.font.SysFont('Arial', 24, bold=True)
font_medium = pygame.font.SysFont('Arial', 18)

class ImprovedBot:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.target_pos = None
        self.prev_pos = None
        self.foot_pos = None
        self.test_data = []
        self.trial = 0
        self.start_time = 0
        self.detected = False
        self.laser_on = False
        self.status = "Click anywhere to start new trial"
        self.bot_position = (WIDTH//2, HEIGHT//2)

    def calculate_position(self):
        """Calculate target position ensuring minimum distance from bot"""
        while True:
            h_angle = random.uniform(*HORIZONTAL_RANGE)
            v_angle = random.uniform(*VERTICAL_RANGE)
            
            # Convert angles to position
            theta = math.radians(abs(v_angle))
            phi = math.radians(h_angle)
            L = LASER_HEIGHT * math.tan(theta)
            x = L * math.sin(phi)
            y = L * math.cos(phi)
            
            # Convert to screen coordinates
            pos = (x * PIXELS_PER_CM + self.bot_position[0],
                   self.bot_position[1] - y * PIXELS_PER_CM)
            
            # Check distance from bot
            distance_from_bot = math.hypot(x, y)
            if distance_from_bot < MIN_DISTANCE_FROM_BOT:
                continue
                
            # Check distance from previous target
            if self.prev_pos:
                dx = (pos[0] - self.prev_pos[0]) / PIXELS_PER_CM
                dy = (pos[1] - self.prev_pos[1]) / PIXELS_PER_CM
                prev_distance = math.hypot(dx, dy)
                if prev_distance < MIN_DISTANCE_FROM_PREVIOUS:
                    continue
                    
            return pos, h_angle, v_angle

    def set_new_target(self):
        """Generate new valid target position"""
        self.target_pos, h_angle, v_angle = self.calculate_position()
        self.detected = False
        self.foot_pos = None
        self.laser_on = True
        self.trial += 1
        self.start_time = time.time()
        self.status = f"Trial {self.trial}: Click target!"

    def check_detection(self, pos):
        """Validate click position with realistic constraints"""
        if not self.laser_on or self.detected:
            return False

        # Calculate distance in cm
        target_cm = (
            (self.target_pos[0] - self.bot_position[0]) / PIXELS_PER_CM,
            (self.bot_position[1] - self.target_pos[1]) / PIXELS_PER_CM
        )
        click_cm = (
            (pos[0] - self.bot_position[0]) / PIXELS_PER_CM,
            (self.bot_position[1] - pos[1]) / PIXELS_PER_CM
        )
        
        distance = math.hypot(click_cm[0]-target_cm[0], click_cm[1]-target_cm[1])
        reaction_time = time.time() - self.start_time

        if reaction_time < HUMAN_REACTION:
            self.status = "Too fast! Wait for laser to stabilize"
            return False
            
        if distance < 3:  # 3cm tolerance
            self.detected = True
            self.laser_on = False
            self.prev_pos = self.target_pos
            
            if len(self.test_data) > 0:
                prev_pos = self.test_data[-1][0]
                dx = target_cm[0] - prev_pos[0]
                dy = target_cm[1] - prev_pos[1]
                distance_moved = math.hypot(dx, dy)
                speed = distance_moved / reaction_time
            else:
                speed = 0
                
            self.test_data.append((target_cm, reaction_time, speed))
            self.status = f"Hit! Time: {reaction_time:.2f}s Speed: {speed:.1f}cm/s"
            return True
            
        self.status = "Miss! Try clicking closer to the target"
        return False

    def draw(self, surface):
        surface.fill(COLORS['background'])
        
        # Draw bot
        pygame.draw.circle(surface, COLORS['bot_base'], self.bot_position, 20)
        
        # Draw laser target
        if self.laser_on and self.target_pos:
            pygame.draw.circle(surface, COLORS['laser'], self.target_pos, 8)
            pygame.draw.circle(surface, COLORS['target'], self.target_pos, 4)
            
        # Draw previous targets
        for i, (pos, _, _) in enumerate(self.test_data):
            screen_pos = (
                pos[0] * PIXELS_PER_CM + self.bot_position[0],
                self.bot_position[1] - pos[1] * PIXELS_PER_CM
            )
            pygame.draw.circle(surface, COLORS['footprint'], (int(screen_pos[0]), int(screen_pos[1])), 6)
            text = font_medium.render(str(i+1), True, COLORS['text'])
            surface.blit(text, (screen_pos[0]+10, screen_pos[1]-10))
        
        # Draw UI
        status_text = font_large.render(self.status, True, COLORS['text'])
        surface.blit(status_text, (20, HEIGHT-40))
        
        trial_text = font_medium.render(f"Trial: {self.trial}/10", True, COLORS['text'])
        surface.blit(trial_text, (WIDTH-150, 20))

def main():
    clock = pygame.time.Clock()
    bot = ImprovedBot()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                
            if event.type == MOUSEBUTTONDOWN:
                if not bot.laser_on and bot.trial < 10:
                    bot.set_new_target()
                else:
                    if bot.check_detection(event.pos) and bot.trial >= 10:
                        running = False

        bot.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()