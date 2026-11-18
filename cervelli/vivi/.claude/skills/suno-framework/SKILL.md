---
name: suno-framework
description: Framework completo per scrivere prompt Suno AI (V5): style prompt da max 200 caratteri, testi con metatag, negative tags, traduzione artista in descrittori. Usala per musica, jingle o colonne sonore dei video.
---

                                      SUNO AI
   PROMPT ENGINEERING FRAMEWORK
     A comprehensive, reusable system for any AI assistant to transform
       a user's music idea into an optimized Suno prompt (in English).




                       Version 2.0 — March 2026 — Based on Suno V5 / Suno Studio
             Compiled from 30+ expert sources, community analysis, and tested prompt patterns.




HOW TO USE THIS DOCUMENT

Feed this PDF to any AI assistant (ChatGPT, Claude, Gemini, etc.) along with a user's music
request. The AI should follow the framework step-by-step to produce:
• A Style Prompt (max 200 chars, optimized tag order)
• Custom Lyrics with metatags (max 3000 chars)
• Optional: a Title, Negative Tags, and iteration guidance.

The output must always be in English, regardless of the user's input language.
TABLE OF CONTENTS
 1. Suno Architecture: How the AI Interprets Prompts
 2. The Two-Field System: Style Prompt vs. Lyrics Field
 3. The 7-Column Prompt Formula
 4. Style Prompt: Priority Order & Character Budget
 5. Artist-to-Descriptor Translation (No Artist Names!)
    5.1 Why Artist Names Fail
    5.2 The 8-Dimension Decomposition Method
    5.3 Worked Examples (Full Process)
    5.4 Reference Table (30+ Artists)
    5.5 Genre Family Mapping (Unknown Artists)
    5.6 Same Artist, Different Eras
    5.7 Combining Multiple Artist References
 6. Metatags: Structure, Voice, Energy & Instruments
 7. Lyrics Field: Writing Singable Text
 8. Negative Prompting: What to Exclude
 9. Common Mistakes & Fixes
 10. Genre-Specific Templates (10 Genres)
 11. The Iteration Workflow
 12. Master Checklist for AI Assistants
 13. Quick-Reference Cheat Sheet
1. SUNO ARCHITECTURE: HOW THE AI INTERPRETS
PROMPTS
Suno does not work like a DAW or a human composer. It navigates a high-dimensional latent space —
a map of all possible sounds learned from its training data. When you write a prompt, you are pushing
the AI toward specific coordinates in that space.

Key architectural principles:
• Genre embeddings set the starting arrangement, chord progressions, and groove.
• Instrument tokens are extremely sticky: a single instrument name can shift the entire output.
• Tempo markers (BPM) strongly influence groove and pacing.
• Pop gravity well: Suno's training data is heavily weighted toward Pop structures
(Verse-Chorus-Verse). Niche genres will drift back toward Pop unless you enforce non-standard
structures.
• First-tokens priority: the first 20-30 words carry the highest weight. Front-load intent.
• Tags are signal weights, not hard commands. They bias output probabilistically.


  CORE RULE: Treat prompts like architectural blueprints, not search queries. Fewer contradictions
  = more controllable output. Change one variable at a time when testing.




2. THE TWO-FIELD SYSTEM: STYLE PROMPT vs.
LYRICS FIELD
Suno Custom Mode splits input into two distinct fields. Mixing their purposes is the most common
mistake:

                  STYLE PROMPT                              LYRICS FIELD

 Purpose          Defines HOW it sounds                     Defines WHAT is sung + WHEN sections change

 Contains         Genre, mood, instruments, vocals,         Lyrics text + structure metatags
                  BPM, production, era                      ([Verse], [Chorus], etc.)

 Char limit       ~200 characters (front 200                ~3000 characters
                  weigh most)                               (aim for 200-300 words)

 Format           Comma-separated tags,                     Line-by-line lyrics with
                  no brackets                               [Bracketed] section tags

 Do NOT put       Lyrics, [Verse] tags,                     Genre, mood, production
                  narrative text                            directions, BPM
