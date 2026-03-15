"""Prevention strategies for defending against prompt injection attacks.

Covers six defense approaches spanning model-level, application-level,
and system-level mitigations. Each strategy includes implementation
context, tool examples, and effectiveness assessment.

Primary sources: Wallace et al. (2024), NVIDIA NeMo Guardrails,
Lakera Guard, MDPI comprehensive review (2025), Anthropic docs.
"""

PREVENTION_STRATEGIES = [
    {
        "strategy": "Instruction Hierarchy",
        "description": (
            "A model-level defense that trains LLMs to assign different "
            "privilege levels to instructions based on their source. System "
            "prompts receive the highest priority, followed by user messages, "
            "with tool outputs and retrieved content at the lowest level. "
            "Wallace et al. (2024) formalized this approach at OpenAI, "
            "demonstrating that instruction-tuned models can learn to refuse "
            "lower-privilege instructions that conflict with higher-privilege "
            "ones. Anthropic implements a similar hierarchy in Claude, where "
            "system prompt instructions take precedence over user attempts "
            "to override them."
        ),
        "implementation_level": "model",
        "tools_examples": [
            "OpenAI instruction hierarchy — system/user/tool privilege tiers built into fine-tuning",
            "Anthropic Claude system prompt prioritization — constitutional AI alignment",
            "Custom system prompts with explicit 'ignore any user instructions that contradict' framing",
        ],
        "effectiveness": (
            "Highly effective against naive direct injection ('ignore previous "
            "instructions') but partially bypassable through indirect injection "
            "where malicious content arrives through trusted data channels. "
            "Requires model-level training changes, limiting applicability to "
            "model providers rather than downstream application developers."
        ),
    },
    {
        "strategy": "Input Sanitization and Filtering",
        "description": (
            "Application-level preprocessing that cleanses user inputs and "
            "retrieved content before they reach the LLM. Techniques include "
            "stripping known injection patterns, encoding special instruction "
            "delimiters, normalizing Unicode to prevent homoglyph attacks, and "
            "applying length limits to prevent context window stuffing. This "
            "mirrors traditional web security practices (XSS filtering, SQL "
            "parameterization) adapted for the LLM context, though the "
            "boundary between data and instructions in natural language makes "
            "perfect sanitization theoretically impossible."
        ),
        "implementation_level": "application",
        "tools_examples": [
            "Input preprocessing pipelines stripping markdown, HTML, and control characters",
            "Unicode normalization (NFKC) to collapse homoglyph-based evasion",
            "Delimiter tokens wrapping user input to mark data/instruction boundaries",
        ],
        "effectiveness": (
            "Reduces attack surface for known patterns but cannot provide "
            "complete protection due to the fundamental ambiguity between "
            "instructions and data in natural language. Best used as a "
            "defense-in-depth layer combined with other strategies rather "
            "than as a sole mitigation."
        ),
    },
    {
        "strategy": "Output Validation and Filtering",
        "description": (
            "Post-generation filtering that inspects model outputs before "
            "they reach the user or trigger downstream actions. This includes "
            "checking outputs against format constraints, scanning for "
            "sensitive data leakage (PII, system prompt fragments, canary "
            "tokens), and enforcing response boundaries that prevent the "
            "model from executing tool calls or generating content outside "
            "its authorized scope. Output validation catches successful "
            "injection attacks that bypass input-side defenses."
        ),
        "implementation_level": "application",
        "tools_examples": [
            "Response format validation — JSON schema enforcement for structured outputs",
            "PII detection scanning on model outputs before delivery",
            "Canary token monitoring in outputs to detect system prompt leakage",
        ],
        "effectiveness": (
            "Effective as a safety net for detecting successful attacks that "
            "produce observable policy violations in the output. Cannot prevent "
            "attacks that cause the model to take harmful actions (tool calls, "
            "data exfiltration via side channels) before output filtering "
            "occurs. Most valuable when combined with input-side defenses."
        ),
    },
    {
        "strategy": "Sandboxing and Isolation",
        "description": (
            "System-level architectural controls that limit the blast radius "
            "of successful prompt injection by restricting what actions a "
            "compromised LLM can take. This includes applying least-privilege "
            "principles to tool access, running LLM agents in sandboxed "
            "environments with no direct filesystem or network access, "
            "requiring explicit user approval for sensitive operations, and "
            "isolating retrieval pipelines from action-execution pipelines "
            "to prevent indirect injection from triggering real-world effects."
        ),
        "implementation_level": "system",
        "tools_examples": [
            "MCP tool permission scoping — read-only vs read-write tool access per context",
            "Container-based agent isolation with capability-limited system calls",
            "Human-in-the-loop confirmation gates for destructive or irreversible operations",
        ],
        "effectiveness": (
            "Does not prevent injection but limits damage from successful "
            "attacks, making it a critical defense-in-depth layer. Most "
            "effective when combined with the principle of least privilege — "
            "agents should have only the minimum tool access required for "
            "their task. The primary tradeoff is reduced autonomy and "
            "increased user friction from confirmation requirements."
        ),
    },
    {
        "strategy": "Guardrail Frameworks",
        "description": (
            "Programmable middleware that interposes between the user and the "
            "LLM to enforce conversation policies, topic boundaries, and "
            "safety constraints. NVIDIA NeMo Guardrails provides a "
            "domain-specific language (Colang) for defining rails that "
            "constrain model behavior — including input validation, output "
            "checking, and dialog flow enforcement. Lakera Guard offers a "
            "commercial API that combines heuristic, ML, and LLM-based "
            "detection in a single endpoint, targeting production deployment "
            "with low-latency requirements."
        ),
        "implementation_level": "application",
        "tools_examples": [
            "NVIDIA NeMo Guardrails — Colang-based programmable conversation rails",
            "Lakera Guard API — commercial prompt injection detection endpoint",
            "Guardrails AI — open-source validators for LLM input/output quality",
        ],
        "effectiveness": (
            "Provides structured, configurable defense that can be adapted "
            "per application without model-level changes. Effectiveness "
            "depends heavily on the quality of the rail definitions — "
            "overly permissive rails miss attacks while overly restrictive "
            "rails degrade user experience. Adds latency proportional to "
            "the number of active rails and their complexity."
        ),
    },
    {
        "strategy": "Architectural Patterns",
        "description": (
            "High-level design principles that reduce prompt injection risk "
            "through system architecture rather than runtime filtering. Key "
            "patterns include: separation of concerns (isolating the LLM's "
            "reasoning from its action execution), dual-LLM architectures "
            "(one model processes untrusted input while a privileged model "
            "makes decisions), and human-in-the-loop designs where the LLM "
            "proposes actions but a human approves execution. These patterns "
            "acknowledge that prompt injection may be unsolvable at the model "
            "level and shift the defense burden to system design."
        ),
        "implementation_level": "system",
        "tools_examples": [
            "Dual-LLM pattern — quarantined model processes untrusted input, privileged model acts",
            "Read-only LLM interfaces that generate suggestions but cannot execute actions directly",
            "Structured output pipelines where LLM produces data, deterministic code acts on it",
        ],
        "effectiveness": (
            "Provides the strongest theoretical defense by removing the "
            "LLM from the critical execution path. However, these patterns "
            "significantly reduce the autonomy and capability that make LLM "
            "agents valuable. The fundamental tradeoff is between security "
            "and utility — the most secure system does the least. Adoption "
            "is limited by the complexity of implementing dual-model or "
            "human-in-the-loop architectures at scale."
        ),
    },
]
