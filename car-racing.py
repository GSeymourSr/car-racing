import pygame
import math
import sys
import os
import random
import glob
import colorsys

# =================================================================================
#                              CONFIGURATION & TUNING
# =================================================================================

TITLE = "Greg Seymour's AI Racing Extreme"
FULLSCREEN = True
FPS = 60
IDLE_TIMEOUT = 8000 

# --- PHYSICS ---
ACCEL = 0.20           
FRICTION = 0.96        
MAX_SPEED = 38         
VEHICLE_SCALE = 120    # Giant Size
CAR_RADIUS = 50        
BUMP_FORCE = 0.9       

# --- AI BEHAVIOR ---
# Steer based on a point closer to the car to avoid "cutting" corners
AI_STEER_LOOKAHEAD = 12     
# Look far ahead only to decide when to brake
AI_BRAKE_LOOKAHEAD = 50     
AI_LANE_CHANGE_SPEED = 5    
AI_AVOID_DISTANCE = 300     

# --- COLORS ---
C_BLACK = (10, 10, 10)
C_WHITE = (255, 255, 255)
C_UI_BG = (0, 0, 0, 160)
C_NEON = (0, 255, 255)
C_GOLD = (255, 215, 0)
C_RED = (255, 50, 50)
C_GREEN = (50, 255, 50)

# --- PATHS ---
# This line finds the folder where your script is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSET_PATHS = {
    "CARS": os.path.join(BASE_DIR, "cars"),
    "BIKES": os.path.join(BASE_DIR, "bikes"),
    "ROCKETS": os.path.join(BASE_DIR, "rockets"),
    "SPACESHIPS": os.path.join(BASE_DIR, "spaceships")
}

# =================================================================================
#                                   THEMES
# =================================================================================

