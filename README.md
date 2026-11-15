# Fiery Night

A dark, animated background theme for the Claude desktop app. The sky is darker than Claude's own dark page. Orange
glows sit in the bottom corners and purple glows in the top corners. Stars twinkle, embers rise slowly and purple wisps
drift, mostly along the sides and bottom so the chat stays easy to read. Motion stops when your system asks for reduced
motion.

## Install

In Claude Code, run:

```
/plugin marketplace add KiranPothana/fiery-night
/plugin install fiery-night@fiery-night
```

Then start a new session.

## Change it

The scene is drawn by `scene/gen5.py`. Edit it, then from this folder run:

```
python3 scene/gen5.py scene/scene.svg hooks/register.tsx
```

## License

MIT
