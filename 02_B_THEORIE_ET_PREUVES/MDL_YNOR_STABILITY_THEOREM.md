# Dissipative Stability of Autoregressive Probabilistic Flows via Information Projection: The Ynor Framework

## Abstract

We introduce a theoretical framework for the stability analysis of autoregressive probabilistic systems, motivated by large language model (LLM) generation dynamics. The system is modeled as a stochastic process evolving in the Wasserstein space $\mathcal{W}_2(\mathcal{H})$, where $\mathcal{H}$ is a high-dimensional Hilbert space of semantic embeddings.

We define a control operator $\mathcal{T}_\mu$ as a Kullback–Leibler (KL) projection onto a convex admissible set $\mathcal{C}_{\mathrm{Ynor}}$, representing structural constraints (e.g., governance or canonical priors). Under a quantitative dissipation hypothesis ($H_\alpha$), we prove that this projection induces a strict contraction of the KL divergence toward a reference distribution $P^*$.

We establish discrete Grönwall-type bounds, global stability, non-explosion of entropy, and asymptotic convergence under summable noise. The results provide a formal basis for controlling divergence in autoregressive generative systems and suggest a geometric interpretation of stability via entropic curvature.

---

## 1. Introduction

Autoregressive generative models, such as large language models, produce sequences via iterative sampling from conditional probability distributions. While effective, these systems may exhibit instability phenomena, often described as *hallucinations*, corresponding to divergence from a desired semantic or probabilistic target.

We propose a mathematical framework in which such systems are modeled as stochastic processes on the space of probability measures. Stability is analyzed in terms of the Kullback–Leibler divergence to a reference distribution $P^*$, interpreted as a canonical or target distribution.

Our central idea is to enforce stability via a projection operator onto a structured admissible set $\mathcal{C}_{\mathrm{Ynor}}$, inducing dissipative dynamics. The resulting system admits rigorous analysis using tools from information geometry, convex analysis, and discrete dynamical systems.

---

## 2. Mathematical Framework

### Definition 1 (State Space)

Let $\mathcal{H}$ be a separable Hilbert space. Denote by $\mathcal{P}(\mathcal{H})$ the set of Borel probability measures on $\mathcal{H}$, endowed with the Wasserstein topology $\mathcal{W}_2$.

Let $P^* \in \mathcal{P}(\mathcal{H})$ be a reference probability measure.

Define the energy functional:
$$
E(P) := D_{KL}(P \,||\, P^*).
$$

---

### Definition 2 (Autoregressive Process)

Let $(P_n)_{n \ge 0} \subset \mathcal{P}(\mathcal{H})$ be a sequence of probability measures.

At each step:

1. A stochastic generator produces a raw distribution $Q_{n+1}$,
2. A control operator $\mathcal{T}_\mu$ yields:
   $$
   P_{n+1}^\mu = \mathcal{T}_\mu(Q_{n+1}).
   $$

---

### Definition 3 (Ynor Operator: KL Projection)

Let $\mathcal{C}_{\mathrm{Ynor}} \subset \mathcal{P}(\mathcal{H})$ be a convex, closed subset such that:
$$
P^* \in \mathcal{C}_{\mathrm{Ynor}}.
$$

Define:
$$
\mathcal{T}_\mu(Q) := \Pi_{\mathcal{C}_{\mathrm{Ynor}}}(Q)
:= \arg\min_{P \in \mathcal{C}_{\mathrm{Ynor}}} D_{KL}(P \,||\, Q).
$$

---

## 3. Dissipative Dynamics

### Lemma 1 (Discrete Grönwall Inequality)

Let $(E_n)$ satisfy:
$$
E_{n+1} \le (1-\mu)E_n + \varepsilon_n, \quad \mu \in (0,1].
$$

Then:
$$
E_n \le (1-\mu)^n E_0 + \sum_{j=0}^{n-1}(1-\mu)^{n-1-j}\varepsilon_j.
$$

If $\varepsilon_n \le \bar{\varepsilon}$, then:
$$
\limsup_{n \to \infty} E_n \le \frac{\bar{\varepsilon}}{\mu}.
$$

---

### Lemma 2 (Asymptotic Convergence)

If:
$$
\sum_{n=0}^{\infty} \varepsilon_n < \infty,
$$
then:
$$
E_n \to 0.
$$

---

## 4. Information Projection and Dissipation

### Lemma 3 (Information Projection Inequality)

Let $P^\mu = \Pi_{\mathcal{C}_{\mathrm{Ynor}}}(Q)$. Then, under suitable regularity assumptions, the projection satisfies:
$$
D_{KL}(P^\mu \,||\, Q) \le D_{KL}(P \,||\, Q), \quad \forall P \in \mathcal{C}_{\mathrm{Ynor}}.
$$

In particular, since $P^* \in \mathcal{C}_{\mathrm{Ynor}}$,
$$
D_{KL}(P^\mu \,||\, Q) \le D_{KL}(P^* \,||\, Q).
$$

