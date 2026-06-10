---
version: alpha
name: MonMS Default
description: Canonical bare scaffold — clean operator-friendly UI with indigo accents
colors:
  primary: "#4f46e5"
  primary-hover: "#4338ca"
  on-primary: "#ffffff"
  background: "#f8fafc"
  surface: "#ffffff"
  text: "#0f172a"
  text-muted: "#475569"
  text-subtle: "#94a3b8"
  border: "#e2e8f0"
  border-hover: "#cbd5e1"
  focus: "#4f46e5"
  success: "#22c55e"
  error-bg: "#fef2f2"
  error-border: "#fecaca"
  error-text: "#991b1b"
  link-on-primary: "#c7d2fe"
typography:
  h1:
    fontFamily: system-ui
    fontSize: 1.5rem
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: system-ui
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: system-ui
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: system-ui
    fontSize: 0.875rem
    fontWeight: 600
    lineHeight: 1.4
  code:
    fontFamily: ui-monospace
    fontSize: 0.875rem
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 8px 16px
    typography: "{typography.label}"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 8px 16px
    typography: "{typography.label}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: 24px
  editor-badge:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    padding: 8px 16px
---

## Overview

MonMS Default is the canonical bare scaffold — a clean, operator-friendly starting point for agent-shaped sites. The aesthetic is utilitarian and calm: light slate backgrounds, crisp white surfaces, and a single indigo accent for actions and focus states.

This template ships Tailwind CSS via CDN for layout utilities and `assets/main.css` for component styles. Agents extending this scaffold should preserve the focus-visible rings, sticky header behavior, and the live-editor badge so inline HTMX editing remains discoverable.

## Colors

The palette is rooted in Tailwind slate neutrals with one indigo accent.

- **Primary (#4f46e5):** Indigo — CTAs, editor badge, focus rings, link hovers.
- **Primary hover (#4338ca):** Darker indigo for button hover states.
- **Background (#f8fafc):** Slate-50 page canvas (`bg-slate-50` in base layout).
- **Surface (#ffffff):** Cards, header, mobile nav — elevated white panels.
- **Text (#0f172a):** Slate-900 headlines and primary copy.
- **Text muted (#475569):** Body text, nav links, secondary content.
- **Border (#e2e8f0):** Dividers, card outlines, secondary button borders.
- **Success (#22c55e):** Live-editor status dot.
- **Error (#fef2f2 / #991b1b):** Save-error toast background and text.

## Typography

System UI stack throughout — no custom web fonts. Hierarchy is weight and size, not display typefaces.

- **H1 (1.5rem / 600):** Hero titles, error page headings.
- **Body (1rem / 400):** Hero body copy, error messages.
- **Label (0.875rem / 600):** Buttons, nav links, editor badge.
- **Code (0.875rem / monospace):** Inline code in cards.

## Layout

- **Max content width:** 72rem (`max-w-6xl`) centered with horizontal padding.
- **Header height:** 64px sticky top bar with bottom border.
- **Hero spacing:** 48px top, 32px bottom padding.
- **Action gaps:** 12px between hero buttons; 8–16px component padding scale.

## Elevation & Depth

Subtle elevation only — no heavy shadows.

- Cards use `0 1px 2px rgba(15, 23, 42, 0.04)` and a 1px border.
- Editor badge uses `0 10px 15px -3px rgba(15, 23, 42, 0.1)`.
- Save-error toast uses `0 4px 12px rgba(15, 23, 42, 0.12)`.

## Shapes

- **Buttons:** 8px radius (`rounded.md`).
- **Cards:** 12px radius (`rounded.lg`).
- **Editor badge:** Full pill (`rounded.full`).
- **Focus rings:** 2px solid primary with 2px offset on interactive elements.

## Components

- **Button primary:** Indigo fill, white label, 8px radius. Hover darkens to primary-hover.
- **Button secondary:** White fill, slate border, dark text. Hover lightens background.
- **Card:** White panel with border and light shadow; code blocks use slate-100 background.
- **Editor badge:** Fixed top-right pill when logged in; green pulsing dot (respects `prefers-reduced-motion`).
- **Hero editable fields:** Text cursor; focus ring matches primary color for inline HTMX editing.

## Do's and Don'ts

**Do**

- Keep indigo as the sole accent — one driver for interaction.
- Preserve focus-visible outlines on editable hero fields and buttons.
- Use system fonts; avoid adding committed font binaries (R2).
- Align new CSS values with tokens in this file.

**Don't**

- Introduce additional accent colors without updating DESIGN.md tokens.
- Remove the editor badge or save-error toast — they signal live-edit mode.
- Commit custom web fonts or heavy decorative typography.
