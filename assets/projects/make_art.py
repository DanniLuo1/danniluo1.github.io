#!/usr/bin/env python3
"""Hand-crafted Anthropic-style editorial illustrations (SVG).

Visual system per anthropic-art skill spec:
  1. full-bleed opaque accent background
  2. one irregular ivory #FAF9F5 carrier blob (~55-80% of canvas)
  3. naive near-black #141413 gestural linework, thick rounded uneven strokes
"""
import math
import random

INK = "#141413"
IVORY = "#FAF9F5"

W = H = 1024


def smooth_noise(seed, harmonics=3):
    rng = random.Random(seed)
    comps = [(rng.uniform(0.5, 1.0), rng.uniform(0, 2 * math.pi), rng.choice([1, 2, 3]))
             for _ in range(harmonics)]

    def f(t):
        return sum(a * math.sin(k * t + p) for a, p, k in comps) / sum(a for a, _, _ in comps)

    return f


def shaky_line(pts, amp=2.2, seg=14, seed=0):
    """Polyline path through pts with perpendicular jitter (hand-drawn shake)."""
    rng = random.Random(seed)
    out = []
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        n = max(2, int(ln / seg))
        for j in range(n + (1 if i == len(pts) - 2 else 0)):
            t = j / n
            jx = rng.uniform(-amp, amp) * math.sin(math.pi * t) if 0 < j < n else 0
            jy = rng.uniform(-amp, amp) * math.sin(math.pi * t) if 0 < j < n else 0
            out.append((x0 + dx * t + nx * jx, y0 + dy * t + ny * jy))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in out)


def wobbly_shape(cx, cy, rx, ry, rot=0.0, irr=0.06, n=48, seed=0, fill=None, stroke=INK, sw=12):
    """Closed wobbly ellipse-ish shape; returns svg element string."""
    noise = smooth_noise(seed)
    rng = random.Random(seed + 999)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        rmod = 1 + irr * noise(t) + rng.uniform(-0.008, 0.008)
        x = rx * rmod * math.cos(t)
        y = ry * rmod * math.sin(t)
        xr = x * math.cos(rot) - y * math.sin(rot) + cx
        yr = x * math.sin(rot) + y * math.cos(rot) + cy
        pts.append((xr, yr))
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    if fill:
        return f'<path d="{d}" fill="{fill}" stroke="none"/>'
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'


def line_el(pts, sw=12, amp=2.2, seed=0, color=INK):
    d = shaky_line(pts, amp=amp, seed=seed)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'


def dot(cx, cy, r, color=INK):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'


def cubic(p0, p1, p2, p3, n=26):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def rot(px, py, cx, cy, deg):
    a = math.radians(deg)
    dx, dy = px - cx, py - cy
    return (cx + dx * math.cos(a) - dy * math.sin(a),
            cy + dx * math.sin(a) + dy * math.cos(a))


def blob(cx, cy, r, seed):
    return wobbly_shape(cx, cy, r, r * 0.94, rot=0.3, irr=0.10, n=56, seed=seed, fill=IVORY)


def svg_doc(bg, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>'
            f'{body}</svg>')