3. THE 7-COLUMN PROMPT FORMULA
Every effective Suno style prompt can be decomposed into 7 dimensions. The sweet spot is 4-7
descriptors total.

             #   DIMENSION        DESCRIPTION                         EXAMPLES

             1   Genre/Sub-genre Primary musical identity.            indie pop, dark trap, grunge

             2   BPM/Tempo        Numeric tempo or feel.              90 BPM, mid-tempo, 140 BPM

             3   Mood/Emotion     1-2 precise adjectives.             melancholic, euphoric, defiant

             4   Key Instruments Max 3-4 instruments.                 acoustic guitar, 808 bass, Rhodes

             5   Vocal Style      Gender + texture + delivery.        breathy female, raspy male tenor

             6   Era/Decade       Time period for production.         80s, 2000s indie, modern

             7   Production/Mix   Final sonic texture.                lo-fi, polished radio mix, raw

Assembled example:
 melancholic 2000s indie rock, electric guitar + warm synth pads, male lead,
 nostalgic vocal tone, wide cinematic mix, 112 BPM




4. STYLE PROMPT: PRIORITY ORDER &
CHARACTER BUDGET
Suno weighs earlier tags more heavily. Follow this strict order:

       PRIORITY      ELEMENT                      BUDGET         RATIONALE

       1st           Genre + sub-genre            ~30 chars      Foundation of the entire sound

       2nd           Vocal direction              ~30 chars      Gender + texture (avoids random voices)

       3rd           Mood / energy                ~20 chars      Emotional direction

       4th           1-2 key instruments          ~30 chars      Core sonic palette

       5th           BPM                          ~10 chars      Locks rhythm and groove

       6th           Production / era             ~30 chars      Final texture and time period

       7th           Negative (if needed)         ~30 chars      Remove unwanted defaults


  GOLDEN RULE: Write descriptions, not commands. Instead of 'Create an upbeat pop track...',
  write 'Upbeat pop track...'. Suno responds to descriptors, not imperatives.
5. ARTIST-TO-DESCRIPTOR TRANSLATION (NO
ARTIST NAMES!)

  CRITICAL COPYRIGHT RULE: Suno blocks most artist and band names. Even when a name is
  not explicitly blocked, using it produces unpredictable, inconsistent results — Suno may ignore it,
  misinterpret it, or generate something completely unrelated. NEVER include artist names, band
  names, song titles, or album titles in the Style Prompt or Lyrics field. Instead, decompose the
  artist's sound into its pure musical DNA. This is the single most important translation skill for Suno
  prompting.



5.1 Why Artist Names Fail
Understanding why names fail helps the AI assistant explain the approach to skeptical users:

    WHAT THE USER TYPES                WHAT SUNO DOES                               THE RESULT

    "Make a Radiohead song"            Name is blocked or ignored.                  A bland pop-rock track with no
                                       Falls back to generic defaults.              atmospheric quality or complexity.

    "Sad song like Adele"              "Sad" is subjective. "Adele" may             Generic ballad, wrong vocal
                                       be blocked. No structure info.               texture, random instruments.

    "Nirvana grunge track"             "Nirvana" blocked. "Grunge"                  Loses the loud-quiet dynamics,
                                       alone is too vague.                          the raw distortion, the angst.

    "Mix of Drake and Billie"          Both names blocked. Model                    Completely random output with
                                       receives almost no signal.                   no resemblance to either artist.




