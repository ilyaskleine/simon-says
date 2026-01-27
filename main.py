import pygame
import threading
import queue
import time
import random
import sys

# --- KONFIGURATION ---

# Standard-Fallback, falls Vollbild Erkennung scheitert
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600

# Farben (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_TRANSPARENT = (0, 0, 0, 180) # Halbtransparenter Hintergrund für Text

# Die 4 Farben für die Felder
COLORS = [
    (200, 0, 0),    # 0: Rot (Oben Links)
    (0, 200, 0),    # 1: Grün (Oben Rechts)
    (0, 0, 200),    # 2: Blau (Unten Links)
    (200, 200, 0)   # 3: Gelb (Unten Rechts)
]
# Helle Versionen (wenn aktiv)
HIGHLIGHT_COLORS = [
    (255, 80, 80),
    (80, 255, 80),
    (80, 80, 255),
    (255, 255, 150)
]

# GPIO Pins (BCM) - Reihenfolge: Rot, Grün, Blau, Gelb
GPIO_PINS = [17, 27, 22, 10] 

# Simulation (Tastatur statt GPIO) automatisch setzen
USE_KEYBOARD_MODE = True 

# --- HARDWARE ABSTRAKTION ---

try:
    import RPi.GPIO as GPIO
    ON_PI = True
    # Wenn wir auf dem Pi sind, bevorzugen wir GPIO, außer man will explizit testen
    USE_KEYBOARD_MODE = False 
except ImportError:
    ON_PI = False
    print("Info: RPi.GPIO nicht gefunden. Starte im Simulations-Modus (WASD).")
    USE_KEYBOARD_MODE = True

class SensorThread(threading.Thread):
    def __init__(self, event_queue, use_keyboard=False):
        super().__init__()
        self.event_queue = event_queue
        self.running = True
        self.use_keyboard = use_keyboard
        self.last_states = [1, 1, 1, 1] 

        if not self.use_keyboard and ON_PI:
            GPIO.setmode(GPIO.BCM)
            for pin in GPIO_PINS:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        while self.running:
            if self.use_keyboard:
                time.sleep(0.1)
            else:
                for i, pin in enumerate(GPIO_PINS):
                    current_state = GPIO.input(pin)
                    # Auslösung bei HIGH -> LOW (Unterbrechung)
                    if self.last_states[i] == 1 and current_state == 0:
                        self.event_queue.put(('INPUT', i))
                        time.sleep(0.1) # Debounce
                    self.last_states[i] = current_state
                time.sleep(0.01)

    def stop(self):
        self.running = False
        if ON_PI and not self.use_keyboard:
            GPIO.cleanup()

# --- SPIEL LOGIK ---

class SimonGame:
    def __init__(self):
        self.sequence = []
        self.input_step = 0
        self.state = "START" # START, SHOWING, WAITING, GAME_OVER
        self.score = 0
        
        # Timing Variablen
        self.wait_start_time = 0 # Wann hat der Computer aufgehört anzuzeigen?
        self.reaction_time_display = 0.0
        self.active_light = -1 
        
        self.show_timer = 0
        self.show_interval = 0.8
        self.pause_interval = 0.2

    def start_new_game(self):
        self.sequence = []
        self.score = 0
        self.add_step()
        self.state = "SHOWING"
        self.input_step = 0
        self.reaction_time_display = 0.0

    def add_step(self):
        self.sequence.append(random.randint(0, 3))

    def update(self, dt, input_queue):
        # 1. Sequenz abspielen
        if self.state == "SHOWING":
            total_cycle = self.show_interval + self.pause_interval
            step_index = int(self.show_timer / total_cycle)
            phase = self.show_timer % total_cycle

            if step_index < len(self.sequence):
                if phase < self.show_interval:
                    self.active_light = self.sequence[step_index]
                else:
                    self.active_light = -1
                self.show_timer += dt
            else:
                # Sequenz beendet -> Umschalten auf Warten
                self.active_light = -1
                self.state = "WAITING"
                self.input_step = 0
                self.show_timer = 0
                # HIER Startzeitpunkt für Reaktion setzen
                self.wait_start_time = time.time()

        # 2. Auf Input warten
        elif self.state == "WAITING":
            try:
                event_type, field_id = input_queue.get_nowait()
                if event_type == 'INPUT':
                    
                    # Reaktionszeit NUR beim allerersten Schritt der Folge berechnen
                    if self.input_step == 0:
                        self.reaction_time_display = time.time() - self.wait_start_time

                    self.active_light = field_id 
                    # Reset Timer für visuelles Feedback (Licht bleibt kurz an)
                    self.vis_feedback_start = time.time()

                    if field_id == self.sequence[self.input_step]:
                        self.input_step += 1
                        if self.input_step >= len(self.sequence):
                            self.score += 1
                            self.add_step()
                            self.state = "SHOWING"
                            self.show_timer = 0
                            time.sleep(0.5) 
                    else:
                        self.state = "GAME_OVER"
            
            except queue.Empty:
                # Licht ausschalten nach kurzem Feedback (0.3s)
                if self.active_light != -1:
                    # Wir nutzen hier time.time() direkt, da wir keinen sauberen Timer im input haben
                    # Ein einfacher Timeout reicht hier.
                    pass 
                # Hinweis: Um das Licht exakt nach 0.3s auszumachen ohne queue input,
                # müsste man hier einen timer prüfen. Für Simon Says reicht oft kurzes Aufblitzen.
                # Wir machen es hier beim nächsten Show-Loop oder Input aus.
                if self.state == "WAITING" and hasattr(self, 'vis_feedback_start'):
                     if time.time() - self.vis_feedback_start > 0.3:
                         self.active_light = -1

        elif self.state == "GAME_OVER":
            try:
                event_type, _ = input_queue.get_nowait()
                if event_type == 'INPUT':
                    self.start_new_game()
            except queue.Empty:
                pass


