# BERT Attention Analysis

## Overview
This analysis examines how BERT's attention mechanism processes masked language modeling tasks.

## Key Findings

### Attention Patterns
- **Early Layers**: Attention tends to focus on syntactic relationships and local context
- **Middle Layers**: Attention begins to incorporate semantic relationships
- **Late Layers**: Attention often focuses on semantically related words that could fill the mask

### Observations
1. **Positional Bias**: BERT often attends more to tokens closer to the [MASK]
2. **Content Words**: Function words (the, of, to) typically receive less attention than content words
3. **Semantic Relationships**: In later layers, attention weights often correlate with semantic similarity

### Example Analysis
When analyzing the sentence "The [MASK] sat on the mat":
- Early layers focus on grammatical structure (determiners, prepositions)
- Middle layers begin to identify that [MASK] is likely a noun
- Later layers focus on semantically appropriate nouns (cat, dog, etc.)

### Head Specialization
Different attention heads in the same layer often specialize in different types of relationships:
- Some heads focus on syntactic dependencies
- Others capture semantic relationships
- Some attend to positional patterns

### Methodology
- Used BERT-base-uncased model with 12 layers and 12 attention heads per layer
- Analyzed attention weights both FROM and TO the [MASK] token
- Averaged attention across heads for layer-level analysis
- Examined individual heads in the final layer for head-specific patterns

## Implications
The attention patterns reveal how BERT processes contextual information to make predictions about masked tokens, providing insights into the model's internal representations and decision-making process. This analysis helps understand:

1. How contextual information flows through the transformer layers
2. The hierarchical nature of language understanding in BERT
3. The specialization of different attention heads
4. The progression from syntactic to semantic processing

## Technical Details
- Model: BERT-base-uncased (110M parameters)
- Architecture: 12 transformer layers, 12 attention heads per layer
- Vocabulary: 30,522 WordPiece tokens
- Context Length: 512 tokens maximum