5.2 The 8-Dimension Decomposition Method
When a user says 'I want something that sounds like [Artist]', systematically extract these 8 dimensions
— a DNA profile of the artist's sound:

           #    DIMENSION       QUESTION TO ASK                           EXAMPLE (Radiohead)

           1    Genre +         What genre family? Be specific.           Alternative rock, art rock,
                Sub-genre                                                 experimental electronic

           2    Era / Decade    Which period of their career?             Late 90s to mid-2000s
                                                                          (OK Computer / Kid A era)

           3    Vocal           Gender, register, texture,                Ethereal male tenor,
                Identity        delivery style. Describe the              falsetto-prone, fragile,
                                voice to someone who never                alternating between whisper
                                heard it.                                 and desperate wail

           4    Signature       What 2-3 instruments define               Shimmering delay guitar,
                Instruments     this sound? Include playing style.        atmospheric synth pads,
                                                                          glitchy electronic textures

           5    Rhythmic        Time signature, groove feel,              Complex polyrhythms,
                Identity        tempo range, rhythmic quirks.             odd time signatures,
                                                                          machine-like drums, 80-130 BPM

           6    Production      Wet/dry? Wide/narrow?                     Spacious reverb-heavy mix,
                Aesthetic       Clean/raw? Layered?                       wide stereo, layered textures,
                                                                          ambient soundscapes
       7   Emotional    Dominant emotional palette.           Existential melancholy,
           Signature    Not just "sad" &mdash; be specific.   alienation, beautiful anxiety,
                                                              technological unease

       8   Structural   How does this artist build songs?     Long builds from quiet to
           Habits       Verse-chorus? Builds? Drops?          cathartic, non-standard structures,
                                                              atmospheric intros



IMPORTANT: You do NOT need all 8 dimensions in the Style Prompt (remember the 200 char
limit). Use dimensions 1-6 for the Style Prompt and dimensions 7-8 to inform the lyrics structure
and metatags. Always prioritize: Genre → Vocals → Key Instruments → Mood → BPM →
Production.
5.3 Worked Examples: Full Decomposition Process
These examples show the complete thought process. The AI assistant should follow this same
reasoning for any artist.


  EXAMPLE 1: "Voglio una canzone stile Radiohead, atmosferica e malinconica"

  Step 1 — Decompose (8 Dimensions):
  Genre: experimental alt-rock, art rock | Era: late 90s-2000s | Vocals: ethereal male tenor, fragile
  falsetto, alternating whisper and desperate crescendo | Instruments: shimmering delay guitars,
  atmospheric synth pads, glitchy electronic textures, piano | Rhythm: complex time signatures,
  machine-like drums, 90-120 BPM | Production: spacious reverb, wide stereo, layered ambient |
  Mood: existential melancholy, alienation | Structure: long atmospheric builds, quiet-to-cathartic
  arcs

  Step 2 — Compress to Style Prompt (<200 chars):
  experimental alt-rock, ethereal male tenor, shimmering delay guitars, atmospheric
  synth pads, melancholic, spacious reverb mix, 100 BPM


  Step 3 — Apply dimensions 7-8 to structure the lyrics:
  Use [Intro] with atmospheric build → quiet [Verse] with whispered delivery → gradual [Build-Up] →
  cathartic [Chorus] with [Energy: High] → stripped-back [Bridge] → massive [Final Chorus]. Match
  the existential mood in lyric themes.


  EXAMPLE 2: "Something funky and electronic, like Daft Punk meets disco"

  Decompose: French house + electronic funk | Era: late 90s-2000s | Vocals: vocoder, robotic
  filtered voice, talk-box effect | Instruments: filtered disco guitar loops, funky bass, four-on-the-floor
  kick, analog synth stabs | Rhythm: steady 4/4, 115-125 BPM, syncopated hi-hats | Production:
  retro-futuristic, warm analog, compressed sidechain pumping | Mood: celebratory, groovy, futuristic
  optimism

  Style Prompt:
  French house, electronic funk, vocoder vocals, filtered disco guitar, funky bass,
  retro-futuristic analog synths, 120 BPM
EXAMPLE 3: "A mix of Amy Winehouse and Billie Eilish"

Step 1 — Decompose each artist separately:
Artist A: retro soul-jazz, raspy warm female vocals, vintage horns, 60s Motown, raw intimate
Artist B: dark pop, whispered female vocals, minimal bass-heavy, lo-fi, eerie atmospheric

Step 2 — Find overlaps: Both female, intimate, emotionally raw, minimal arrangements
Step 3 — Find unique contributions: A = retro warmth, jazz chords, horns | B = dark electronic
bass, whispered delivery, modern lo-fi
Step 4 — Check contradictions: A is retro/warm, B is modern/dark → merge as "retro-modern"
fusion

