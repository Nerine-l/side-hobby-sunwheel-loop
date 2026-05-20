import math
import random

import pygame

W, H = 800, 450
FPS = 60
LOOP_SEC = 8.0
TAU = math.tau

random.seed(8)


def clamp(value, lo=0, hi=255):
    return max(lo, min(hi, int(value)))


def lerp(a, b, t):
    return a + (b - a) * t


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def mix_color(a, b, t):
    return tuple(clamp(lerp(a[i], b[i], t)) for i in range(3))


def palette_at(t01):
    """朝焼け、昼の淡さ、夕焼け、薄暮を8秒で一周する色セット。"""
    stops = [
        (0.00, (23, 27, 61), (247, 141, 98), (255, 220, 145), (67, 70, 115)),
        (0.18, (93, 150, 204), (255, 198, 125), (255, 242, 188), (102, 132, 172)),
        (0.48, (86, 176, 219), (181, 224, 242), (255, 249, 204), (104, 158, 183)),
        (0.70, (246, 132, 93), (122, 76, 142), (255, 181, 86), (94, 83, 125)),
        (0.88, (39, 34, 91), (239, 101, 87), (255, 126, 73), (45, 45, 87)),
        (1.00, (23, 27, 61), (247, 141, 98), (255, 220, 145), (67, 70, 115)),
    ]

    for i in range(len(stops) - 1):
        t0, top0, bottom0, sun0, water0 = stops[i]
        t1, top1, bottom1, sun1, water1 = stops[i + 1]
        if t0 <= t01 <= t1:
            k = smoothstep((t01 - t0) / (t1 - t0))
            return {
                "top": mix_color(top0, top1, k),
                "bottom": mix_color(bottom0, bottom1, k),
                "sun": mix_color(sun0, sun1, k),
                "water": mix_color(water0, water1, k),
            }

    _, top, bottom, sun, water = stops[0]
    return {"top": top, "bottom": bottom, "sun": sun, "water": water}


def draw_soft_circle(surface, center, radius, color, layers=7):
    glow = pygame.Surface((W, H), pygame.SRCALPHA)
    for i in range(layers, 0, -1):
        k = i / layers
        alpha = int(10 + 30 * (1.0 - k))
        pygame.draw.circle(glow, (*color, alpha), center, int(radius * (1.0 + k * 1.9)))
    surface.blit(glow, (0, 0))
    pygame.draw.circle(surface, color, center, radius)


def sun_pos(t01):
    sx = int(W * (0.10 + 0.80 * t01))
    arc = math.sin(TAU * (0.08 + 0.74 * t01))
    sy = int(H * 0.70 - arc * H * 0.42)
    return sx, sy


def draw_background(surface, t01):
    palette = palette_at(t01)
    bands = 74

    for i in range(bands):
        k = i / (bands - 1)
        wave = 0.025 * math.sin(TAU * (t01 + k * 0.65))
        color = mix_color(palette["top"], palette["bottom"], smoothstep(k + wave))
        y = int(H * i / bands)
        pygame.draw.rect(surface, color, (0, y, W, math.ceil(H / bands) + 1))

    sx, sy = sun_pos(t01)
    draw_soft_circle(surface, (sx, sy), 31, palette["sun"])

    horizon_y = int(H * 0.74)
    pygame.draw.rect(surface, palette["water"], (0, horizon_y, W, H - horizon_y))

    for i in range(18):
        y = horizon_y + i * 7
        line_color = mix_color(palette["water"], palette["bottom"], 0.25 + i / 26)
        pygame.draw.line(surface, line_color, (0, y), (W, y), 1)

    reflection_width = int(180 + 70 * math.sin(TAU * t01) ** 2)
    for i in range(15):
        k = i / 14
        y = horizon_y + 12 + i * 6
        half = int(reflection_width * (1.0 - k) * 0.5)
        jitter = int(18 * math.sin(TAU * (t01 + k * 0.9)))
        start = max(0, sx - half + jitter)
        end = min(W, sx + half + jitter)
        pygame.draw.line(surface, mix_color(palette["sun"], palette["water"], k), (start, y), (end, y), 2)


def lissajous_pos(t01):
    t = TAU * t01
    x = math.sin(3 * t + math.pi / 2)
    y = math.sin(2 * t)
    amp = min(W, H) * 0.32
    return int(W // 2 + amp * x), int(H // 2 + amp * y)


def draw_lissajous_trail(surface, t01, accent):
    for i in range(58):
        age = i / 58
        p = (t01 - age * 0.34) % 1.0
        x, y = lissajous_pos(p)
        radius = max(2, int(14 * (1.0 - age) + 2))
        color = mix_color(accent, (255, 251, 231), 0.25 + 0.45 * (1.0 - age))
        pygame.draw.circle(surface, color, (x, y), radius, 1)


def make_particles(count):
    particles = []
    for i in range(count):
        particles.append(
            {
                "phase": i / count,
                "size": random.randint(2, 8),
                "drift": random.uniform(-0.07, 0.07),
                "warmth": random.uniform(0.0, 1.0),
            }
        )
    return particles


def draw_orbit_particles(surface, particles, t01, palette):
    center = (W // 2, H // 2)
    ring_color = mix_color(palette["sun"], (255, 247, 220), 0.35)

    for i in range(4):
        radius = int(min(W, H) * (0.215 + i * 0.015))
        pygame.draw.circle(surface, mix_color(ring_color, palette["top"], i / 5), center, radius, 1)

    for particle in particles:
        ph = (particle["phase"] + t01) % 1.0
        angle = TAU * ph
        orbit = min(W, H) * 0.22 + 30 * math.sin(TAU * (t01 + particle["phase"]))
        x = int(center[0] + orbit * math.cos(angle + particle["drift"]))
        y = int(center[1] + orbit * math.sin(angle))

        pulse = 0.5 + 0.5 * math.sin(TAU * (ph * 2.0 + t01))
        size = max(2, int(particle["size"] + 2 * pulse))
        color = mix_color(palette["sun"], (206, 232, 255), particle["warmth"] * 0.55)
        pygame.draw.circle(surface, color, (x, y), size, 1)


def draw_main_orb(surface, t01, palette):
    x, y = lissajous_pos(t01)
    pulse = 0.5 + 0.5 * math.sin(TAU * t01)
    radius = int(17 + 10 * pulse)
    color = mix_color(palette["sun"], (255, 255, 245), 0.28)
    draw_soft_circle(surface, (x, y), radius, color, layers=5)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("side-hobby-sunwheel-loop")
    clock = pygame.time.Clock()
    particles = make_particles(140)
    time_sec = 0.0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        time_sec += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t01 = (time_sec % LOOP_SEC) / LOOP_SEC
        palette = palette_at(t01)

        draw_background(screen, t01)
        draw_lissajous_trail(screen, t01, palette["sun"])
        draw_orbit_particles(screen, particles, t01, palette)
        draw_main_orb(screen, t01, palette)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
