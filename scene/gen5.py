"""Fiery Night v5: ambient only. A darker sky than Claude's own dark page, ember and violet glows in the corners,
twinkling stars, embers rising from the bottom and violet wisps drifting, spread over the whole window and
thickest along the sides and the bottom, where the chat panel does not frost them.
usage: python3 gen5.py <scene.svg> <register.tsx>"""
import random, sys, json

random.seed(23)
W, H = 1600, 900     # the scene's drawing space; it fills any window, cropped at the edges
P, T = 22, 18        # grid pitch and tile size

def edge_x():
    """An x, weighted toward the left and right sides of the window."""
    r = random.random()
    if r < .33:
        return random.uniform(0, W * .36)
    if r < .7:
        return random.uniform(W * .72, W)
    return random.uniform(0, W)

def tile(x, y, fill, op):
    return (f'<g opacity="{op}"><rect x="{x}" y="{y}" width="{T}" height="{T}" rx="3" fill="{fill}"/>'
            f'<text x="{x + T // 2}" y="{y + 13}" fill="#1a100d">{random.choice("X%$jt:;S#*+o")}</text></g>')

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">']
out.append("""<style>
text{font:700 11px ui-monospace,Menlo,monospace;text-anchor:middle}
.s text,.s{font-weight:400;font-size:13px}
.tw{animation:tw 7s steps(4) infinite}.tw2{animation:tw 11s steps(6) infinite}
@keyframes tw{0%,100%{opacity:.08}50%{opacity:.6}}
.ts{animation:ts 12s steps(6) infinite}
@keyframes ts{0%,100%{opacity:.15}50%{opacity:.7}}
.e1{animation:e1 40s steps(200) infinite}.e2{animation:e2 58s steps(290) infinite}
@keyframes e1{0%{transform:translateY(0);opacity:0}10%{opacity:.9}100%{transform:translateY(-380px);opacity:0}}
@keyframes e2{0%{transform:translate(0,0);opacity:0}10%{opacity:.8}50%{transform:translate(18px,-300px)}100%{transform:translate(-6px,-640px);opacity:0}}
.wisp{animation:wisp 20s ease-in-out infinite}
@keyframes wisp{0%,100%{transform:translate(0,0);opacity:.12}50%{transform:translate(16px,-70px);opacity:.7}}
.breath{animation:breath 15s ease-in-out infinite}
@keyframes breath{0%,100%{opacity:.75}50%{opacity:1}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>""")

# Ground: darker than Claude's page colour, an ember glow in both bottom corners, violet in both top corners.
out.append(f"""<defs>
<linearGradient id="base" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1a19"/><stop offset="1" stop-color="#121211"/></linearGradient>
<radialGradient id="emb" r="0.5"><stop offset="0" stop-color="#d97757" stop-opacity=".22"/><stop offset=".55" stop-color="#8f3f2a" stop-opacity=".07"/><stop offset="1" stop-color="#121211" stop-opacity="0"/></radialGradient>
<radialGradient id="vio" r="0.5"><stop offset="0" stop-color="#5b4a8a" stop-opacity=".2"/><stop offset=".55" stop-color="#2c2445" stop-opacity=".06"/><stop offset="1" stop-color="#121211" stop-opacity="0"/></radialGradient>
<radialGradient id="floor" cx=".5" cy="1" r=".7"><stop offset="0" stop-color="#b4553a" stop-opacity=".12"/><stop offset="1" stop-color="#121211" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#ffffff" stroke-opacity=".025"/></pattern>
</defs>
<rect width="{W}" height="{H}" fill="url(#base)"/>
<g class="breath">
<ellipse cx="0" cy="{H}" rx="760" ry="620" fill="url(#emb)"/>
<ellipse cx="{W}" cy="{H}" rx="760" ry="620" fill="url(#emb)"/>
<rect width="{W}" height="{H}" fill="url(#floor)"/>
</g>
<ellipse cx="0" cy="0" rx="720" ry="560" fill="url(#vio)"/>
<ellipse cx="{W}" cy="0" rx="720" ry="560" fill="url(#vio)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>""")

