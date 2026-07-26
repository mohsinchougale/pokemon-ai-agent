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

Implemented multiple agent baselines.

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

## Current Benchmarks

| Matchup | Win Rate |
|---------|---------:|
| Strategic vs Random | **81.7%** |
| Strategic vs Heuristic | **87.7%** |

(1000 self-play games per matchup)

---

# Card Knowledge System

Implemented a structured card understanding pipeline.

The agent now interprets raw card metadata and converts every card into a collection of strategic features.

## Pokémon Features

Extracted features include:

- Card classification
- Evolution stage
- Previous evolution tracking
- HP statistics
- Attack parsing
- Maximum damage extraction
- Energy requirements
- Pokémon ex detection
- Ability detection

## Trainer & Energy Features

Supported functionality:

- Trainer classification
- Energy classification
- Card metadata lookup
- Fast card search utilities

---

# Evolution Knowledge System

Implemented evolution-aware reasoning.

Instead of treating every Pokémon independently, the agent now builds complete evolution chains.

Example:

```text
Froakie
   │
Frogadier
   │
Greninja ex
```

Current capabilities:

- ✅ Evolution stage linking
- ✅ Previous-stage resolution
- ✅ Evolution line construction
- ✅ Evolution database generation

Current database:

```text
336 evolution lines discovered
```

This allows future deck generation algorithms to reason about playable Pokémon cores instead of selecting isolated cards.

---

# Deck Construction System

Implemented a complete constraint-based deck generation framework.

Instead of randomly choosing 60 cards, the generator now constructs legal decks around predefined strategic archetypes.

## Deck Generation

Current capabilities:

- ✅ Random legal 60-card generation
- ✅ Card database integration
- ✅ Constraint-based deck construction
- ✅ Strategy-based Pokémon selection
- ✅ Evolution-aware deck building
- ✅ Trainer package selection
- ✅ Automatic energy allocation
- ✅ Complete archetype generation

## Implemented Archetypes

### Evolution Heavy

Focuses on:

- multiple evolution cores
- Stage 2 attackers
- evolution consistency

### Balanced

Focuses on:

- evolution lines
- standalone attackers
- consistency trainers
- balanced resources

### Aggressive EX

Focuses on:

- Pokémon ex
- high HP attackers
- high damage output
- fast offensive pressure

---

# Deck Evaluation System

Implemented a feature-based deck scoring engine.

Every generated deck is analyzed across multiple strategic dimensions.

## Composition Analysis

Measures:

- Pokémon / Trainer / Energy balance
- Basic Pokémon count
- Stage 1 count
- Stage 2 count

## Pokémon Quality

Measures:

- Average HP
- Average damage output
- Pokémon quality score
- Pokémon ex count

Unlike earlier versions, deck strength is no longer based only on HP and evolution consistency.

Attack damage is now incorporated into the evaluation, allowing stronger offensive decks to receive higher scores.

## Evolution Consistency

Analyzes:

- Evolution line detection
- Supported Stage 1 evolutions
- Supported Stage 2 evolutions
- Orphan evolution detection

Example evaluation:

```text
{
    pokemon_count: 15,
    energy_count: 15,
    trainer_count: 30,

    basic_pokemon: 9,
    stage1_pokemon: 5,
    stage2_pokemon: 1,

    average_hp: 171.6,
    average_damage: 122.4,

    pokemon_quality: 15,

    evolution_lines: 3,
    orphan_stage1: 1,
    orphan_stage2: 0,

    evolution_score: 19,

    deck_score: 114
}
```

---

# Deck Optimization

Implemented a mutation-based deck optimization engine.

Instead of evaluating only a single generated deck, the optimizer now searches through multiple candidate decks and keeps stronger variations.

## Current Optimization Strategy

Current workflow:

1. Generate an initial deck from an archetype
2. Apply deck mutations
3. Validate mutated decks
4. Evaluate strategic quality
5. Keep improvements using hill-climbing search
6. Track the best-performing deck

This forms the foundation for future evolutionary search algorithms.

## Optimization Results

Latest optimizer benchmark:

