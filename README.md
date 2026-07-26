# Pokémon TCG AI Agent

Building an autonomous Pokémon Trading Card Game agent for the Kaggle  
**"The Pokémon Company – PTCG AI Battle Challenge Simulation."**

The goal of this project is to develop an AI agent capable of playing Pokémon TCG through simulation, combining:
- rule-based strategies
- structured card understanding
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

## Agents

- ✅ Random baseline agent
- ✅ Heuristic rule-based agent
- ✅ Strategic feature-based agent

Current strategic agent uses:
- board state evaluation
- Pokémon strength heuristics
- attack selection logic
- survival/value estimation

---

## Card Knowledge System

Implemented structured card understanding pipeline.

Features extracted:

### Pokémon Features
- Card type classification
- Evolution stage
- Previous evolution tracking
- HP statistics
- Attack parsing
- Damage estimation
- Energy requirements
- Pokémon ex detection
- Ability detection

### Trainer/Energy Features
- Trainer classification
- Energy classification
- Card metadata lookup utilities

---

## Deck Generation & Evaluation

Implemented a deck analysis framework.

Current capabilities:

### Deck Generation
- ✅ Random deck generation
- ✅ Valid 60-card deck construction
- ✅ Card database integration

### Deck Evaluation

Evaluates:

- Pokémon / Trainer / Energy balance
- Basic / Stage 1 / Stage 2 distribution
- Evolution consistency
- Orphan evolution detection
- Pokémon quality
- Average HP
- Average damage output
- ex Pokémon count

Example evaluation output:

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

        |
        v

Card Database
        |
        v

Card Feature Extraction
        |
        |
        +----------------+
        |                |
        v                v

State Encoder      Deck Evaluator
        |                |
        |                |
        v                v

AI Agents       Deck Generation
        |
        v

Battle Simulator
        |
        v

Evaluation Framework
```

---

# Current Benchmarks

| Matchup | Win Rate |
|---------|---------:|
| Strategic vs Random | **81.7%** |
| Strategic vs Heuristic | **87.7%** |

(1000 self-play games per matchup)

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
- Evolution analysis
- Deck evaluation framework

---

## Phase 3 — Constraint-Based Deck Generation (Next)

Goals:

- Generate playable evolution lines
- Avoid orphan evolutions
- Balance Pokémon / Trainer / Energy ratios
- Prefer synergistic card combinations

Planned components:

- Evolution line database
- Constraint-based deck builder
- Deck scoring optimization

---

## Phase 4 — Deck Optimization

Planned:

- Genetic algorithm deck search
- Mutation and crossover strategies
- Automated deck improvement
- Optimized decks for self-play training

---

## Phase 5 — Advanced AI Agents

Planned:

- Monte Carlo Tree Search (MCTS)
- Rollout-based planning
- Imitation learning
- Reinforcement learning through self-play

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
│   └── evolution.py
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

The final objective is an autonomous Pokémon TCG agent that can:

- understand card interactions
- construct competitive decks
- plan multiple turns ahead
- adapt strategies through self-play
- combine search and learning-based approaches
