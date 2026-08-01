# Prompt Templates

## Universal illustration

```text
Create [deliverable] featuring the exact character defined by the attached identity contract.

ROOT BODY — preserve [height impression, head-body ratio, silhouette, shoulder/ribcage/waist/pelvis relation, limbs, neutral posture].
ROOT FACE — preserve [head and face shape, eyes and brows, nose, mouth, ears, skin, age cues].
PERMANENT DETAILS — preserve [must_keep, asymmetries, species traits].
APPROVED APPEARANCE — use [selected hair state], [selected outfit state], [selected accessories/state]. Do not invent unapproved permanent changes.

ACTING — [expression, gaze, posture, hands, movement, interaction].
CAMERA — [shot, angle, lens feel, perspective, depth of field, framing].
SCENE — [location, time, weather, foreground, midground, background, props].
LIGHT/COLOR — [key direction, contrast, shadow quality, reflection/rim, palette distribution].
STYLE — [observable line, shape, rendering, material and post-process traits].
CONTINUITY — [fixed topology, light direction, prop and state constraints when series].

Avoid [root identity drift, wrong apparent age, unapproved hair/outfit, missing permanent details, anatomy/hand errors, unauthorized people, text/watermark].
```

## Local edit

```text
Edit only [authorized fields]. Preserve the root body, root face, permanent identity details, selected appearance state, camera, background and all unspecified elements exactly. Do not redesign or beautify the character.
```

## Series frame

```text
Continue from frame [previous]. Preserve identity, selected appearance, scene topology, prop count, key-light direction and time progression. Change only [action delta, expression delta, camera delta, object-state delta].
```
