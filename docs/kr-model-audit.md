# Kind Robots Model Audit — Storymaker Session Compatibility

Generated: 2026-06-30
Task: storymaker/t-006

---

## Purpose

Audit the kind_robots Prisma schema for Bot, Character, Scenario, Chat, and Reward models to determine what a Storymaker session would need that's already there vs. what's missing or would require a backend pitch.

---

## Model Inventory

### Bot

**Purpose in Storymaker:** The narrator. Drives the story, generates options, provides in-character responses.

| Field | Type | Storymaker use |
|---|---|---|
| id, name, slug | PK + identity | Session references narrator by slug |
| BotType | String | Distinguish narrator bots from other bot types |
| botIntro | VarChar(3000) | The Bot's story context / scene-setting opening |
| userIntro | VarChar(764) | How the Bot greets a new player |
| narrativeVoice | Text | Narrator's writing style and tone guidance |
| forgeIntro | Text | System prompt for LLM generation |
| prompt | VarChar(764) | Core behavior prompt |
| personality | VarChar(764) | Characterization notes |
| isPublic, isActive, isMature | Booleans | Session visibility and safety filtering |
| theme | VarChar(764) | Visual/tonal theme (feeds UI styling) |
| imagePath, avatarImage | VarChar | Bot portrait for the session UI |
| Chats | Chat[] | ALL chat messages where this bot is the narrator |
| Dreams | Dream[] | Dreams associated with this bot (not used for sessions) |
| NarratorThreads | NarratorThread[] | Thread tracking for narrative continuity |

**What's there:** ✓ Narrator system prompt + voice + intro. ✓ NarratorThread model for thread continuity. ✓ Chat relation for history.  
**What's missing for Storymaker:** No "available for storytelling" flag — would need to filter by BotType or add an `isStoryteller` boolean (pitch if needed).

---

### Character

**Purpose in Storymaker:** The player's avatar. Carries stats, inventory, history, and narrative identity across sessions.

| Field | Type | Storymaker use |
|---|---|---|
| id, name, slug | PK + identity | Player selects a Character to play |
| level, experience | Int | Progression tracking per session |
| class, species, alignment, genre | String | Character type + alignment system |
| backstory, personality, quirks | Text | Character sheet content for LLM context |
| charm, empathy, grace, luck, might, wits | Rarity (COMMON/UNCOMMON/RARE/EPIC/LEGENDARY) | Skill stats — 5-tier rarity system maps well to RPG attributes |
| drive | VarChar(764) | Character motivation (scene-driving prompt context) |
| honorific | VarChar(256) | How the narrator addresses the character |
| imagePath | VarChar(764) | Portrait art for session UI |
| isPublic, isActive, isMature | Booleans | Visibility and safety |
| Rewards | Reward[] via CharacterToReward | Items/achievements the character owns |
| Scenarios | Scenario[] via CharacterToScenario | Scenarios this character has appeared in |
| Chats | Chat[] | Messages involving this character |

**What's there:** ✓ Full stat system (6 Rarity stats). ✓ Rewards inventory via relation. ✓ Backstory/personality/quirks for LLM context. ✓ Level/experience progression.  
**What's missing:** No `currentSessionId` field — a character doesn't know which active session it's in. No "status" enum (idle, in-session, locked). These are soft gaps that the session layer (not the Character model) should track.

---

### Scenario

**Purpose in Storymaker:** The story setting — defines the world, starting situation, available characters, locations, and rules.

| Field | Type | Storymaker use |
|---|---|---|
| id, title, description | PK + narrative | Scenario selection + summary display |
| intros | Text | Opening narrative(s) — can be multiple (pipe-separated or JSON) |
| locations | Text | Available in-world locations |
| genres | String | Genre tags (fantasy, horror, sci-fi, etc.) |
| cast | Json | Cast of characters/entities; flexible schema for session participants |
| difficulty | Int? | Session difficulty level |
| tier | String? | "beginner" / "advanced" / etc. |
| group | String? | Scenario series or campaign grouping |
| secretNotes | String? | GM-only notes not shown to players |
| inspirations | Text | Thematic inspiration seeds for LLM context |
| outputType | ScenarioOutputType | What the scenario produces: STORY/ART/CHARACTER/REWARD/DREAM/SCENARIO/MIXED |
| Characters | Character[] via CharacterToScenario | Pre-cast characters for the scenario |
| Dreams | Dream[] via DreamToScenario | Dreams linked to this scenario |
| Rewards | Reward[] via DreamToReward (through dream) | Potential rewards in this scenario |

**What's there:** ✓ Rich scenario context (intros, locations, genres, cast JSON). ✓ `outputType` enum already anticipates STORY/ART/CHARACTER/REWARD/DREAM output types. ✓ difficulty + tier for skill matching. ✓ Character pre-cast via relation.  
**What's missing:** No "branching options schema" — the scenario defines a starting point but not the branch tree itself. No "session state persistence" — the scenario doesn't track how far a particular session has progressed through it.

