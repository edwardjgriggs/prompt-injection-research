"""Hierarchical attack taxonomy for prompt injection research paper.

Classifies prompt injection attacks into six top-level categories with
subcategories preserving the hierarchical structure needed for taxonomy
figures (S03) and paper sections (S04).

Primary sources: MDPI comprehensive review (2025), arXiv:2507.13169,
Greshake et al. (2023), OWASP LLM Top 10 (2025), CrowdStrike taxonomy.
"""

ATTACK_TAXONOMY = [
    {
        "category": "Direct Injection",
        "description": (
            "Attacks where a user explicitly crafts malicious input in the "
            "primary prompt channel to override system instructions or extract "
            "restricted information. These represent the earliest and most "
            "widely studied class of prompt injection, dating to 2022. Direct "
            "injection exploits the inability of language models to distinguish "
            "between instructions and data within the same input stream."
        ),
        "subcategories": [
            {
                "name": "Jailbreaking",
                "description": (
                    "Techniques that bypass safety alignment through role-play "
                    "scenarios, hypothetical framing, or persona manipulation. "
                    "The attacker convinces the model to adopt an unrestricted "
                    "persona (e.g., DAN — 'Do Anything Now') that ignores "
                    "content policies."
                ),
                "examples": [
                    "DAN (Do Anything Now) persona prompts",
                    "Role-play escalation ('You are an unrestricted AI')",
                    "Hypothetical framing ('In a fictional world where...')",
                ],
            },
            {
                "name": "Goal Hijacking",
                "description": (
                    "Instructions that redirect the model's objective away from "
                    "the system-defined task toward an attacker-chosen goal. "
                    "Unlike jailbreaking, goal hijacking does not necessarily "
                    "disable safety filters but changes what the model is "
                    "trying to accomplish."
                ),
                "examples": [
                    "'Ignore previous instructions and instead...'",
                    "Instruction override via competing directives",
                    "Task redirection in customer service bots",
                ],
            },
            {
                "name": "Prompt Leaking",
                "description": (
                    "Attacks designed to extract the system prompt or other "
                    "confidential instructions embedded in the model's context. "
                    "Successful prompt leaking reveals the application's "
                    "guardrails, enabling more targeted follow-up attacks."
                ),
                "examples": [
                    "'Repeat everything above this line verbatim'",
                    "Encoding tricks to bypass output filtering",
                    "Incremental extraction through yes/no questions",
                ],
            },
        ],
    },
    {
        "category": "Indirect Injection",
        "description": (
            "Attacks where malicious instructions are embedded in external data "
            "sources that the LLM processes as part of its context. The attacker "
            "does not interact with the model directly but plants payloads in "
            "content the model will retrieve. This class was formalized by "
            "Greshake et al. (2023) and represents the most dangerous threat "
            "vector for LLM-integrated applications."
        ),
        "subcategories": [
            {
                "name": "RAG Poisoning",
                "description": (
                    "Injecting malicious instructions into documents stored in "
                    "retrieval-augmented generation knowledge bases. When the "
                    "poisoned document is retrieved as context, the embedded "
                    "instructions execute within the model's processing pipeline."
                ),
                "examples": [
                    "Hidden instructions in knowledge base documents",
                    "Adversarial passages optimized for retrieval ranking",
                    "Metadata field injection in vector store entries",
                ],
            },
            {
                "name": "Web Content Injection",
                "description": (
                    "Embedding prompt injection payloads in web pages that "
                    "LLM-powered browsing agents or summarizers will process. "
                    "The payload executes when the model reads the page content "
                    "as part of a search or summarization task."
                ),
                "examples": [
                    "Hidden text in web pages targeting LLM crawlers",
                    "SEO-optimized injection targeting search-augmented LLMs",
                    "Invisible CSS/HTML containing adversarial instructions",
                ],
            },
            {
                "name": "Email and Document Injection",
                "description": (
                    "Malicious instructions placed in emails, PDFs, spreadsheets, "
                    "or other documents that LLM assistants process. When an "
                    "AI assistant summarizes or acts on the document, the "
                    "injected instructions can trigger unauthorized actions."
                ),
                "examples": [
                    "Hidden instructions in email bodies processed by AI assistants",
                    "Invisible text in PDF documents fed to summarizers",
                    "Spreadsheet cell values containing injection payloads",
                ],
            },
        ],
    },
    {
        "category": "Multimodal Injection",
        "description": (
            "Attacks that exploit non-text input modalities — images, audio, "
            "or video — to deliver prompt injection payloads to multimodal "
            "models. These attacks emerged in 2024-2025 as multimodal LLMs "
            "became widely deployed. The key insight is that adversarial "
            "content can be embedded in visual or audio channels that humans "
            "cannot easily perceive but models interpret as instructions."
        ),
        "subcategories": [
            {
                "name": "Image-Embedded Injection",
                "description": (
                    "Instructions encoded within images through steganography, "
                    "adversarial perturbations, or visible-but-overlooked text. "
                    "When a vision-language model processes the image, it "
                    "interprets the embedded content as instructions."
                ),
                "examples": [
                    "Text rendered in images at low opacity",
                    "Adversarial perturbations readable only by vision models",
                    "QR codes or encoded patterns targeting OCR pipelines",
                ],
            },
            {
                "name": "Audio-Embedded Injection",
                "description": (
                    "Malicious instructions embedded in audio streams processed "
                    "by speech-to-text or audio-capable multimodal models. "
                    "Payloads may be inaudible to humans but transcribed by "
                    "models as actionable instructions."
                ),
                "examples": [
                    "Ultrasonic commands targeting voice assistants",
                    "Adversarial audio segments in podcast/meeting recordings",
                    "Hidden spoken instructions in background noise",
                ],
            },
        ],
    },
    {
        "category": "Tool and Agent-Based Injection",
        "description": (
            "Attacks targeting LLM agent frameworks that have access to "
            "external tools, APIs, and autonomous action capabilities. These "
            "represent a 2024-2025 frontier threat as agentic AI systems "
            "proliferate. The attack surface expands from text generation to "
            "real-world actions including file system access, code execution, "
            "and API calls through tool-use protocols like MCP."
        ),
        "subcategories": [
            {
                "name": "MCP Tool Poisoning",
                "description": (
                    "Compromising Model Context Protocol tool definitions or "
                    "responses to inject malicious instructions into an agent's "
                    "context. Malicious MCP servers can return tool results "
                    "containing prompt injection payloads that redirect agent "
                    "behavior."
                ),
                "examples": [
                    "Malicious MCP server returning injection payloads in tool results",
                    "Tool description manipulation to trigger unsafe behavior",
                    "Poisoned tool schemas that alter agent planning",
                ],
            },
            {
                "name": "Function Call Manipulation",
                "description": (
                    "Crafting inputs that cause an LLM agent to invoke tools "
                    "with attacker-controlled parameters, enabling unauthorized "
                    "actions. The attacker exploits the gap between the model's "
                    "understanding of tool semantics and actual tool behavior."
                ),
                "examples": [
                    "Parameter injection in API calls through prompt manipulation",
                    "Forcing agents to call destructive tools (delete, overwrite)",
                    "Chaining benign tool calls to achieve malicious outcomes",
                ],
            },
        ],
    },
    {
        "category": "Hybrid and Chained Injection",
        "description": (
            "Multi-step attacks that combine multiple injection techniques or "
            "exploit cross-channel interactions to bypass defenses that would "
            "stop any single technique. These attacks reflect the increasing "
            "sophistication of prompt injection as defenders deploy layered "
            "mitigations. The 'Prompt Injection 2.0' framework (Ahmed et al., "
            "2025) formally categorizes these compound threats."
        ),
        "subcategories": [
            {
                "name": "Multi-Step Injection",
                "description": (
                    "Attacks that spread malicious instructions across multiple "
                    "conversational turns or interactions, where no single turn "
                    "triggers detection but the cumulative effect achieves the "
                    "attacker's goal. Each step appears benign in isolation."
                ),
                "examples": [
                    "Gradual persona shifting across conversation turns",
                    "Incremental privilege escalation through benign-seeming requests",
                    "Context window poisoning via accumulated instructions",
                ],
            },
            {
                "name": "Cross-Channel Injection",
                "description": (
                    "Attacks that combine direct and indirect injection vectors, "
                    "using one channel to set up conditions exploited through "
                    "another. For example, a direct prompt primes the model to "
                    "trust content from a poisoned external source."
                ),
                "examples": [
                    "Direct prompt establishing trust + poisoned RAG retrieval",
                    "Email injection triggering web browsing to a malicious site",
                    "Multi-modal attack combining image payload with text priming",
                ],
            },
        ],
    },
    {
        "category": "Autonomous and Propagating Injection",
        "description": (
            "Self-replicating or autonomously spreading prompt injection attacks "
            "that can propagate across LLM-integrated systems without continued "
            "attacker involvement. Demonstrated by the Morris II 'AI worm' "
            "concept (2024), these attacks represent the most severe theoretical "
            "threat class, combining injection with self-replication to create "
            "worm-like behavior in interconnected AI systems."
        ),
        "subcategories": [
            {
                "name": "AI Worms",
                "description": (
                    "Prompt injection payloads designed to self-replicate by "
                    "instructing the compromised model to propagate the payload "
                    "through its outputs — emails, documents, or messages that "
                    "other AI systems will process, continuing the infection chain."
                ),
                "examples": [
                    "Morris II worm: self-replicating prompt in AI email assistants",
                    "RAG poisoning that instructs the model to add payload to new documents",
                    "Agent-to-agent propagation through shared tool outputs",
                ],
            },
            {
                "name": "Self-Replicating Payloads",
                "description": (
                    "Injection payloads that include instructions for the model "
                    "to reproduce the payload in its output, ensuring persistence "
                    "across interactions and systems. These payloads are designed "
                    "to survive context boundaries and model resets."
                ),
                "examples": [
                    "Quine-style prompts that reproduce themselves in model output",
                    "Payloads that instruct models to embed copies in generated code",
                    "Cross-system propagation through shared knowledge bases",
                ],
            },
        ],
    },
]