Merged Style Prompt:
dark jazz-pop, intimate raspy-to-whispered female vocals, vintage horns, deep sub
bass, lo-fi retro-modern warmth, 85 BPM
5.4 Artist Translation Reference Table (30+ Artists)
When the user references an artist not listed here, apply the 8-Dimension Method (5.2).

  USER SAYS...            SUNO STYLE PROMPT (no names, under 200 chars)

  "like Radiohead"        experimental alt-rock, ethereal male tenor, shimmering delay guitars,
                          atmospheric synth pads, melancholic, spacious reverb mix, 100 BPM

  "like The Weeknd"       dark cinematic R&B, falsetto male vocals, 80s analog synth bass,
                          moody atmospheric production, pulsing beat, 85 BPM

  "like Billie Eilish"    dark pop, whispered female vocals, minimal bass-heavy production,
                          intimate lo-fi feel, eerie atmospheric undertones, 75 BPM

  "like Nirvana"          90s grunge, distorted power chords, raw raspy male vocals,
                          loud-quiet dynamics, tape-saturated mix, angst-filled, 130 BPM

  "like Taylor Swift      modern synth-pop, clear bright female vocals, catchy hooks,
  (pop era)"              polished radio production, emotional storytelling, 120 BPM

  "like Taylor Swift      indie folk, intimate female vocals, fingerpicked acoustic guitar,
  (folk era)"             warm analog, confessional storytelling, gentle strings, 95 BPM

  "like Daft Punk"        French house, electronic funk, vocoder vocals, filtered disco loops,
                          retro-futuristic analog synths, four-on-the-floor groove, 120 BPM

  "like Adele"            soul-pop ballad, powerful female alto, piano-led arrangement,
                          cinematic strings, emotional torch song, wide reverb, 70 BPM

  "like Kendrick Lamar"   conscious hip-hop, dynamic male rap, jazz-influenced beats,
                          layered production, aggressive-to-introspective flow, 90 BPM

  "like Coldplay"         atmospheric alt-rock, emotional male tenor, ambient piano,
                          shimmering guitars, anthemic crescendos, uplifting, 120 BPM

  "like Arctic Monkeys"   indie rock, British swagger, baritone male vocals, driving guitar
                          riffs, tight drums, garage-rock energy, 130 BPM

  "like Bon Iver"         indie folk, ethereal falsetto male vocals, close-mic intimate,
                          layered harmonies, ambient atmospheric, warm analog, 85 BPM

  "like Beyonce"          modern R&B pop, powerful female mezzo-soprano, dynamic range,
                          polished layered harmonies, danceable groove, 100 BPM

  "like Pink Floyd"       70s progressive rock, spacious guitar textures, philosophical,
                          wide stereo synth pads, slow atmospheric build, 80 BPM

  "like Massive Attack"   trip-hop, dark atmospheric beats, deep bass, sparse production,
                          cinematic tension, haunting female vocals, 80 BPM
