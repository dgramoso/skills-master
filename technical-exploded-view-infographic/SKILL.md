---
name: technical-exploded-view-infographic
description: Generate a precise engineering-style image prompt for a square exploded-view technical infographic of any mechanical, electronic, architectural, or engineering object. Use when the user wants to create, refine, or standardize an image prompt where the only editable variable is an object name.
---

# Technical Exploded View Infographic Skill

Use this skill when the user asks to generate or adapt a prompt for an engineering-style exploded-view infographic of an object.

The workflow has one editable input:

```text
[OBJECT]
```

Replace `[OBJECT]` with a mechanical, electronic, architectural, aerospace, nautical, musical, optical, or engineering object, for example:

- analog camera
- rocket engine
- aircraft turbine
- mechanical watch
- electric guitar
- submarine
- reflex camera
- suspension bridge
- telescope
- industrial robot arm

Do not introduce additional user-editable variables unless the user explicitly asks for them.

## Goal

Produce a high-density, square, print-ready technical illustration prompt that asks the image model to create:

- a central exploded-view diagram;
- an auxiliary clean cross-section;
- three detailed close-up insets;
- a technical specification panel;
- precise annotations and engineering-style typography;
- a strict four-element color palette;
- no decorative, photorealistic, cinematic, social-media, or commercial-render styling.

## Required reasoning before writing the final prompt

Before producing the prompt, derive the following from `[OBJECT]`:

1. **Main components**  
   Identify 8 to 14 relevant parts, assemblies, or subsystems. These become the exploded-view nodes.

2. **Key mechanism**  
   Identify the internal mechanism, structural principle, optical path, fluid path, electronic flow, drivetrain, load path, or movement that justifies the cross-section.

3. **Three close-up details**  
   Select the three densest or most informative engineering areas.

4. **Numerical specifications**  
   Include plausible, verifiable-style dimensions, materials, performance data, tolerances, capacities, manufacturing data, or historical data.  
   If exact values are uncertain, use typical ranges and phrase them as typical, canonical, or representative values. Do not invent fake certainty.

5. **Best explosion axis**  
   Choose the axis that reveals the most assembly logic:
   - axial;
   - lateral;
   - diagonal;
   - vertical stack;
   - radial;
   - diagonal ascending from bottom-left to top-right.

Use object-specific choices. For example, a camera may use optical-axis explosion; a turbine may use axial explosion; a bridge may use structural layers; a guitar may use body-to-neck/pickup/electronics assembly.

## Output format

Return a single production-ready prompt in Spanish unless the user asks for another language.

Use these sections:

1. `PROMPT FINAL`
2. `PROMPT NEGATIVO`
3. `NOTAS DE CONTROL DE CALIDAD`

Do not include long commentary before the prompt. Keep the output directly usable.

## Prompt construction rules

### Variable

State that there is only one editable element: the object.

```text
Objeto: [resolved object]
```

### Automatic object analysis

Include a concise technical derivation inside the prompt:

- components list;
- key mechanism;
- close-up details;
- numerical specs;
- optimal explosion axis.

### Canvas and layout

Always specify:

- square 1:1 composition;
- pure white background `#FFFFFF`;
- subtle graph-paper overlay across the whole image;
- grid lines in gray at 6–8% opacity;
- central exploded view occupying about 55%;
- right technical specification panel occupying about 20%;
- auxiliary views occupying about 15%;
- distributed annotation area.

### Central exploded view

Always specify:

- isometric or axonometric perspective at 30° or 45°;
- no photorealistic vanishing-point perspective;
- components separated along the chosen assembly axis;
- relative position preserved;
- proportional spacing;
- dotted assembly guide lines;
- clear outer and inner line weights;
- grayscale technical shading;
- no material textures;
- 3 to 5 accent uses only.

### Accent color

Choose exactly one:

- amber electric `#F5A623` for mechanical, warm, historical, analog, combustion, wood, or metalcraft objects;
- technical cyan `#00B4D8` for electronic, optical, aerospace, digital, scientific, or high-tech objects.

Use the accent only in 3 to 5 elements in the whole image. Never use it as a background or body text color.

### Cross-section

Always include:

- one clean straight-cut section;
- label such as `SECCIÓN A–A`;
- standard 45° hatching;
- internal critical mechanism visible;
- accent color only on the most critical internal component.

### Close-up details

Always include three insets:

- `DETALLE 1`;
- `DETALLE 2`;
- `DETALLE 3`.

Each inset must have:

- thin rectangular border;
- zoom factor 2x to 4x;
- connector line to source area;
- dotted source rectangle on main exploded view.

### Annotations

Always require:

- straight hairline callouts;
- no curved lines;
- no crossing callout lines;
- terminal dot over the component;
- labels aligned in two vertical columns;
- two typographic levels:
  - component name in geometric sans-serif bold uppercase;
  - technical note/material in monospace regular.

### Specification panel

Always include a right-side panel with:

- vertical left border in the accent color;
- header `ESPECIFICACIONES`;
- subsections:
  - `DIMENSIONES`;
  - `MATERIALES`;
  - `DATOS TÉCNICOS`;
  - `FECHA / ORIGEN`.

Use monospace typography for numeric values and technical data.

### Typography

Use only two font classes:

- monospace: IBM Plex Mono, Courier, Space Mono, or equivalent;
- geometric sans-serif: Futura, DIN, Aktiv Grotesk, or equivalent.

Forbid:

- serif fonts;
- decorative fonts;
- slogans;
- titles;
- illegible microtext;
- body text that is not technical.

### Color palette

Require exactly four elements:

1. pure white `#FFFFFF`;
2. technical black `#1A1A1A`;
3. engineering gray `#888888`;
4. one accent color: `#F5A623` or `#00B4D8`.

### Lighting

Use engineering-illustration lighting:

- light from upper-left;
- two-tone grayscale shadows;
- very subtle projected shadows at about 8% opacity;
- no specular highlights;
- no cinematic shadows;
- no photorealistic lighting.

### Style references

Use this style direction:

```text
Haynes Manual technical illustrations × Scientific American cutaway diagrams × NASA aerospace engineering blueprints × 1970s Larousse technical encyclopedia plates × Monocle-style editorial engineering layout.
```

### Technical image requirements

Always include:

- 4K;
- 300 DPI;
- print-ready;
- all text legible;
- object recognizable at first glance;
- every component has at least one visible edge;
- no watermark;
- no screen frame;
- no elements outside the infographic.

## Negative prompt

Always include a negative prompt that rejects:

- colored background;
- gray background;
- gradients;
- photorealistic lighting;
- photographic material textures;
- decorative typography;
- serif typography;
- title or slogan;
- curved or crossed annotation lines;
- more than one accent color;
- commercial 3D render style;
- videogame render style;
- floating parts without visible assembly axis;
- exploded diagram without guide lines;
- dramatic cinematic shadows;
- low component density;
- social-media infographic look;
- illegible text;
- fake pseudo-technical labels.

## Quality control checklist

After the negative prompt, include a compact checklist confirming:

- one object variable only;
- 8 to 14 components;
- one accent color only;
- square 1:1;
- white background;
- graph-paper overlay;
- exploded view + cross-section + three insets + spec panel;
- no crossed annotations;
- print-ready technical style.

## Example user request

```text
Crear prompt para [OBJECT] = una cámara analógica.
```

## Example output skeleton

```markdown
## PROMPT FINAL

Objeto: una cámara analógica.

Generar una ilustración técnica infográfica...
[full prompt here]

## PROMPT NEGATIVO

Fondo de color, fondo gris, gradientes...

## NOTAS DE CONTROL DE CALIDAD

- Variable única: objeto.
- Componentes principales: 8–14.
...
```
