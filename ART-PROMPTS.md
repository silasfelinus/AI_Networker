# Prompt Library for ChatGPT Image Generation

Act as an OpenAI image-generation art director working from a Conductor image queue for Kind Robots.

Kind Robots represents a consortium of projects aimed at multi-genre, cross-dimensional experiences. Treat the art direction as inclusive by default: when a scene includes people, characters, teams, crowds, families, players, operators, or companions, represent a diverse array of figures across genders, races, ages, body sizes, body shapes, presentation styles, and species. Mix humans, robots, animal-like beings, fantasy creatures, and other original nonhuman companions when it fits the asset. Do this naturally and respectfully, without tokenism or flattening anyone into a stereotype.

Generate exactly one finished image for each queued asset the user provides. Do not create collages, contact sheets, grids, comparison sheets, or multi-image layouts. Each requested asset must be a unique standalone file that matches its listed `size`, `variant`, `image_path`, and intent.

Use modern image generation standards: premium product illustration, strong composition, crisp focal subject, professional art direction, and a coherent Kind Robots visual language. Icons should be instantly readable at small sizes with polished app-icon silhouettes. Cards should feel like portrait key art. Heroes should feel like high-quality design work from professional illustration, product, and game design studios.

Hard rules for every generation: no readable text, no logos, no watermarks, no UI labels, no accidental typography, no collage. Preserve the requested aspect ratio. Keep images visually rich but not cluttered. Prefer cinematic lighting, expressive staging, tactile detail, and confident visual hierarchy over generic placeholder art.

When asked for a batch, generate up to ten images in the same order as the queue. If a batch contains mixed dimensions, keep each image’s own aspect ratio. After generation, identify each output by its `image_path` so the files can be saved into the repo correctly.

## Active queue vs prompt catalog

- `projects/art-generate.yaml` is the active send-this-to-the-generator queue. Keep only assets that still need generation there.
- `projects/art-prompts.yaml` is the canonical prompt catalog and missing-image request ledger. It can keep reusable prompts even when they are not in the active generator batch.
- ArtCollection parity folders use `public/images/artcollections/<dream-slug>/` in Kind Robots. Public URLs omit `public`, for example `/images/artcollections/<dream-slug>/<dream-slug>-card.webp`.

## Current starter asset sets

Pending project asset sets currently cataloged in `projects/art-prompts.yaml`:

- `sketchy` — icon, card, hero
- `art-generator-connect` — icon, card, hero
- `storymaker` — icon, card, hero
- `media-watchlist` — icon, card, hero
- `conductor-app` — icon, card, hero
- `alexa-integration` — icon, card, hero

Save generated project files to `projects/images/{slug}-{type}.webp`, then run:

```bash
python scripts/build_workspace.py
```

For Kind Robots ArtCollection images, save generated files to:

```text
public/images/artcollections/<dream-slug>/<dream-slug>-<variant>.webp
```

## Existing project inspiration prompt backlog

These are not automatically queued for legacy projects. Generate them manually when useful, save them into the matching ArtCollection folder, and attach the image records to the collection.

### sketchy

- `sketchy-inspiration-01.webp` — A luminous sketch-practice room where simple shapes become confident character drawings on floating transparent layers, an encouraging tiny robot art coach gesturing toward the next exercise, premium cozy creative-tool concept art, no text, no collage.
- `sketchy-inspiration-02.webp` — Close-up of a tactile sketchbook page with graphite studies, eraser crumbs, gesture thumbnails, and one charming character breaking out of the page into the real desk light, crisp professional illustration, no text, no collage.
- `sketchy-inspiration-03.webp` — A friendly critique interface imagined as physical art objects: pinned sketches, color chips, tiny spark badges, and a pencil companion guiding improvement without judgment, polished product key art, no text, no collage.

### art-generator-connect

- `art-generator-connect-inspiration-01.webp` — A conductor-like robot routing prompt cards through glowing image machines into neatly labeled visual asset folders, cinematic creative pipeline energy without readable UI text, professional sci-fi product art, no collage.
- `art-generator-connect-inspiration-02.webp` — Macro view of generated thumbnails crystallizing from light inside transparent tubes, each landing into a project collection tray, premium post-Flux image-generation visual metaphor, no text, no collage.
- `art-generator-connect-inspiration-03.webp` — A calm operations desk where failed placeholders are transformed into finished art assets by small robot technicians and luminous validation rails, crisp studio illustration, no text, no collage.

### storymaker

- `storymaker-inspiration-01.webp` — A tabletop map blooming into multiple possible scenes at once: forest, airship, castle, sea cave, and dragon trail, with players shaping the story through glowing choice tokens, high-end cozy fantasy game art, no text, no collage.
- `storymaker-inspiration-02.webp` — A robot narrator opening a starry book while diverse adventurers step from the pages into a shared world, expressive character design and cinematic depth, no text, no collage.
- `storymaker-inspiration-03.webp` — A branching story tree made of portals and miniature scenes, each branch held by different hands, paws, claws, and robot fingers, polished collaborative storytelling key art, no text, no collage.

### media-watchlist

- `media-watchlist-inspiration-01.webp` — A personal media observatory where books, films, games, comics, and podcasts orbit as glowing constellations around a calm archive console, diverse fans browsing together, no text, no collage.
- `media-watchlist-inspiration-02.webp` — A cozy reading-and-watch room with story portals opening from shelves into tiny genre worlds, polished editorial app art, warm lighting, no readable titles, no collage.
- `media-watchlist-inspiration-03.webp` — A decade-spanning memory timeline rendered as an elegant knowledge atlas, with media objects becoming paths through a cross-dimensional library, no text, no collage.

### conductor-app

- `conductor-app-inspiration-01.webp` — Mobile and desktop dashboards as physical glass cards floating above a command table, agent status pulses and approval tokens moving between screens, futuristic productivity key art, no readable UI text, no collage.
- `conductor-app-inspiration-02.webp` — A diverse multi-species operations crew coordinating project cards from phones, tablets, and desktop monitors, calm high-stakes command-center mood, premium app launch art, no text, no collage.
- `conductor-app-inspiration-03.webp` — Close-up of a hand approving a glowing project card while tiny robot agents carry subtasks into folders and checklists, crisp tactile product illustration, no readable text, no collage.

### alexa-integration

- `alexa-integration-inspiration-01.webp` — Luminous voice ribbons traveling from a smart speaker through a home server into project cards, todos, approvals, and art requests, cinematic smart-home automation art, no text, no collage.
- `alexa-integration-inspiration-02.webp` — Cozy workshop bench with a relay box, tidy cables, glowing audio waveforms, and household helpers testing hands-free task control, practical hacker-home charm, no text, no collage.
- `alexa-integration-inspiration-03.webp` — A cross-room home automation scene where spoken requests become gentle light paths connecting family spaces, maker tools, and Conductor workflows, warm polished product art, no text, no collage.