5.4 Artist Translation Reference Table (continued)
  USER SAYS...           SUNO STYLE PROMPT (no names, under 200 chars)

  "like Ed Sheeran"      folk-pop, acoustic guitar loops, warm male vocals, mellow intimate,
                         light beatbox percussion, heartfelt storytelling, 100 BPM

  "like Fleetwood Mac"   classic 70s rock, mellow male-female harmonies, jangly guitars,
                         emotional storytelling, warm analog production, 115 BPM

  "like Travis Scott"    dark trap, auto-tuned male vocals, heavy 808 bass, atmospheric
                         reverb, psychedelic production, hi-hat rolls, 145 BPM

  "like Amy Winehouse"   retro soul-jazz, raspy warm female vocals, vintage horns, 60s
                         Motown feel, raw intimate production, upright bass, 95 BPM

  "like Linkin Park"     nu-metal alt-rock, heavy distorted guitars, ffual vocals (rap +
                         melodic singing), electronic glitch elements, aggressive, 130 BPM

  "like Frank Ocean"     alternative R&B, introspective male vocals, lush synth pads,
                         dreamy reverb, lo-fi warmth, jazz chords, 80 BPM

  "like Tame Impala"     psychedelic pop-rock, dreamy male falsetto, swirling synths,
                         phaser-laden guitars, retro 70s feel, modern production, 110 BPM

  "like SZA"             alternative R&B, airy breathy female vocals, neo-soul,
                         lush layered production, vulnerable intimate, 85 BPM

  "like Gorillaz"        alt-hip-hop, electronic, genre-blending, laid-back male vocals,
                         funky bass, lo-fi cartoon aesthetic, eclectic, 105 BPM

  "like Lana Del Rey"    cinematic dream pop, sultry alto female vocals, vintage reverb,
                         orchestral strings, Americana melancholy, 80 BPM

  "like System of        alt-metal, chaotic time signatures, dramatic male vocals with
  a Down"                scream-to-melody shifts, Middle Eastern scales, 140 BPM

  "like The 1975"        synth-pop alt-rock, smooth male vocals, 80s-inspired production,
                         shimmering synths, emotional indie-pop, 115 BPM

  "like Bad Bunny"       reggaeton-trap fusion, Latin urban flow, auto-tuned male vocals,
                         dembow rhythm, heavy bass, 95 BPM

  "like Aphex Twin"      experimental IDM, glitchy electronic textures, complex broken
                         beats, ambient pads, no vocals, unsettling beauty, 130 BPM

  "like Queen"           theatrical rock, operatic male vocals, multi-layered harmonies,
                         orchestral guitar, piano-driven, anthemic stadium sound, 115 BPM

  "like Portishead"      dark trip-hop, haunting female soprano, scratchy vinyl samples,
                         minimal beats, jazz noir atmosphere, cinematic, 75 BPM

  "like Bruno Mars"      funk-pop, groovy male vocals, danceable rhythm, retro brass,
                         clean polished mix, upbeat feel-good energy, 115 BPM




5.5 Genre Family Mapping (for Unknown Artists)
When the user references an artist the AI does not know well, identify which genre family they belong
to and use the family's signature characteristics as a base:

     GENRE FAMILY        SIGNATURE DNA (always include)                                  TYPICAL VOCAL CUES

     Rock / Alt-Rock     Distorted electric guitars, live drums,                         Male tenor/baritone, raw or
                         bass guitar, verse-chorus dynamics                              emotional delivery

     Hip-Hop / Rap       808 bass or boom-bap drums, rhythmic                            Male/female rap delivery,
                         flow, sampled beats, sub-heavy mix                              flow patterns, ad-libs

     Electronic / EDM    Synthesizers, drum machines, sidechain                          Vocoder, pitched vocals,
                         compression, build-drop structure                               chopped vocal samples

     R&B / Soul          Smooth chord progressions, groove-led                           Melismatic, breathy,
                         bass, warm keys, laid-back drums                                intimate or powerful belt
Pop                 Catchy melodic hooks, polished mix,        Clear pitch, commercial
                    radio-friendly structure, bright tones     delivery, accessible range

Folk / Acoustic     Acoustic guitar, minimal production,       Natural timbre, close-mic,
                    organic textures, storytelling focus       confessional or narrative

Metal               Heavy distorted guitars, double kick,      Growl, scream, clean-to-harsh
                    aggressive energy, complex riffs           contrast, powerful

Jazz                Complex chord voicings, swing feel,        Scat, smooth crooning,
                    improvisational, brass/keys/upright bass   instrumental focus

Latin / Reggaeton   Dembow rhythm, tropical percussion,        Melodic rap, auto-tune,
                    bass-heavy, rhythmic vocal flow            bilingual phrasing
