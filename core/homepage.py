"""Homepage copy and catalog data. Phase 7 will source these collections from CMS models."""

SERVICES = [
    {
        "mark": "◈",
        "title": "Data platforms",
        "description": "Build governed data foundations across warehouses, lakehouses, engineering and integration.",
        "href": "/services/#data-platform",
    },
    {
        "mark": "▥",
        "title": "Business intelligence",
        "description": "Turn operational and executive data into clear reporting, shared KPIs and timely decisions.",
        "href": "/services/#business-intelligence",
    },
    {
        "mark": "⌘",
        "title": "Enterprise software",
        "description": "Connect ERP, HR, CRM and workflow applications to the way your organization works.",
        "href": "/services/#enterprise-software",
    },
    {
        "mark": "⌂",
        "title": "Banking technology",
        "description": "Plan core banking migration, banking data platforms and regulatory reporting foundations.",
        "href": "/services/#banking-technology",
    },
    {
        "mark": "◎",
        "title": "Cloud transformation",
        "description": "Modernize with cloud migration, hybrid architectures and integration across your ecosystem.",
        "href": "/services/#cloud-transformation",
    },
]

SERVICE_GROUPS = [
    {
        "id": "data-platform",
        "mark": "◈",
        "title": "Data platform",
        "description": "Create a trusted foundation for data across systems, teams and use cases.",
        "features": ["Enterprise Data Warehouse", "Data Lakehouse", "Data Engineering", "Data Integration", "Data Governance"],
        "outcome": "A consistent, governed data layer ready for analytics and operational use.",
    },
    {
        "id": "business-intelligence",
        "mark": "▥",
        "title": "Business intelligence",
        "description": "Turn business questions into shared metrics, clear reporting and useful insight.",
        "features": ["Management BI", "Executive Dashboard", "KPI Reporting", "Operational Reporting", "Enterprise Reporting"],
        "outcome": "A common view of performance for leadership and operational teams.",
    },
    {
        "id": "enterprise-software",
        "mark": "⌘",
        "title": "Enterprise software",
        "description": "Connect core business processes with applications built around your operating model.",
        "features": ["ERP", "HR Management", "CRM", "Workflow", "Enterprise Applications"],
        "outcome": "More connected business workflows and a clearer path to application modernization.",
    },
    {
        "id": "banking-technology",
        "mark": "⌂",
        "title": "Banking technology",
        "description": "Support complex banking change with careful planning across core systems and data.",
        "features": ["Core Banking Migration", "FLEXCUBE Migration", "T24 / Temenos Migration", "Banking Data Platform", "SBV Reporting"],
        "outcome": "A structured approach to migration, integration and banking data requirements.",
    },
    {
        "id": "cloud-transformation",
        "mark": "◎",
        "title": "Cloud & digital transformation",
        "description": "Modernize platforms in line with your architecture, security and business priorities.",
        "features": ["AWS", "Microsoft Azure", "Oracle", "IBM", "Cloud Migration", "Hybrid Cloud", "System Integration"],
        "outcome": "An integrated, fit-for-purpose cloud and technology foundation.",
    },
]

