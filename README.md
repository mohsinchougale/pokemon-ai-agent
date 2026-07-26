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

## Current Benchmarks

| Matchup | Win Rate |
|---------|---------:|
| Strategic vs Random | **81.7%** |
| Strategic vs Heuristic | **87.7%** |

(1000 self-play games per matchup)

## Project Roadmap

### Phase 1 — Baseline Agents ✅
- Random agent
- Heuristic agent
- Strategic rule-based agent

### Phase 2 — Rich State Representation (Next)
- Expand feature engineering
- Parse full card database
- Build structured card knowledge base
- Improve strategic evaluation

### Phase 3 — Learning Agents
- Imitation learning from strategic agent
- Reinforcement learning through self-play
- Search-based methods (MCTS / rollout)

### Phase 4 — Deck Optimization
- Automated deck construction
- Evolutionary deck search
- Joint optimization of deck and policy