5.6 Same Artist, Different Eras
Many artists have evolved dramatically. When a user says 'like [Artist]', ask (or infer) which era they
mean:

    REFERENCE             EARLY ERA TRANSLATION                                 LATER ERA TRANSLATION

    "Radiohead            Britpop alt-rock, jangly guitars,                     Experimental electronic art-rock,
    (early vs later)"     emotional male vocals, 90s indie                      glitchy textures, ambient pads,
                          rock energy, anthem-like, 125 BPM                     fragile falsetto, sparse, 95 BPM

    "Kanye West           Soulful hip-hop, pitched vocal                        Experimental industrial hip-hop,
    (early vs later)"     samples, warm beats, optimistic                       distorted 808s, dark aggressive,
                          male rap, chipmunk soul, 92 BPM                       abrasive textures, 130 BPM

    "Taylor Swift         Country-pop, acoustic guitar, twangy                  Indie folk, fingerpicked guitar,
    (country vs folk)"    female vocals, Americana storytelling,                intimate whispered female vocals,
                          clean Nashville production, 110 BPM                   warm analog, confessional, 90 BPM

    "Bowie                Glam rock, theatrical male vocals,                    Art-rock ambient, cold synths,
    (glam vs Berlin)"     electric guitars, dramatic flair,                     minimal krautrock drums, detached
                          colorful, anthemic, 120 BPM                           male vocals, experimental, 100 BPM




5.7 Combining Multiple Artist References
When the user says 'a mix of Artist A and Artist B', follow this merge protocol:

1. Decompose each artist separately using the 8-Dimension Method.
2. Identify overlaps (shared traits become the core of the prompt).
3. Identify unique contributions from each (pick the most distinctive element per artist).
4. Check for contradictions (if A is 'minimal' and B is 'maximalist', choose one direction or describe a
gradient: 'minimal verses that build to lush choruses').
5. Compress into one coherent Style Prompt under 200 characters.

   USER REQUEST                 MERGED STYLE PROMPT

   "Radiohead meets             atmospheric trip-hop meets art rock, ethereal male vocals,
   Massive Attack"              deep bass, layered delay guitars, dark cinematic reverb, 85 BPM

   "Billie Eilish meets         dark jazz-pop, intimate raspy-to-whispered female vocals,
   Amy Winehouse"               vintage horns, deep sub bass, lo-fi retro-modern warmth, 85 BPM

   "Daft Punk meets             psychedelic electro-funk, vocoder + dreamy falsetto vocals,
   Tame Impala"                 swirling synths, filtered disco bass, retro-futuristic, 115 BPM

   "Kendrick Lamar              progressive conscious hip-hop, dynamic male rap over spacious
   meets Pink Floyd"            jazz-rock textures, atmospheric synth pads, wide stereo, 90 BPM

   "Queen meets                 theatrical alt-metal, operatic male vocals with aggressive shifts,
   System of a Down"            orchestral guitar, Middle Eastern scales, dramatic builds, 130 BPM



  ABSOLUTE RULE FOR AI ASSISTANTS: When a user references ANY artist, band, song title, or
  album name, your job is to TRANSLATE, NEVER TRANSCRIBE. Extract the musical DNA using
  the 8-Dimension Method, discard every proper name. The final output prompt must contain ZERO
  artist names, band names, song titles, or album titles. This is non-negotiable for Suno
  compatibility and copyright compliance. If unsure about an artist's sound, use the Genre Family
  table (5.5) as a fallback and ask the user to describe the specific qualities they want.
6. METATAGS: STRUCTURE, VOICE, ENERGY &
INSTRUMENTS
Metatags are [bracketed] cues placed inside the lyrics field. Place each tag on its own line, before the
section it describes.

6.1 Structure Tags (highest impact)
 [Intro] • [Verse] / [Verse 1] / [Verse 2] • [Pre-Chorus] • [Chorus] • [Bridge] •
 [Hook] • [Break] • [Interlude] • [Outro] • [Build] / [Build-Up] • [Drop] • [Fade
 Out] • [Big Finish]


6.2 Voice / Delivery Tags
 [Whispered] • [Belted] • [Falsetto] • [Growl] • [Spoken Word] • [Rap] • [Soft] •
 [Powerful] • [Breathy] • [Male Vocal] • [Female Vocal] • [Duet]