SOLUTIONS = [
    {"slug": "enterprise-data-platform", "title": "Enterprise Data Platform", "description": "A governed foundation to bring trusted enterprise data together.", "capabilities": ["Data integration across business systems", "Shared data models and quality controls", "Governance, lineage and secure access"], "value": "Give teams a dependable source for analytics, reporting and data products.", "mark": "◈"},
    {"slug": "lakehouse-platform", "title": "Lakehouse Platform", "description": "Unify analytics and data engineering in a flexible lakehouse architecture.", "capabilities": ["Scalable ingestion and transformation", "Structured and semi-structured data", "Open architecture for varied workloads"], "value": "Create a flexible path from raw data to trusted analytical outputs.", "mark": "◌"},
    {"slug": "management-bi-platform", "title": "Management BI Platform", "description": "Align leadership around shared metrics, dashboards and reporting.", "capabilities": ["Executive dashboards and scorecards", "Consistent KPI definitions", "Operational and management reporting"], "value": "Help teams make decisions from a shared view of business performance.", "mark": "▥"},
    {"slug": "enterprise-management-platform", "title": "Enterprise Management Platform", "description": "Connect business workflows with ERP, HR and CRM capabilities.", "capabilities": ["Connected ERP and finance workflows", "HR and workforce processes", "Customer relationship management"], "value": "Reduce process fragmentation across core business applications.", "mark": "⌘"},
    {"slug": "banking-data-reporting", "title": "Banking Data & Reporting", "description": "Create reliable data flows for financial and regulatory reporting.", "capabilities": ["Banking data integration", "Traceable reporting pipelines", "Reconciliations and quality controls"], "value": "Improve visibility and control across reporting data flows.", "mark": "⌂"},
    {"slug": "core-banking-migration", "title": "Core Banking Migration", "description": "Structure migration planning around systems, data and operational continuity.", "capabilities": ["Source and target assessment", "Data mapping and migration planning", "Integration and cutover readiness"], "value": "Manage migration complexity through a clear, phased delivery approach.", "mark": "⇄"},
    {"slug": "sbv-regulatory-reporting", "title": "SBV Regulatory Reporting", "description": "Build traceable reporting pipelines for State Bank of Vietnam submissions.", "capabilities": ["Source-to-report data mapping", "Validation and reconciliation workflows", "Repeatable reporting outputs"], "value": "Strengthen traceability and consistency in regulatory reporting processes.", "mark": "▧"},
    {"slug": "cloud-data-transformation", "title": "Cloud & Data Transformation", "description": "Move toward a secure, integrated cloud and data operating model.", "capabilities": ["Cloud and hybrid architecture", "Workload migration planning", "Integration and platform modernization"], "value": "Align technology change with long-term operating and business needs.", "mark": "☁"},
]

PRODUCTS = [
    {"slug": "data-warehouse", "title": "Data Warehouse Platform", "description": "Organize trusted enterprise data for consistent analysis.", "technology": "Data engineering · Governance", "mark": "▤", "features": ["Integrated enterprise data", "Curated subject areas", "Quality and governance controls"], "value": "A dependable analytical foundation for consistent business reporting."},
    {"slug": "lakehouse", "title": "Lakehouse Platform", "description": "Support modern analytics on a flexible data foundation.", "technology": "Cloud · Open data formats", "mark": "◈", "features": ["Flexible data ingestion", "Scalable processing patterns", "Analytics-ready data layers"], "value": "A flexible platform approach for evolving data and analytics workloads."},
    {"slug": "bi-reporting", "title": "BI Reporting Platform", "description": "Deliver shared KPIs, executive dashboards and operational reports.", "technology": "Power BI · SQL Server", "mark": "▥", "features": ["Executive dashboards", "KPI and scorecard reporting", "Operational reports"], "value": "A consistent view of performance across business roles."},
    {"slug": "erp", "title": "ERP", "description": "Bring essential finance and operational workflows into view.", "technology": "Enterprise applications", "mark": "⌘", "features": ["Core business processes", "Workflow integration", "Operational visibility"], "value": "Connect day-to-day operations to a coherent enterprise process model."},
    {"slug": "hr-management", "title": "HR Management", "description": "Support connected people processes and workforce information.", "technology": "HR · Workflow", "mark": "♙", "features": ["People data management", "Workforce processes", "Role-based workflows"], "value": "Make people operations clearer and easier to coordinate."},
    {"slug": "crm", "title": "CRM", "description": "Connect customer processes with a clearer view of relationships.", "technology": "CRM · Integration", "mark": "◎", "features": ["Customer information", "Relationship workflows", "Connected service processes"], "value": "Help teams work from a more complete view of customer relationships."},
    {"slug": "banking-data", "title": "Banking Data Platform", "description": "Structure banking data for analytics, migration and reporting.", "technology": "Core banking · Data", "mark": "⌂", "features": ["Core system data integration", "Banking subject areas", "Analytics and reporting layers"], "value": "Provide a structured data foundation for banking transformation needs."},
    {"slug": "sbv-reporting", "title": "SBV Reporting Solution", "description": "Support traceable regulatory reporting workflows.", "technology": "Regulatory · Reporting", "mark": "▧", "features": ["Source mapping and validation", "Reconciliation workflows", "Repeatable reporting outputs"], "value": "Support controlled, traceable regulatory reporting processes."},
]

