# Polaris Grids Design Tokens
> Extracted from https://www.polarisgrids.com — use this as the style reference for dashboard builds.

---

## Fonts

### @font-face (Custom)
| Name | Weight | File |
|------|--------|------|
| `Satoshi-Black` | 800 | `Satoshi-Black.woff` |
| `Satoshi-Bold` | 700 | `Satoshi-Bold.woff` |
| `Satoshi-Medium` | 600 | `Satoshi-Medium.woff` |

### Font Stack
```css
font-family: 'Satoshi-Bold', 'Arial', sans-serif;
```
Fallbacks: `Arial`, `sans-serif` | Decorative/blockquote: `Georgia, serif`

### Font Sizes
```
10px  12px  13px  14px  15px  16px  18px  20px
22px  24px  26px  28px  30px  32px  34px  40px  44px  45px
```

### Font Weights
| Token | Value | Usage |
|-------|-------|-------|
| Light | 300 | Subtle labels |
| Normal | 400 | Body text |
| Medium | 500 | Secondary emphasis |
| Bold | 700 | Headings, CTAs |
| Black | 800 | Hero headings |
| Extra Bold | 900 | Special display |

### Line Heights
```
130%  140%  150%  160%  165%  170%  180%
12px  20px  21px  24px  normal
```

---

## Heading Styles

| Tag | Font | Size | Color | Letter Spacing |
|-----|------|------|-------|----------------|
| `h1` | Satoshi-Black | 40–45px | `#0a3690` | `-0.44px` |
| `h2` | Satoshi-Black | 28–34px | `#0a3690` | `-0.14px` to `-0.374px` |
| `h3` | Satoshi-Black / Bold | 18–28px | `#0a3690` or `#1645a4` | — |
| `h4` | Satoshi-Bold | 16–26px | `#0a3690` or `#1645a4` | — |
| `h5` | Satoshi-Black | 26px | `#0a3690` | `1.56px` |
| `h6` | inherits body | — | — | — |

---

## Color Palette

### CSS Custom Properties
```css
--Primary-blue:   #1645a4
--Brand-grey:     #464e5f
--Link-text:      #3959ff
--White:          #ffffff
--blue-900:       #0a3690
--blue-800:       #1645a4
--blue-750:       #1b469e
```

### Extended Palette
| Role | Hex | Usage |
|------|-----|-------|
| Primary Dark | `#0a3690` | Headings, nav, primary bg |
| Primary | `#1645a4` | Buttons, links |
| Primary Mid | `#144bbd` | Hover states |
| Link / CTA | `#3959ff` | Interactive elements |
| Accent Blue | `#37aafe` | Gradient start |
| Accent Teal | `#02c9a8` | Gradient accent, highlights |
| Accent Cyan | `#11abbe` | Gradient end |
| Accent Purple | `#6573f2` | Icon gradients |
| Light Purple | `#b5bfff` | Icon gradient end |
| Lavender | `#abc7ff` | Gradient highlight |
| Body Text | `#464e5f` | Paragraph / label text |
| Muted Blue | `#384c77` | Secondary text |
| Soft Blue | `#6c86bc` | Tertiary / disabled text |
| Background Light | `#f7fafc` | Page/section backgrounds |
| Background Blue | `#ebf4fb` | Card backgrounds |
| Background Dark | `#032c7e` | Dark section backgrounds |
| White | `#ffffff` | Text on dark, cards |

---

## Gradients

```css
/* Primary brand gradient */
--Primary-gradient: linear-gradient(238deg, #02c9a8 35.6%, #abc7ff 92.64%);

/* CTA / button gradient */
--dddd: linear-gradient(234deg, #37aafe 16.59%, #3c63ff 47.03%, #11abbe 79.53%);

/* Icon gradient purple */
--icon-gradient-purple: linear-gradient(0deg, #6573f2 0%, #b5bfff 100%);

/* Dark overlay (hero images) */
linear-gradient(0deg, rgba(15,27,45,0.13) 50%, rgba(15,27,45,1) 100%);
```

---

## Buttons

### Primary Button `.button__primary`
```css
background-color: #0a3690;
color: #ffffff;
height: 42px;
border-radius: 25px;           /* pill shape */
box-shadow: 0px 8.75px 26.24px -1.94px rgba(60, 99, 255, 0.4);
font-family: 'Satoshi-Bold';
font-weight: 700;
```

### Secondary Button `.btn-down`
```css
background: rgba(255, 255, 255, 0.4);
border: 1px solid #02c9a8;    /* teal border */
border-radius: 25px;
box-shadow: subtle rgba shadow;
```

---

## Border Radius
```
4px    — inputs, small chips
6px    — tags, badges
10px   — cards, panels
12px   — modals, large cards
25px   — buttons (pill)
50%    — avatars, circular icons
```

---

## Shadows / Elevation

```css
/* Card / component shadow */
box-shadow: 0px 9.5px 28.51px -11.4px rgba(96, 173, 245, 0.3);

/* Button hover shadow */
box-shadow: 0px 8.75px 26.24px -1.94px rgba(60, 99, 255, 0.4);
```

---

## Spacing Scale
```
Padding:  0 → 180px  (common: 16px, 24px, 32px, 48px, 64px, 80px, 120px, 160px, 180px)
Margin:   0 → 200px  (common: 8px, 16px, 24px, 32px, 48px, 80px, 120px, 200px)
```

---

## Filters / Effects
```css
backdrop-filter: blur(5.5px);   /* nav / glass cards */
backdrop-filter: blur(150px);   /* background blobs */
filter: grayscale(1);           /* partner logos (hover removes) */
opacity: 0 → 1;
```

---

## Quick Reference — Dashboard Color Map

| Element | Value |
|---------|-------|
| Page background | `#f7fafc` |
| Card background | `#ffffff` |
| Card alt background | `#ebf4fb` |
| Dark section bg | `#032c7e` |
| Primary heading | `#0a3690` |
| Body text | `#464e5f` |
| Muted / secondary text | `#6c86bc` |
| Primary action / link | `#3959ff` |
| Accent / success | `#02c9a8` |
| Border / divider | `rgba(96, 173, 245, 0.3)` |
| Nav background | `#0a3690` |
| Nav text | `#ffffff` |
