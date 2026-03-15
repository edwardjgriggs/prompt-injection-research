"""Detection techniques for identifying prompt injection attacks.

Covers five major approaches to detecting prompt injection, from simple
heuristic rules to LLM-as-judge secondary evaluation. Each technique
includes practical tool examples and known limitations.

Primary sources: Rebuff (ProtectAI), Alon & Kamfonas (2023),
MDPI comprehensive review (2025), Liu et al. (2024).
"""

DETECTION_TECHNIQUES = [
    {
        "technique": "Heuristic and Rule-Based Detection",
        "description": (
            "Pattern-matching approaches that scan user inputs for known "
            "injection signatures such as 'ignore previous instructions', "
            "'you are now', or role-play escalation phrases. These systems "
            "maintain curated keyword lists and regular expressions derived "
            "from documented attack patterns. While fast and interpretable, "
            "heuristic methods suffer from high false-positive rates on "
            "legitimate inputs and are trivially bypassed through paraphrasing, "
            "encoding tricks (Base64, ROT13), or language translation."
        ),
        "approach_type": "static",
        "tools_examples": [
            "Rebuff heuristic layer — keyword and regex matching against known injection patterns",
            "Custom input validation middleware with configurable rule sets",
            "OWASP ModSecurity-style WAF rules adapted for LLM inputs",
        ],
        "limitations": (
            "Easily evaded through synonym substitution, character-level "
            "obfuscation, or multi-language attacks. Cannot detect novel "
            "injection patterns not in the rule set. High maintenance burden "
            "as new attack patterns emerge continuously."
        ),
    },
    {
        "technique": "ML Classification",
        "description": (
            "Trained machine learning models that classify inputs as benign "
            "or adversarial based on learned features. These range from "
            "traditional text classifiers (SVM, logistic regression on TF-IDF "
            "features) to fine-tuned transformer models trained on labeled "
            "prompt injection datasets. Embedding similarity approaches "
            "compare input embeddings against a vector database of known "
            "injection examples, flagging inputs that fall within a threshold "
            "distance of known attacks."
        ),
        "approach_type": "learned",
        "tools_examples": [
            "Rebuff vector similarity layer — cosine distance against known injection embeddings",
            "Lakera Guard API — commercial classifier trained on proprietary injection dataset",
            "HuggingFace prompt injection classifiers (e.g., deepset/deberta-v3-base-injection)",
        ],
        "limitations": (
            "Dependent on training data quality and coverage — novel attack "
            "patterns outside the training distribution are missed. Requires "
            "ongoing retraining as the attack landscape evolves. Embedding "
            "similarity approaches can be fooled by adversarial inputs "
            "optimized to be semantically distant from known attacks while "
            "remaining functionally equivalent."
        ),
    },
    {
        "technique": "Perplexity Analysis",
        "description": (
            "Statistical anomaly detection that measures the perplexity of "
            "input text under a reference language model. Adversarial prompts "
            "often exhibit unusual token distributions — either abnormally "
            "low perplexity (highly formulaic injection templates) or "
            "abnormally high perplexity (obfuscated or encoded payloads). "
            "Alon and Kamfonas (2023) demonstrated that perplexity-based "
            "windowed analysis can detect gradient-based adversarial suffixes "
            "with high accuracy, as these optimized token sequences produce "
            "statistically anomalous perplexity scores compared to natural text."
        ),
        "approach_type": "statistical",
        "tools_examples": [
            "Perplexity windowing — sliding window analysis flagging regions with anomalous scores",
            "GPT-2 or similar small model used as perplexity reference baseline",
            "Token entropy analysis as a lightweight proxy for full perplexity computation",
        ],
        "limitations": (
            "Effective primarily against machine-generated adversarial suffixes "
            "rather than human-crafted injection prompts, which tend to have "
            "natural perplexity. Requires calibration of thresholds per domain "
            "and language. Does not detect semantically valid injection prompts "
            "that are syntactically natural."
        ),
    },
    {
        "technique": "Canary Token Detection",
        "description": (
            "A proactive detection strategy where unique, secret tokens are "
            "planted within the system prompt or context. If the model's "
            "output contains these canary tokens, it indicates that an "
            "injection attack has successfully manipulated the model into "
            "revealing privileged context. Rebuff implements this as a "
            "defense layer: canary strings are appended to the system prompt, "
            "and all outputs are scanned for their presence before being "
            "returned to the user."
        ),
        "approach_type": "proactive",
        "tools_examples": [
            "Rebuff canary token layer — random strings injected into system context and monitored in output",
            "Custom canary middleware that rotates tokens per session",
            "Honeypot instructions designed to trigger detectable behavior if the model is compromised",
        ],
        "limitations": (
            "Only detects successful attacks that result in context leakage — "
            "does not prevent the injection itself. Canary tokens can be "
            "detected and filtered by sophisticated attackers who instruct "
            "the model to strip unusual strings from output. Limited to "
            "detecting prompt leaking; does not address goal hijacking or "
            "tool manipulation attacks."
        ),
    },
    {
        "technique": "LLM-as-Judge Detection",
        "description": (
            "Using a secondary language model to evaluate whether an input "
            "or output contains prompt injection attempts. The judge model "
            "receives the user input (and optionally the system prompt) and "
            "classifies whether the input is attempting to subvert intended "
            "behavior. This approach leverages the LLM's own understanding "
            "of instruction semantics to detect manipulation that statistical "
            "methods miss, particularly for semantically sophisticated attacks "
            "that use natural language to redirect model behavior."
        ),
        "approach_type": "model-based",
        "tools_examples": [
            "Rebuff LLM-based detection layer — GPT-4 prompt evaluating injection likelihood",
            "Dual-LLM architecture: a smaller model screens inputs before the primary model processes them",
            "OpenAI Moderation API extended with custom injection detection prompts",
        ],
        "limitations": (
            "Adds latency and cost from a second model inference per request. "
            "The judge model is itself susceptible to prompt injection — an "
            "attacker can craft inputs that fool both the primary and judge "
            "models simultaneously. Effectiveness degrades when the judge "
            "model is weaker than the primary model, as it cannot reliably "
            "detect attacks it would itself fall for."
        ),
    },
]
