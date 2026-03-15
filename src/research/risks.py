"""Risk categories for prompt injection impact analysis.

Each category describes a class of real-world harm that prompt injection
attacks can cause, with concrete examples and severity assessment.

Primary sources: OWASP LLM01 (2025), CrowdStrike taxonomy,
Simon Willison's documentation, Greshake et al. (2023), Anthropic research.
"""

RISK_CATEGORIES = [
    {
        "category": "Data Exfiltration",
        "description": (
            "Prompt injection can cause LLMs to leak sensitive information "
            "including system prompts, training data fragments, user personal "
            "data, and proprietary business logic. Indirect injection is "
            "particularly dangerous here because the exfiltration can occur "
            "without the user's awareness — for example, a poisoned document "
            "can instruct the AI assistant to encode confidential data into "
            "a URL that the model renders as a markdown image, triggering an "
            "HTTP request that transmits the data to an attacker-controlled "
            "server. OWASP ranks this among the highest-impact outcomes of "
            "LLM01 prompt injection."
        ),
        "examples": [
            "System prompt extraction from ChatGPT custom GPTs via 'repeat your instructions' attacks",
            "Markdown image exfiltration: injected instructions cause model to embed user data in image URLs",
            "Indirect injection in Bing Chat leaking user search context through crafted web pages",
        ],
        "severity": "critical",
        "affected_systems": [
            "AI assistants with access to personal data",
            "RAG systems over confidential document stores",
            "Customer service chatbots with backend database access",
            "Code assistants with repository access",
        ],
    },
    {
        "category": "Unauthorized Actions",
        "description": (
            "When LLMs are integrated with tools and APIs, prompt injection "
            "can cause the model to execute actions the user never intended — "
            "sending emails, modifying files, making purchases, or calling "
            "APIs with attacker-controlled parameters. Agentic AI systems "
            "with broad tool access are especially vulnerable because a "
            "single successful injection can cascade through multiple tool "
            "calls. The severity scales with the agent's permission scope: "
            "an agent with file system and network access poses fundamentally "
            "different risks than a text-only chatbot."
        ),
        "examples": [
            "AI email assistants sending messages to attacker-specified recipients via indirect injection",
            "Code agents executing malicious commands through injected instructions in repository files",
            "Shopping assistants making unauthorized purchases through manipulated product descriptions",
        ],
        "severity": "critical",
        "affected_systems": [
            "AI agents with tool-use capabilities (MCP, function calling)",
            "Email and calendar AI assistants",
            "Autonomous coding agents with shell access",
            "Financial and e-commerce AI integrations",
        ],
    },
    {
        "category": "Content Manipulation",
        "description": (
            "Attackers can use prompt injection to control, bias, or corrupt "
            "the model's output without detection by the end user. This "
            "includes generating disinformation, inserting propaganda into "
            "AI-generated summaries, biasing recommendations, or suppressing "
            "specific information. Content manipulation is particularly "
            "insidious because the user trusts the AI's output as objective, "
            "and the manipulated content appears identical in form to "
            "legitimate responses."
        ),
        "examples": [
            "Indirect injection via web pages biasing Bing Chat responses about products or people",
            "RAG poisoning to suppress negative information in AI-generated summaries",
            "SEO-style injection causing AI search assistants to promote specific content",
        ],
        "severity": "high",
        "affected_systems": [
            "AI-powered search and summarization tools",
            "Content recommendation systems",
            "Automated report and brief generation",
            "Customer-facing chatbots providing product information",
        ],
    },
    {
        "category": "System Compromise",
        "description": (
            "In agentic and tool-augmented deployments, prompt injection can "
            "escalate to full system compromise — arbitrary code execution, "
            "privilege escalation, or persistent backdoor installation. When "
            "AI agents have access to shell commands, file systems, or "
            "container orchestration, a successful injection effectively "
            "grants the attacker the same privileges as the agent process. "
            "This transforms prompt injection from an AI safety concern into "
            "a traditional cybersecurity vulnerability with potentially "
            "catastrophic consequences."
        ),
        "examples": [
            "Code execution through AI coding assistants processing malicious repository files",
            "Container escape scenarios via AI agents with Docker/Kubernetes access",
            "Persistent backdoor installation through AI-generated infrastructure-as-code",
        ],
        "severity": "critical",
        "affected_systems": [
            "AI agents with code execution capabilities",
            "DevOps and infrastructure automation agents",
            "AI systems with elevated OS-level permissions",
            "Cloud orchestration AI integrations",
        ],
    },
    {
        "category": "Supply Chain and Downstream Propagation",
        "description": (
            "Prompt injection can propagate through AI supply chains, where "
            "the output of one compromised AI system becomes the input of "
            "another. This creates cascading failures across interconnected "
            "AI systems. Poisoned AI-generated content entering training data, "
            "knowledge bases, or shared document stores can perpetuate the "
            "attack across temporal and organizational boundaries. The Morris "
            "II AI worm concept demonstrates how self-replicating payloads "
            "could spread autonomously through networks of AI agents."
        ),
        "examples": [
            "AI-generated code containing injection payloads committed to shared repositories",
            "Poisoned AI summaries entering knowledge bases consumed by other AI systems",
            "Morris II worm concept: self-replicating prompts spreading through AI email systems",
        ],
        "severity": "high",
        "affected_systems": [
            "Multi-agent AI architectures",
            "AI-generated content pipelines",
            "Shared knowledge bases and vector stores",
            "AI-assisted software supply chains",
        ],
    },
]
