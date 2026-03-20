# ============================================================
# voice_visualizer.py — Jarvis / Siri-Style Animated Orb
# ============================================================
# A Canvas-based animated widget that shows the assistant's
# current state: IDLE (gentle pulse), LISTENING (ripple waves),
# SPEAKING (dancing waveform + particles).
#
# USAGE:
#   visualizer = VoiceVisualizer(parent_frame, size=200)
#   visualizer.pack()
#   visualizer.set_state("idle")      # gentle glow
#   visualizer.set_state("listening") # expanding ripples
#   visualizer.set_state("speaking")  # waveform animation
#   visualizer.destroy_animation()    # clean up on exit
#
# HOW TO CUSTOMIZE:
#   - Change SIZE to make the orb bigger or smaller
#   - Change colors in STATE_COLORS dictionary
#   - Adjust FPS (frames per second) for smoother/lighter animation
# ============================================================

import tkinter as tk
import math
import random
import time


# ============================================================
# CONFIGURATION
# ============================================================
FPS = 30                  # Animation frames per second
DEFAULT_SIZE = 180        # Default canvas size (px)

STATE_COLORS = {
    "idle": {
        "core":   "#FF6600",   # Orange core
        "glow":   "#FF8533",   # Lighter outer glow
        "ring":   "#CC5200",   # Darker ring accent
        "bg":     "#0D0D0D",   # Background
    },
    "listening": {
        "core":   "#00CCFF",   # Cyan/blue core
        "glow":   "#00E5FF",   # Light cyan glow
        "ring":   "#0099CC",   # Darker cyan ring
        "bg":     "#0D0D0D",
    },
    "speaking": {
        "core":   "#FF6600",   # Orange core
        "glow":   "#FFAA00",   # Gold glow
        "ring":   "#FF3300",   # Red-orange ring accent
        "bg":     "#0D0D0D",
    },
}


