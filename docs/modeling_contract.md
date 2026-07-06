# Adaptive Interview Coach — V1 Modeling Contract

## 1. Purpose

Adaptive Interview Coach recommends candidate practice problems for a user based on their study history and the candidate problem's attributes.

V1 is a candidate-scoring recommendation system.

For each eligible candidate problem, the model estimates:

```text
P(candidate_problem is solved within 7 days
  | candidate_problem was shown to the user at as_of_ts)
```

The system ranks candidate problems by this predicted probability and returns the highest-scoring recommendations.

This is a predictive recommendation proxy. V1 estimates which shown candidate is most likely to be solved based on historical behavior and candidate metadata. It does not estimate the causal lift of recommending one problem instead of another.

---

## 2. Unit of Prediction

One training row represents:

```text
one user
+ one candidate problem
+ one historical decision point
```

Formally:

```text
(user_id, candidate_problem_id, as_of_ts)
```

At `as_of_ts`, the system hypothetically shows the candidate problem to the user and predicts whether that candidate will be solved during the following seven days.

A `prediction_instance` represents the decision point for a user.

A `training_example` represents one candidate shown at that prediction instance.

---

## 3. Prediction Target and Label

### Target

```text
candidate_solved_7d
```

### Label definition

```text
candidate_solved_7d = 1
```

when the candidate was shown at `as_of_ts` and the user solves that specific candidate problem during:

```text
(as_of_ts, as_of_ts + 7 days]
```

Otherwise:

```text
candidate_solved_7d = 0
```

A zero means:

```text
the candidate was shown but was not solved during the seven-day label window
```

It does not mean that every unobserved or unshown problem is a negative example.

### Delayed outcomes

These are outcomes that occur after the prediction decision:

```text
candidate_attempted_7d
candidate_solved_7d
```

They are stored for diagnostics, evaluation, and future ranking improvements.

They must never be model input features for the same training row.

---

## 4. Candidate Policy

For every decision point, the system generates a deterministic eligible candidate set.

The candidate policy may use only:

```text
- the active problems catalog
- user events with event.ts <= as_of_ts
- candidate metadata such as topic and difficulty
- a fixed candidate_generation_version
- a fixed random seed when sampling is needed
```

The candidate policy must not use:

```text
- future attempts
- future solves
- candidate_solved_7d
- any event with ts > as_of_ts
```

Initial candidate policy:

```text
- Start from active problems.
- Exclude problems solved recently by the user.
- Prefer a mix of weak-topic candidates, review candidates, and difficulty-appropriate candidates.
- Generate up to 20 eligible candidates per prediction instance.
- Keep candidate generation deterministic for the same
  (user_id, as_of_ts, candidate_generation_version).
```

The same candidate-generation module must be used for historical training replay and live serving.

---

## 5. Feature Cutoff Rule

Every feature is computed strictly as of the decision time.

```text
A feature for (user_id, candidate_problem_id, as_of_ts)
may use only events where:

event.ts <= as_of_ts
```

Features must never read events after `as_of_ts`.

### User-state feature examples

```text
- rolling 7-day accuracy by topic
- days since last attempt
- days since last attempt in candidate topic
- current study streak
- recent attempt count
- recent average minutes spent
- prior solve rate by difficulty
```

### Candidate feature examples

```text
- candidate topic tag
- candidate difficulty
- whether the user previously attempted the candidate
- user accuracy for the candidate topic
- user difficulty fit
- candidate matches weak topic
```

Feature functions should conceptually follow this signature:

```text
build_features(
    user_id,
    candidate_problem_id,
    as_of_ts
)
```

---

## 6. Temporal Dataset Construction

Historical training data is created by replaying past decision points.

For each valid user decision point:

```text
1. Select as_of_ts.
2. Build the shown candidate set using only information available by as_of_ts.
3. Build features using only events at or before as_of_ts.
4. Inspect the following seven days.
5. Assign candidate_solved_7d for each shown candidate.
```

A training example must not be created when the full seven-day future label window is unavailable.

```text
as_of_ts + 7 days <= maximum available event timestamp
```

Each prediction instance must have at least three prior study events.

---

## 7. Train, Validation, and Test Splits

Splits are time-based using `prediction_instances.as_of_ts`.

Random row splits are prohibited because they can leak future user behavior into training.

A seven-day embargo separates each split because labels look seven days into the future.

Example:

```text
Training cutoffs: through January 31
Embargo: February 1 through February 7
Validation cutoffs: begin February 8
```

The same rule applies between validation and test.

---

## 8. Model and Ranking Behavior

V1 uses a `LightGBMClassifier`.

For each candidate, the model outputs:

```text
P(candidate_solved_7d = 1)
```

The recommendation system ranks candidates by sorting this score in descending order.

```text
candidate score
→ sort descending
→ top-k recommendations
```

V1 is a classifier used as a recommendation scorer.

A future V2 may use logged real recommendation impressions and a true learning-to-rank objective such as `LightGBMRanker`.

---

## 9. Evaluation Metrics

### Candidate-level classification metrics

```text
- PR-AUC
- ROC-AUC
- calibration
```

PR-AUC is important because solved candidates are expected to be less common than unsolved candidates.

### Recommendation-list metrics

Candidate rows are grouped by `prediction_instance_id`.

```text
- NDCG@3
- HitRate@3
```

NDCG@3 is calculated only for candidate groups containing at least one positive label.

The evaluation report must also include:

```text
- total prediction-instance groups
- eligible ranking groups
- groups containing at least one positive label
- NDCG coverage
```

---

## 10. Event-Time Policy

Each study event has two timestamps:

```text
study_events.ts
```

When the study behavior actually happened.

```text
study_events.ingested_at
```

When the platform received or recorded the event.

### V1 late-event policy

The system accepts events up to seven days late.

When a late event is accepted:

```text
- Persist the raw event.
- Refresh current online features.
- Invalidate or refresh current recommendations if needed.
- Do not silently mutate an already-versioned historical training dataset,
  feature snapshot, or completed model run.
```

Historical datasets are immutable once versioned.

A later training run may deliberately regenerate a newer dataset version that incorporates accepted late events.

---

## 11. Training-Serving Parity

Offline training replay and online serving must use:

```text
- the same candidate-generation policy
- the same feature transformations
- the same feature definitions
- the same feature-set version
```

Parity tests must verify that the same `(user_id, candidate_problem_id, as_of_ts)` produces matching offline and online feature values and the same eligible candidate set.

---

## 12. Out of Scope for V1

V1 does not claim to estimate:

```text
- causal lift from showing a recommendation
- long-term learning outcomes
- whether a user would solve a problem if it were not shown
- true learning-to-rank performance from real user impressions
```

Those become future work after the platform collects real recommendation-run and interaction logs.