---

## 5. Strong Entropic Curvature Condition

### Hypothesis ($H_\alpha$) (Quantitative Dissipation)

There exists $\alpha > 0$ such that for all admissible $Q$,
$$
D_{KL}(Q \,||\, P^\mu) \ge \alpha \, D_{KL}(Q \,||\, P^*),
$$
where $P^\mu = \Pi_{\mathcal{C}_{\mathrm{Ynor}}}(Q)$.

---

### Lemma 4 (Contraction under Entropic Curvature)

Under ($H_\alpha$), there exists $\mu = \mu(\alpha) \in (0,1]$ such that:
$$
D_{KL}(P^\mu \,||\, P^*) \le (1-\mu) \, D_{KL}(Q \,||\, P^*).
$$

---

## 6. Main Theorem

### Theorem (Ynor Stability)

Assume:

1. (Raw dynamics)
   $$
   D_{KL}(Q_{n+1} \,||\, P^*) \le D_{KL}(P_n \,||\, P^*) + \varepsilon_n,
   $$

2. (Projection)
   $$
   P_{n+1}^\mu = \Pi_{\mathcal{C}_{\mathrm{Ynor}}}(Q_{n+1}),
   $$

3. (Entropic curvature)
   ($H_\alpha$) holds.

Then:
$$
D_{KL}(P_{n+1}^\mu \,||\, P^*)
\le
(1-\mu) \, D_{KL}(P_n \,||\, P^*) + \varepsilon_n.
$$

Consequently:

* (Stability) $ \sup_n D_{KL}(P_n \,||\, P^*) < \infty $,
* (Non-explosion) no divergence occurs,
* (Convergence) if $ \sum \varepsilon_n < \infty $, then:
  $$
  D_{KL}(P_n \,||\, P^*) \to 0.
  $$

---

## 7. Discussion

The Ynor framework formalizes stability in autoregressive systems as a consequence of **information-theoretic dissipation**. The projection operator enforces structural constraints, interpreted as a geometric restriction in probability space.

The parameter $\mu$ acts as a dissipation coefficient, analogous to viscosity in physical systems, but defined purely in terms of KL contraction.

---

## 8. Limitations

* The key assumption ($H_\alpha$) is not automatic and requires structural design of $\mathcal{C}_{\mathrm{Ynor}}$.
* The analysis is discrete and does not directly address continuous-time limits.
* The connection with Wasserstein gradient flows remains formal at this stage.

---

## 9. Future Work

* Construct explicit admissible sets $\mathcal{C}_{\mathrm{Ynor}}$ satisfying ($H_\alpha$),
* Establish links with Log-Sobolev inequalities and Fisher information,
* Extend the framework to continuous-time stochastic flows,
* Apply the theory to concrete LLM architectures and prompt constraints.

---

## 10. Explicit Admissible Sets

This section provides explicit constructions of admissible sets $\mathcal{C}_{\mathrm{Ynor}} \subset \mathcal{P}(\mathcal{H})$ satisfying the structural requirements introduced in the previous sections. In particular, we exhibit:

* a **globally exact admissible set**, for which the dissipation hypothesis ($H_\alpha$) holds with $\alpha=1$,
* a **non-trivial convex admissible family**, suitable for controlled generative systems, satisfying a **local version** of ($H_\alpha$).

These examples demonstrate that the Ynor framework is not purely abstract, but admits concrete realizations.

---

### 10.1. Example 1 — The Singleton Admissible Set (Global Exact Theorem)

Let $P^* \in \mathcal{P}(\mathcal{H})$ be the reference distribution.

Define:
$$
\mathcal{C}_{\mathrm{Ynor}} := \{P^*\}.
$$

---

#### Proposition 10.1 (Exact Dissipation)

For all $Q \in \mathcal{P}(\mathcal{H})$, the KL projection satisfies:
$$
\Pi_{\mathcal{C}_{\mathrm{Ynor}}}(Q) = P^*.
$$

Moreover:
$$
D_{KL}(Q \,||\, \Pi_{\mathcal{C}_{\mathrm{Ynor}}}(Q)) = D_{KL}(Q \,||\, P^*),
$$
so that hypothesis ($H_\alpha$) holds with $\alpha = 1$.

---

#### Proof

By definition of $\mathcal{C}_{\mathrm{Ynor}}$, the projection reduces to:
$$
\arg\min_{P \in \{P^*\}} D_{KL}(P \,||\, Q) = P^*.
$$

Thus,
$$
D_{KL}(Q \,||\, \Pi_{\mathcal{C}_{\mathrm{Ynor}}}(Q)) = D_{KL}(Q \,||\, P^*),
$$
and ($H_\alpha$) holds with $\alpha=1$. ∎

---

#### Corollary 10.2 (Maximal Contraction)

For all $Q$,
$$
D_{KL}(P^\mu \,||\, P^*) = 0,
$$
and the contraction factor satisfies $\mu = 1$.