class VoiceVisualizer(tk.Canvas):
    """
    Animated orb widget inspired by Jarvis/Siri voice assistants.

    Three visual states:
      - idle:      Gentle pulsing glow (breathe effect)
      - listening: Expanding concentric ripple rings
      - speaking:  Waveform pattern with floating particles

    All drawing uses tkinter Canvas items (ovals, arcs, lines)
    updated at ~30 FPS via root.after().
    """

    def __init__(self, parent, size: int = DEFAULT_SIZE, **kwargs):
        """
        Create the visualizer canvas.

        Args:
            parent: Tk parent widget
            size:   Width and height of the canvas (square)
        """
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("bg", "#0D0D0D")
        super().__init__(parent, width=size, height=size, **kwargs)

        self.size = size
        self.cx = size / 2          # Center X
        self.cy = size / 2          # Center Y
        self.state = "idle"         # Current animation state
        self._running = True        # Animation loop flag
        self._tick = 0              # Frame counter
        self._particles = []        # Floating particles (speaking mode)
        self._ripples = []          # Ripple ring radii  (listening mode)

        # Start the animation loop
        self._animate()

    # ============================================================
    # PUBLIC API
    # ============================================================

    def set_state(self, state: str) -> None:
        """
        Switch the visualizer to a new state.

        Args:
            state: "idle", "listening", or "speaking"
        """
        if state not in STATE_COLORS:
            return
        if state != self.state:
            self.state = state
            self._tick = 0
            self._ripples = []
            self._particles = []

    def destroy_animation(self) -> None:
        """Stop the animation loop. Call this before closing."""
        self._running = False

    # ============================================================
    # ANIMATION LOOP
    # ============================================================

    def _animate(self) -> None:
        """Main animation loop — called every frame via after()."""
        if not self._running:
            return

        self.delete("all")  # Clear canvas each frame

        if self.state == "idle":
            self._draw_idle()
        elif self.state == "listening":
            self._draw_listening()
        elif self.state == "speaking":
            self._draw_speaking()

        self._tick += 1
        self.after(1000 // FPS, self._animate)

    # ============================================================
    # IDLE STATE — Gentle pulsing glow
    # ============================================================

    def _draw_idle(self) -> None:
        """Draw a softly pulsing orb with concentric glowing rings."""
        colors = STATE_COLORS["idle"]
        t = self._tick / FPS  # Time in seconds

        # --- Outer glow rings (pulse in and out) ---
        for i in range(4):
            phase = t * 1.2 + i * 0.5
            pulse = math.sin(phase) * 0.15 + 0.85
            radius = (30 + i * 12) * pulse
            alpha_approx = max(0.08, 0.3 - i * 0.07)
            color = self._blend(colors["bg"], colors["glow"], alpha_approx)
            self._draw_circle(self.cx, self.cy, radius, fill=color, outline="")

        # --- Core orb (breathes slowly) ---
        core_pulse = math.sin(t * 1.5) * 0.12 + 0.88
        core_r = 22 * core_pulse
        self._draw_circle(self.cx, self.cy, core_r,
                          fill=colors["core"], outline=colors["glow"])

        # --- Thin rotating ring ---
        ring_r = 38 + math.sin(t * 0.8) * 4
        angle = t * 40  # degrees
        self._draw_arc_ring(self.cx, self.cy, ring_r, angle, 120,
                            outline=colors["ring"], width=1.5)
        self._draw_arc_ring(self.cx, self.cy, ring_r, angle + 180, 90,
                            outline=colors["ring"], width=1.5)

    # ============================================================
    # LISTENING STATE — Expanding ripple waves
    # ============================================================

    def _draw_listening(self) -> None:
        """Draw an orb with outward-expanding ripple rings."""
        colors = STATE_COLORS["listening"]
        t = self._tick / FPS

        # --- Spawn new ripple every ~0.6 seconds ---
        if self._tick % int(FPS * 0.6) == 0:
            self._ripples.append(0.0)  # initial radius offset

        # --- Draw ripples (expanding circles that fade out) ---
        max_radius = self.size * 0.45
        alive = []
        for r_offset in self._ripples:
            r = 20 + r_offset
            if r < max_radius:
                fade = 1.0 - (r_offset / (max_radius - 20))
                color = self._blend(colors["bg"], colors["glow"], fade * 0.5)
                self._draw_circle(self.cx, self.cy, r,
                                  fill="", outline=color, width=2)
                alive.append(r_offset + 1.8)  # grow outward
        self._ripples = alive

        # --- Pulsing core ---
        pulse = math.sin(t * 3) * 0.15 + 0.9
        core_r = 20 * pulse
        self._draw_circle(self.cx, self.cy, core_r + 6,
                          fill=self._blend(colors["bg"], colors["glow"], 0.25),
                          outline="")
        self._draw_circle(self.cx, self.cy, core_r,
                          fill=colors["core"], outline=colors["glow"])

        # --- Small reactive bumps around core ---
        num_bumps = 8
        for i in range(num_bumps):
            angle = (360 / num_bumps) * i + t * 60
            bump = math.sin(t * 5 + i) * 6 + 28
            x = self.cx + math.cos(math.radians(angle)) * bump
            y = self.cy + math.sin(math.radians(angle)) * bump
            dot_r = 2.5 + math.sin(t * 4 + i * 0.8) * 1.5
            self._draw_circle(x, y, dot_r,
                              fill=colors["glow"], outline="")

    # ============================================================
    # SPEAKING STATE — Waveform + floating particles
    # ============================================================

    def _draw_speaking(self) -> None:
        """Draw an animated waveform ring with floating particles."""
        colors = STATE_COLORS["speaking"]
        t = self._tick / FPS

        # --- Floating particles ---
        if self._tick % 3 == 0 and len(self._particles) < 25:
            angle = random.uniform(0, 360)
            dist = random.uniform(25, 55)
            self._particles.append({
                "angle": angle,
                "dist": dist,
                "speed": random.uniform(0.3, 1.0),
                "size": random.uniform(1.5, 3.5),
                "life": random.randint(20, 50),
            })

        alive = []
        for p in self._particles:
            p["life"] -= 1
            p["dist"] += p["speed"]
            p["angle"] += random.uniform(-2, 2)
            if p["life"] > 0 and p["dist"] < self.size * 0.45:
                fade = p["life"] / 50.0
                x = self.cx + math.cos(math.radians(p["angle"])) * p["dist"]
                y = self.cy + math.sin(math.radians(p["angle"])) * p["dist"]
                color = self._blend(colors["bg"], colors["glow"], min(fade, 0.8))
                self._draw_circle(x, y, p["size"], fill=color, outline="")
                alive.append(p)
        self._particles = alive

        # --- Waveform ring (audio-reactive look) ---
        num_points = 60
        wave_points = []
        for i in range(num_points + 1):
            angle_deg = (360 / num_points) * i
            angle_rad = math.radians(angle_deg)
            # Multiple sine waves for organic look
            wave = (math.sin(t * 6 + i * 0.4) * 8 +
                    math.sin(t * 9 + i * 0.7) * 5 +
                    math.sin(t * 3 + i * 0.2) * 3)
            r = 32 + wave
            x = self.cx + math.cos(angle_rad) * r
            y = self.cy + math.sin(angle_rad) * r
            wave_points.extend([x, y])

        if len(wave_points) >= 6:
            self.create_polygon(
                wave_points, fill="", outline=colors["glow"],
                width=2, smooth=True
            )

        # --- Inner glow ---
        glow_pulse = math.sin(t * 4) * 0.1 + 0.9
        glow_r = 28 * glow_pulse
        self._draw_circle(self.cx, self.cy, glow_r + 5,
                          fill=self._blend(colors["bg"], colors["ring"], 0.2),
                          outline="")

        # --- Core orb ---
        core_pulse = math.sin(t * 5) * 0.08 + 0.92
        core_r = 18 * core_pulse
        self._draw_circle(self.cx, self.cy, core_r,
                          fill=colors["core"], outline=colors["glow"])

        # --- Spinning arcs ---
        arc_r = 48 + math.sin(t * 2) * 5
        self._draw_arc_ring(self.cx, self.cy, arc_r, t * 80, 60,
                            outline=colors["ring"], width=1.5)
        self._draw_arc_ring(self.cx, self.cy, arc_r, t * 80 + 120, 45,
                            outline=colors["glow"], width=1)
        self._draw_arc_ring(self.cx, self.cy, arc_r, t * 80 + 240, 70,
                            outline=colors["ring"], width=1.5)

    # ============================================================
    # DRAWING HELPERS
    # ============================================================

    def _draw_circle(self, cx, cy, r, **kwargs) -> None:
        """Draw a circle centered at (cx, cy) with radius r."""
        self.create_oval(cx - r, cy - r, cx + r, cy + r, **kwargs)

    def _draw_arc_ring(self, cx, cy, r, start_angle, extent,
                       outline="#FF6600", width=2) -> None:
        """Draw an arc (partial ring) around a center point."""
        self.create_arc(
            cx - r, cy - r, cx + r, cy + r,
            start=start_angle, extent=extent,
            style="arc", outline=outline, width=width
        )

    @staticmethod
    def _blend(color1: str, color2: str, factor: float) -> str:
        """
        Blend two hex colors together.

        Args:
            color1: Background hex color (e.g., "#0D0D0D")
            color2: Foreground hex color (e.g., "#FF6600")
            factor: 0.0 = pure color1, 1.0 = pure color2

        Returns:
            str: Blended hex color
        """
        factor = max(0.0, min(1.0, factor))
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"