---

### Chat

**Purpose in Storymaker:** The conversation record. Each turn in a session is a Chat message.

| Field | Type | Storymaker use |
|---|---|---|
| id, createdAt | PK + timestamp | Message ordering and session history |
| type | ChatType (enum) | Distinguish bot messages from user messages, system messages |
| sender, recipient | VarChar(255) | Username or bot identifier |
| content | Text | The actual narrative/response text |
| title | VarChar(255) | Optional turn title or heading |
| originId | Int? | Groups messages into a thread/session — all messages in a session share an originId |
| previousEntryId | Int? | Explicit linked-list pointer for message chaining |
| botId | Int? | Which Bot/narrator generated this message |
| characterId | Int? | Which Character this message is "from" or "about" |
| userId | Int? | The human player behind this turn |
| channel | VarChar(255) | Can be used as a session identifier |
| botResponse | String? | The bot's response text (if sender is human) |

**What's there:** ✓ `originId` threading — a Storymaker session's entire conversation can share one `originId`. ✓ `botId` + `characterId` + `userId` — all three participant types are tracked. ✓ `previousEntryId` for explicit turn chaining. ✓ `channel` can serve as a session tag/slug.  
**What's missing:** No "player choice" field — when a player picks from multiple options, what option they chose isn't stored on the Chat record. No "branch state" (which path was taken). No "session start/end" markers — these must be inferred from the first/last message in a thread.

---

### Reward

**Purpose in Storymaker:** Items, achievements, and collectibles that characters earn during sessions.

| Field | Type | Storymaker use |
|---|---|---|
| id, name, slug | PK + identity | Item identification and display |
| description, flavorText | Text/VarChar | Item card text |
| effect | Text | What the item does in gameplay |
| icon | VarChar(256) | Emoji or icon slug for quick display |
| collection | VarChar(764) | Item set grouping (e.g. "forest-loot", "epic-tier") |
| rarity | Rarity | COMMON through LEGENDARY — item scarcity |
| rewardType | RewardType (ITEM default) | Item type classification |
| imagePath | VarChar | Card art path |
| isPublic, isActive | Booleans | Visibility controls |
| Characters | Character[] via CharacterToReward | Characters who own this reward |

**What's there:** ✓ Full item system (rarity, effect, collection, icon). ✓ Character ownership via relation (Character.Rewards). ✓ Rarity for loot table logic.  
**What's missing:** No `quantity` field — Character owns a Reward but can't hold multiple copies without multiple relation records. No `expiresAt` for temporary/consumable items. These are soft gaps; MVP inventory works with current structure.

---

## What Storymaker Needs That Isn't in the Schema

| Need | Gap | Recommendation |
|---|---|---|
| **Session model** (participants, status, turn count, start/end, game mode) | No `StorySession` model exists | **Must pitch:** `StorySession { id, scenarioId, botId, status, mode (EXQUISITE_CORPSE|GUIDED_ADVENTURE), startedAt, endedAt, participantIds Json }` |
| **Branch choices log** (what options were presented, what was selected at each turn) | No `BranchChoice` or `TurnOption` model | **Must pitch:** `TurnChoice { id, chatId, sessionId, optionsOffered Json, optionChosen String }` |
| **Active session link on Character** | Characters don't know their active session | **Nice to have:** `Character.activeSessionId Int?` or handle at the session layer |
| **Inventory snapshot per session** | Character.Rewards is global, not session-specific | **MVP approach:** Use the global Rewards relation; session rewards are just new relation entries. No new model needed at MVP. |
| **Session status lifecycle** | No lifecycle model for ACTIVE/PAUSED/COMPLETE sessions | Handled by the StorySession model above |

---

## Summary

**Rich and ready to use:**
- Bot narrator system (narrativeVoice, forgeIntro, prompt, NarratorThread)
- Character stat system (6 Rarity stats, level, experience, backstory, Rewards)
- Scenario setting (intros, locations, genres, cast JSON, outputType enum)
- Chat threading (originId, previousEntryId, botId, characterId, userId — full participant tracking)
- Reward item system (rarity, effect, collection, Character ownership)

**Must pitch to the kind_robots backend (do not implement directly):**
1. `StorySession` model — session lifecycle, participants, mode, status
2. `TurnChoice` model — branch option logging per turn

**Can defer to MVP-plus:**
- `Character.activeSessionId` — handle at session layer for now
- `Reward.quantity` — multiple relation records work at MVP
- "Available for storytelling" flag on Bot — filter by BotType convention for now

This document feeds into storymaker/t-001 (session data model spec) so the spec uses real schema data rather than assumptions.
