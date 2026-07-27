# Pokémon TCG AI Agent

Building an autonomous Pokémon Trading Card Game AI agent for the Kaggle competition:

**"The Pokémon Company – PTCG AI Battle Challenge Simulation."**

The goal of this project is to create an AI system capable of playing Pokémon TCG through simulation by combining:

- structured card understanding
- rule-based decision making
- evolution-aware deck construction
- strategic deck evaluation
- optimization search
- future reinforcement learning

The project has evolved from simple battle agents into a complete pipeline covering:

- card intelligence
- deck generation
- deck validation
- deck optimization
- battle strategy

---

# Current Progress

## Environment & Simulation ✅

Completed:

- Pokémon TCG simulator integration
- Local battle execution
- Observation exploration
- Agent evaluation framework

---

# Agents

## Random Agent ✅

Baseline agent using random legal actions.

Used for benchmarking stronger strategies.

---

## Heuristic Agent ✅

Rule-based agent using:

- damage evaluation
- survival evaluation
- board state analysis
- basic action scoring

---

## Strategic Agent ✅

Feature-driven agent using:

- Pokémon strength evaluation
- attack selection
- board value estimation
- survival prioritization
- strategic scoring

Current benchmarks:

| Matchup | Win Rate |
|---------|---------:|
| Strategic vs Random | **81.7%** |
| Strategic vs Heuristic | **87.7%** |

(1000 self-play games per matchup)

---

# Card Knowledge System

Implemented a centralized card intelligence layer.

The `CardDatabase` provides a unified interface for:

- card lookup
- card classification
- Pokémon detection
- trainer detection
- energy detection
- attack extraction
- rule extraction

Supported card categories:

| Category | Status |
|----------|--------|
| Basic Pokémon | ✅ |
| Stage 1 Pokémon | ✅ |
| Stage 2 Pokémon | ✅ |
| Item | ✅ |
| Supporter | ✅ |
| Stadium | ✅ |
| Pokémon Tool | ✅ |
| Basic Energy | ✅ |
| Special Energy | ✅ |

---

# Pokémon Feature System

Pokémon cards are converted into structured features.

Extracted information includes:

- evolution stage
- previous evolution
- HP
- type
- attacks
- attack damage
- attack energy requirements
- Pokémon ex detection
- ability information

This allows the deck builder and agents to reason about Pokémon strategically instead of treating cards as IDs.

---

# Evolution Knowledge System

Implemented evolution-aware reasoning.

The system builds complete evolution chains.

Example:

