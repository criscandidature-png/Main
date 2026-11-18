# 09 — Template pronti (richieste a Claude e blocchi riutilizzabili)

I testi tra virgolette sono richieste reali di Kaye o ricostruzioni fedeli del suo metodo. I blocchi in inglese sono pensati per essere incollati nei generatori. Adatta i [campi].

> Nota: Kaye condivide i suoi prompt esatti, il "camera block" e la sua skill personale di prompt (e "Fight Engine") in guide gratuite su Notion/Higgsfield linkate nelle descrizioni (vedi `13-indice-video.md`). I blocchi qui sotto sono ricostruiti dalle sue spiegazioni, non copiati da quelle guide.

---
## 1. Director's brief (primo messaggio di ogni progetto)
```
I'm making a [durata] [tipo: short film / spec commercial for BRAND / music video / reel] for [piattaforma, aspect ratio].
STORY (plain language): [racconta la storia come a un'amica: inizio, svolta, finale, cosa deve provare lo spettatore]
CHARACTERS: [nome — chi è, età, look; allego selfie/riferimenti 1..n]
LOCATIONS: [luoghi; allego riferimenti]
PROPS / PRODUCT: [oggetti chiave]
SCENES I IMAGINE: [lista grezza delle scene, cosa fa la camera se ho un'idea]
DIALOGUE / VOICE-OVER: [battute o script]
Please give me ONE organized file with: scene-by-scene script (acts + finale), list of all assets with file names, a prompt for every character sheet, location sheet and prop sheet, and a video prompt for every scene that tags assets by file name.
```