THEMES = {
    # --- DYNAMIC / WHIMSICAL ---
    "RAINBOW ROAD":   {"BG": (10,0,20), "ROAD": "RAINBOW", "KERB_A": (255,255,0), "KERB_B": (0,255,255), "OBJ_COL": (255,255,255), "OBJ_TYPE": "STAR"},
    "INFERNO":        {"BG": (40,0,0), "ROAD": "LAVA", "KERB_A": (255,50,0), "KERB_B": (100,0,0), "OBJ_COL": (255,200,0), "OBJ_TYPE": "EMBER"},
    "NORTHERN LIGHTS":{"BG": (0,10,30), "ROAD": "AURORA", "KERB_A": (0,255,200), "KERB_B": (100,0,255), "OBJ_COL": (200,255,255), "OBJ_TYPE": "CRYSTAL"},
    "ACID BATH":      {"BG": (20,40,0), "ROAD": "TOXIC", "KERB_A": (150,255,0), "KERB_B": (0,100,0), "OBJ_COL": (200,255,0), "OBJ_TYPE": "SLIME"},
    "DISCO FEVER":    {"BG": (0,0,0), "ROAD": "DISCO", "KERB_A": (255,0,255), "KERB_B": (0,255,255), "OBJ_COL": (255,255,255), "OBJ_TYPE": "SPHERE"},
    "PLASMA STORM":   {"BG": (20,0,40), "ROAD": "PLASMA", "KERB_A": (200,0,200), "KERB_B": (50,0,100), "OBJ_COL": (255,0,255), "OBJ_TYPE": "LIGHTS"},
    "WATER SLIDE":    {"BG": (100,200,255), "ROAD": "OCEANIC", "KERB_A": (255,255,255), "KERB_B": (0,100,200), "OBJ_COL": (0,0,255), "OBJ_TYPE": "BUBBLE"},
    "STARLIGHT RUN":  {"BG": (0,0,10), "ROAD": "GLITTER", "KERB_A": (255,255,255), "KERB_B": (100,100,255), "OBJ_COL": (255,255,200), "OBJ_TYPE": "STAR"},

    # --- CLASSIC & SCIFI ---
    "MUSHROOM CUP":   {"BG": (100,160,255), "ROAD": (210,180,140), "KERB_A": (200,0,0), "KERB_B": (255,255,255), "OBJ_COL": (255,0,0), "OBJ_TYPE": "MUSHROOM"},
    "GRAND PRIX":     {"BG": (100,200,100), "ROAD": (80,80,90), "KERB_A": (255,0,0), "KERB_B": (255,255,255), "OBJ_COL": (255,255,255), "OBJ_TYPE": "TREE"},
    "CYBER CITY":     {"BG": (5,5,20), "ROAD": (30,30,35), "KERB_A": (0,255,0), "KERB_B": (255,0,255), "OBJ_COL": (40,40,50), "OBJ_TYPE": "BUILDING"},
    "FLOWER GARDEN":  {"BG": (144,238,144), "ROAD": (255,228,196), "KERB_A": (255,105,180), "KERB_B": (255,255,224), "OBJ_COL": (255,20,147), "OBJ_TYPE": "FLOWER"},
    "DESERT RALLY":   {"BG": (210,180,140), "ROAD": (160,130,90), "KERB_A": (139,69,19), "KERB_B": (255,228,196), "OBJ_COL": (120,80,40), "OBJ_TYPE": "ROCK"},
    "GALAXY VOYAGE":  {"BG": (10,0,30), "ROAD": (60,60,80), "KERB_A": (100,0,255), "KERB_B": (0,255,255), "OBJ_COL": (255,255,200), "OBJ_TYPE": "PLANET"},
    "MARS BASE":      {"BG": (100,30,20), "ROAD": (150,70,50), "KERB_A": (255,100,50), "KERB_B": (100,20,10), "OBJ_COL": (200,80,60), "OBJ_TYPE": "ROCK"},
    "MATRIX":         {"BG": (0,20,0), "ROAD": (0,40,0), "KERB_A": (0,255,0), "KERB_B": (0,100,0), "OBJ_COL": (50,255,50), "OBJ_TYPE": "PIXEL"},
    
    # --- CREATIVE THEMES ---
    "CANDY MOUNTAIN": {"BG": (255,200,220), "ROAD": (255,240,240), "KERB_A": (255,0,0), "KERB_B": (255,255,255), "OBJ_COL": (255,100,100), "OBJ_TYPE": "LOLLIPOP"},
    "NEON JUNGLE":    {"BG": (20,0,40), "ROAD": (50,0,50), "KERB_A": (0,255,255), "KERB_B": (255,0,255), "OBJ_COL": (0,255,0), "OBJ_TYPE": "PALM"},
    "ICE CAVERN":     {"BG": (200,240,255), "ROAD": (220,230,255), "KERB_A": (0,100,200), "KERB_B": (255,255,255), "OBJ_COL": (150,220,255), "OBJ_TYPE": "CRYSTAL"},
    "GOLD RUSH":      {"BG": (60,40,0), "ROAD": (120,100,50), "KERB_A": (255,215,0), "KERB_B": (255,255,255), "OBJ_COL": (255,223,0), "OBJ_TYPE": "ROCK"},
    "LEGO LAND":      {"BG": (0,100,200), "ROAD": (255,200,0), "KERB_A": (255,0,0), "KERB_B": (0,0,255), "OBJ_COL": (255,0,0), "OBJ_TYPE": "SQUARE"},
    "PAPER WORLD":    {"BG": (250,250,250), "ROAD": (240,240,240), "KERB_A": (0,0,0), "KERB_B": (200,200,200), "OBJ_COL": (0,0,0), "OBJ_TYPE": "TRIANGLE"},
    "MIDNIGHT CITY":  {"BG": (10,10,20), "ROAD": (30,30,40), "KERB_A": (255,255,0), "KERB_B": (10,10,20), "OBJ_COL": (255,255,100), "OBJ_TYPE": "LIGHTS"},
    "CHOCO LAND":     {"BG": (100,50,0), "ROAD": (80,40,10), "KERB_A": (200,150,100), "KERB_B": (100,50,0), "OBJ_COL": (255,255,255), "OBJ_TYPE": "MUSHROOM"},
    "EMERALD ISLE":   {"BG": (0,30,10), "ROAD": (0,60,30), "KERB_A": (100,255,100), "KERB_B": (0,100,50), "OBJ_COL": (50,255,50), "OBJ_TYPE": "CRYSTAL"},
    "RUBY CANYON":    {"BG": (50,0,0), "ROAD": (80,0,0), "KERB_A": (255,100,100), "KERB_B": (150,0,0), "OBJ_COL": (255,50,50), "OBJ_TYPE": "ROCK"},
    "SAPPHIRE SEA":   {"BG": (0,0,50), "ROAD": (0,0,100), "KERB_A": (100,100,255), "KERB_B": (0,0,150), "OBJ_COL": (100,200,255), "OBJ_TYPE": "BUBBLE"},
    "VOID RUNNER":    {"BG": (0,0,0), "ROAD": (30,30,30), "KERB_A": (100,100,100), "KERB_B": (0,0,0), "OBJ_COL": (50,50,50), "OBJ_TYPE": "STAR"},
    "DIGITAL STORM":  {"BG": (0,0,20), "ROAD": (0,0,0), "KERB_A": (0,255,0), "KERB_B": (0,0,0), "OBJ_COL": (0,255,0), "OBJ_TYPE": "GRID"},
    "TOY BOX":        {"BG": (255,255,200), "ROAD": (100,100,255), "KERB_A": (255,0,0), "KERB_B": (0,255,0), "OBJ_COL": (255,165,0), "OBJ_TYPE": "SQUARE"},
    "HAUNTED HOUSE":  {"BG": (10,0,10), "ROAD": (40,20,30), "KERB_A": (150,0,200), "KERB_B": (50,0,50), "OBJ_COL": (200,200,200), "OBJ_TYPE": "GHOST"},
    "FROST BITE":     {"BG": (200,220,255), "ROAD": (220,240,255), "KERB_A": (0,0,255), "KERB_B": (100,200,255), "OBJ_COL": (255,255,255), "OBJ_TYPE": "SNOWMAN"},
    "SUNFLOWER FLD":  {"BG": (100,200,255), "ROAD": (200,150,50), "KERB_A": (255,255,0), "KERB_B": (0,100,0), "OBJ_COL": (255,200,0), "OBJ_TYPE": "FLOWER"},
    "CHECKERBOARD":   {"BG": (50,50,50), "ROAD": (0,0,0), "KERB_A": (255,255,255), "KERB_B": (0,0,0), "OBJ_COL": (200,0,0), "OBJ_TYPE": "SPHERE"},
    "BLUEPRINT":      {"BG": (0,50,150), "ROAD": (0,70,180), "KERB_A": (255,255,255), "KERB_B": (200,200,255), "OBJ_COL": (255,255,255), "OBJ_TYPE": "SQUARE"},
    "SEPIA TONE":     {"BG": (112,66,20), "ROAD": (210,180,140), "KERB_A": (100,50,0), "KERB_B": (200,150,100), "OBJ_COL": (90,40,0), "OBJ_TYPE": "TREE"},
    "NEGATIVE ZONE":  {"BG": (255,255,255), "ROAD": (20,20,20), "KERB_A": (0,0,0), "KERB_B": (50,50,50), "OBJ_COL": (0,0,0), "OBJ_TYPE": "ROCK"},
    "ALIEN HIVE":     {"BG": (20,0,20), "ROAD": (60,0,60), "KERB_A": (200,255,0), "KERB_B": (100,0,100), "OBJ_COL": (150,255,50), "OBJ_TYPE": "EGG"},
    "VOLCANO":        {"BG": (40,0,0), "ROAD": "LAVA", "KERB_A": (255,50,0), "KERB_B": (100,20,0), "OBJ_COL": (255,100,0), "OBJ_TYPE": "EMBER"},
    "WINTER NIGHT":   {"BG": (0,10,30), "ROAD": (50,50,70), "KERB_A": (100,200,255), "KERB_B": (200,200,200), "OBJ_COL": (200,220,255), "OBJ_TYPE": "CRYSTAL"},
    "STEAMPUNK":      {"BG": (80,70,60), "ROAD": (50,40,30), "KERB_A": (184,134,11), "KERB_B": (205,127,50), "OBJ_COL": (139,69,19), "OBJ_TYPE": "GEAR"},
    "MONOCHROME":     {"BG": (200,200,200), "ROAD": (50,50,50), "KERB_A": (0,0,0), "KERB_B": (255,255,255), "OBJ_COL": (100,100,100), "OBJ_TYPE": "ROCK"},
    "BLOOD MOON":     {"BG": (50,0,0), "ROAD": (30,0,0), "KERB_A": (150,0,0), "KERB_B": (100,0,0), "OBJ_COL": (255,0,0), "OBJ_TYPE": "PLANET"},
    "COTTON CANDY":   {"BG": (255,220,230), "ROAD": (255,240,250), "KERB_A": (255,150,200), "KERB_B": (150,220,255), "OBJ_COL": (255,100,150), "OBJ_TYPE": "BUBBLE"},
    "VAPORWAVE":      {"BG": (255,100,200), "ROAD": (0,200,255), "KERB_A": (255,0,255), "KERB_B": (0,255,255), "OBJ_COL": (255,255,255), "OBJ_TYPE": "SQUARE"},
    "TOXIC SWAMP":    {"BG": (30,40,20), "ROAD": (50,60,40), "KERB_A": (150,255,0), "KERB_B": (50,100,0), "OBJ_COL": (100,200,50), "OBJ_TYPE": "SLIME"},
    "SANDSTORM":      {"BG": (210,180,140), "ROAD": (160,130,90), "KERB_A": (139,69,19), "KERB_B": (255,228,196), "OBJ_COL": (120,80,40), "OBJ_TYPE": "ROCK"},
    "CHERRY BLOSSOM": {"BG": (255,240,245), "ROAD": (100,80,80), "KERB_A": (255,182,193), "KERB_B": (255,105,180), "OBJ_COL": (255,192,203), "OBJ_TYPE": "FLOWER"},
    "DEEP SPACE":     {"BG": (0,0,10), "ROAD": (30,30,40), "KERB_A": (100,0,200), "KERB_B": (200,200,255), "OBJ_COL": (255,255,255), "OBJ_TYPE": "PLANET"},
    "SUNSET BLVD":    {"BG": (100,50,100), "ROAD": (40,30,50), "KERB_A": (255,100,50), "KERB_B": (255,200,100), "OBJ_COL": (100,0,50), "OBJ_TYPE": "PALM"},
    "JUNGLE RUINS":   {"BG": (20,60,20), "ROAD": (100,100,80), "KERB_A": (50,100,50), "KERB_B": (150,150,100), "OBJ_COL": (80,120,80), "OBJ_TYPE": "ROCK"},
    
    # --- EVEN MORE NEW THEMES ---
    "CORAL REEF":     {"BG": (0,150,200), "ROAD": (0,100,150), "KERB_A": (255,150,150), "KERB_B": (255,200,100), "OBJ_COL": (255,100,100), "OBJ_TYPE": "BUBBLE"},
    "MOLTEN CORE":    {"BG": (80,20,0), "ROAD": (50,10,0), "KERB_A": (255,100,0), "KERB_B": (255,200,0), "OBJ_COL": (255,50,0), "OBJ_TYPE": "EMBER"},
    "ELECTRIC AVE":   {"BG": (10,0,30), "ROAD": (20,20,40), "KERB_A": (0,255,255), "KERB_B": (255,255,0), "OBJ_COL": (100,200,255), "OBJ_TYPE": "LIGHTS"},
    "WILD WEST":      {"BG": (200,150,100), "ROAD": (150,100,50), "KERB_A": (100,50,20), "KERB_B": (200,180,140), "OBJ_COL": (139,69,19), "OBJ_TYPE": "ROCK"},
    "ALIEN JUNGLE":   {"BG": (50,0,100), "ROAD": (80,0,150), "KERB_A": (0,255,100), "KERB_B": (255,0,255), "OBJ_COL": (100,255,0), "OBJ_TYPE": "MUSHROOM"},
    "CLOUD CITY":     {"BG": (200,230,255), "ROAD": (255,255,255), "KERB_A": (150,200,255), "KERB_B": (200,220,255), "OBJ_COL": (240,240,255), "OBJ_TYPE": "BUBBLE"},
    "RETRO GRID":     {"BG": (20,0,20), "ROAD": (0,0,0), "KERB_A": (255,0,100), "KERB_B": (0,200,255), "OBJ_COL": (255,0,200), "OBJ_TYPE": "GRID"},
    "SWAMP FEVER":    {"BG": (40,50,30), "ROAD": (60,70,50), "KERB_A": (150,200,50), "KERB_B": (100,150,50), "OBJ_COL": (100,255,100), "OBJ_TYPE": "SLIME"},
    "GOLDEN TEMPLE":  {"BG": (100,80,0), "ROAD": (150,120,20), "KERB_A": (255,215,0), "KERB_B": (200,180,0), "OBJ_COL": (255,230,100), "OBJ_TYPE": "PILLAR"},
    "NEON TOKYO":     {"BG": (10,10,30), "ROAD": (20,20,20), "KERB_A": (255,0,100), "KERB_B": (0,100,255), "OBJ_COL": (255,255,0), "OBJ_TYPE": "BUILDING"},
}

