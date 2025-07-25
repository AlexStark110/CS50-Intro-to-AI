# MyCS50 - Complete Collection of CS50 AI Projects

This repository contains all the CS50 AI (AI50) projects from Harvard's Introduction to Artificial Intelligence with Python course. Each project demonstrates different concepts in artificial intelligence, machine learning, and computer science.

## Projects Overview

### 1. **Attention** 📱
- **Files**: `mask.py`, `analysis.md`
- **Concept**: Natural Language Processing with Transformers
- **Description**: Analyze BERT model attention mechanisms for masked language prediction

### 2. **Crossword** 🧩
- **Files**: `crossword.py`, `generate.py`
- **Concept**: Constraint Satisfaction Problems (CSPs)
- **Description**: Generate crossword puzzles using constraint satisfaction algorithms

### 3. **Degrees** 🎬
- **Files**: `degrees.py`, `util.py`
- **Concept**: Graph Search Algorithms
- **Description**: Find the shortest path between actors using breadth-first search (like "Six Degrees of Kevin Bacon")

### 4. **Heredity** 🧬
- **Files**: `heredity.py`
- **Concept**: Bayesian Networks and Probability
- **Description**: Calculate probabilities of genetic trait inheritance using Bayesian inference

### 5. **Knights** ⚔️
- **Files**: `logic.py`, `puzzle.py`
- **Concept**: Knowledge Representation and Logical Reasoning
- **Description**: Solve logic puzzles involving knights (who always tell the truth) and knaves (who always lie)

### 6. **Minesweeper** 💣
- **Files**: `minesweeper.py`, `runner.py`
- **Concept**: Logical Inference and Knowledge Representation
- **Description**: AI that can play Minesweeper using logical deduction

### 7. **Nim** 🎯
- **Files**: `nim.py`, `play.py`
- **Concept**: Adversarial Search and Game Theory
- **Description**: AI that learns to play the game of Nim using Q-learning

### 8. **PageRank** 🔗
- **Files**: `pagerank.py`
- **Concept**: Markov Models and Random Walks
- **Description**: Implement Google's PageRank algorithm to rank web pages

### 9. **Parser** 📝
- **Files**: `parser.py`
- **Concept**: Natural Language Processing and Context-Free Grammars
- **Description**: Parse sentences and extract noun phrases using natural language processing

### 10. **Shopping** 🛒
- **Files**: `shopping.py`
- **Concept**: Machine Learning and Classification
- **Description**: Predict whether a user will make a purchase based on browsing behavior

### 11. **Tic-Tac-Toe** ❌⭕
- **Files**: `tictactoe.py`, `runner.py`
- **Concept**: Minimax Algorithm and Game Theory
- **Description**: AI that plays optimal Tic-Tac-Toe using the minimax algorithm

### 12. **Traffic** 🚦
- **Files**: `traffic.py`
- **Concept**: Neural Networks and Computer Vision
- **Description**: Neural network to classify traffic signs using TensorFlow and computer vision

## Technologies Used

- **Python**: Primary programming language
- **TensorFlow/Keras**: Neural networks and deep learning
- **OpenCV**: Computer vision and image processing
- **PyGame**: Game interfaces and visualizations
- **scikit-learn**: Machine learning utilities
- **PIL (Pillow)**: Image processing
- **Transformers**: Natural language processing with BERT

## Key AI Concepts Covered

### Search Algorithms
- **Breadth-First Search** (Degrees)
- **Minimax with Alpha-Beta Pruning** (Tic-Tac-Toe)
- **Constraint Satisfaction** (Crossword)

### Machine Learning
- **Neural Networks** (Traffic, Shopping)
- **Reinforcement Learning** (Nim)
- **Supervised Learning** (Shopping, Traffic)

### Logic and Knowledge
- **Propositional Logic** (Knights, Minesweeper)
- **Bayesian Networks** (Heredity)
- **Knowledge Representation** (Multiple projects)

### Natural Language Processing
- **Context-Free Grammars** (Parser)
- **Transformer Models** (Attention)
- **Masked Language Modeling** (Attention)

### Probability and Statistics
- **Markov Models** (PageRank)
- **Bayesian Inference** (Heredity)
- **Random Sampling** (PageRank)

## Project Structure

```
ai50-projects/
├── attention/          # NLP with transformers
├── crossword/          # Constraint satisfaction
├── degrees/            # Graph search
├── heredity/           # Bayesian networks
├── knights/            # Logic puzzles
├── minesweeper/        # Logical inference
├── nim/                # Reinforcement learning
├── pagerank/           # Markov models
├── parser/             # Natural language parsing
├── shopping/           # Machine learning classification
├── tictactoe/          # Minimax algorithm
└── traffic/            # Neural networks & computer vision
```

## Getting Started

### Prerequisites
```bash
pip install tensorflow opencv-python pygame scikit-learn pillow transformers
```

### Running the Projects

Each project can be run independently. For example:

```bash
# Play Tic-Tac-Toe against AI
cd ai50-projects/tictactoe
python runner.py

# Train traffic sign classifier
cd ai50-projects/traffic
python traffic.py data_directory

# Find degrees of separation between actors
cd ai50-projects/degrees
python degrees.py large
```

## Academic Integrity

These projects were completed as part of Harvard's CS50 AI course. They are shared for educational purposes and to demonstrate AI concepts. If you're currently taking the course, please follow your institution's academic integrity policies.

## Course Information

- **Course**: CS50's Introduction to Artificial Intelligence with Python
- **Institution**: Harvard University
- **Platform**: edX / CS50
- **Topics**: Search, Knowledge, Uncertainty, Optimization, Learning, Neural Networks, Language

## License

Educational use only. Please respect academic integrity policies if you're currently enrolled in CS50 AI.

---

**Note**: This repository represents a complete collection of CS50 AI projects, showcasing the breadth of artificial intelligence concepts covered in Harvard's renowned computer science curriculum.