\`\`\`text
Froakie
   │
Frogadier
   │
Greninja ex
\`\`\`

Capabilities:

- evolution stage detection
- previous-stage resolution
- evolution line construction
- evolution database generation

Current database:

\`\`\`text
336 evolution lines discovered
\`\`\`

This allows deck generation to select playable evolution cores.

---

# Trainer Intelligence System

Implemented a dedicated trainer analysis pipeline.

Trainer cards are converted into strategic features.

Current trainer tags:

- draw support
- search effects
- switching effects
- recovery effects
- disruption effects
- energy acceleration effects

The trainer selector prioritizes consistency-focused cards before filling remaining slots.

Selection priority:

1. Draw support
2. Search support
3. Recovery
4. Additional utility trainers

---

# Energy Intelligence System

Implemented energy-aware deck construction.

The system analyzes Pokémon attack requirements and generates compatible energy packages.

## Energy Cost Parsing

Examples:

\`\`\`text
{G}      → Grass Energy

{R}●     → Fire Energy

{F}{M}   → Fighting + Metal Energy

{W}{W}   → Water + Water Energy
\`\`\`

The parser handles:

- basic energy symbols
- multiple energy requirements
- mixed colored and colorless costs

---

## Energy Allocation

The Energy Selector:

- extracts attack requirements
- counts required energy types
- allocates energy proportionally
- returns valid basic energy card IDs

Example:

\`\`\`text
Pokémon Core:

Roaring Moon
Gouging Fire ex
Raging Bolt

Generated Energy:

Darkness Energy
Fire Energy
Lightning Energy
Fighting Energy
\`\`\`

---

# Deck Construction System

Implemented modular 60-card deck generation.

Pipeline:

\`\`\`text
Pokémon Selection
        │
        ▼
Trainer Selection
        │
        ▼
Energy Selection
        │
        ▼
Deck Validation
        │
        ▼
Deck Evaluation
\`\`\`

Current capabilities:

- legal deck generation
- evolution-aware Pokémon selection
- trainer package generation
- energy allocation
- energy requirement validation
- archetype-based generation

---

# Deck Validation System

Implemented legality checking.

Validation includes:

- deck size
- duplicate restrictions
- Basic Pokémon requirements
- evolution consistency
- energy requirements

Energy validation checks that generated decks contain the required energy types needed by selected Pokémon attacks.

---

# Deck Evaluation System

Implemented feature-based deck scoring.

The evaluator measures:

## Composition

- Pokémon count
- Trainer count
- Energy count
- Basic Pokémon count
- Stage 1 count
- Stage 2 count

## Pokémon Quality

Measures:

- average HP
- average damage
- Pokémon ex count
- offensive potential

## Evolution Consistency

Analyzes:

- evolution lines
- orphan evolutions
- supported evolution chains

Example:

\`\`\`text
{
    pokemon_count: 15,
    trainer_count: 30,
    energy_count: 15,

    evolution_lines: 3,
    evolution_score: 19,

    deck_score: 114
}
\`\`\`

---

# Deck Optimization

Implemented mutation-based optimization.

Optimization workflow:

1. Generate initial deck
2. Apply mutations
3. Validate candidates
4. Evaluate deck quality
5. Keep improvements
6. Track best-performing decks

Current capabilities:

- multi-archetype comparison
- mutation search
- hill-climbing improvement
- best deck tracking
- archetype ranking

---

# Implemented Archetypes

## Evolution Heavy

Focus:

- evolution cores
- Stage 2 attackers
- evolution consistency

---

## Balanced

Focus:

- evolution lines
- standalone attackers
- consistency trainers
- balanced resources

---

## Aggressive EX

Focus:

- Pokémon ex
- high HP attackers
- high damage output
- offensive pressure

---

# Project Roadmap

## Phase 1 — Baseline Agents ✅

Completed:

- Random agent
- Heuristic agent
- Strategic agent

---

## Phase 2 — Card Understanding ✅

Completed:

- card database
- feature extraction
- attack parsing
- evolution analysis
- trainer analysis
- energy analysis

---

## Phase 3 — Deck Construction ✅

Completed:

- Pokémon selection
- evolution-aware generation
- trainer selection
- energy selection
- validation framework

---

## Phase 4 — Optimization ✅

Completed:

- mutation-based optimization
- hill-climbing search
- archetype comparison
- improvement tracking

---

## Phase 5 — Advanced AI Agents

Planned:

- Monte Carlo Tree Search
- rollout planning
- hidden information reasoning
- reinforcement learning
- self-play training
- learned policy/value networks

---

# Project Structure

\`\`\`text
src/

├── agent/
│   ├── random_agent.py
│   ├── heuristic_agent.py
│   └── strategic_agent.py
│
├── cards/
│   ├── card_database.py
│   └── card_features.py
│
├── deckbuilding/
│   ├── deck.py
│   ├── deck_generator.py
│   ├── deck_validator.py
│   ├── deck_evaluator.py
│   │
│   ├── archetypes/
│   │   ├── evolution_heavy.py
│   │   ├── balanced.py
│   │   └── aggressive_ex.py
│   │
│   ├── pokemon/
│   │   ├── pool.py
│   │   ├── selector.py
│   │   ├── evolution.py
│   │   └── evolution_database.py
│   │
│   ├── trainers/
│   │   ├── pool.py
│   │   ├── selector.py
│   │   └── features.py
│   │
│   ├── energy/
│   │   └── selector.py
│   │
│   └── optimization/
│       ├── optimizer.py
│       └── search.py
│
├── environment/
│   └── ptcg_env.py
│
├── evaluation/
│   └── battle_stats.py
│
└── engine/
    └── cg/
\`\`\`

---

# Future Vision

The final objective is an autonomous Pokémon TCG AI capable of:

- understanding complex card interactions
- discovering strong decks
- planning multiple turns ahead
- optimizing strategies through search
- learning through self-play
- combining symbolic reasoning with machine learning

The long-term goal is to build an end-to-end Pokémon TCG agent capable of discovering strategies and competing autonomously against advanced opponents.