## 2. Character sheet
Richiesta a Claude:
```
Write me a three-panel character sheet prompt of the [girl/guy] in my selfie: full body front, front portrait close-up, and side profile. Keep my exact face, skin tone, and hair from the selfie, but put me in the outfit from the reference image. Clean white studio background, photorealistic. Crop both full-body panels at the neck so the face appears only in the sharp close-up panel. Spend most of the detail on realistic skin: [undertone, freckles, birthmarks, pores]. Include precise numbers (age, height, build). Add positive constraints and a negative list (no plastic skin, no extra elements, no background props).
```
Blocco base (da adattare all'outfit):
```
Professional three-panel character reference sheet on a seamless pure white studio background, even neutral lighting. Left: full-body front view, standing straight, arms relaxed, framed from the neck down. Center: full-body back view, framed from the neck down. Right: tight chest-up portrait, front-facing, sharp focus on the face.
Subject: [age]-year-old [description], [height] cm, [build]. Face identical to the reference selfie: same facial structure, eye shape, nose, lips, hairline and hair.
Skin: [fair skin with warm undertone], visible natural pores, light freckles across the nose and cheeks, a few small birthmarks, subtle natural imperfections, no retouching.
Outfit: [detailed outfit from reference: materials, colors, fit, wear].
Photorealistic, true-to-life textures, 2K.
Negative: no plastic or waxy skin, no beauty filter, no harsh sharpening, no oversaturation, no background objects, no text, no extra people, no distorted hands.
```
Varianti rapide:
- Secondario senza ref: "Write me a character sheet prompt for a [75-year-old Asian grandmother with a high bun]."
- Animale: "…a large German Shepherd, 5 years old, 35 kg, 65 cm at the withers, tennis ball in his mouth."
- Stato: "Same face, same cap, same goggles, but with wounds, scrapes and dirt."
- Folla: "Write a crowd character sheet: [n] distinct people, varied ages/styles, each clearly separated…"
- Stile: "Transform these character sheets into matching LEGO minifigure character sheets. Keep their exact clothes, hair, glasses, and accessories, but adapt them to classic plastic minifigure proportions."

## 3. Location sheet + camera/optical block
Richiesta:
```
Write me a prompt for [location] — [ora del giorno, meteo, atmosfera, dettagli]. [35 mm cinematic style]. No people in the frame. Describe surfaces and materials in detail, the light (hard directional light with real shadows, not soft haze), the camera and lens, and list what to avoid.
```
Blocco ottico da incollare in fondo a OGNI location (ricostruzione del "camera block" di Kaye):
```
Shot on a cinema camera with anamorphic lenses: subtle anamorphic distortion and oval bokeh, natural lens falloff and gentle vignetting, organic 35mm film grain, filmic color grade with rich shadows and controlled highlights, real atmospheric depth and haze layers, physically accurate light bounce. Photographed on a real location, not rendered. Avoid: CGI smoothness, plastic surfaces, over-sharpening, HDR look, oversaturated colors, people in frame.
```

## 4. Prop / product / model sheet
```
Write me a prompt for a collage model sheet of this [product] from front, back, and side angles on a white background. Keep exact proportions, materials, logos and color [name].
```
Wrap: "Image 1 is an example of how I want my [car] wrapped, and image 2 is my [car]. I need a prompt where my [car] from image 2 gets wrapped and customized exactly like the one in image 1."
Oggetto per il personaggio: "Here is my character sheet. Give me a prompt for a neat, refined [sword and helmet] suited to the girl and her costume."

## 5. Keyframe/scene still
```
Using [char_X.png] for face/outfit and [loc_Y.png] for the environment, write [n] scene-still prompts: [descrizione di ogni shot]. Vary shot scale (wide establishing, macro extreme close-up, floor-level low angle, 85mm shallow depth of field close-up, 24mm low on the exact moment of action). IMPORTANT: re-light the character according to the scene's light sources — the sheet was shot in flat white studio light.
```

## 6. Prompt video di scena
Richiesta (2–3 frasi dell'utente + struttura):
```
Scene [n]. Assets: [char_..., loc_..., prop_...] — tag them by these exact file names.
What the camera does: [...]
What [character] does: [...] — and how she feels inside: [...]
What the scene should make the viewer feel: [...]
Write a detailed video prompt, frame by frame with timing, only about motion (the references already lock look and location). Include: a physics block, natural wind/cloth movement if outdoors, re-lighting to match the environment, sound effect cues, and a negative list (no unrequested zoom or push-in, no morphing, no extra people).
```
Scheletro del prompt risultante:
```
Continuous single take, [duration]s, [aspect]. [@char_X] in [@loc_Y].
0–2s: [camera: start low on her feet…] [action] [emotion]
2–5s: [camera rises slowly…] [action]
5–8s: [camera pans to side angle…] [action / ending frame]
Lighting: [motivated sources], her face re-lit to match; hard shadows.
Physics: [weight of objects, body weight transfer, hair and cloak moving in light breeze, dust/water behavior].
Sound: [footsteps on…, wind, metal clank when helmet drops].
Negative: no zoom, no camera drift, no face morphing, no extra characters, no plastic skin.
```

## 7. Correzione di un draft
```
Keep everything that already works ([lista]). Only change: [1 variabile]. Specifically: [problema osservato] → [cosa voglio invece]. [Eventuale fisica scritta a parole.]
```
Framing: "Tighter on the product, cut the first 2 seconds of empty air, keep the phone visible during the bump so we see his reaction, group them tightly behind me in the last shot."

## 8. Genjutsu
- Swap: "Replace the person in the reference video with [@char_X]; keep the exact original motion, camera and timing."
- Avanzato: "Keep the exact stage-jump motion from the reference, but set it on [a snowy stage at night]; [@char_X] replaces the performer; add [huge explosion behind her at the end]." (Uno per ogni ambientazione.)

## 9. Suno
Richiesta: "Write a Suno prompt for a [high energy K-pop girl crush dance rap track], [solo female artist], [mixed English/Korean verses], and a catchy one-word English hook of your choice. Give me: style description, full lyrics with bracket performance tags, and an exclude-styles list."
Se l'hook è banale: "The hook feels too generic — give me a few more unusual one-word hooks." → "Rewrite the lyrics around [replica]."

## 10. Lip-sync
"Here is the isolated vocal stem (no drums) for [5–11 s]. Write a lip-sync performance prompt for [@char_X] in [@loc_Y], singing straight into the camera, with a dolly zoom (vertigo shot): camera moves in while zooming out, subject stays the same size, background widens."

## 11. Motion graphics (Claude Artifacts → Motion)
"Here is my raw video and its script. Reference clips attached for the style. Add motion graphics: [captions style, graphics at specific phrases, B-roll where I mention X, gradients/brand colors]. You can generate visuals with Higgsfield. Keep it clean and in one style." → iterazioni: "Lock everything that works; change [grain / unify style / text animation]."

## 12. Design con testo (ChatGPT Image 2.0)
"Describe the product [nome], packaging [forma, materiali, colori], tagline '[testo]', small print on the back '[testo]'. No broken letters, only actual readable text. [Aspect ratio]."

## 13. Voice-over (ElevenLabs v3 su Higgsfield)
Voce narrativa calda (es. "Arthur"), delivery mode **Creative**, batch 4, scegli la take migliore.