# =================================================================================
#                           MATH & TRACK GENERATION
# =================================================================================

def get_spline_point(t, p0, p1, p2, p3):
    return 0.5 * (
        (2 * p1) +
        (-p0 + p2) * t +
        (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2 +
        (-p0 + 3 * p1 - 3 * p2 + p3) * t**3
    )

def generate_track_points():
    points = []
    num_points = random.randint(22, 28) 
    
    map_w, map_h = 12000, 12000
    center_x, center_y = map_w // 2, map_h // 2
    
    base_radius = random.randint(3500, 4500)
    
    freq1 = random.uniform(2, 5) 
    mag1 = random.uniform(500, 1500)
    freq2 = random.uniform(1, 3)
    mag2 = random.uniform(200, 800)
    
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        distortion = math.sin(angle * freq1) * mag1 + math.cos(angle * freq2) * mag2
        r = base_radius + distortion
        
        if r > 5500: r = 5500
        if r < 1500: r = 1500
        
        x = center_x + math.cos(angle) * r
        y = center_y + math.sin(angle) * r
        points.append((x, y))
    return points

def spline_track(key_points, density=60):
    points = []
    normals = [] 
    count = len(key_points)
    for i in range(count):
        p0 = pygame.math.Vector2(key_points[(i - 1) % count])
        p1 = pygame.math.Vector2(key_points[i])
        p2 = pygame.math.Vector2(key_points[(i + 1) % count])
        p3 = pygame.math.Vector2(key_points[(i + 2) % count])
        
        for j in range(density):
            t = j / density
            x = get_spline_point(t, p0.x, p1.x, p2.x, p3.x)
            y = get_spline_point(t, p0.y, p1.y, p2.y, p3.y)
            
            tt = t * t
            tx = 0.5 * ((-p0.x + p2.x) + (2*p0.x - 5*p1.x + 4*p2.x - p3.x)*2*t + (-p0.x + 3*p1.x - 3*p2.x + p3.x)*3*tt)
            ty = 0.5 * ((-p0.y + p2.y) + (2*p0.y - 5*p1.y + 4*p2.y - p3.y)*2*t + (-p0.y + 3*p1.y - 3*p2.y + p3.y)*3*tt)
            tangent = pygame.math.Vector2(tx, ty)
            if tangent.length() > 0: tangent = tangent.normalize()
            normal = pygame.math.Vector2(-tangent.y, tangent.x)
            
            points.append((x, y))
            normals.append(normal)
    return points, normals

# =================================================================================
#                                ASSET MANAGEMENT
# =================================================================================
class AssetManager:
    def __init__(self):
        self.car_data = [] 
        self.current_mode = "MIXED" 

    def load_vehicles(self, mode_str):
        self.car_data = []
        self.current_mode = mode_str
        
        to_load = []
        if mode_str == "MIXED":
            to_load = ["CARS", "BIKES", "ROCKETS", "SPACESHIPS"]
        else:
            to_load = [mode_str] 

        for category in to_load:
            path = ASSET_PATHS.get(category, "")
            self.load_from_dir(path, category)

        if not self.car_data:
            self.create_defaults(to_load)

    def load_from_dir(self, directory, category):
        if not os.path.exists(directory):
            return

        files = []
        files.extend(glob.glob(os.path.join(directory, "*.png")))
        files.extend(glob.glob(os.path.join(directory, "*.jpg")))
        files = list(set(files))

        for f in files:
            try:
                img = pygame.image.load(f).convert_alpha()
                img = pygame.transform.rotate(img, -90)
                
                # SCALE TO 120
                target_size = VEHICLE_SCALE
                
                scale = target_size / max(img.get_width(), img.get_height())
                new_s = (int(img.get_width()*scale), int(img.get_height()*scale))
                img = pygame.transform.scale(img, new_s)
                
                base_name = os.path.splitext(os.path.basename(f))[0]
                name = base_name.replace("_", " ").title()
                
                skid_type = 1 if category in ["BIKES", "ROCKETS"] else 2
                
                self.car_data.append({
                    'name': name, 
                    'img': img, 
                    'type': category, 
                    'skid_type': skid_type
                })
            except: pass

    def create_defaults(self, categories):
        cols = [(200,40,40),(40,200,40),(40,40,200),(200,200,40),(200,40,200),(40,200,200)]
        
        for i, c in enumerate(cols):
            cat = categories[i % len(categories)]
            name = f"{cat.title()} {i+1}"
            
            s = pygame.Surface((120, 60), pygame.SRCALPHA)
            skid_type = 2
            
            if cat == "CARS":
                pygame.draw.rect(s, c, (0,0,120,60), border_radius=12)
                pygame.draw.rect(s, (0,0,0), (80,6,30,48), border_radius=6)
            elif cat == "BIKES":
                pygame.draw.rect(s, c, (20,20,80,20), border_radius=4)
                pygame.draw.line(s, (50,50,50), (0,30), (120,30), 6)
                skid_type = 1
            elif cat == "ROCKETS":
                pygame.draw.ellipse(s, c, (0,15,120,30))
                pygame.draw.polygon(s, (100,0,0), [(0,15),(0,45),(-20,30)])
                skid_type = 1
            elif cat == "SPACESHIPS":
                pygame.draw.polygon(s, c, [(120,30), (0,0), (20,30), (0,60)])
            
            self.car_data.append({'name': name, 'img': s, 'type': cat, 'skid_type': skid_type})

# =================================================================================
#                              TRACK RENDERER
# =================================================================================
class Track:
    def __init__(self, theme_key):
        kp = generate_track_points()
        self.points, self.normals = spline_track(kp)
        self.width, self.height = 12000, 12000 
        self.surface = pygame.Surface((self.width, self.height))
        self.mask = pygame.Surface((self.width, self.height))
        self.minimap_bg = None 
        self.checkpoints = []
        
        self.theme = THEMES[theme_key]
        self.theme_name = theme_key
        # Reverted to 650 - Enough for 2x 120px cars, not "too wide"
        self.road_width = 650
        
        self.render_mesh()

    def render_mesh(self):
        self.surface.fill(self.theme["BG"])
        self.mask.fill((0,0,0))
        
        rw = self.road_width
        
        left_edge, right_edge = [], []
        mask_left, mask_right = [], []
        k_left, k_right = [], []
        
        for i in range(len(self.points)):
            p = pygame.math.Vector2(self.points[i])
            n = self.normals[i]
            
            left_edge.append(p + n * (rw/2 - 20))
            right_edge.append(p - n * (rw/2 - 20))
            k_left.append(p + n * (rw/2 + 20))
            k_right.append(p - n * (rw/2 + 20))
            # Tighter mask to allow bouncing off walls
            mask_left.append(p + n * (rw/2 - 50))
            mask_right.append(p - n * (rw/2 - 50))

        def draw_strip(surf, color, l_points, r_points, dyn_type=None):
            cnt = len(l_points)
            for i in range(cnt):
                p1 = l_points[i]
                p2 = r_points[i]
                p3 = r_points[(i+1)%cnt]
                p4 = l_points[(i+1)%cnt]
                
                c = color
                
                if dyn_type:
                    val = i / cnt
                    if dyn_type == "RAINBOW":
                        hue = (val * 4) % 1.0 
                        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                        c = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
                    elif dyn_type == "LAVA": 
                        r = int(200 + 55 * math.sin(val * 10))
                        g = int(50 + 50 * math.sin(val * 20))
                        c = (r, g, 0)
                    elif dyn_type == "AURORA":
                        r = int(50 + 50 * math.sin(val * 10))
                        g = int(100 + 100 * math.cos(val * 10))
                        b = 200
                        c = (r, g, b)
                    elif dyn_type == "TOXIC":
                        g = int(150 + 100 * math.sin(val * 30))
                        c = (50, g, 50)
                    elif dyn_type == "PLASMA":
                        r = int(128 + 127 * math.sin(val * 15))
                        b = int(128 + 127 * math.cos(val * 15))
                        c = (r, 0, b)
                    elif dyn_type == "DISCO":
                        if (i // 10) % 2 == 0: c = (255,255,255)
                        else: c = (0,0,0)
                    elif dyn_type == "OCEANIC":
                         b = int(150 + 100 * math.sin(val * 5))
                         c = (0, 100, b)
                    elif dyn_type == "GLITTER":
                        if i % 5 == 0: c = (200,200,255)
                        else: c = (10,0,40)
                    
                pygame.draw.polygon(surf, c, [p1, p2, p3, p4])

        # --- CREATIVE SCENERY ---
        obj_type = self.theme["OBJ_TYPE"]
        obj_col = self.theme["OBJ_COL"]
        
        for i in range(1500): 
            sx = random.randint(0, self.width)
            sy = random.randint(0, self.height)
            
            close = False
            for p in self.points[::80]:
                if math.hypot(sx-p[0], sy-p[1]) < rw + 250:
                    close = True
                    break
            if not close:
                if obj_type == "STAR":
                     pygame.draw.line(self.surface, obj_col, (sx-15,sy), (sx+15,sy), 3)
                     pygame.draw.line(self.surface, obj_col, (sx,sy-15), (sx,sy+15), 3)
                elif obj_type == "GHOST":
                    pygame.draw.circle(self.surface, (255,255,255,100), (sx,sy), 30)
                elif obj_type == "SNOWMAN":
                    pygame.draw.circle(self.surface, (255,255,255), (sx,sy), 20)
                    pygame.draw.circle(self.surface, (255,255,255), (sx,sy-25), 15)
                elif obj_type == "TRIANGLE":
                    pygame.draw.polygon(self.surface, obj_col, [(sx,sy-40), (sx-30,sy+30), (sx+30,sy+30)])
                elif obj_type == "SPHERE":
                    pygame.draw.circle(self.surface, obj_col, (sx,sy), 30)
                    pygame.draw.circle(self.surface, (255,255,255), (sx-10,sy-10), 8)
                elif obj_type == "BUILDING":
                    w, h = random.randint(40, 90), random.randint(80, 200)
                    pygame.draw.rect(self.surface, obj_col, (sx, sy, w, h))
                    win_c = random.choice([(255,255,0), (0,255,255), (255,0,255)])
                    for wx in range(sx+5, sx+w-5, 15):
                        for wy in range(sy+5, sy+h-5, 20):
                            if random.random()>0.3: pygame.draw.rect(self.surface, win_c, (wx, wy, 8, 12))
                elif obj_type == "FLOWER":
                    pc = (random.randint(100,255), random.randint(0,100), random.randint(100,255))
                    pygame.draw.circle(self.surface, pc, (sx-8, sy), 8)
                    pygame.draw.circle(self.surface, pc, (sx+8, sy), 8)
                    pygame.draw.circle(self.surface, pc, (sx, sy-8), 8)
                    pygame.draw.circle(self.surface, pc, (sx, sy+8), 8)
                    pygame.draw.circle(self.surface, (255,255,0), (sx, sy), 6)
                elif obj_type == "TREE":
                    gc = (0, random.randint(100,200), 0)
                    pygame.draw.circle(self.surface, gc, (sx, sy), random.randint(30, 60))
                else:
                    pygame.draw.circle(self.surface, obj_col, (sx, sy), random.randint(20, 50))

        draw_strip(self.surface, self.theme["KERB_A"], k_left, left_edge)
        draw_strip(self.surface, self.theme["KERB_A"], right_edge, k_right)
        
        for i in range(0, len(left_edge), 8):
            if i+4 < len(left_edge):
                poly1 = [k_left[i], left_edge[i], left_edge[i+4], k_left[i+4]]
                poly2 = [right_edge[i], k_right[i], k_right[i+4], right_edge[i+4]]
                pygame.draw.polygon(self.surface, self.theme["KERB_B"], poly1)
                pygame.draw.polygon(self.surface, self.theme["KERB_B"], poly2)

        road_conf = self.theme["ROAD"]
        dyn_type = None
        col = (100,100,100)
        if isinstance(road_conf, str):
            dyn_type = road_conf
        else:
            col = road_conf
            
        draw_strip(self.surface, col, left_edge, right_edge, dyn_type=dyn_type)
        draw_strip(self.mask, (255,255,255), mask_left, mask_right)
        
        # Center Line
        for i in range(0, len(self.points), 6):
            if i+3 < len(self.points):
                pygame.draw.line(self.surface, (255,255,255, 100), self.points[i], self.points[i+3], 6)

        # Finish Line
        p, n = self.points[0], self.normals[0]
        p1 = pygame.math.Vector2(p) + n * (rw/2)
        p2 = pygame.math.Vector2(p) - n * (rw/2)
        
        steps = 18
        vec = p2 - p1
        for i in range(steps):
            pos = p1 + vec * (i/steps)
            c = C_BLACK if i%2==0 else C_WHITE
            pygame.draw.rect(self.surface, c, (pos.x-18, pos.y-18, 36, 36))

        # Checkpoints
        step = 80 
        for i in range(0, len(self.points), step):
            pt = self.points[i]
            r = pygame.Rect(pt[0]-1000, pt[1]-1000, 2000, 2000)
            self.checkpoints.append(r)
        
        if len(self.checkpoints) > 0:
            self.checkpoints.append(self.checkpoints[0])

        # Minimap
        self.minimap_bg = pygame.Surface((200, 200), pygame.SRCALPHA)
        self.minimap_bg.fill((0,0,0,150))
        scaled_points = []
        scale = 200 / self.width
        for p in self.points:
            scaled_points.append((p[0]*scale, p[1]*scale))
        if len(scaled_points) > 2:
            mc = col if not dyn_type else (200,200,200)
            pygame.draw.lines(self.minimap_bg, (150,150,150), True, scaled_points, 8)
            pygame.draw.lines(self.minimap_bg, mc, True, scaled_points, 4)
            sp = scaled_points[0]
            pygame.draw.circle(self.minimap_bg, (255, 255, 255), (int(sp[0]), int(sp[1])), 4)
            pygame.draw.circle(self.minimap_bg, (255, 0, 0), (int(sp[0]), int(sp[1])), 2)

# =================================================================================
#                                CAR LOGIC
# =================================================================================
class Car(pygame.sprite.Sprite):
    def __init__(self, track, asset_data, grid_idx, control):
        super().__init__()
        self.track = track
        self.original_image = asset_data['img']
        self.image = self.original_image
        self.name = asset_data['name']
        self.vehicle_type = asset_data.get('type', 'CARS')
        self.skid_type = asset_data.get('skid_type', 2)
        self.control = control
        
        row = grid_idx // 3 
        col = grid_idx % 3
        spawn_idx_offset = row * 22
        idx = (len(track.points) - 80 - spawn_idx_offset) % len(track.points)
        
        p = pygame.math.Vector2(track.points[idx])
        n = track.normals[idx]
        
        next_idx = (idx + 5) % len(track.points)
        forward_vec = (pygame.math.Vector2(track.points[next_idx]) - p).normalize()
        
        side_offset = (col - 1) * 120
        
        self.pos = p + (n * side_offset)
        self.angle = math.degrees(math.atan2(-forward_vec.y, forward_vec.x))
        
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pygame.math.Vector2(0,0)
        self.speed = 0
        
        self.lap = 1  
        self.has_crossed_start_line = False 
        
        self.next_cp = 0 
        self.finished = False
        self.finish_time = 0
        self.on_grass = False
        
        self.spline_idx = idx
        
        self.lane_offset = 0 # STRICT CENTER DEFAULT
        self.overtake_timer = 0
        
        self.skill = random.uniform(0.95, 1.05)
        if "Player" in self.name or "Greg" in self.name: self.skill = 1.15
        
    def update(self, can_move, skidmarks, all_cars):
        if not can_move:
            self.speed = 0
        elif self.finished:
            self.speed *= 0.94
            if self.control != "AI" and self.speed > 5: self.ai_step(all_cars)
        else:
            if self.control == "AI": self.ai_step(all_cars)
            elif self.control == "P1": self.human_step(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
            
        self.physics(skidmarks)
        self.check_cp()
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def human_step(self, up, down, left, right):
        k = pygame.key.get_pressed()
        if k[up]: self.speed += ACCEL
        elif k[down]: self.speed -= ACCEL
        else: self.speed *= FRICTION
        
        if abs(self.speed) > 1:
            turn = 2.0 
            if self.on_grass: turn *= 0.5
            speed_factor = 1.0 - (max(0, self.speed - 25) / 100) 
            turn *= speed_factor
            
            if k[left]: self.angle += turn
            if k[right]: self.angle -= turn

    def ai_step(self, all_cars):
        # 1. STEERING LOOK AHEAD (SHORT RANGE)
        # Prevents cutting corners by looking at a point closer to the car
        speed_bonus = int(self.speed * 0.4) 
        steer_idx = (self.spline_idx + AI_STEER_LOOKAHEAD + speed_bonus) % len(self.track.points)
        
        # 2. BRAKING LOOK AHEAD (LONG RANGE)
        # Look far ahead to see if a sharp turn is coming
        brake_idx = (self.spline_idx + AI_BRAKE_LOOKAHEAD) % len(self.track.points)
        
        # Calculate Curvature between steer point and brake point
        p_steer = pygame.math.Vector2(self.track.points[steer_idx])
        p_brake = pygame.math.Vector2(self.track.points[brake_idx])
        vec_path = p_brake - p_steer
        vec_now = p_steer - self.pos
        
        curvature = 0
        if vec_now.length() > 0 and vec_path.length() > 0:
            curvature = abs(vec_now.angle_to(vec_path))

        # 3. Traffic Check
        car_ahead = False
        my_rad = math.radians(self.angle)
        my_vec = pygame.math.Vector2(math.cos(my_rad), -math.sin(my_rad))
        
        for other in all_cars:
            if other == self: continue
            dist = self.pos.distance_to(other.pos)
            if dist < AI_AVOID_DISTANCE and dist > 0:
                to_other = (other.pos - self.pos).normalize()
                angle_diff = my_vec.angle_to(to_other)
                if abs(angle_diff) < 20: 
                    car_ahead = True
                    break
        
        # 4. Lane Logic: CENTER LINE IS PRIORITY
        target_lane = 0
        
        # ONLY Overtake if track is straight (low curvature)
        if car_ahead and curvature < 15:
            if self.overtake_timer == 0:
                if random.random() > 0.5: self.overtake_side = -220
                else: self.overtake_side = 220
                self.overtake_timer = 80 
            target_lane = self.overtake_side
            self.overtake_timer -= 1
        else:
            self.overtake_timer = 0
            target_lane = 0

        # Move lane offset
        if self.lane_offset < target_lane: self.lane_offset += AI_LANE_CHANGE_SPEED
        if self.lane_offset > target_lane: self.lane_offset -= AI_LANE_CHANGE_SPEED

        # 5. Steering Target Calculation
        p_vec = pygame.math.Vector2(self.track.points[steer_idx])
        norm = self.track.normals[steer_idx]
        
        # If off road, ignore offset and target center immediately
        if self.on_grass:
            target = p_vec
        else:
            target = p_vec + (norm * self.lane_offset)

        # 6. Apply Steering
        vec = target - self.pos
        if vec.length() != 0:
            tgt_ang = math.degrees(math.atan2(-vec.y, vec.x))
            diff = (tgt_ang - self.angle + 180) % 360 - 180
            
            turn_power = 5.0
            if self.on_grass: turn_power = 8.0
            if abs(diff) > 30: turn_power = 8.0 # Panic turn

            if abs(diff) < turn_power: self.angle += diff
            elif diff > 0: self.angle += turn_power
            else: self.angle -= turn_power
        
        # 7. Speed Control
        limit = MAX_SPEED * self.skill
        
        if self.on_grass: 
            limit = 8
        elif curvature > 45: # Sharp turn incoming
            limit *= 0.4
        elif curvature > 20:
            limit *= 0.7
        
        if self.speed < limit: self.speed += ACCEL
        else: self.speed -= FRICTION * 2.0 

        # Update spline index
        best = 9999
        start = self.spline_idx
        for i in range(50): 
            ii = (start + i) % len(self.track.points)
            d = self.pos.distance_to(pygame.math.Vector2(self.track.points[ii]))
            if d < best:
                best = d
                self.spline_idx = ii

    def physics(self, skidmarks):
        rad = math.radians(self.angle)
        dvec = pygame.math.Vector2(math.cos(rad), -math.sin(rad))
        
        grip = 0.2 if not self.on_grass else 0.05
        self.vel = self.vel.lerp(dvec * self.speed, grip)
        
        next_pos = self.pos + self.vel
        
        # --- WALL BOUNCE / PUSH BACK ---
        hit_grass = True
        try:
            ix, iy = int(next_pos.x), int(next_pos.y)
            if 0 <= ix < self.track.width and 0 <= iy < self.track.height:
                if self.track.mask.get_at((ix, iy))[0] > 50:
                    hit_grass = False
        except: pass
        
        if hit_grass:
            # GENTLE PUSH BACK TO CENTER
            center_pt = pygame.math.Vector2(self.track.points[self.spline_idx])
            to_center = (center_pt - self.pos).normalize()
            
            # Push them back onto the track
            self.pos += to_center * 12
            
            # Realign angle slightly to track direction
            fwd = pygame.math.Vector2(self.track.points[(self.spline_idx+5)%len(self.track.points)]) - center_pt
            if fwd.length() > 0:
                fwd = fwd.normalize()
                target_angle = math.degrees(math.atan2(-fwd.y, fwd.x))
                # Soft blend current angle towards correct angle
                diff = (target_angle - self.angle + 180) % 360 - 180
                self.angle += diff * 0.1 

            self.speed *= 0.90 # Slow down slightly on hit
            self.on_grass = False 
        else:
            self.on_grass = False
            self.pos = next_pos
        
        self.rect.center = self.pos
        
        # Skid marks
        if abs(self.speed) > 14 and abs(self.vel.angle_to(dvec)) > 8 and not self.on_grass:
             right_vec = pygame.math.Vector2(-dvec.y, dvec.x) 
             offset_back = dvec * -30
             
             if self.skid_type == 1:
                 tire_c = self.pos + offset_back
                 skidmarks.append([tire_c, tire_c, 150]) 
             else:
                 offset_side = right_vec * 25
                 tire_l = self.pos + offset_back - offset_side
                 tire_r = self.pos + offset_back + offset_side
                 skidmarks.append([tire_l, tire_r, 150])

    def check_cp(self):
        if self.next_cp >= len(self.track.checkpoints):
             self.next_cp = 0 
        
        cp_rect = self.track.checkpoints[self.next_cp]
        
        if self.rect.colliderect(cp_rect):
            if self.next_cp == 0:
                if not self.has_crossed_start_line:
                    self.has_crossed_start_line = True
                else:
                    self.lap += 1
                self.next_cp = 1 
            else:
                self.next_cp += 1
                if self.next_cp >= len(self.track.checkpoints):
                    self.next_cp = 0

# =================================================================================
#                                 GAME ENGINE
# =================================================================================
class Game:
    def __init__(self):
        pygame.init()
        if FULLSCREEN: self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else: self.screen = pygame.display.set_mode((1280, 720))
        self.sw, self.sh = self.screen.get_size()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        
        self.f_xl = pygame.font.SysFont("Impact", 100)
        self.f_l = pygame.font.SysFont("Arial Black", 40)
        self.f_m = pygame.font.SysFont("Arial", 28, bold=True)
        self.f_s = pygame.font.SysFont("Arial", 20, bold=True)
        
        self.state = "MENU"
        self.last_input = pygame.time.get_ticks()
        self.key_repeat_timer = 0
        
        self.laps_setting = 3
        self.ai_count_setting = 15 # Lower default due to huge cars
        self.class_options = ["MIXED", "CARS", "BIKES", "ROCKETS", "SPACESHIPS"]
        self.class_idx = 0 
        
        self.track_names = ["RANDOM"] + list(THEMES.keys())
        self.track_idx = 0
        
        self.track = None
        self.cars = []
        self.skidmarks = []
        self.cam = pygame.math.Vector2(0,0)
        
        self.demo_end_timer = 0
        self.scroll_y = 0
        self.hold_timer = 0
        
        self.demo_roster = None
        self.ai_stats = {} 
        self.theme_playlist = []

    def get_next_theme(self, specific=None):
        if specific and specific != "RANDOM":
            return specific
            
        if not self.theme_playlist:
            self.theme_playlist = list(THEMES.keys())
            random.shuffle(self.theme_playlist)
        return self.theme_playlist.pop(0)

    def draw_rainbow_text(self, text, y_pos, scale=1.0):
        cx = self.sw // 2
        total_w = sum([self.f_l.size(char)[0] for char in text]) * scale
        start_x = cx - total_w // 2
        
        time = pygame.time.get_ticks() / 200
        
        cur_x = start_x
        colors = [C_RED, (255,165,0), C_GOLD, C_GREEN, C_NEON, (100,100,255), (200,0,255)]
        
        font = self.f_xl if scale > 1.5 else self.f_l
        
        for i, char in enumerate(text):
            col = colors[(i + int(time)) % len(colors)]
            offset_y = math.sin(time + i) * 10
            
            s = font.render(char, True, col)
            self.screen.blit(s, (cur_x, y_pos + offset_y))
            cur_x += s.get_width()

    def get_text_input(self, prompt):
        txt = ""
        while True:
            self.screen.fill((20,20,40))
            t = self.f_l.render(prompt, True, C_NEON)
            self.screen.blit(t, (self.sw//2 - t.get_width()//2, 200))
            inp = self.f_xl.render(txt + "_", True, C_WHITE)
            self.screen.blit(inp, (self.sw//2 - inp.get_width()//2, 350))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT: sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN: return txt if txt else "Player"
                    if e.key == pygame.K_BACKSPACE: txt = txt[:-1]
                    elif e.unicode.isalnum() and len(txt) < 12: txt += e.unicode

    def select_car(self, name):
        if not self.assets.car_data:
            self.assets.load_vehicles(self.class_options[self.class_idx])

        idx = 0
        cols = 5
        while True:
            self.screen.fill((20,20,40))
            t = self.f_l.render(f"{name}, SELECT VEHICLE:", True, C_NEON)
            self.screen.blit(t, (self.sw//2 - t.get_width()//2, 30))
            
            row = idx // cols
            target_y = row * 140 - 200 # Adjusted for bigger cars
            if target_y < 0: target_y = 0
            self.scroll_y += (target_y - self.scroll_y) * 0.2
            
            start_x = self.sw//2 - (cols * 180)//2
            start_y = 150 - int(self.scroll_y)
            
            for i, data in enumerate(self.assets.car_data):
                img = data['img']
                c_name = data['name']
                r, c = i // cols, i % cols
                x, y = start_x + c * 180, start_y + r * 140
                if y > -100 and y < self.sh:
                    col = C_NEON if i == idx else (50,50,60)
                    pygame.draw.rect(self.screen, col, (x-10,y-10,160,110), border_radius=10)
                    
                    # Center image
                    ix = x + 80 - img.get_width()//2
                    iy = y + 55 - img.get_height()//2
                    self.screen.blit(img, (ix, iy))
                    
                    n_txt = self.f_s.render(c_name, True, C_WHITE)
                    self.screen.blit(n_txt, (x+80-n_txt.get_width()//2, y+100))
            
            pygame.display.flip()
            
            keys = pygame.key.get_pressed()
            now = pygame.time.get_ticks()
            
            moved = False
            if now - self.hold_timer > 150:
                if keys[pygame.K_RIGHT]: idx = (idx+1)%len(self.assets.car_data); moved=True
                if keys[pygame.K_LEFT]: idx = (idx-1)%len(self.assets.car_data); moved=True
                if keys[pygame.K_DOWN]: idx = (idx+cols)%len(self.assets.car_data); moved=True
                if keys[pygame.K_UP]: idx = (idx-cols)%len(self.assets.car_data); moved=True
                if moved: self.hold_timer = now

            for e in pygame.event.get():
                if e.type == pygame.QUIT: sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN: return idx
                    self.hold_timer = now - 150

    def start_race(self, mode):
        selected_class = self.class_options[self.class_idx]
        self.assets.load_vehicles(selected_class)
        
        sel_track = self.track_names[self.track_idx]
        theme = self.get_next_theme(sel_track)
        
        self.track = Track(theme) 
        
        self.cars = []
        self.skidmarks = []
        self.game_mode = mode
        
        roster = []
        
        ai_to_spawn = self.ai_count_setting
        if mode == "AI DEMO":
            ai_to_spawn = max(2, ai_to_spawn)

        if mode == "1 PLAYER":
            n = self.get_text_input("PLAYER 1 NAME")
            c = self.select_car(n)
            roster.append({'data': self.assets.car_data[c], 'ctrl': "P1"})
            
            remaining = [d for i, d in enumerate(self.assets.car_data) if i != c]
            if not remaining: remaining = [self.assets.car_data[c]]

            for i in range(ai_to_spawn):
                data = remaining[i % len(remaining)] 
                roster.append({'data': data, 'ctrl': "AI"})
            self.demo_roster = None

        elif mode == "AI DEMO":
            if self.demo_roster is None or len(self.demo_roster) != ai_to_spawn:
                self.demo_roster = []
                greg_data = next((d for d in self.assets.car_data if "Greg" in d['name']), None)
                if greg_data: self.demo_roster.append({'data': greg_data, 'ctrl': "AI"})
                
                others = [d for d in self.assets.car_data if "Greg" not in d['name']]
                if not others: others = self.assets.car_data
                random.shuffle(others)
                
                fill = ai_to_spawn - len(self.demo_roster)
                for i in range(fill):
                    d = others[i % len(others)]
                    self.demo_roster.append({'data': d, 'ctrl': "AI"})
            
            roster = self.demo_roster

        for i, r in enumerate(roster):
            self.cars.append(Car(self.track, r['data'], i, r['ctrl']))
            
        self.cd_start = pygame.time.get_ticks()
        self.state = "COUNTDOWN"
        self.demo_end_timer = 0

    def get_leader_order(self):
        return sorted(self.cars, key=lambda c: (
            c.finished, 
            -c.finish_time if c.finished else 0,
            c.lap, 
            c.next_cp, 
            -c.pos.distance_to(pygame.math.Vector2(self.track.checkpoints[c.next_cp % len(self.track.checkpoints)].center))
        ), reverse=True)

    def update_camera(self):
        sorted_cars = self.get_leader_order()
        target_car = sorted_cars[0] if sorted_cars else None
        players = [c for c in self.cars if "P" in c.control]
        
        if self.game_mode == "AI DEMO":
            if sorted_cars: target_car = sorted_cars[0]
        elif len(players) > 0:
            target_car = players[0]

        if target_car:
            tgt = target_car.pos
            self.cam.x += (tgt.x - self.sw/2 - self.cam.x) * 0.1
            self.cam.y += (tgt.y - self.sh/2 - self.cam.y) * 0.1

    def draw_hud(self):
        panel = pygame.Surface((250, 180), pygame.SRCALPHA)
        panel.fill((0,0,0,140))
        self.screen.blit(panel, (10, 10))
        
        leaders = self.get_leader_order()
        
        y = 15
        for i in range(min(3, len(leaders))):
            c = leaders[i]
            col = C_GOLD if i==0 else (C_NEON if "P" in c.control else C_WHITE)
            name_txt = c.name[:12]
            
            if self.game_mode == "AI DEMO":
                wins = self.ai_stats.get(c.name, 0)
                txt = self.f_s.render(f"{i+1}. {name_txt} ({wins})", True, col)
            else:
                txt = self.f_s.render(f"{i+1}. {name_txt}", True, col)
                
            self.screen.blit(txt, (20, y+10))
            
            info = "FIN" if c.finished else f"L{c.lap}"
            lt = self.f_s.render(info, True, col)
            self.screen.blit(lt, (180, y+10))
            y += 25
            
        lt = self.laps_setting
        lr = self.f_s.render(f"GOAL: {lt} LAPS", True, C_WHITE)
        self.screen.blit(lr, (20, 110))
        
        cls = self.class_options[self.class_idx]
        ct = self.f_s.render(f"CLASS: {cls}", True, C_RED)
        self.screen.blit(ct, (20, 135))
        
        theme_txt = self.f_m.render(f"TRACK: {self.track.theme_name}", True, C_GOLD)
        self.screen.blit(theme_txt, (self.sw - theme_txt.get_width() - 20, 20))

    def update_and_draw(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.cd_start
        can_move = False
        stage = 0
        if elapsed > 4000: can_move = True; stage = 4
        elif elapsed > 3000: stage = 3
        elif elapsed > 2000: stage = 2
        elif elapsed > 1000: stage = 1
        
        target_laps = self.laps_setting
        
        # COLLISION PHYSICS
        for _ in range(2): 
            for i, c1 in enumerate(self.cars):
                for c2 in self.cars[i+1:]:
                    if abs(c1.pos.x - c2.pos.x) > 150: continue 
                    
                    dist = c1.pos.distance_to(c2.pos)
                    if dist < CAR_RADIUS * 2:
                        if dist == 0: vec = pygame.math.Vector2(1,0)
                        else: vec = (c1.pos - c2.pos).normalize()

                        overlap = (CAR_RADIUS * 2) - dist
                        c1.pos += vec * (overlap * 0.5)
                        c2.pos -= vec * (overlap * 0.5)
                        
                        c1.rect.center = c1.pos
                        c2.rect.center = c2.pos

                        v1 = c1.vel.project(vec)
                        v2 = c2.vel.project(vec)
                        
                        c1.vel += (v2 - v1) * BUMP_FORCE
                        c2.vel += (v1 - v2) * BUMP_FORCE
                        
                        c1.angle += random.uniform(-2, 2)
                        c2.angle += random.uniform(-2, 2)

        finished_count = 0
        for c in self.cars:
            c.update(can_move, self.skidmarks, self.cars)
            if c.lap > target_laps and not c.finished: 
                c.finished = True
                c.finish_time = pygame.time.get_ticks() 
            if c.finished: finished_count += 1
            
        if self.game_mode == "AI DEMO":
            if finished_count > 0 and self.state != "GAMEOVER":
                 self.state = "GAMEOVER"
                 self.demo_end_timer = now
                 winner = self.get_leader_order()[0]
                 self.ai_stats[winner.name] = self.ai_stats.get(winner.name, 0) + 1
        else:
             humans = [c for c in self.cars if "P" in c.control]
             if len(humans) > 0:
                 humans_done = sum(1 for h in humans if h.finished)
                 if humans_done == len(humans):
                     if self.state != "GAMEOVER":
                        self.state = "GAMEOVER"
                        self.demo_end_timer = now

        self.update_camera()
        
        self.screen.fill(C_BLACK)
        cx, cy = int(self.cam.x), int(self.cam.y)
        self.screen.blit(self.track.surface, (-cx, -cy))
        
        for s in self.skidmarks[:]:
            if s[2] > 0:
                if s[0] == s[1]:
                    pygame.draw.circle(self.screen, (20,20,20,s[2]), (int(s[0].x-cx), int(s[0].y-cy)), 8)
                else:
                    pygame.draw.circle(self.screen, (20,20,20,s[2]), (int(s[0].x-cx), int(s[0].y-cy)), 6)
                    pygame.draw.circle(self.screen, (20,20,20,s[2]), (int(s[1].x-cx), int(s[1].y-cy)), 6)
                s[2] -= 3
            else: self.skidmarks.remove(s)
            
        for c in sorted(self.cars, key=lambda x: x.rect.bottom):
            self.screen.blit(c.image, (c.rect.x-cx, c.rect.y-cy))
            if "P" in c.control or self.game_mode == "AI DEMO":
                col = C_NEON if "P" in c.control else C_WHITE
                t = self.f_s.render(c.name, True, col)
                self.screen.blit(t, (c.rect.centerx-cx-t.get_width()//2, c.rect.y-cy-50))
                
        self.draw_hud()
        
        mx, my = self.sw - 220, self.sh - 220
        self.screen.blit(self.track.minimap_bg, (mx, my))
        scale = 200 / self.track.width
        for c in self.cars:
            mcx = mx + c.pos.x * scale
            mcy = my + c.pos.y * scale
            col = C_NEON if "P" in c.control else C_WHITE
            if c == self.get_leader_order()[0]: col = C_GOLD
            pygame.draw.circle(self.screen, col, (int(mcx), int(mcy)), 3)
        
        if stage < 4:
            lx, ly = self.sw//2, 150
            pygame.draw.rect(self.screen,(20,20,20),(lx-150,ly-50,300,100),border_radius=20)
            c1,c2,c3 = (50,0,0),(50,50,0),(0,50,0)
            if stage>=1: c1=(255,0,0)
            if stage>=2: c2=(255,255,0)
            if stage>=3: c3=(0,255,0)
            pygame.draw.circle(self.screen,c1,(lx-80,ly),35)
            pygame.draw.circle(self.screen,c2,(lx,ly),35)
            pygame.draw.circle(self.screen,c3,(lx+80,ly),35)
        elif stage == 4 and elapsed < 5000:
            t = self.f_xl.render("GO!!!", True, (0,255,0))
            self.screen.blit(t, (self.sw//2-t.get_width()//2, 200))

    def run(self):
        opts = [
            "1 PLAYER", 
            "AI DEMO", 
            "TRACK: ",
            "LAPS: ", 
            "AI BOTS: ", 
            "CLASS: ", 
            "CLEAR SCORES", 
            "EXIT"
        ]
        idx = 0
        
        while True:
            if self.state == "MENU":
                if pygame.time.get_ticks() - self.last_input > IDLE_TIMEOUT:
                    self.start_race("AI DEMO")
            if self.state == "GAMEOVER" and self.game_mode == "AI DEMO":
                if pygame.time.get_ticks() - self.demo_end_timer > 5000:
                    self.start_race("AI DEMO")

            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()

            for e in pygame.event.get():
                if e.type == pygame.QUIT: sys.exit()
                if e.type == pygame.KEYDOWN:
                    self.last_input = current_time 
                    if self.state == "MENU":
                        if e.key == pygame.K_UP: idx = (idx-1)%len(opts)
                        if e.key == pygame.K_DOWN: idx = (idx+1)%len(opts)
                        
                        if e.key == pygame.K_RETURN:
                            if idx == 7: sys.exit() 
                            elif idx == 6: self.ai_stats = {}
                            elif idx not in [2, 3, 4, 5]:
                                self.demo_roster = None 
                                self.start_race(opts[idx])
                    elif self.state == "GAMEOVER":
                         if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN: 
                             self.state = "MENU"; self.demo_roster = None
                    else:
                        if e.key == pygame.K_ESCAPE: self.state = "MENU"; self.demo_roster = None

            if self.state == "MENU":
                if current_time - self.key_repeat_timer > 100: 
                    changed = False
                    if idx == 2: # Track
                        if keys[pygame.K_LEFT]: self.track_idx = (self.track_idx-1)%len(self.track_names); changed=True
                        if keys[pygame.K_RIGHT]: self.track_idx = (self.track_idx+1)%len(self.track_names); changed=True
                    if idx == 3: # Laps
                        if keys[pygame.K_LEFT]: self.laps_setting = max(1, self.laps_setting-1); changed=True
                        if keys[pygame.K_RIGHT]: self.laps_setting = min(50, self.laps_setting+1); changed=True
                    if idx == 4: # Bots
                        if keys[pygame.K_LEFT]: self.ai_count_setting = max(0, self.ai_count_setting-1); changed=True
                        if keys[pygame.K_RIGHT]: self.ai_count_setting = self.ai_count_setting+1; changed=True 
                    if idx == 5: # Class
                        if keys[pygame.K_LEFT]: 
                            self.class_idx = (self.class_idx - 1) % len(self.class_options)
                            changed = True
                        if keys[pygame.K_RIGHT]: 
                            self.class_idx = (self.class_idx + 1) % len(self.class_options)
                            changed = True
                    
                    if changed:
                        self.key_repeat_timer = current_time
                        self.last_input = current_time

            if self.state == "MENU":
                self.screen.fill((15,10,25))
                
                self.draw_rainbow_text("Greg Seymour's", 60, 0.8)
                self.draw_rainbow_text("AI Racing Extreme", 110, 2.0)
                
                for i, o in enumerate(opts):
                    txt = o
                    if i == 2: txt = o + self.track_names[self.track_idx]
                    if i == 3: txt = o + str(self.laps_setting)
                    if i == 4: txt = o + str(self.ai_count_setting)
                    if i == 5: txt = o + self.class_options[self.class_idx]
                    
                    col = C_GOLD if i == idx else (100, 100, 100)
                    if i == 6 and idx == 6: col = C_RED 
                    
                    x_off = 0
                    if i == idx: x_off = math.sin(current_time/100) * 10
                    
                    surf = self.f_l.render(txt, True, col)
                    self.screen.blit(surf, (self.sw//2 - surf.get_width()//2 + x_off, 280+i*55))

            elif self.state in ["COUNTDOWN", "RACE", "GAMEOVER"]:
                self.update_and_draw()
                
                if self.state == "GAMEOVER":
                    s = pygame.Surface((self.sw,self.sh), pygame.SRCALPHA)
                    s.fill((0,0,0,180))
                    self.screen.blit(s,(0,0))
                    
                    win = self.get_leader_order()[0]
                    
                    self.draw_rainbow_text("WINNER", self.sh//2 - 100, 2.0)
                    
                    t = self.f_xl.render(f"{win.name}", True, C_GOLD)
                    self.screen.blit(t, (self.sw//2-t.get_width()//2, self.sh//2))
                    
                    if self.game_mode == "AI DEMO":
                        sub = self.f_l.render(f"Total Wins: {self.ai_stats[win.name]}", True, C_WHITE)
                        self.screen.blit(sub, (self.sw//2-sub.get_width()//2, self.sh//2 + 100))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()