6.3 Energy, Mood & Sound Effect Tags
 [Energy: Low/Medium/High] • [Mood: Introspective/Triumphant/Dark/Hopeful] •
 [Breakdown] • [Guitar Solo] • [Piano Solo] • [Rain] • [Thunder] • [Cheering]



6.4 Complete Example (Lyrics Field)
 [Mood: Focused] [Energy: Medium]
 [Intro]
 (gentle pulse)

 [Verse 1]
 Walking through the city lights
 Everything feels so right tonight

 [Pre-Chorus] [Build-Up]
 And I know, I know

 [Chorus] [Energy: High]
 We're alive, we're alive
 Nothing's gonna bring us down

 [Bridge] [Breakdown]
 When the world gets heavy
 I'll be right here, ready

 [Final Chorus] [Energy: High]
 We're alive, we're alive
 Nothing's gonna bring us down

 [Outro] (fade)
7. LYRICS FIELD: WRITING SINGABLE TEXT
• Syllable matching: Verse 1 and Verse 2 must have the same syllable count (±2).
• Format like a lyric sheet, not a paragraph. 4 lines/verse, 2-4 lines/chorus.
• Each line under ~12 syllables. Leave blank lines between sections.
• Hook design: short (3-6 syllables), repeatable, in the chorus.
• Use ALL CAPS for emphasis. (Parentheses) for backup vocals.
• ONE central metaphor per song. No mixed metaphors.
• Duets: [male vocal] line / [female vocal] line / [both] line.




8. NEGATIVE PROMPTING: WHAT TO EXCLUDE
Negative prompts = guidance, not hard bans. Max 2-3 negatives. Be specific. Prefer positives.
 warm reggae groove, steady bass, no electric guitar
 cinematic orchestral, emotional strings, no choir
 lo-fi chillhop, warm Rhodes, soft drums, no vocals, no risers




9. COMMON MISTAKES & FIXES
      MISTAKE                  WHY IT FAILS                  FIX

      "Make a sad rock song"   Too vague, no structure       melancholic 2000s alt-rock, distorted
                                                             guitars, raspy male vocals, 108 BPM

      Using artist names       Names blocked/unpredictable   Use 8-Dimension decomposition (Sec. 5)

      10+ descriptors          Confuses the model            Max 4-7 descriptors, 3-4 instruments

      Contradictions           Incoherent output             Pick one primary + one secondary attribute

      Genre cues in lyrics     Wrong field                   Move to style prompt

      No BPM                   Unpredictable rhythm          Always include BPM

      Bad syllable counts      Rushed/empty vocals           Match syllables across verses

      500+ char style prompt   Truncated silently            Front-load within 200 chars
10. GENRE-SPECIFIC TEMPLATES (10 GENRES)
POP (Modern)
 modern pop, upbeat, catchy hooks, polished production, bright synths, female
 vocals, powerful chorus, radio-ready mix, 122 BPM

INDIE ROCK
 indie rock, jangly electric guitars, warm male vocals, nostalgic tone, roomy
 live-band mix, 118 BPM

HIP-HOP / TRAP
 dark trap, aggressive male rap, 808 bass, hi-hat rolls, hard-hitting, professional
 mix, 145 BPM

R&B; / NEO-SOUL
 modern R&B; slow jam, intimate female vocals, warm Rhodes, subtle bass, velvet
 production, 78 BPM

EDM / HOUSE
 melodic techno, 124 BPM, rolling bass, airy synths, restrained vocal hook, clean
 club mix

CINEMATIC
 cinematic orchestral, sweeping strings, brass fanfare, timpani, epic trailer
 music, wide stereo, 90 BPM

LO-FI / CHILL
 lo-fi chillhop, warm Rhodes, soft drums, vinyl crackle, no vocals, mellow study
 mood, 85 BPM

COUNTRY
 modern country-pop, acoustic guitar, light banjo, clear male vocals, heartfelt,
 Americana, 105 BPM

METAL / ROCK
 progressive metal, heavy distorted guitars, double kick, powerful male growl,
 complex time, 160 BPM