INDUSTRIES = [
    {"slug": "banking-financial-services", "title": "Banking & financial services", "description": "Modernize complex banking platforms and build reliable foundations for reporting, analytics and change.", "index": "01", "focus": ["Core banking migration", "Banking data platforms", "Regulatory reporting"], "solutions": ["Core Banking Migration", "Banking Data & Reporting", "SBV Regulatory Reporting"]},
    {"slug": "public-sector", "title": "Public sector", "description": "Connect information and processes to support transparent, accountable, data-informed services.", "index": "02", "focus": ["Data integration", "Management reporting", "Enterprise applications"], "solutions": ["Enterprise Data Platform", "Management BI Platform", "Enterprise Management Platform"]},
    {"slug": "multi-entity-enterprises", "title": "Multi-entity enterprises", "description": "Bring business units onto connected applications, shared data definitions and consistent reporting.", "index": "03", "focus": ["Enterprise data warehouse", "ERP and HR workflows", "Executive dashboards"], "solutions": ["Enterprise Data Platform", "Management BI Platform", "Enterprise Management Platform"]},
    {"slug": "digital-businesses", "title": "Digital businesses", "description": "Build adaptable cloud and data foundations as products, operations and customer needs evolve.", "index": "04", "focus": ["Cloud migration", "Lakehouse analytics", "System integration"], "solutions": ["Lakehouse Platform", "Cloud & Data Transformation", "Enterprise Data Platform"]},
]

TECHNOLOGIES = [
    "Oracle", "IBM", "Microsoft", "Microsoft Azure", "AWS", "PostgreSQL", "Power BI", "SQL Server",
]

DELIVERY_PATTERNS = [
    {
        "industry": "Illustrative delivery scenario",
        "title": "Core banking data modernization",
        "summary": "A representative path from fragmented source systems to governed banking data and reporting layers.",
        "impact": "Architecture focus: source integration · governed data · regulatory reporting",
        "href": "/case-studies/",
    },
    {
        "industry": "Illustrative delivery scenario",
        "title": "Enterprise lakehouse foundation",
        "summary": "A reference architecture for bringing data engineering and analytics onto a shared platform.",
        "impact": "Architecture focus: ingestion · lakehouse · BI semantic layer",
        "href": "/case-studies/",
    },
    {
        "industry": "Illustrative delivery scenario",
        "title": "Connected management reporting",
        "summary": "An example reporting flow that connects operational measures to an executive view of performance.",
        "impact": "Architecture focus: shared KPIs · data quality · executive dashboards",
        "href": "/case-studies/",
    },
]

INSIGHTS = [
    {
        "category": "Data strategy",
        "title": "From fragmented reporting to a trusted data foundation",
        "summary": "What organizations should align before building an enterprise data platform.",
        "href": "/insights/",
    },
    {
        "category": "Banking technology",
        "title": "Planning a core banking data migration",
        "summary": "A practical view of dependencies, data quality and continuity planning.",
        "href": "/insights/",
    },
    {
        "category": "Business intelligence",
        "title": "Why shared KPI definitions matter",
        "summary": "How a common measurement layer helps teams make decisions from the same picture.",
        "href": "/insights/",
    },
]