# ---------------------------------------------------------------- health card
def health():
    bg = "#EBCECE"  # coral: care
    el = [blob(512, 508, 348, seed=11)]

    # blueprint sheet: wobbly rect, rotated -6 deg
    scx, scy, ang = 530, 430, -6
    hw, hh = 205, 158
    corners = [rot(scx - hw, scy - hh, scx, scy, ang), rot(scx + hw, scy - hh, scx, scy, ang),
               rot(scx + hw, scy + hh, scx, scy, ang), rot(scx - hw, scy + hh, scx, scy, ang)]
    el.append(line_el(corners + [corners[0]], sw=13, amp=2.6, seed=21))

    # rolled top-right corner: small spiral
    cx0, cy0 = corners[1]
    spiral = []
    for i in range(40):
        t = 3.2 * math.pi * i / 39
        r = 30 * (1 - i / 60)
        spiral.append((cx0 - 6 + r * math.cos(t + 2.6), cy0 + 4 + r * math.sin(t + 2.6)))
    el.append(line_el(spiral, sw=9, amp=1.2, seed=22))

    # faint blueprint guide lines
    for k, yy in enumerate((-70, 70)):
        p0 = rot(scx - hw + 34, scy + yy, scx, scy, ang)
        p1 = rot(scx + hw - 34, scy + yy, scx, scy, ang)
        el.append(line_el([p0, p1], sw=6, amp=1.8, seed=23 + k))

    # ECG pulse across the sheet
    base = scy + 6
    raw = [(-hw + 30, 0), (-74, 0), (-56, -26), (-38, 0), (-18, 0), (2, -92),
           (22, 58), (40, 0), (66, 0), (84, -20), (100, 0), (hw - 30, 0)]
    pts = [rot(scx + dx, base + dy, scx, scy, ang) for dx, dy in raw]
    el.append(line_el(pts, sw=13, amp=1.6, seed=30))
    peak = rot(scx + 2, base - 92, scx, scy, ang)
    el.append(dot(peak[0], peak[1] - 26, 14))

    # naive heart outline, lower left, tilted -8 deg (health signal)
    hcx, hcy, hang = 318, 738, -8
    heart = []
    segs = [
        ((0, 42), (-10, 18), (-56, 2), (-58, -26)),
        ((-58, -26), (-60, -52), (-30, -62), (-12, -44)),
        ((-12, -44), (-4, -36), (0, -28), (0, -20)),
        ((0, -20), (0, -28), (4, -36), (12, -44)),
        ((12, -44), (30, -62), (60, -52), (58, -26)),
        ((58, -26), (56, 2), (10, 18), (0, 42)),
    ]
    for p0, p1, p2, p3 in segs:
        heart += cubic(p0, p1, p2, p3)[:-1]
    heart = [rot(hcx + x * 1.15, hcy + y * 1.15, hcx, hcy, hang) for x, y in heart]
    el.append(line_el(heart + [heart[0]], sw=13, amp=2.4, seed=41))
    # tiny pulse tick inside the heart
    tick = [(-26, 2), (-10, 2), (-2, -14), (8, 12), (16, 2), (28, 2)]
    tick = [rot(hcx + x * 1.15, hcy + y * 1.15, hcx, hcy, hang) for x, y in tick]
    el.append(line_el(tick, sw=9, amp=1.4, seed=42))

    el.append(dot(770, 690, 11))
    el.append(dot(806, 732, 8))
    return svg_doc(bg, "".join(el))


# ------------------------------------------------------------ job market card
def jobmarket():
    bg = "#CBCADB"  # heather: research
    el = [blob(500, 510, 348, seed=77)]

    # bar chart: baseline + 4 uneven wobbly bars (kept low so the lens frames them)
    base_y = 700
    el.append(line_el([(292, base_y + 6), (716, base_y - 4)], sw=12, amp=2.4, seed=61))
    bars = [(330, 132), (418, 188), (596, 154), (678, 108)]
    for k, (bx, bh) in enumerate(bars):
        top = base_y - bh
        el.append(line_el([(bx, base_y), (bx - 3, top), (bx + 54, top - 4), (bx + 56, base_y)],
                          sw=11, amp=2.0, seed=62 + k))

    # highlighted tall bar at the center, framed by the lens
    el.append(line_el([(500, base_y), (497, 392), (555, 388), (558, base_y)], sw=12, amp=2.0, seed=80))
    el.append(dot(526, 352, 15))

    # magnifying glass over the central bar
    mcx, mcy, mr = 540, 440, 208
    el.append(wobbly_shape(mcx, mcy, mr, mr, irr=0.035, n=64, seed=71, sw=17))
    # handle, down-right, spilling past the blob edge
    hx0, hy0 = mcx + mr * 0.70, mcy + mr * 0.70
    el.append(line_el([(hx0, hy0), (hx0 + 130, hy0 + 134)], sw=26, amp=2.6, seed=73))

    # scattered data dots
    for k, (dx, dy, r) in enumerate([(326, 330, 9), (382, 268, 7), (694, 316, 10),
                                     (730, 392, 7), (310, 470, 8), (706, 506, 8)]):
        el.append(dot(dx, dy, r))
    return svg_doc(bg, "".join(el))


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/logos"
    open(f"{out}/art_health.svg", "w").write(health())
    open(f"{out}/art_jobmarket.svg", "w").write(jobmarket())
    print("written")