# Far stars: dim twinkling characters on the grid, everywhere, more toward the sides.
out.append('<g class="s">')
for _ in range(230):
    x = int(edge_x() // P) * P + 11
    y = random.randrange(0, H // P) * P + 15
    col = random.choice(["#e8c9a8", "#d97757", "#b9a8e0", "#f3e6d0"])
    out.append(f'<text class="{random.choice(["tw", "tw2"])}" x="{x}" y="{y}" fill="{col}" '
               f'style="animation-delay:-{random.uniform(0, 11):.2f}s">{random.choice(".:*+o`,")}</text>')
out.append("</g>")

# Small tile stars: a plus of five tiles, a few on each side and one or two across the top.
spots = [(random.uniform(30, 290), random.uniform(60, 840)) for _ in range(4)] + \
        [(random.uniform(1310, 1570), random.uniform(60, 840)) for _ in range(4)] + \
        [(random.uniform(400, 1200), random.uniform(40, 120)) for _ in range(2)]
for sx, sy in spots:
    cx, cy = int(sx // P) * P, int(sy // P) * P
    col = random.choice(["#f3e0c2", "#c9b8f0"])
    out.append(f'<g class="ts" style="animation-delay:-{random.uniform(0, 12):.2f}s">')
    for dx, dy in [(0, 0), (-P, 0), (P, 0), (0, -P), (0, P)]:
        out.append(tile(cx + dx, cy + dy, col, .85 if (dx, dy) == (0, 0) else .45))
    out.append("</g>")

# Embers rising from the bottom edge, all along it and thickest at the sides.
for _ in range(90):
    x = edge_x()
    y = random.uniform(H - 60, H + 40)
    col = random.choice(["#f6c27a", "#f39a4a", "#d9573a", "#ffe2a0", "#e8763a"])
    sz = random.choice([4, 5, 6, 8])
    out.append(f'<rect class="{random.choice(["e1", "e2"])}" style="animation-delay:-{random.uniform(0, 58):.2f}s" '
               f'x="{x:.0f}" y="{y:.0f}" width="{sz}" height="{sz}" rx="1.5" fill="{col}"/>')

# Violet wisps drifting, mostly on the sides and across the top.
for _ in range(26):
    x = edge_x()
    y = random.uniform(30, H * .75)
    out.append(f'<circle class="wisp" style="animation-delay:-{random.uniform(0, 20):.2f}s" cx="{x:.0f}" cy="{y:.0f}" '
               f'r="{random.choice([3, 4, 5])}" fill="#c9b8f0"/>')

out.append("</svg>")
svg = "".join(out)
sys.stderr.write(f"scene chars: {len(svg)}\n")
assert len(svg) < 131072, "scene too big"
open(sys.argv[1], "w").write(svg)
open(sys.argv[2], "w").write(f"""import type {{ Register, ThemeSetArgs }} from 'claude-code'

// Fiery Night: a darker sky than Claude's own dark page, with ember and violet glows, twinkling stars, rising
// embers and drifting wisps all around the window, thickest along the sides and the bottom.
// The scene is generated by scene/gen5.py; edit that, not this string.
const SCENE = {json.dumps(svg)}

const LOOK: ThemeSetArgs = {{
  backdrop: {{ scene: 'fiery-night', glass: {{ blur: 14, tint: '#1f1e1d', opacity: 0.72 }} }},
  overrideColorScheme: 'dark',
}}

export const register: Register = on => {{
  on('session.start', async ($, e, next) => {{
    await $.command.register({{
      name: 'fiery-night',
      description: 'Turn the Fiery Night theme on, or off with "/fiery-night off"',
    }})

    // A session with no app attached (a terminal run, `claude -p`) has no theme to set: skip it quietly.
    try {{
      const set = await $.theme.set(LOOK)

      if (!set.isDrawn) {{
        $.ui.status(set.reason)
      }}
    }} catch {{
      // nothing draws here
    }}

    return next(e)
  }})

  // "/fiery-night" (or "on") switches the theme on in this chat; "/fiery-night off" goes back to Claude's own look.
  on('command.run', {{ command: 'fiery-night' }}, async ($, e) => {{
    const ask = e.args.trim().toLowerCase()

    if (ask !== '' && ask !== 'on' && ask !== 'off') {{
      return {{ text: 'Type /fiery-night to turn the theme on, or /fiery-night off to turn it off.' }}
    }}

    // A chat with no app attached (a terminal run) has no theme to change.
    try {{
      if (ask === 'off') {{
        await $.theme.clear()

        return {{ text: 'Fiery Night is off. Type /fiery-night to turn it back on.' }}
      }}

      const set = await $.theme.set(LOOK)

      return {{ text: set.isDrawn ? 'Fiery Night is on.' : `Fiery Night can't show here: ${{set.reason}}` }}
    }} catch {{
      return {{ text: "Fiery Night can't show here: themes only show in the Claude app." }}
    }}
  }})

  on('ui.render', {{ component: 'Backdrop' }}, ($, e, next) => {{
    if ((e.surface !== 'desktop' && e.surface !== 'mobile') || e.props.scene !== 'fiery-night') {{
      return next(e)
    }}

    const {{ Svg }} = $.ui.resolve(e)

    return <Svg source={{SCENE}} alt="A dark sky with twinkling stars and rising embers" isInteractive />
  }})
}}
""")
