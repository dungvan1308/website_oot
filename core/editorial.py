"""Illustrative case studies and editorial content for Phase 6."""

CASE_STUDIES = [
    {
        "id": "banking-data-modernization",
        "category": "Banking technology",
        "title": "Modernizing a banking data and reporting landscape",
        "summary": "An illustrative scenario for bringing core banking and supporting data into a governed reporting foundation.",
        "challenge": "Banking information can be distributed across core systems, channels and supporting applications. Inconsistent definitions and manual reporting steps make it harder to trace figures from source to report.",
        "solution": "Establish a governed banking data layer that integrates priority sources, applies quality controls and provides consistent reporting outputs.",
        "architecture": ["Core banking and channel sources", "Secure ingestion and validation", "Governed banking data model", "Reconciled reporting and BI layer"],
        "technology": ["Core banking platforms", "Oracle / PostgreSQL", "Power BI", "Integration services"],
        "implementation": ["Map source data and regulatory requirements", "Prioritize high-value reporting domains", "Build and validate data pipelines", "Roll out reporting in controlled stages"],
        "impact": ["Clearer data lineage from source to report", "More repeatable reporting workflows", "A foundation for future banking analytics"],
    },
    {
        "id": "enterprise-lakehouse",
        "category": "Data platform",
        "title": "Creating a flexible enterprise lakehouse foundation",
        "summary": "A reference pattern for joining data engineering and analytics on a shared, governed platform.",
        "challenge": "Separate data stores and point-to-point pipelines can create duplicated work, uneven data quality and limited discovery across business domains.",
        "solution": "Design a layered lakehouse platform with clear ownership, repeatable ingestion, curated data products and fit-for-purpose access controls.",
        "architecture": ["Enterprise and operational sources", "Batch and change-based ingestion", "Lakehouse storage and processing", "Curated data products and semantic models"],
        "technology": ["AWS or Microsoft Azure", "Open data formats", "SQL and data engineering tools", "Power BI or equivalent BI"],
        "implementation": ["Assess source systems and workloads", "Define platform guardrails and data domains", "Deliver an initial high-value domain", "Expand through reusable patterns"],
        "impact": ["A clearer path to reuse data across teams", "More consistent data quality practices", "Room to scale analytics as needs evolve"],
    },
    {
        "id": "management-bi",
        "category": "Business intelligence",
        "title": "Aligning management reporting around shared measures",
        "summary": "An illustrative BI scenario for connecting operational data to a consistent leadership view.",
        "challenge": "Teams may define key measures differently or rely on manually assembled reports, making comparisons and follow-up harder than they need to be.",
        "solution": "Create a governed KPI layer with agreed definitions, validated data sources and role-focused dashboards for leadership and operations.",
        "architecture": ["Operational application data", "Integration and data quality checks", "Shared KPI and semantic layer", "Executive and operational dashboards"],
        "technology": ["SQL Server", "Power BI", "Enterprise data warehouse", "Source system APIs"],
        "implementation": ["Agree decision questions and KPI ownership", "Validate source data and definitions", "Build a focused dashboard set", "Iterate with stakeholder feedback"],
        "impact": ["A common language for business performance", "Less ambiguity in KPI interpretation", "More direct access to decision-ready information"],
    },
]

INSIGHTS = [
    {
        "id": "trusted-data-foundation",
        "category": "Data strategy",
        "title": "From fragmented reporting to a trusted data foundation",
        "summary": "What to align before building an enterprise data platform.",
        "reading_time": "5 min read",
        "sections": [
            ("Start with decisions, not tools", "List the decisions the platform should support and the teams who make them. This grounds architecture choices in real information needs rather than a technology shopping list."),
            ("Map ownership and meaning", "Identify source owners, critical data elements and competing definitions. Agreeing who owns a measure is often as important as deciding where it will be stored."),
            ("Build a useful first domain", "Choose a domain with visible value and manageable dependencies. Establish ingestion, quality, access and lineage patterns there, then reuse what works."),
            ("Treat governance as part of delivery", "Governance is most useful when it is built into everyday workflows: ownership, access controls, quality rules and change processes should be clear from the start."),
        ],
    },
    {
        "id": "core-banking-migration-planning",
        "category": "Banking technology",
        "title": "Planning a core banking data migration",
        "summary": "A practical view of dependencies, data quality and continuity planning.",
        "reading_time": "6 min read",
        "sections": [
            ("Understand the full data landscape", "Inventory source systems, interfaces, reporting dependencies, data owners and downstream consumers. The migration boundary is usually wider than the core platform alone."),
            ("Make data mapping testable", "Define mappings, transformation rules and exception handling in a form that can be reviewed and tested. Reconciliation criteria should be agreed before cutover rehearsals."),
            ("Plan the transition in stages", "Use representative data and realistic operational scenarios to rehearse migration steps. Define decision points, responsibilities and fallback conditions for each stage."),
            ("Keep continuity visible", "Track the reports, integrations and business processes that must remain available during transition. Include operational teams in readiness reviews and cutover planning."),
        ],
    },
    {
        "id": "shared-kpi-definitions",
        "category": "Business intelligence",
        "title": "Why shared KPI definitions matter",
        "summary": "How a common measurement layer helps teams make decisions from the same picture.",
        "reading_time": "4 min read",
        "sections": [
            ("Resolve differences at the source", "When teams use the same label for different calculations, dashboards amplify the disagreement. A shared definition makes filters, time periods and business rules explicit."),
            ("Assign clear ownership", "Each important measure needs an accountable business owner and a technical steward. Together they can review meaning, quality and changes over time."),
            ("Publish context with the number", "Definitions, refresh timing and known limitations help people interpret a KPI correctly. Make this information available where the measure is used."),
            ("Improve through use", "Start with the measures that drive decisions today. Review them with users, capture questions and refine the shared model as business needs change."),
        ],
    },
]
