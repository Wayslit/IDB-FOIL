# IDB-FOIL

**IDB-FOIL: Iterative Dual-Branch Inductive Logic Learning for Automated and Interpretable Image Labeling** — A neuro-symbolic framework that extends the classical FOIL paradigm with iterative dual-branch learning and decayed predicate selection metrics for fully automated inference of interpretable labeling rules.

![Overview of IDB-FOIL for automatic image labeling](picture/Overview%20of%20IDB-FOIL%20for%20automatic%20image%20labeling.jpg)

---

## Overview

IDB-FOIL is a neuro-symbolic framework that combines the perceptual strength of deep models with the interpretability of rule-based reasoning for fully automated image labeling. It addresses the key limitation of existing rule-based approaches that still rely on human guidance to define or refine labeling rules, by extending the classical FOIL paradigm through two complementary learning branches:

1. **Information-guided branch** — Favors frequent, high-information predicates, prioritizing predicates that cover more positive examples and carry greater information gain.
2. **Balanced branch** — Treats frequent and infrequent predicates equally, ensuring coverage of rare but discriminative patterns.

The two branches interact iteratively under **decayed predicate selection metrics**, which penalize overused or replaceable predicates to promote diversity and novel rule discovery. Furthermore, a **tf–idf–weighted voting scheme** is introduced to resolve label conflicts and enhance decision reliability.

The learned rules take the form of disjunctions of conjunctions (DNF), e.g.:

```
teacher(X): wall(X,B) ∧ screen(X,I) ∨ wall(X,B) ∧ chair(X,K) ∨ hair(X,C) ∧ woman(X,D) ∧ floor(X,E) ∨ ...
```

These rules are fully interpretable and can be directly inspected, validated, and modified by domain experts — while eliminating the need for human intervention in rule learning.

---

## Key Features

- **Iterative Dual-Branch Learning** — Runs two complementary FOIL learning branches iteratively: an information-guided branch (`foil_gain_v1`) that favors frequent, high-information predicates, and a balanced branch (`foil_gain_v2`) that treats frequent and infrequent predicates equally.
- **Decayed Predicate Selection Metrics** — Penalizes overused or replaceable predicates across iterations via a cohesion-based decay factor, promoting diversity and novel rule discovery.
- **TF-IDF Weighted Voting** — Introduces a tf–idf–weighted voting scheme to resolve label conflicts among multiple rules, enhancing decision reliability.
- **Fully Automated Rule Inference** — Eliminates the need for human intervention in rule learning, achieving high labeling accuracy, rule diversity, and interpretability.
- **Multi-Domain Support** — Built-in support for four distinct domains with domain-specific FOIL and labeling modules, spanning both specialized (medical) and general visual domains.
- **Interpretable Output** — Produces human-readable DNF rules and per-class accuracy metrics in YAML format.

---

## Environment Dependencies

- **Python** >= 3.7
- **NumPy** (`numpy`)
- **PyYAML** (`pyyaml`)

Install dependencies:

```bash
pip install numpy pyyaml
```

---

## Installation

```bash
git clone https://github.com/Wayslit/IDB-FOIL.git
cd IDB-FOIL
pip install numpy pyyaml
```

---

## Configuration

All configuration is managed in `utils/config.py`:

```python
class Config:
    # Dataset paths
    trainset_path = "data/Glaucoma/Glaucoma_train.json"
    testset_path  = "data/Glaucoma/Glaucoma_test.json"

    # Output directory for final results
    output_dir = "output"

    # Intermediate files directory
    middle_dir = "middle"

    # Number of FOIL iterations
    iter_times = 5

    # Task type: "Glaucoma" | "Bird" | "Occupation" | "Traffic"
    task_type = "Glaucoma"
```

To switch domains, modify `trainset_path`, `testset_path`, and `task_type` accordingly:

| Task | `trainset_path` | `testset_path` | `task_type` |
|---|---|---|---|
| Glaucoma | `data/Glaucoma/Glaucoma_train.json` | `data/Glaucoma/Glaucoma_test.json` | `"Glaucoma"` |
| Bird | `data/Bird/bird_train.json` | `data/Bird/bird_test.json` | `"Bird"` |
| Occupation | `data/Occupation/occupation_train.json` | `data/Occupation/occupation_test.json` | `"Occupation"` |
| Traffic | `data/Traffic/traffic_train.json` | `data/Traffic/traffic_test.json` | `"Traffic"` |

---

## Usage

### Run with default configuration

```bash
python main.py
```

### Run a different domain

Edit `utils/config.py` to set the desired task, then:

```bash
python main.py
```

### What happens during execution

For each iteration `i` (1 to `iter_times`):