# --- GRAFIK HELPER ---

def draw_centered_text(surface, text, font, color, center_x, center_y, bg_color=None):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(center_x, center_y))
    
    if bg_color:
        # Etwas Padding um den Text
        bg_rect = text_rect.inflate(20, 10) 
        s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        s.fill(bg_color)
        surface.blit(s, bg_rect)
        
    surface.blit(text_obj, text_rect)

def draw_game(screen, font_big, font_small, game):
    w, h = screen.get_size()
    mid_x, mid_y = w // 2, h // 2
    
    # 4 Felder
    rects = [
        (0, 0, mid_x, mid_y),       # Rot
        (mid_x, 0, mid_x, mid_y),   # Grün
        (0, mid_y, mid_x, mid_y),   # Blau
        (mid_x, mid_y, mid_x, mid_y)# Gelb
    ]

    for i in range(4):
        color = COLORS[i]
        if game.active_light == i:
            color = HIGHLIGHT_COLORS[i]
        pygame.draw.rect(screen, color, rects[i])
        pygame.draw.rect(screen, BLACK, rects[i], 4)

    # Zentrales Overlay (HUD)
    # Wir erstellen eine Box in der Mitte für Informationen
    hud_width = 400
    hud_height = 200
    hud_rect = pygame.Rect(0, 0, hud_width, hud_height)
    hud_rect.center = (mid_x, mid_y)

    # Hintergrundbox für Text (Semi-Transparent)
    hud_surf = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
    hud_surf.fill(GRAY_TRANSPARENT)
    screen.blit(hud_surf, hud_rect)
    pygame.draw.rect(screen, WHITE, hud_rect, 3)

    # Text Logik
    center_x, center_y = hud_rect.center

    if game.state == "START":
        draw_centered_text(screen, "SIMON SAYS", font_big, WHITE, center_x, center_y - 30)
        draw_centered_text(screen, "Zum Starten Feld betreten", font_small, (200, 200, 200), center_x, center_y + 30)
    
    elif game.state == "GAME_OVER":
        draw_centered_text(screen, "GAME OVER", font_big, (255, 50, 50), center_x, center_y - 30)
        draw_centered_text(screen, f"Score: {game.score}", font_big, WHITE, center_x, center_y + 20)
        draw_centered_text(screen, "Neustart: Feld betreten", font_small, (200, 200, 200), center_x, center_y + 60)
    
    else:
        # Im Spiel
        status_text = "Merken!" if game.state == "SHOWING" else "Du bist dran!"
        draw_centered_text(screen, status_text, font_big, WHITE, center_x, center_y - 40)
        draw_centered_text(screen, f"Punkte: {game.score}", font_small, WHITE, center_x, center_y + 10)
        
        # Reaktionszeit nur anzeigen, wenn verfügbar
        if game.reaction_time_display > 0:
             draw_centered_text(screen, f"Reaktion: {game.reaction_time_display:.2f}s", font_small, (255, 255, 0), center_x, center_y + 50)

    pygame.display.flip()

# --- MAIN ---

def main():
    pygame.init()
    
    # Vollbild Modus
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # Maus verstecken für Kiosk-Feeling
    pygame.mouse.set_visible(False)
    
    clock = pygame.time.Clock()
    
    # Schriftarten skalieren basierend auf Auflösung
    h = screen.get_height()
    font_big = pygame.font.SysFont("Arial", int(h * 0.08), bold=True)
    font_small = pygame.font.SysFont("Arial", int(h * 0.04))

    input_queue = queue.Queue()
    sensor_thread = SensorThread(input_queue, use_keyboard=USE_KEYBOARD_MODE)
    sensor_thread.start()

    game = SimonGame()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Notausgang aus dem Vollbild mit ESCAPE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # WASD Simulation
                if USE_KEYBOARD_MODE:
                    field = -1
                    if event.key == pygame.K_w: field = 0 
                    elif event.key == pygame.K_d: field = 1
                    elif event.key == pygame.K_s: field = 2
                    elif event.key == pygame.K_a: field = 3
                    
                    if field != -1:
                        input_queue.put(('INPUT', field))
                        if game.state == "START":
                            # Queue leeren vor Start um Fehlstarts zu vermeiden
                            with input_queue.mutex: input_queue.queue.clear()
                            game.start_new_game()

        game.update(dt, input_queue)
        
        # Start über Sensor Input
        if game.state == "START" and not input_queue.empty():
             with input_queue.mutex: input_queue.queue.clear()
             game.start_new_game()

        draw_game(screen, font_big, font_small, game)

    sensor_thread.stop()
    sensor_thread.join()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()