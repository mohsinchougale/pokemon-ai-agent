# Pokémon TCG AI Agent

An autonomous Pokémon Trading Card Game AI built for Kaggle's **The Pokémon Company – PTCG AI Battle Challenge Simulation**.

This project aims to develop an intelligent battle agent capable of playing Pokémon TCG through simulation by combining:

- Rule-based decision making
- Strategic board evaluation
- Feature engineering
- Search and planning (future work)
- Reinforcement learning (future work)

The long-term objective is to evolve from handcrafted strategies into a fully autonomous agent that can learn and improve through gameplay experience.

---

# Current Progress

## Environment & Simulation ✅

Successfully integrated the official Pokémon TCG simulator provided by the competition.

Completed:

- Simulator integration
- Local battle execution
- Observation parsing
- Action submission
- Replay generation
- Self-play evaluation framework
- Kaggle submission pipeline

The agent can now run successfully both locally and on Kaggle.

---

# Battle Agents

## Random Agent ✅

Baseline agent that selects a random legal action.

Used as the initial benchmark for evaluating stronger agents.

---

## Heuristic Agent ✅

Rule-based agent that evaluates legal actions using handcrafted heuristics.

Decision factors include:

- Damage evaluation
- Survival estimation
- Board state analysis
- Action scoring

---

## Strategic Agent ✅

A feature-driven battle agent that uses structured game-state information to make decisions.

Current decision process includes:

- Board evaluation
- Active Pokémon health analysis
- Energy availability
- Hand and deck resources
- Prize tracking
- Bench evaluation
- Status conditions
- Turn-state awareness
- Action scoring

The Strategic Agent represents the current competition submission iteration and serves as the foundation for future improvements through stronger planning, search, and learned policies.

---

# Feature Engineering

A dedicated feature encoder converts raw simulator observations into structured numerical features for decision making.

Current extracted features include:

## Game State

- Current turn
- Turn action count

## Active Pokémon

- HP
- Maximum HP
- HP ratio

for both players.

## Resources

- Hand size
- Deck size
- Remaining prize cards

## Board State

- Bench size
- Attached energy count

## Status Conditions

- Poisoned
- Burned
- Asleep
- Paralyzed
- Confused

## Turn Resources

- Energy attachment availability
- Supporter usage
- Stadium usage

These features provide a compact representation of the current game state while remaining independent of the raw simulator objects.

---

# Kaggle Integration

The project supports the complete Kaggle competition workflow.

Completed:

- Submission packaging
- Competition-compatible project structure
- Local validation
- Replay generation
- Multiple successful Kaggle submissions
- Simulator compatibility

The current Strategic Agent has been successfully submitted multiple times to the competition leaderboard, with each iteration serving as a baseline for further improvements.

---

# Evaluation

## Local Benchmark Results

| Matchup | Win Rate |
|---------|---------:|
| Strategic vs Random | **81.7%** |
| Strategic vs Heuristic | **87.7%** |

(1,000 self-play games per matchup)

These benchmarks demonstrate that the Strategic Agent performs significantly better than simpler baseline policies in the local simulation environment.

However, competition results against external agents revealed limitations in the current strategy. The next development phase focuses on understanding agent behavior, analyzing gameplay decisions, and improving competitive performance.

---

# Current Development Focus

## Replay Analysis & Strategic Improvements 🚧

The current priority is moving beyond handcrafted heuristics and understanding how the agent actually plays.

Focus areas:

- Replay inspection
- Action selection analysis
- Attack prioritization
- Energy management
- Retreat decisions
- Bench management
- Opening-game strategy
- Resource conservation
- Opponent modeling
- Evaluation function improvements

The goal is to identify cases where the agent makes legal but strategically weak decisions and improve the underlying decision-making process.

---

# Project Roadmap

## Phase 1 — Baseline Agents ✅

Completed

- Random Agent
- Heuristic Agent
- Strategic Agent

---

## Phase 2 — Environment Integration ✅

Completed

- Simulator integration
- Observation parsing
- Feature extraction
- Local battle execution
- Kaggle submission pipeline

---

## Phase 3 — Strategic Agent Improvement 🚧

In Progress

- Replay analysis
- Better attack selection
- Smarter retreat logic
- Improved opening decisions
- Better board evaluation
- More effective resource management
- Opponent-aware strategies

---

## Phase 4 — Search & Planning

Planned

- Monte Carlo Tree Search (MCTS)
- Limited-depth planning
- Rollout evaluation
- Hidden-information reasoning

---

## Phase 5 — Machine Learning

Planned

- Replay collection
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
- Adapting to hidden information
- Learning directly from gameplay
- Improving through self-play
- Combining symbolic reasoning with machine learning

Rather than relying solely on handcrafted heuristics, the long-term vision is an autonomous agent that continually improves through experience while remaining compatible with the official Pokémon TCG simulator and Kaggle competition environment.