1. **Information-Guided Branch** — Run FOIL with information-theoretic gain (`foil_gain_v1`), which favors frequent, high-information predicates. Save rules to `middle/rules_v1_{i}.yaml`.
2. **Balanced Branch** — Run FOIL with frequency-based gain (`foil_gain_v2`), which treats frequent and infrequent predicates equally. Save rules to `middle/rules_v2_{i}.yaml`.
3. **Branch Aggregation** — Merge v1 and v2 rules (deduplication) into `middle/rules_{i}.yaml`.
4. **Full Aggregation** — Merge all iterations' rules (1 to i) into `middle/rules_all_from_1_to_{i}.yaml`.
5. **Score & Evaluate** — Compute tf–idf scores and test-set accuracy for each rule set; apply tf–idf weighted voting to resolve label conflicts.

After the final iteration, results are copied to the `output/` directory.

---

## Output

The `output/<task>_output/` directory contains:

| File | Description |
|---|---|
| `labeling_rules.yaml` | Final learned DNF rules for each class |
| `rules_clause_score.yaml` | tf–idf scores for each rule clause |
| `Labeling_Accuracy_for_{N}_iter.yaml` | Per-class accuracy and average accuracy |

Example output (Glaucoma):

```yaml
# labeling_rules.yaml
gdrishti(X): ACDR(X,A)∧area(A,N)∧threshold(N,0.439,10000) ∨ HCDR(X,A)∧area(A,N)∧threshold(N,0.575,10000) ∨ ...
ndrishti(X): ACDR(X,A)∧area(A,N)∧threshold(N,0,0.304) ∨ HCDR(X,A)∧area(A,N)∧threshold(N,0,0.517) ∨ ...

# Labeling_Accuracy_for_5_iter.yaml
average_accuray: 0.8188
gdrishti(X): 0.7667
ndrishti(X): 0.8710
```

---

## Algorithm Details

### FOIL Gain Functions

- **v1 (Information-Guided Branch):** `gain = now_p × (log₂(now_p/(now_p+now_n)) - log₂(pre_p/(pre_p+pre_n)))` — Favors frequent, high-information predicates.
- **v2 (Balanced Branch):** `gain = now_p / (now_p + now_n)` — Treats frequent and infrequent predicates equally.

### Decayed Predicate Selection Metrics

For each predicate `p`, the decay factor is computed as:

```
decay(p) = θ^(Cohesion(T_p) + ε)
```

where `θ = 0.95`, `ε = 1e-5`, and `Cohesion(T_p)` is the average pairwise Jaccard similarity among positive instances covered by predicate `p`.

The effective gain at iteration `i` becomes: `effective_gain = foil_gain × decay(p)^(count(p))`, where `count(p)` is the number of times `p` appeared in prior iterations' rule bases.

This mechanism penalizes overused or replaceable predicates, promoting diversity and novel rule discovery across iterations.

### TF-IDF Weighted Voting

When multiple learned rules assign conflicting labels to the same instance, a tf–idf–weighted voting scheme resolves the conflict. Each rule's vote is weighted by its tf–idf score, which reflects the rule's discriminative power — rules that are more specific to a class receive higher weight, enhancing decision reliability.

## Data Format

Input data is stored in JSON format. Each entry contains:

- `imageId`: Unique identifier
- `type`: Class label
- `object_detect`: Detected objects, spatial features, or attributes (domain-specific)

**Example (Glaucoma):**
```json
{
    "imageId": 1,
    "type": "gdrishti",
    "object_detect": {
        "space": {
            "OD": 64251, "OC": 27981,
            "HCup": 177, "HDisc": 281,
            "VCup": 199, "VDisc": 291
        }
    }
}
```

**Example (Occupation/Traffic):**
```json
{
    "imageId": "63477ea6e69f25e2eb46e190",
    "type": "cook",
    "object_detect": {
        "object": { "0": {"name": "stove", "coordinate": [...]} },
        "overlap": { ... },
        "panoptic_segmentation": { ... }
    }
}
```

---

## Citation

This work is built upon [RAPID](https://github.com/Neural-Symbolic-Image-Labeling/Rapid) (KDD 2023). If you find this project useful, please cite:

```bibtex
@inproceedings{
  wang2023rapid,
  title={Rapid Image Labeling via Neuro-Symbolic Learning},
  author={Wang, Yifeng and Tu, Zhi and Xiang, Yiwen and Zhou, Shiyuan and Chen, Xiyuan and Li, bingxuan and Zhang, Tianyi},
  booktitle={29th SIGKDD Conference on Knowledge Discovery and Data Mining - Research Track},
  year={2023},
}
```

---

## License

This project is licensed under the MIT License.
