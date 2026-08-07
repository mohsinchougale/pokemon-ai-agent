# Pokémon TCG AI Agent

An autonomous Pokémon Trading Card Game AI built for Kaggle's **The Pokémon Company – PTCG AI Battle Challenge Simulation**.

This project develops an intelligent Pokémon TCG battle agent capable of interacting with the official competition simulator through:

- Rule-based strategic decision making
- Feature-driven game-state evaluation
- Combat analysis
- Board management
- Resource optimization
- Future search and learning-based improvements

The long-term goal is to evolve from handcrafted heuristics into an autonomous agent capable of planning, adapting, and improving through gameplay experience.

---

# Current Progress

## Environment & Simulation ✅

Successfully integrated the official Pokémon TCG simulator provided by the competition.

Completed:

- Simulator integration
- Observation parsing
- Action submission
- Replay generation
- Local battle execution
- Self-play evaluation framework
- Kaggle submission pipeline

The agent runs successfully both locally and inside the Kaggle environment.

---

# Battle Agents

## Random Agent ✅

Baseline agent that selects random legal actions.

Used for initial benchmarking and validating simulator integration.

---

## Heuristic Agent ✅

Rule-based agent using handcrafted action scoring.

Decision factors include:

- Attack damage
- Survival estimation
- Board state
- Action value estimation

Serves as an intermediate benchmark between random play and strategic reasoning.

---

## Strategic Agent V3 ✅

Current competition submission agent.

The Strategic Agent uses a structured feature-based decision system to evaluate game states and select actions.

Current capabilities:

### Board Evaluation

Analyzes:

- Active Pokémon state
- Bench development
- HP advantage
- Prize situation
- Opponent threats
- Game phase

### Combat Evaluation

Considers:

- Attack damage
- Knockout opportunities
- Opponent HP
- Survival after attacking

### Resource Management

Evaluates:

- Energy attachments
- Hand resources
- Card value
- Evolution opportunities
- Bench expansion

### Strategic Decisions

Supports:

- Attack selection
- Energy attachment decisions
- Card selection
- Evolution choices
- Attached card management
- Survival-oriented decisions

Strategic Agent V3 represents the first fully integrated strategic submission capable of completing full games inside the Kaggle simulation environment.

---

# Feature Engineering

A dedicated feature encoder converts raw simulator observations into structured game-state representations.

Current extracted features include:

## Game State

- Current turn
- Turn action count
- Game phase information

## Active Pokémon

- Current HP
- Maximum HP
- HP ratio
- Available attacks
- Energy requirements

## Resources

- Hand size
- Deck size
- Remaining prize cards
- Available energy

## Board State

- Active Pokémon
- Bench size
- Attached energy count
- Opponent board information

## Status Conditions

Tracks:

- Poison
- Burn
- Sleep
- Paralysis
- Confusion

## Turn Resources

Tracks:

- Energy attachment availability
- Supporter usage
- Stadium usage

These features provide a compact representation of the game state while remaining independent from raw simulator objects.

---

# Kaggle Integration

The project supports the complete competition workflow.

Completed:

- Competition-compatible submission structure
- Submission packaging
- Shared simulator dependency handling
- Local validation
- Replay generation
- Successful Kaggle execution

Strategic Agent V3 has successfully completed Kaggle simulation matches against independent agents.

---

# Evaluation

## Local Benchmark Results

| Matchup | Win Rate |
|---|---:|
| Strategic vs Random | **81.7%** |
| Strategic vs Heuristic | **87.7%** |

(1,000 local evaluation games per matchup)

These results demonstrate significant improvement over simpler baseline strategies.

---

## External Agent Evaluation 🚧

Initial external-agent matches have revealed new strategic limitations.

Observed areas for improvement:

- Attack prioritization
- Opening-game decisions
- Energy planning
- Retreat management
- Long-term planning
- Opponent modeling

Current efforts focus on replay analysis to identify cases where the agent makes legal but strategically weak decisions.

---

# Current Development Focus

## Replay Analysis & Strategic Improvement 🚧

The current priority is understanding agent behavior in realistic competitive environments.

Focus areas:

- Why attacks are selected or skipped
- Energy allocation decisions
- Evolution timing
- Retreat choices
- Bench management
- Opening strategy
- Resource conservation
- Opponent threat evaluation

The objective is improving the decision function rather than simply adding more rules.

---

# Project Roadmap

## Phase 1 — Baseline Agents ✅

Completed:

- Random Agent
- Heuristic Agent
- Strategic Agent

---

## Phase 2 — Environment Integration ✅

Completed:

- Simulator integration
- Observation parsing
- Feature extraction
- Local battle framework
- Kaggle submission pipeline

---

## Phase 3 — Strategic Agent V3 ✅

Completed:

- Feature-based decision making
- Combat evaluation
- Energy management
- Evolution logic
- Board evaluation
- Kaggle-compatible submission

---

## Phase 4 — Strategic Improvement 🚧

Current phase:

- Replay analysis
- Better attack selection
- Smarter retreat logic
- Improved opening decisions
- Improved evaluation functions
- Opponent-aware strategies

---

## Phase 5 — Search & Planning

Planned:

- Monte Carlo Tree Search (MCTS)
- Limited-depth planning
- Rollout evaluation
- Hidden-information reasoning

---

## Phase 6 — Machine Learning

Planned:

- Replay dataset generation
- Imitation learning
- Reinforcement learning
- Self-play training
- Policy networks
- Value networks

---

# Future Vision

The ultimate goal is to build a competitive Pokémon TCG AI capable of:

- Understanding complex board states
- Planning multiple turns ahead
- Managing hidden information
- Learning from gameplay experience
- Improving through self-play
- Combining symbolic reasoning with machine learning

The current Strategic Agent represents the first major step toward an autonomous Pokémon TCG AI system that can evolve beyond handcrafted heuristics and continuously improve through experience.