```text
EvolutionHeavyArchetype: 0/50 best=100
EvolutionHeavyArchetype: 10/50 best=103
EvolutionHeavyArchetype: 20/50 best=111
EvolutionHeavyArchetype: 30/50 best=111
EvolutionHeavyArchetype: 40/50 best=111

BalancedArchetype: 0/50 best=114
BalancedArchetype: 10/50 best=116
BalancedArchetype: 20/50 best=120
BalancedArchetype: 30/50 best=122
BalancedArchetype: 40/50 best=122

AggressiveEXArchetype: 0/50 best=100
AggressiveEXArchetype: 10/50 best=100
AggressiveEXArchetype: 20/50 best=100
AggressiveEXArchetype: 30/50 best=100
AggressiveEXArchetype: 40/50 best=100


====================
Optimization Results
====================

Rank: 1
Archetype: BalancedArchetype
Initial Score: 114
Best Score: 122
Improvements: 4
Iterations: 50
Deck Size: 60

Rank: 2
Archetype: EvolutionHeavyArchetype
Initial Score: 100
Best Score: 111
Improvements: 3
Iterations: 50
Deck Size: 60

Rank: 3
Archetype: AggressiveEXArchetype
Initial Score: 100
Best Score: 102
Improvements: 1
Iterations: 50
Deck Size: 60

====================
Optimization Complete
====================
```

The optimizer now:

- compares multiple archetypes
- mutates existing decks
- tracks best-performing variations
- measures improvement over initial decks
- ranks archetypes automatically

---

# Current Architecture

```text
                     Card Database
                           │
                           ▼

                Card Feature Extraction
                           │
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼

 Evolution Knowledge                 State Encoder
          │                                 │
          ▼                                 ▼

  Deck Construction                 Battle Agents
          │
          ▼

    Deck Evaluation
          │
          ▼

    Deck Optimizer
          │
          ▼

 Mutation Search + Archetype Ranking
          │
          ▼

 Pokémon TCG Simulator
          │
          ▼

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

## Phase 3 — Constraint-Based Deck Construction ✅

Completed:

- Evolution-core based Pokémon selection
- Constraint-based deck construction
- Balanced Pokémon / Trainer / Energy ratios
- Orphan evolution prevention
- Strategy-based deck archetypes
- Automated deck validation
- Energy requirement analysis

The system can now generate complete legal 60-card decks.

---

## Phase 4 — Deck Optimization ✅

Completed:

- Multi-archetype optimization
- Mutation-based deck optimizer
- Hill-climbing improvement search
- Best-deck tracking
- Improvement tracking
- Live optimization progress
- Automatic archetype comparison
- Archetype ranking system

Current capability:

The system can automatically improve generated decks instead of only evaluating static archetypes.

Upcoming:

- Advanced mutation strategies
- Crossover-based evolutionary search
- Population-based optimization
- Self-play driven evaluation
- Competitive deck discovery

---

## Phase 5 — Advanced AI Agents

Planned:

- Monte Carlo Tree Search (MCTS)
- Rollout-based planning
- Hidden-information reasoning
- Search-based battle planning
- Reinforcement learning through self-play
- Learned policy/value networks

---

# Project Structure

```text
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
│   ├── optimization/
│   │   ├── optimizer.py
│   │   └── search.py
│   │
│   ├── pokemon/
│   │   ├── pool.py
│   │   ├── selector.py
│   │   ├── scoring.py
│   │   ├── evolution.py
│   │   ├── evolution_builder.py
│   │   └── evolution_database.py
│   │
│   ├── trainers/
│   │   ├── pool.py
│   │   ├── selector.py
│   │   └── features.py
│   │
│   └── energy/
│       └── selector.py
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

- understanding complex card interactions
- constructing competitive decks
- planning multiple turns ahead
- optimizing decks through search
- adapting strategies through self-play
- combining symbolic reasoning with machine learning

Ultimately, the project aims to build a complete end-to-end Pokémon TCG AI capable of discovering strong decks, learning effective strategies, and competing autonomously against other advanced agents.