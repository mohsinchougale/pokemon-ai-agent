# Pokémon TCG AI Agent

Building an autonomous Pokémon Trading Card Game agent for the Kaggle  
**"The Pokémon Company – PTCG AI Battle Challenge Simulation."**

The goal of this project is to develop an AI agent capable of playing Pokémon TCG through simulation, combining:

- rule-based strategies
- structured card understanding
- evolution-aware deck construction
- deck optimization
- search-based decision making
- reinforcement learning

---

# Current Progress

## Environment & Simulation

- ✅ Project setup
- ✅ Pokémon TCG simulator integration
- ✅ Local battle execution
- ✅ Observation exploration tools
- ✅ Evaluation framework

---

# Agents

Implemented multiple agent baselines:

## Random Agent ✅

Simple random action selection baseline used for benchmarking.

## Heuristic Agent ✅

Rule-based decision making using:

- available action evaluation
- damage opportunities
- survival considerations
- basic board value estimation

## Strategic Agent ✅

Feature-driven agent using:

- board state evaluation
- Pokémon strength heuristics
- attack selection logic
- survival/value estimation
- strategic scoring functions

Current benchmarks:

| Matchup | Win Rate |
|---------|---------:|
| Strategic vs Random | **81.7%** |
| Strategic vs Heuristic | **87.7%** |

(1000 self-play games per matchup)

---

# Card Knowledge System

Implemented a structured card understanding pipeline.

The agent can now interpret card metadata and extract strategic information.

## Pokémon Features

Extracted features:

- Card classification
- Evolution stage
- Previous evolution tracking
- HP statistics
- Attack parsing
- Damage estimation
- Energy requirements
- Pokémon ex detection
- Ability detection

## Trainer & Energy Features

Supported:

- Trainer classification
- Energy classification
- Card metadata lookup
- Card search utilities

---

# Evolution Knowledge System

Implemented evolution-aware card reasoning.

The system now builds structured Pokémon evolution chains.

Example:

```
Froakie
   |
Frogadier
   |
Greninja ex
```

Current capabilities:

- ✅ Evolution stage linking
- ✅ Previous-stage resolution
- ✅ Evolution line construction
- ✅ Evolution database generation

Current database:

```
336 evolution lines discovered
```

This allows future deck generation algorithms to reason about playable Pokémon cores instead of selecting isolated cards.

---

# Deck Generation & Evaluation

Implemented a complete deck analysis framework.

## Deck Generation

Current capabilities:

- ✅ Random 60-card deck generation
- ✅ Card database integration
- ✅ Valid deck construction

## Deck Evaluation

Evaluates:

### Composition

- Pokémon / Trainer / Energy balance
- Basic Pokémon count
- Stage 1 Pokémon count
- Stage 2 Pokémon count

### Pokémon Strength

- Average HP
- Average damage output
- Pokémon quality score
- ex Pokémon count

### Evolution Consistency

- Evolution line detection
- Supported Stage 1 evolutions
- Supported Stage 2 evolutions
- Orphan evolution detection

Example output:

```text
{
pokemon_count: 15,
energy_count: 15,
trainer_count: 30,

basic_pokemon: 9,
stage1_pokemon: 5,
stage2_pokemon: 1,

evolution_lines: 1,

orphan_stage1: 4,
orphan_stage2: 1,

pokemon_quality: 6,
evolution_score: -10,

deck_score: 66
}
```

---

# Current Architecture

```
Pokemon TCG AI Agent


                 Card Database
                       |
                       v

             Card Feature Extraction
                       |
        +--------------+--------------+
        |                             |
        v                             v

 Evolution Knowledge            State Encoder
        |                             |
        v                             v

 Deck Generation              Battle Agents
        |
        v

 Deck Evaluation
        |
        v

 Deck Optimization


                       |
                       v

              Pokémon TCG Simulator

                       |
                       v

            Evaluation Framework
```

---

# Project Roadmap


## Phase 1 — Baseline Agents ✅

Completed:

- Random agent
- Heuristic agent
- Strategic rule-based agent


---

## Phase 2 — Card Understanding & Evaluation ✅

Completed:

- Card metadata pipeline
- Feature extraction
- Attack parsing
- Ability detection
- Evolution analysis
- Evolution database
- Deck evaluation framework


---

# Phase 3 — Constraint-Based Deck Generation 🚧

Current focus.

Goal:

Move from random decks to strategically meaningful decks.

Planned:

- Evolution-core based Pokémon selection
- Constraint-based deck construction
- Balanced Pokémon / Trainer / Energy ratios
- Avoid orphan evolutions
- Synergistic card selection
- Automated deck scoring


Example:

Instead of:

```
Random Pokémon:
- Greninja ex
- Charizard
- Magcargo ex
- Random Stage 1 cards
```

Generate:

```
Evolution Core:

Froakie
   |
Frogadier
   |
Greninja ex


+
Supporting trainers
+
Required energy package
+
Consistency cards
```


---

# Phase 4 — Deck Optimization

Planned:

- Evolutionary deck search
- Mutation strategies
- Crossover strategies
- Self-play based deck improvement
- Automated competitive deck discovery


---

# Phase 5 — Advanced AI Agents

Planned:

- Monte Carlo Tree Search (MCTS)
- Rollout-based planning
- Imitation learning
- Reinforcement learning through self-play
- Learned policy networks


---

# Project Structure

```
src/

├── agent/
│   ├── random_agent.py
│   ├── heuristic_agent.py
│   └── strategic_agent.py
│
├── cards/
│   ├── card_database.py
│   ├── card_features.py
│   ├── deck.py
│   ├── deck_generator.py
│   ├── deck_evaluator.py
│   ├── evolution.py
│   ├── evolution_builder.py
│   └── evolution_database.py
│
├── environment/
│   └── ptcg_env.py
│
├── evaluation/
│   └── battle_stats.py
│
├── features/
│   └── state_encoder.py
│
└── engine/
    └── cg/
```

---

# Future Vision

The final objective is an autonomous Pokémon TCG agent capable of:

- understanding card interactions
- constructing competitive decks
- planning multiple turns ahead
- optimizing decks through search
- adapting strategies through self-play
- combining symbolic reasoning with machine learning

The long-term goal is a complete AI system that can discover, evaluate, and play Pokémon TCG strategies autonomously.