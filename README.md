# Pokémon TCG AI Agent

Building an autonomous Pokémon Trading Card Game agent for the Kaggle  
**"The Pokémon Company – PTCG AI Battle Challenge Simulation."**

## Current Progress

### Environment
- ✅ Project setup
- ✅ Simulator integration
- ✅ Local battle execution

### Agents
- ✅ Random baseline agent
- ✅ Heuristic rule-based agent
- ✅ Strategic feature-based agent

### Evaluation
- ✅ Benchmark framework
- ✅ Automated agent-vs-agent evaluation
- ✅ Performance statistics (win rate & average game length)

### Data & Features
- ✅ Card metadata utilities
- ✅ Observation exploration tools
- ✅ State encoder for ML agents
- ✅ Card feature extraction pipeline
- ✅ Pokémon / Trainer / Energy classification
- ✅ Attack parsing and filtering
- ✅ Damage and energy cost extraction
- ✅ Ability and Pokémon ex detection
- ✅ Card metadata normalization

## Current Benchmarks

| Matchup | Win Rate |
|---------|---------:|
| Strategic vs Random | **81.7%** |
| Strategic vs Heuristic | **87.7%** |

*(1000 agent-vs-agent simulations per matchup)*

## Current Architecture

    Card Database
          |
          v
    Card Feature Extractor
          |
          v
    Strategic Agent
          |
          v
    Battle Simulator
          |
          v
    Evaluation Framework

The current strategic agent uses extracted card knowledge and game-state features to make rule-based decisions during battles.

## Project Roadmap

### Phase 1 — Baseline Agents ✅
- Random agent
- Heuristic agent
- Strategic rule-based agent

### Phase 2 — Strategic Understanding (In Progress)
- Expand card feature engineering
- Build deck evaluation framework
- Analyze card synergy and deck composition
- Improve action evaluation logic
- Add richer game-state representations

### Phase 3 — Advanced Decision Making
- Search-based methods (MCTS / rollout)
- Simulation-based action planning
- Improved strategy evaluation

### Phase 4 — Learning Agents
- Generate self-play datasets
- Imitation learning from expert agents
- Reinforcement learning through self-play
- Policy/value-based agents

### Phase 5 — Deck Optimization
- Automated deck construction
- Evolutionary deck search
- Joint optimization of deck and policy