---

#### Interpretation

This admissible set corresponds to a **fully constrained regime**, where the system collapses deterministically onto the canonical distribution $P^*$ at every step.

It provides:

* **global stability**,
* **zero residual entropy**,
* and **maximal dissipation**.

This case serves as a **reference extremum** for the Ynor framework.

---

### 10.2. Example 2 — The Canonical Lower-Bound Polytope (Governed Generation)

We now construct a non-trivial admissible set allowing controlled variability.

Let $V$ be a finite vocabulary, and identify $\mathcal{P}(\mathcal{H})$ locally with the probability simplex:
$$
\Delta_V = \left\{ p \in [0,1]^V : \sum_{i=1}^V p_i = 1 \right\}.
$$

Let $p^* \in \Delta_V$ with strictly positive coordinates:
$$
p_i^* > 0, \quad \forall i.
$$

Fix $\eta \in (0,1)$, and define:
$$
\mathcal{C}_\eta := \left\{ p \in \Delta_V :\, p_i \ge \eta \, p_i^*, \quad \forall i \right\}.
$$

---

#### Proposition 10.3 (Geometric Properties)

The set $\mathcal{C}_\eta$ satisfies:

1. **Convexity**: $\mathcal{C}_\eta$ is convex,
2. **Closedness**: $\mathcal{C}_\eta$ is closed in $\Delta_V$,
3. **Non-emptiness**: $p^* \in \mathcal{C}_\eta$.

---

#### Proof

Convexity follows from linear inequalities.
Closedness follows from continuity of coordinate projections.
Since $p_i^* \ge \eta p_i^*$, we have $p^* \in \mathcal{C}_\eta$. ∎

---

#### Proposition 10.4 (Existence and Uniqueness of Projection)

For any $q \in \Delta_V$ with full support ($q_i > 0$), the projection
$$
\Pi_{\mathcal{C}_\eta}(q) = \arg\min_{p \in \mathcal{C}_\eta} D_{KL}(p \,||\, q)
$$
exists and is unique.

---

#### Sketch of Proof

The function $p \mapsto D_{KL}(p||q)$ is strictly convex on the interior of $\Delta_V$, and $\mathcal{C}_\eta$ is convex and compact. Standard convex optimization arguments yield existence and uniqueness. ∎

---

#### Proposition 10.5 (Local Dissipation / Local ($H_\alpha$))

Let $K \subset \mathrm{int}(\Delta_V)$ be a compact set such that all $q \in K$ satisfy:
$$
q_i \ge m > 0, \quad p_i^* \ge m_* > 0.
$$

Assume that there exists $\gamma > 0$ such that:
$$
|q - \Pi_{\mathcal{C}_\eta}(q)|_2^2 \ge \gamma |q - p^*|_2^2, \quad \forall q \in K.
$$

Then there exists $\alpha_K > 0$ such that:
$$
D_{KL}(q \,||\, \Pi_{\mathcal{C}_\eta}(q)) \ge \alpha_K \, D_{KL}(q \,||\, p^*), \quad \forall q \in K.
$$

---

#### Sketch of Proof

On compact subsets of the simplex interior, the KL divergence is equivalent to the squared Euclidean norm:
$$
c_1 |x-y|_2^2 \le D_{KL}(x||y) \le c_2 |x-y|_2^2.
$$

Applying this equivalence to both divergences yields:
$$
D_{KL}(q \,||\, \Pi_{\mathcal{C}_\eta}(q))
\ge c_1 |q - \Pi_{\mathcal{C}_\eta}(q)|_2^2
\ge c_1 \gamma |q - p^*|_2^2
\ge \frac{c_1 \gamma}{c_2} D_{KL}(q \,||\, p^*).
$$

Setting $\alpha_K = \frac{c_1 \gamma}{c_2}$ concludes the proof. ∎

---

### 10.3. Interpretation for Controlled Generative Systems

The admissible set $\mathcal{C}_\eta$ enforces a **coordinate-wise lower bound relative to the canonical distribution**:
$$
p_i \ge \eta \, p_i^*.
$$

This has a natural interpretation in autoregressive generative systems:

* $p^*$ encodes a **canonical semantic prior**,
* $\eta$ defines a **minimum fidelity threshold**,
* the projection operator enforces a **soft but irreversible constraint** on generation.

In contrast to the singleton case, this structure allows:

* **controlled variability** (degrees of freedom remain),
* while preventing **degenerate or highly entropic deviations** from the canonical structure.

---

### 10.4. Closing Remark

The two examples illustrate a fundamental dichotomy:

* the singleton admissible set provides **global exact contraction** with maximal dissipation,
* the polytope $\mathcal{C}_\eta$ provides a **flexible, structurally constrained regime** with local contraction properties.

Together, they demonstrate that the Ynor framework admits both:

* **strict stabilization regimes**, and
* **governed generative regimes**,

bridging deterministic control and probabilistic expressivity within a unified information-geometric formalism.