FOLK / ACOUSTIC
 indie folk, fingerpicked acoustic guitar, gentle female vocals, intimate
 close-mic, warm analog, 90 BPM




11. THE ITERATION WORKFLOW
1. Generate 3-5 variations with the same style prompt. 2. Identify best vibe/vocals/groove. 3. Adjust
ONE variable at a time. 4. Use Suno Studio's Replace Section to fix weak parts. 5. Use Extend for
full-length tracks. 6. Export stems for DAW post-production.

   VOCAL PROBLEM            FIX

   Too breathy              "firmer support, brighter tone, reduce breath noise"

   Too flat/dull            "increase dynamic contrast, add gentle vibrato"
Timing off            "lock vocal phrasing to drum groove, tighten consonants"

Robotic               "less quantized, micro-timing variation, humanized dynamics"

Inconsistent chorus   Shorten lyrics, add repetition, predictable cadence

Mispronunciation      Replace word with safer spelling or phonetic synonym
12. MASTER CHECKLIST FOR AI ASSISTANTS

  INSTRUCTIONS FOR THE AI ASSISTANT
  When a user requests a Suno prompt, follow these phases in order. Always output in English.



PHASE 1: INTAKE
• Identify intent: genre, mood, theme, vocal preference, references.
• If vague, ask clarifying questions. If the user names an artist: apply 8-Dimension Decomposition
(Section 5.2). NEVER use artist names in output.

PHASE 2: STYLE PROMPT
• Apply 7-Column Formula. Follow Priority Order. Under 200 chars. 4-7 descriptors. Comma-separated,
no brackets. Descriptions not commands. ZERO artist/band/song names.

PHASE 3: LYRICS
• [Bracketed] structure tags on own lines. 4 lines/verse, 2-4/chorus. Match syllables. Hook: 3-6 syllables,
repeatable. One metaphor. Max one voice tag/section. Under 300 words.

PHASE 4: QUALITY CHECK
• Under 200 chars? • 4-7 descriptors? • No artist names? • No contradictions? • BPM? • Syllables
matched? • Hook short? • One metaphor? • Tags consistent? • No genre cues in lyrics?

PHASE 5: OUTPUT FORMAT
 TITLE: [Song Title]
 STYLE PROMPT: [tags, under 200 chars]
 NEGATIVE TAGS (optional): [no X, no Y]
 LYRICS: [full lyrics with metatags]
 ITERATION NOTES: [adjustment suggestions]




13. QUICK-REFERENCE CHEAT SHEET

All Structure Tags
 [Intro] [Verse] [Verse 1] [Verse 2] [Pre-Chorus] [Chorus] [Final Chorus]
 [Post-Chorus] [Hook] [Bridge] [Break] [Breakdown] [Build] [Build-Up] [Drop]
 [Interlude] [Instrumental] [Guitar Solo] [Piano Solo] [Outro] [Ending] [Fade Out]
 [Big Finish] [Refrain]


All Voice Tags
 [Whispered] [Soft] [Belted] [Powerful] [Falsetto] [Growl] [Spoken Word] [Rap]
 [Breathy] [Raspy] [Clear] [Vibrato] [Ad-libs] [Harmonies] [Male Vocal] [Female
 Vocal] [Duet] [both] [Choir]


Energy & Effects
 [Energy: Low/Medium/High] [Mood: Introspective/Triumphant/Focused/Dark/Hopeful]
 [Rain] [Thunder] [Wind] [Cheering] [Vinyl Crackle] [Heartbeat]


BPM by Genre
          GENRE                BPM             GENRE                BPM

          Ballad/R&B           60-80           Pop                  100-130

          Lo-fi/Chill          75-90           Rock                 110-140

          Hip-Hop              80-115          House/EDM            120-130

          Country              95-120          D&B                  160-180

          Folk                 85-110          Trap                 130-160

          Jazz                 80-160          Metal                140-200




 REMEMBER: Suno V5 amplifies good prompting. Treat every prompt like a production brief. And
 NEVER use artist names — translate them into musical DNA using the 8-Dimension Method.
