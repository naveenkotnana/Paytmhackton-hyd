from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(r"D:\Deploy-OpsPilot-Razorpay-inspired-AI-FinOps-Platform")
OUT = ROOT / "docs" / "PayBridge_Beginner_to_Interview_Project_Guide.docx"
BUILD = ROOT / "docs" / ".paybridge_build"
BUILD.mkdir(exist_ok=True)

NAVY = "0B1836"
BLUE = "315BFF"
TEAL = "07866D"
MUTED = "52627A"
PALE = "F3F7FC"
LINE = "D8E1EE"
AMBER = "A45A00"
RED = "A83434"

chapters = [
 ("01 What PayBridge Is", [
  ("In one sentence", "PayBridge is a payment-operations learning prototype. It brings payment records into one place, computes operational summaries, flags patterns for review, gathers database and procedure evidence, and records an operator's decision. The project is designed around a practical question: when payments fail or remain pending, how can a team understand the saved evidence and decide what to check next?"),
  ("The simplest explanation", "Imagine a cafe sees several UPI payments fail. PayBridge can store compatible payment records, count results by status or payment route, help an operator look up a payment reference, and present an investigation workflow. The investigator can see facts from the database and relevant procedure text. A human reviews the suggestion. That is the product story; importing a CSV does not prove that the source transactions are genuine, and an admin decision does not control a real bank route."),
  ("What it combines", "The code combines a Streamlit interface, a FastAPI application, SQLAlchemy models, SQLite by default, optional PostgreSQL configuration, CSV processing, SQL analytics, scikit-learn Isolation Forest logic, a LangGraph workflow, local TF-IDF retrieval, and optional Ollama generation. Razorpay Standard Checkout is a separate test/live-provider integration that requires valid server-side credentials. Each capability has a different level of integration; the status matrix near the end explains those boundaries."),
  ("How to describe it to different people", "HR: I built a payment-operations prototype that helps teams review payment failures using structured records and evidence.\nBackend engineer: The API exposes payment, ingestion, analytics, investigation, approval, and checkout routes backed by SQLAlchemy.\nData engineer: CSV headers are mapped to a canonical payment schema, accepted rows are stored, and import outcomes are recorded.\nML engineer: Payment records are grouped into gateway, method, and bank features; an Isolation Forest proposes unusual groups and deterministic thresholds provide severity signals.\nGenAI engineer: A LangGraph workflow combines named read-only SQL queries, analytics, and retrieved procedure text, then asks a human to review sensitive actions."),
 ]),
 ("02 Business Problem", [
  ("Why payment operations are difficult", "A payment may be captured, failed, authorized, or still pending. The customer, merchant, gateway, and operations team may need different answers. A failed attempt may have a recorded error code, but the record may not contain the full root cause. When evidence is spread across files and dashboards, an operator spends time locating facts before making a decision."),
  ("Before and after", "Before a structured workflow, an operator may search a CSV, calculate a failure rate manually, look up a procedure, and separately record a decision. After organizing the steps, PayBridge can validate an import, store accepted records, produce consistent metrics, flag an unusual group, retrieve supporting text, and persist review information. This is a demonstration of a workflow pattern; it is not evidence of measured operational time savings."),
  ("Problem to capability map", "Payment lookup answers what the saved record says. Analytics answers how a group behaves within a stated time window. Anomaly detection highlights an unusual aggregate. Investigation assembles evidence. Approval captures a human decision for an application action. Audit records activity. These concepts should not be mixed: approval is not a payment outcome, and an anomaly signal is not proof of fraud."),
  ("What PayBridge does not claim", "It does not connect to a bank's private switch logs, establish that every uploaded row came from a provider, guarantee that a failed payment's cause is known, or automatically reroute real payment traffic. Synthetic data and explicit demo behavior exist in the repository. The guide uses status labels wherever this distinction matters."),
 ]),
 ("03 System Architecture", [
  ("The main layers", "The Streamlit app renders customer, merchant, and admin views. FastAPI provides REST endpoints and serves a separate static landing page from the same application. Service modules implement checkout, ingestion, data quality, analytics, investigation, and other business logic. SQLAlchemy connects these paths to a configured SQL database. The ML and AI components operate on selected database facts and local reference documents."),
  ("How a request travels", "A user interaction begins in Streamlit or an API client. A request reaches a view or FastAPI route. The route validates inputs, calls a service, and opens a SQLAlchemy session when data is required. The service reads or writes database rows and returns structured results. Streamlit formats those results for the user. Some checkout helpers are called directly from the Streamlit process, while API callers can use the HTTP checkout endpoints; do not imply that every screen is a fully API-separated client."),
  ("Where the layers live", "Primary code paths include frontend/dashboard.py and frontend/views/ for Streamlit; backend/app/api/main.py and backend/app/api/checkout.py for FastAPI; backend/app/db/base.py for engine/session setup; backend/app/models/ for SQLAlchemy models; backend/app/services/ for domain operations; backend/app/analytics/ for named queries and metrics; backend/app/ml/anomaly.py for anomaly logic; backend/app/agent/ for LangGraph and tools; and backend/app/rag/ for retrieval and Ollama calls."),
  ("Architecture diagram", "The diagram below is a simplified reading map. It shows the main direction of data, not a claim that every page is wired to every service."),
 ], "architecture"),
 ("04 End-to-End Payment Operations Story", [
  ("One coherent story", "A customer chooses cafe menu items and a payment method. The order total is calculated from the menu. A wallet payment uses simulated stored credit; a Razorpay payment creates a provider order and waits for server verification. The resulting payment record is visible to the merchant and platform operations views. Separately, CSV ingestion can add compatible payment records from another source. SQL analytics summarizes saved rows, while anomaly and investigation modules help an operator examine unusual patterns."),
  ("The operational loop", "Payment or CSV data → validation → SQL storage → metrics → anomaly or alert signal → investigation evidence → recommendation → human decision → local action record and audit. Each arrow has a responsible module. If the current UI uses illustrative evidence, hard-coded sample text, or a demo-only mitigation, say so at that exact step rather than presenting the whole chain as live automation."),
  ("Sources are not payment methods", "A source identifies how a row entered the platform, such as a CSV batch, generated synthetic set, demo wallet, or Razorpay test checkout. A method identifies how the payer attempted to pay, such as UPI, card, netbanking, or wallet. A source label such as ‘test CSV’ is not the same as a payment rail. The payment model contains both kinds of provenance fields."),
  ("Diagram", "Use this flow to narrate the project in a demo. Pause to identify which data is synthetic and which provider result has been verified."),
 ], "lifecycle"),
 ("05 Customer Portal", [
  ("What the customer sees", "The Customer view is rendered from frontend/views/customer_portal.py. It shows a cafe menu, quantity choices, an initially empty cart, a total, payment choices, order/payment progress, and a receipt when the stored payment satisfies the receipt lookup. The cafe menu and price calculation live in backend/app/services/cafe_menu.py. Quantities are checked as whole numbers within the code's allowed range, and the server-side helper computes the total from known item prices."),
  ("Wallet payment", "The demo wallet is application data stored in the demo_wallets table. Its model has a default balance of INR 50,000, but this is simulated credit, not a bank account or Razorpay balance. backend/app/services/demo_wallet.py performs the wallet order/payment operation and records the resulting payment with a source that identifies it as a demo-wallet transaction. The receipt labels this path as simulated and states that no money moved through Razorpay."),
  ("Razorpay checkout", "For the provider path, PayBridge creates a Razorpay order, opens Standard Checkout, receives checkout identifiers and signature, and calls server verification. The server checks the signature and fetches provider payment details before inserting a captured payment. A browser success callback alone is not enough. The receipt is based on a matching captured database row; a pending or failed verification should not be described as paid."),
  ("Customer boundary", "The customer screen is a demonstration surface and uses a configured customer identity in its Streamlit flow. The role selector is not proof of authenticated customer identity. The backend has authentication components, but the public checkout routes currently do not include the same require-role dependency used by several operational endpoints. Treat the UI as a prototype, not a secure customer-facing production checkout."),
 ]),
 ("06 Merchant Portal", [
  ("Merchant view", "frontend/views/merchant_portal.py selects the configured Rameshwaram Cafe merchant and reads its PaymentTransaction rows. The overview calculates captured volume from CAPTURED payments, counts failed and pending/authorized statuses, and provides buttons to show filtered payment rows. Recent customer orders are loaded from payment_orders joined to cafe_order_items. This is based on database content, not only the uploaded CSV; the source field helps distinguish imports from checkout records."),
  ("Useful merchant questions", "A merchant asks: what is the status of this order, how many payments completed, what is pending, and what failure reason is actually saved? The payment table is a record-level answer. The overview is an aggregate answer. If the failure reason is blank, the system should say it is unavailable rather than inventing a reason. Settlement is also a separate process from capture; a captured payment is not automatically the same as a completed payout."),
  ("What is illustrative", "Some fulfillment or operational advisories in the merchant interface are presentation content. The code reads payment/order records for the ledger and visible counts, but no food kitchen system or external merchant point-of-sale integration is present in the reviewed files. Do not say PayBridge updates a real kitchen or merchant fulfillment platform."),
  ("GMV and profit", "Captured GMV is the sum of captured payment amounts in the selected group. It is payment volume, not merchant profit. Profit requires costs and other accounting inputs. An average ticket is captured amount divided by captured payment count; explain its denominator if you show it."),
 ]),
 ("07 Admin Portal", [
  ("Admin responsibilities", "The Admin dashboard is implemented in frontend/views/admin_dashboard.py. It brings together overview metrics, payment records, anomaly-related screens, data pipeline controls, investigation links, approvals, and audit activity. Some parts are database-backed and some incident panels use fixed illustrative scenarios. Read each section's implementation before describing it as live."),
  ("Overview", "The current admin overview computes transaction counts, captured volume, success rate, and failures from payment rows in the configured SQL database. A setup helper also creates or refreshes one global alert from the aggregate payment summary. That alert is a demo alert mechanism and is not identical to the Isolation Forest detector's per-group anomaly run. The distinction is important when explaining where an alert came from."),
  ("Operations workflow", "The operator can view stored payments, examine source information, enter a payment reference for a saved-record lookup, inspect an investigation, and record an approval decision. A separate investigation workspace contains hard-coded sample narrative, latency, percentages, and error distributions for certain prompts; those figures are not all calculated from live database rows. Use the payment-reference lookup when demonstrating a database-grounded answer."),
  ("Admin identity", "The UI's persona switch is for navigation and demonstration. Several API operations require a JWT and role permissions, but the Streamlit persona switch by itself is not an authenticated account boundary. This should be disclosed as a prototype limitation."),
 ]),
 ("08 Streamlit Frontend", [
  ("Entry points", "frontend/app.py prepares import paths and runs frontend/dashboard.py. frontend/dashboard.py builds the top-level navigation and selects which renderer to call for Admin, Merchant, or Customer. Reusable page fragments and formatting are in frontend/components.py and frontend/styles.py. Individual screens sit in frontend/views/. The FastAPI application also serves a static landing page, so there are two browser-facing surfaces: the landing page and the Streamlit operations UI."),
  ("State and reruns", "Streamlit reruns the Python script after widget interactions. Temporary interaction values may live in st.session_state; saved business facts should live in the database. A widget key should not be changed after that widget has already been created during the same run. The prior screenshot showed this exact class of StreamlitAPIException. The code now uses navigation callbacks for the affected flow, but any future session-state change must follow Streamlit's widget lifecycle."),
  ("How it communicates with services", "Some pages query SQLAlchemy sessions directly and some make HTTP requests through shared API helpers. The checkout page imports FastAPI endpoint functions and request/response models directly for local integration, while the browser checkout script talks to Razorpay. This is a pragmatic prototype structure; it is not a uniformly separated frontend/API architecture. See frontend/views and backend/app/api for the precise screen-to-service paths."),
  ("Limit", "A successful widget click is not automatically a successful backend operation. For a demo, check the saved payment, workflow, or audit row when one is expected. Avoid saying the entire UI is connected to every API unless that specific action has been traced."),
 ]),
 ("09 FastAPI Backend", [
  ("What an API does", "An API is a contract between a caller and a service. A caller sends an HTTP method, a path, and sometimes JSON or an uploaded file. FastAPI validates the request, calls a Python function, and serializes the result as JSON or a file response. OpenAPI documentation is generated from the routes and schemas, and is available at /docs while the service is running."),
  ("Application setup", "backend/app/api/main.py creates the FastAPI application, installs middleware, includes the checkout router, mounts static assets, defines application lifespan, initializes SQLAlchemy tables, seeds demo users in demo mode, and registers API routes. backend/main.py is a small entry point that adjusts import paths and exposes the application. backend/app/db/base.py builds the SQLAlchemy engine using DATABASE_URL and provides request-scoped sessions."),
  ("Request lifecycle", "For a protected route, FastAPI resolves dependencies such as get_db and get_current_user. The route checks role permissions, validates input via Pydantic, invokes domain logic, then commits or returns a result. A `Session` is closed after the request. This gives a simple separation between HTTP handling, data models, and service code, although several routes still contain orchestration logic."),
  ("Error handling", "A missing record should result in a not-found response; an invalid CSV should return a useful validation/import result; provider verification errors should keep the payment unconfirmed; and a downstream model outage should not necessarily make the API unavailable. The code includes several of these fallbacks. When debugging, start with `/health`, then `/docs`, then the response body and server logs."),
 ]),
 ("10 Important API Routes", [
  ("Core routes", "The following paths are registered in backend/app/api/main.py and backend/app/api/checkout.py. Request bodies and exact response schemas are defined in backend/app/schemas/api.py or checkout.py. Use the live `/docs` schema as the authoritative request example for the running code."),
  ("Route list", "GET /health — database and optional Ollama/RAG readiness summary.\nPOST /auth/login and GET /auth/me — obtain and inspect an API user token.\nGET /alerts and GET /alerts/{alert_id} — read alert records and related workflow identifiers.\nPOST /alerts/{alert_id}/investigate — execute the investigation graph.\nGET /workflows/{workflow_id} — retrieve saved evidence, recommendation, and decision state.\nPOST /workflows/{workflow_id}/approve or /reject — decide a pending workflow and handle the local follow-up.\nGET /audit — inspect audit records.\nGET /api/v1/payments/kpis and /api/v1/payments/dashboard — calculated payment metrics.\nPOST /api/v1/ingestion/csv and GET /api/v1/ingestion/runs — import a CSV and view runs.\nPOST /api/create-order and /api/verify-payment — Razorpay checkout integration."),
  ("Authorization nuance", "The analytics, ingestion, alert, workflow, approval, audit, and related operational routes use permission dependencies in the code. The checkout router's create-order and verify-payment endpoints do not currently declare the same JWT permission dependency. That is a security hardening issue for any public deployment. Do not share development credentials or real test secrets in documentation or screenshots."),
  ("Database effect", "GET routes normally read records or compute results. CSV ingestion inserts payment/order/customer rows and ingestion lineage. Investigation creates Workflow, Approval, and AuditLog rows. Approval updates its Approval row and may write local ActionRecord data. Checkout inserts PaymentOrder on order creation and a PaymentTransaction and PaymentEvent after provider verification. Exact side effects should be checked in their route/service before replaying an action."),
 ]),
 ("11 Razorpay Checkout and Verification", [
  ("Order and payment are different", "A Razorpay order is a request to collect a specified amount. It is not proof that the payer completed checkout. The browser opens Standard Checkout using the public key ID and order ID. The secret key stays in the server environment. After checkout returns a payment ID, order ID, and signature, PayBridge sends these details to its server verification function."),
  ("Verification checks", "backend/app/api/checkout.py verifies the signature using HMAC-SHA256 or the SDK helper, finds the local order, fetches the payment from Razorpay, checks provider order ID, amount, currency, and captured status, then stores a CAPTURED transaction. It is idempotent for an already stored matching captured payment. If verification fails, the project should not show a captured receipt. The receipt query in the customer page requires a matching customer, order, payment ID, and captured status."),
  ("Money arithmetic", "The API accepts the payment amount in paise. For INR 280.00, the order amount is 28,000 paise because 1 rupee = 100 paise. The current prototype calculates an illustrative 2% fee and 18% tax on that fee when recording a checkout transaction: fee = ₹280 × 0.02 = ₹5.60; fee tax = ₹5.60 × 0.18 = ₹1.008, rounded half-up to ₹1.01; net amount = ₹280 − ₹5.60 − ₹1.01 = ₹273.39. This is an application calculation, not a statement of Razorpay's actual fee schedule."),
  ("Test mode and limits", "When the configured key ID begins with `rzp_test_`, the saved source is labeled RAZORPAY_TEST. A completed test payment should appear in the Razorpay Test Mode account and in PayBridge after successful verification. This walkthrough does not independently prove a currently running Render payment. Credentials are not copied into this guide. Test keys must stay out of Git and the public deck."),
 ], "checkout"),
 ("12 Database Basics", [
  ("Tables, rows, and columns", "A database table is like a structured sheet. A row represents one entity, such as one payment. Columns describe attributes, such as amount, status, method, merchant ID, or timestamp. A primary key uniquely identifies a row. A foreign key connects related tables, such as a transaction to its order. Indexes help the database find rows more quickly when queries filter by common fields."),
  ("PayBridge database configuration", "backend/app/core/config.py reads DATABASE_URL. If it is not set, the local configuration selects a SQLite file under backend/data, preferring paybridge.db when it exists and otherwise payment_data.db. backend/app/db/base.py creates the engine and session factory, then `init_db()` imports model metadata and calls SQLAlchemy `create_all`. This is schema creation at startup, not a complete database migration workflow."),
  ("PostgreSQL", "The requirements include psycopg2-binary, and the engine accepts a PostgreSQL SQLAlchemy URL. That means the code has a PostgreSQL connection path. It does not by itself prove that the current database was migrated, that production data was copied, or that a deployed service uses PostgreSQL. The root docker-compose.yml shown in this repository runs API and Streamlit with a shared SQLite file volume; it does not define a Postgres service."),
  ("Alembic status", "Alembic configuration and one revision file exist, but the reviewed initial revision has empty upgrade and downgrade bodies. Therefore a working, complete Alembic schema migration is NOT IMPLEMENTED by that revision. The operational schema is currently created through SQLAlchemy metadata at startup. Do not tell an interviewer that a real schema migration is complete."),
 ]),
 ("13 Data Model and Relationships", [
  ("Payment entities", "The payment models live in backend/app/models/payments.py. Merchant identifies the business; Customer is associated with a merchant; PaymentOrder stores the order amount, currency, customer/merchant reference, receipt, and order status; PaymentTransaction stores payment status, payment method, bank, gateway, amounts, error fields, and provenance. PaymentEvent stores state-change events; PaymentAttempt represents individual retry attempts; CafeOrderItems stores the cart summary used by the customer receipt."),
  ("Operations records", "PaymentIngestionRun stores the source identifier, run status, received/accepted/rejected/duplicate counts, and archive/report paths. PaymentIngestionRecord stores rejected row details. Workflow stores the alert, investigator, recommendation, evidence, approval status, errors, and latency. Approval records the pending/approved/rejected choice. ActionRecord stores local business actions and idempotency keys. AuditLog stores workflow/node/tool outcomes and decision events."),
  ("Additional schema tables", "The payment model file also defines refunds, settlements, settlement items, disputes, reconciliation discrepancies, gateway health metrics, and incidents. A class existing in source does not prove that a screen or integration fully uses it. The app also retains a separate older billing model in backend/app/models/core.py (buildings, apartments, devices, water usage, revenue, anomalies, and alerts). These older tables explain why some legacy docs and routes use billing terms."),
  ("Relationship sketch", "Merchant → orders → transactions; Customer → orders/transactions; PaymentTransaction → events and attempts; an ingestion run → rejected row records; an alert → workflow → approval → local action and audit rows. Some foreign keys are enforced in SQLAlchemy models, while other associations are represented by matching identifiers. Inspect each model before asserting relational guarantees."),
 ]),
 ("14 CSV Ingestion", [
  ("Input and mapping", "The payment import service is backend/app/services/ingestion_payments.py. It reads a CSV and maps recognized alternate headers to a canonical set, for example txn_id to payment_id, txn_amount to amount, payment_mode to method, and payment_status to status. It creates a PaymentIngestionRun before processing, archives the raw source, processes rows, and tracks accepted, rejected, and duplicate counts."),
  ("Processing steps", "The basic sequence is: read header → detect mapping → ensure required fields exist → normalize values such as method and status → parse amounts and dates → check whether a payment ID is already stored → create structured payment/order/customer records where appropriate → save accepted results → write rejected rows with reasons → finish the run with counts and status. The API rejects CSV uploads larger than 10 MB before passing them to the service."),
  ("What happens to uploaded records", "Accepted CSV rows become database records; they are not a separately generated ‘processed CSV’. The original upload is archived and rejected rows are written separately. Ingestion history is in payment_ingestion_runs and payment_ingestion_records. The admin payment ledger reads stored payment rows. The source field distinguishes imported rows from synthetic and Razorpay checkout rows."),
  ("What messy means", "A file with alternate but recognized column names may still be mapped. Invalid required data, unrecognized timestamps, duplicate IDs, or missing required headers can cause rejection or import failure. Arbitrary prose or an unrelated spreadsheet is not automatically converted into trustworthy payment events. Review the import report and accepted rows before treating totals as meaningful."),
 ]),
 ("15 Data Quality Guardrails", [
  ("Why checks matter", "Data quality is a set of checks that protects later calculations. If an amount is missing, a status is misspelled, or the same payment ID appears twice, an aggregate can be misleading. PayBridge has row-level checks in the import service and a separate run_data_quality_audit function for stored payment relationships and financial rules."),
  ("Examples", "A required payment ID that is missing cannot reliably identify a transaction. A negative amount is invalid for this payment model. A duplicate payment ID should not silently create a second ledger payment. An invalid date cannot reliably place an event in a time window. A stored captured transaction should have an appropriate capture timestamp according to the audit rules. A failed transaction without an error code is less useful for diagnosis."),
  ("Financial invariant", "The code checks amount = net_amount + fee + tax. Suppose amount is ₹280.00, fee is ₹5.60, and tax is ₹1.01. Then net_amount should be ₹273.39, because ₹273.39 + ₹5.60 + ₹1.01 = ₹280.00. Decimal arithmetic and two-place rounding reduce common binary floating-point errors. This is a consistency check, not proof that the fee inputs are correct for a real provider."),
  ("Quality score caveat", "The audit function counts checks and returns a percentage based on checks passed. That score is a summary of the checks that function runs; it is not a universal measure of data truth. A score of 100% only means all included rules passed for the inspected database snapshot."),
 ]),
 ("16 Analytics and Useful Mathematics", [
  ("Payment KPIs", "backend/app/analytics/payment_analytics.py runs named SQL queries and formats deterministic results. It can summarize attempts, captured, failed and pending counts, captured GMV, fee totals, average transaction value, method and bank breakdowns, merchant performance, hourly trend, refunds, settlements, top errors, discrepancies, gateway comparison, and retry recovery. The API returns KPI and dashboard routes."),
  ("Success and failure rates", "The KPI engine defines terminal payments as captured + failed and calculates success rate as captured ÷ terminal × 100. Pending/authorized rows are not in that denominator. Example: 80 captured and 20 failed gives 80 ÷ (80 + 20) × 100 = 80% success; failure rate is 20%. If there are 10 pending rows, do not quietly add them to the denominator when reproducing this metric."),
  ("GMV, fees, and averages", "Captured GMV is the sum of captured amounts. Average transaction value is GMV divided by captured count, where available. Effective take-rate in this code is calculated as fee total ÷ GMV × 100. GMV is not profit; profit would require operating costs and other accounting data. A metric should always state its time window and denominator."),
  ("Interpreting a pattern", "If a payment-method group has 4 failures out of 10 terminal payments, failure rate is 4 ÷ 10 × 100 = 40%. That may meet the code's chosen anomaly threshold, but an anomaly is a prompt to inspect, not a fraud verdict or confirmed gateway outage. A tiny sample can be noisy; bank success-rate queries include a minimum-attempt guard in their documented code."),
 ]),
 ("17 Machine Learning Anomaly Detection", [
  ("The model input", "backend/app/ml/anomaly.py groups payment_transactions by gateway, method, and bank. It builds features including total attempts, captured count, failed count, failure rate, total amount volume, failed volume, average amount, and retryable failure count. Derived ratios are calculated before scoring. The group, not an individual customer's intent, is the unit of analysis."),
  ("Isolation Forest", "Isolation Forest is an unsupervised anomaly-detection algorithm. It isolates unusual rows by repeatedly splitting feature values; unusual combinations tend to be isolated with fewer splits. The code uses scikit-learn IsolationForest with 100 estimators and a configurable contamination setting defaulting to 0.08. With fewer than three groups, the current code skips model fitting and assigns a small default score."),
  ("Rules and severity", "Deterministic rules add meaning to the score: a UPI failure rate at or above 20% with at least five attempts, a bank group at or above 25% with at least five attempts, a broader channel at or above 20% with at least ten attempts, or a threshold count of retryable failures can create signals. Severity uses thresholds in code. ML-only findings are capped at LOW; rule findings can produce higher severities. Thresholds are prototype rules, not learned business policy."),
  ("What it proves", "The implementation demonstrates feature creation, unsupervised scoring, and rule-assisted anomaly records. The repository does not establish production accuracy on representative labeled traffic. A broad precision/recall benchmark and a live streaming detector are not demonstrated. Re-running detection deletes existing anomaly and alert rows before inserting refreshed results, so this behaves as a batch refresh rather than an append-only event stream."),
 ]),
 ("18 Alerts and Incidents", [
  ("Two paths to an alert", "There is an ML detector path that writes anomaly and alert rows from payment groups. There is also backend/app/services/demo.py, which refreshes a single alert called ALT-PAYMENT-DEMO from aggregate payment counts. That helper calculates a global failure rate and labels one alert. These paths should not be described as the same detector. The second is a demonstration alert refresh; the first is the model/rule detection service."),
  ("Investigation input", "The current FastAPI incident investigation endpoint accepts an alert ID and reads an Alert row. In this repository, Alert is part of the older core model, reused as an alert record. Workflow intake looks up alert fields such as metric, entity, billing month, severity, and evidence summary. Payment facts are then available through the payment query registry and analytics tools. This is a hybrid transition between older shared alert structures and payment models."),
  ("One scenario", "For a clear explanation, use a synthetic UPI failure cluster. The database contains multiple payment statuses; the aggregation calculates the observed failure rate; an anomaly rule can flag the group; the alert becomes an investigation target; SQL and procedure retrieval contribute evidence; and the admin records a decision. If using the UI's Rameshwaram narrative with fixed bank-latency figures, explicitly state that part of that screen is illustrative rather than live bank telemetry."),
  ("No unsupported causal claim", "A pattern can support a hypothesis such as gateway/network timeouts when error codes and comparisons point that way. It cannot prove that a bank or network caused the issue unless provider/bank evidence supports it. Keep the terms FACT, EVIDENCE, INFERENCE, and UNKNOWN distinct."),
 ]),
 ("19 LangGraph Investigation Workflow", [
  ("What LangGraph contributes", "LangGraph represents a multi-step workflow as nodes that read and update shared state. A node performs a bounded step; an edge determines which node runs next. It is useful here because payment investigation involves ordered evidence collection, validation, recommendation, approval gating, and audit logging."),
  ("Actual graph nodes", "backend/app/agent/workflow.py wires nine nodes in build_graph: intake → planner → sql_investigator → retrieval_investigator → analytics_investigator → evidence_validator → recommendation_generator → approval_gate → audit_logger. The action_executor function is not included in this first graph; it is called through resume_after_approval after an approval decision is saved. This is why counting it as one ordinary ten-node graph would be inaccurate."),
  ("State and outputs", "WFState carries workflow ID, alert ID, user/role, question, trace ID, SQL results, retrieved documents, metrics, evidence verdict, recommendation, approval status, final action, errors, and node timings. Each node updates part of the state and writes audit information. The workflow stores evidence/recommendation JSON and marks the saved workflow as awaiting approval, completed, or failed."),
  ("Planner and tools", "The planner chooses application-owned investigation steps. The SQL tool uses named query allowlists; the RAG tool returns procedure chunks; the analytics tool computes trusted metrics. The LLM is not allowed to invent and execute arbitrary SQL. The action tool is separate and is reached after a saved approval. The first graph and post-approval continuation are shown below."),
 ], "langgraph"),
 ("20 Retrieval-Augmented Generation", [
  ("RAG in plain language", "RAG means Retrieval-Augmented Generation. Instead of asking a language model to answer only from its training, the application searches a local set of reference documents, selects relevant passages, and gives those passages to the model as context. The answer can then point to a source section. RAG does not guarantee truth; retrieval may miss relevant text, and the model can still misinterpret it."),
  ("PayBridge retrieval", "backend/app/rag/store.py reads text documents under backend/data/documents, parses metadata, splits at numbered sections, and subdivides long sections using configured chunk size and overlap. The default retrieval method is scikit-learn TF-IDF with cosine similarity. The store is held in process memory and is not a managed vector database. Optional EMBEDDING_MODE=ollama uses a local embedding path when configured. There is no LlamaIndex dependency in requirements.txt or the reviewed code."),
  ("What is embedded", "In default TF-IDF mode, terms and term patterns are represented numerically and compared using cosine similarity. This is lexical retrieval: it works best when the query shares words with the procedure. It is not a neural embedding model and not semantic matching at the same level as a trained sentence embedding. The system returns document ID/version/section citations with each hit."),
  ("Untrusted retrieved text", "Retrieved documents are treated as untrusted content by backend/app/agent/tools/rag_tool.py. The tool scans for selected instruction-injection patterns and wraps retrieved text inside a clearly marked untrusted block; flagged text is redacted before model use. This is a guardrail, not a proof that all malicious prompt injection is stopped."),
 ], "rag"),
 ("21 Evidence and AI Recommendation", [
  ("Evidence streams", "The investigation can combine three broad evidence streams: SQL rows or counts from named queries, deterministic analytics, and policy/procedure documents from RAG. backend/app/agent/evidence.py defines an EvidenceBundle and checks that at least two evidence streams succeeded and that a baseline condition is available before it calls evidence sufficient. It also has a numeric-claim grounding check against known numbers in computed data."),
  ("How to interpret the answer", "A database value is a fact about what is stored. A retrieved procedure is a policy reference. A conclusion connecting them is an inference. A missing provider response or absent error description is uncertainty. The AI should not transform ‘no record found’ into ‘the payment failed’; it should report that the configured database has no matching record."),
  ("LLM execution", "The only LLM client in the current code is backend/app/rag/ollama_client.py, which calls a local Ollama server. Settings default the model name to qwen2.5:3b-instruct, but code configuration is not proof the model is installed or reachable. If unavailable, the client returns a structured unavailable state and the workflow has deterministic fallback behavior. For documentation, label actual runtime model availability NOT VERIFIED FROM REPOSITORY."),
  ("Quality limits", "The grounding check is a lightweight numeric token check, not a full semantic verifier. TF-IDF may miss paraphrases. A source citation tells the user which chunk was retrieved, not that the chunk fully supports every sentence. Recommendations must remain reviewable and should include a caveat when evidence is insufficient."),
 ]),
 ("22 Human Approval and Mitigation", [
  ("Why human review exists", "Suppose payment evidence suggests a gateway route may be degraded. An automated action could be wrong, too broad, or based on incomplete data. Human review adds a checkpoint: an operator sees the evidence, decides whether the proposed application action is appropriate, and leaves a record of who decided and why. The decision is about an operational response, not whether a customer's payment succeeded."),
  ("API workflow", "In the backend API path, the workflow creates a pending Approval row when required. The approve route changes that saved row, writes a human_decision AuditLog entry, and calls resume_after_approval. The post-approval action executor checks the saved approval in the database and invokes a registered local action such as creating an incident, ticket, or notification record. The rejection path records the decision and does not execute that action."),
  ("No live routing", "The registered actions are local mock/business records. They do not alter Razorpay routing, bank weights, customer checkout settings, or external payment traffic. Thus ‘approved and executed’ means the local action handler completed, not that a bank route changed. Operational mitigation is simulated in this project."),
  ("UI paths can differ", "The newer API-backed workflow page and the Admin dashboard's illustrated incident card are not necessarily the same approval object. The Admin card has its own decision persistence under a fixed illustrative workflow identifier; other workspace sections contain hard-coded example narratives. Demonstrate one known path and verify its saved result rather than assuming all approval controls share a workflow."),
 ], "approval"),
 ("23 Audit Records", [
  ("What audit means here", "An audit record is a stored trace that says which workflow or node ran, what tool was involved, what outcome occurred, when it happened, and whether approval was required or recorded. backend/app/models/ops.py defines AuditLog. The workflow helper writes node-level events, and the approve/reject API writes human decision events with a hash of the decision payload."),
  ("What audit does not mean", "An audit table is not automatically an immutable ledger. The current database is an ordinary SQL database, and there is no demonstrated cryptographic chain or write-once storage in this code. The record helps explain application activity, but production compliance would require retention, access controls, integrity protection, monitoring, and operational procedures."),
  ("Useful trace", "A useful audit walk-through starts from workflow_id, then looks at node records, the pending approval, the human decision, and any local ActionRecord. The trace ID and workflow ID help connect logs. Avoid exposing secrets or unnecessary personal data in audit payloads; the code stores hashes and selected status details for some events."),
 ]),
 ("24 Security Boundaries", [
  ("Implemented safeguards", "backend/app/core/security.py uses password hashing and JWT access tokens. API dependencies provide role-based permissions for operations such as viewing, investigating, configuring, approving, and rejecting. SQL access for the investigation tool uses named allowlisted queries and row caps. Retrieved document text is treated as untrusted, and a saved database approval is checked before local actions execute."),
  ("Prototype caveats", "The configured DEMO_MODE seeds development accounts. The Streamlit role switch is only a UI persona and does not authenticate a user. Checkout endpoints do not currently use the same authentication dependency as operational endpoints. The FastAPI CORS middleware allows all origins. A default development JWT secret exists in source configuration and must be replaced outside demo mode. Rate limiting, production identity management, tenant isolation, and deployment hardening are not established by this repository."),
  ("Secrets", "Razorpay credentials are expected as environment configuration or local .env values. The source tree includes .env.example but .env is ignored by Git. This guide intentionally does not read or reproduce the local .env. Never place secrets in a report, slide, screenshot, public repository, or frontend code. A public key ID may be used by checkout, but the secret must remain server-side."),
  ("Safe language", "Say ‘prototype includes JWT and role checks on protected API routes’ rather than ‘secure payment platform’. Security is a set of controls and review, not a single library or checkbox."),
 ]),
 ("25 Docker and Running Locally", [
  ("Why Docker is present", "Docker packages an application with its runtime and dependencies into a container image. The root Dockerfile builds the FastAPI service image; frontend/Dockerfile builds the Streamlit image. docker-compose.yml runs those two services and mounts the same backend/data directory so the app processes can use the same SQLite database file. This supports a repeatable local demo setup."),
  ("Compose scope", "The checked docker-compose.yml contains API and dashboard services, a shared SQLite path, and Ollama pointed at host.docker.internal. It does not define a PostgreSQL service or container. Ollama itself is not bundled into the compose file. Docker files and a GitHub Actions Docker build job are present, but the repository audit status of the currently running user environment was not independently tested while authoring this guide."),
  ("Local launcher", "start-demo.ps1 changes to the project root, selects the local database file, runs setup_demo.py, starts FastAPI on 127.0.0.1:8000 if it is not already running, checks /health, and then launches Streamlit. The expected local addresses are Streamlit 127.0.0.1:8501, API 127.0.0.1:8000, and API docs 127.0.0.1:8000/docs."),
  ("First run", "Install requirements in a virtual environment. Copy .env.example to .env only for local configuration and replace development secrets. Run the demo setup. Start the services. Check API health and the Streamlit page. Use a disposable database before running tests or experiments that write data. Do not upload .env or a database file containing private information."),
 ]),
 ("26 Configuration and Deployment", [
  ("Environment settings", "backend/app/core/config.py reads DEMO_MODE, DATABASE_URL, OLLAMA_BASE_URL, OLLAMA_MODEL, embedding mode, chunk settings, JWT settings, Razorpay credentials, SQL limits, and data paths. .env.example documents the expected variables. The code reads configuration at process startup except the checkout credential helper also rereads a local .env pair per request to support key rotation locally. A cloud deployment should use its platform's secret settings, not a committed env file."),
  ("Render status", "The repository snapshot reviewed for this guide has no render.yaml, Procfile, or other Render service manifest at the root. The user-provided Render URL and reported deployment are NOT VERIFIED FROM REPOSITORY. The Docker Compose configuration is local and binds ports to loopback. A running public deployment may have been configured manually or from another revision, but the source tree alone does not prove its service settings, persistent disk, database URL, model access, or current health."),
  ("Persistence risk", "The local database file is mounted in Compose. A cloud container filesystem may be ephemeral unless persistent storage is configured. If the deployed app uses SQLite without a persistent disk or mounted volume, writes may disappear after redeploy/restart. The current repository does not confirm the user's hosted database configuration."),
  ("Safe deployment explanation", "Say ‘I deployed a public demo’ only if you personally checked it after deployment. Then state the exact database and model configuration you observed. If you have not inspected those platform settings, say that persistence and hosted configuration have not been verified."),
 ]),
 ("27 Tests and CI", [
  ("What is present", "The repository has unit tests, integration tests, evaluation scripts, and .github/workflows/ci.yml. The workflow installs dependencies, runs Ruff, Mypy, setup, pytest with coverage, RAG and agent evaluation scripts, and separately builds API and dashboard Docker images. This shows that automated checks are designed into the project."),
  ("What this guide verified", "This writing pass inspected the test files, CI workflow, and existing README validation statement. It did not execute the test suite or inspect the latest remote CI run. Therefore the current pass does not claim that all tests or jobs are green. The README contains a reported previous validation total; use the latest GitHub Actions result when reporting current status."),
  ("Evaluation measures", "A RAG evaluation set and an agent evaluation script exist. Evaluation results are only meaningful for the defined test cases, data, and scoring rules. A high pass rate on a small curated set is not proof of general accuracy. Anomaly detection also needs a broader labeled benchmark before precision or recall claims are appropriate."),
  ("How to explain a failed check", "A CI failure identifies a check and a log, not necessarily a product failure. For example, lint can fail while Docker build succeeds. Open the failed job, identify the first error, reproduce the specific command locally, fix only the cause, and rerun the relevant check. Report both the successful and unsuccessful checks accurately."),
 ]),
 ("28 Repository File Map", [
  ("Where to start", "README.md is the project overview. frontend/app.py and frontend/dashboard.py start Streamlit. backend/main.py and backend/app/api/main.py start FastAPI. backend/app/api/checkout.py owns provider checkout routes. The following map links the project story to actual modules."),
  ("Business-to-code map", "Customer screens → frontend/views/customer_portal.py; cafe menu and pricing → backend/app/services/cafe_menu.py; simulated wallet → backend/app/services/demo_wallet.py.\nMerchant screen → frontend/views/merchant_portal.py.\nAdmin overview/pipeline/approvals → frontend/views/admin_dashboard.py. API-backed approvals → frontend/views/approvals.py and backend/app/api/main.py.\nPayment models → backend/app/models/payments.py; older billing and Alert models → backend/app/models/core.py; workflow/audit/auth models → backend/app/models/ops.py.\nCSV import → backend/app/services/ingestion_payments.py; URL ingestion → backend/app/services/url_ingestion.py.\nPayment analytics → backend/app/analytics/payment_analytics.py and payment_queries.py.\nAnomaly detection → backend/app/ml/anomaly.py and backend/app/services/anomaly.py.\nLangGraph → backend/app/agent/workflow.py; evidence checks → backend/app/agent/evidence.py; SQL/RAG/action tools → backend/app/agent/tools/.\nRAG → backend/app/rag/store.py, retriever.py, ollama_client.py; procedures → backend/data/documents/.\nRuntime and packaging → start-demo.ps1, Dockerfile, frontend/Dockerfile, docker-compose.yml, .github/workflows/ci.yml."),
  ("Read source in order", "For a payment question, start with the Streamlit view, follow the service or API call, inspect the model, then inspect the SQL query or persistence path. For AI behavior, begin with the API route, then workflow node, then tool, then evidence model. This path-based approach is more reliable than reading the whole repository from top to bottom."),
 ]),
 ("29 Implemented and Simulated Matrix", [
  ("Status labels", "IMPLEMENTED means a concrete code path exists in the reviewed source. SIMULATED means the behavior is local or modeled rather than an external operational change. DEMO ONLY marks sample UI or seeded demonstration behavior. SIMPLIFIED IMPLEMENTATION marks a reduced prototype design. NOT IMPLEMENTED means the current source does not perform the function. NOT VERIFIED FROM REPOSITORY means source inspection cannot establish the runtime or deployment fact."),
  ("Matrix", "Razorpay order creation and server verification — IMPLEMENTED in code when valid keys and provider access are available; this authoring pass did not confirm a live completed payment.\nCustomer demo wallet — SIMULATED local balance and ledger record.\nCSV mapping/ingestion — IMPLEMENTED for supported CSV schema and validation; not arbitrary unstructured files.\nPayment analytics — IMPLEMENTED as deterministic SQL summaries.\nIsolation Forest and deterministic anomaly rules — IMPLEMENTED in source; benchmark quality not established.\nLangGraph evidence workflow — IMPLEMENTED in source with nine first-graph nodes and approval continuation.\nDefault TF-IDF RAG — IMPLEMENTED local lexical retrieval; optional Ollama embeddings/model depend on runtime.\nAI narrative — conditional local Ollama; model availability NOT VERIFIED FROM REPOSITORY.\nHuman approve/reject API — IMPLEMENTED for saved workflow decision and local action continuation.\nLive bank/gateway rerouting — NOT IMPLEMENTED.\nAudit rows — IMPLEMENTED as database records; immutable audit ledger NOT IMPLEMENTED.\nPostgreSQL configuration — IMPLEMENTED as a connection option; migrated/hosted PostgreSQL state NOT VERIFIED FROM REPOSITORY.\nAlembic revision — NOT IMPLEMENTED as a schema migration (empty upgrade/downgrade).\nDocker files and CI build job — IMPLEMENTED; local Compose execution and current remote job status NOT VERIFIED FROM REPOSITORY.\nRender deployment — NOT VERIFIED FROM REPOSITORY; no manifest present in the snapshot."),
  ("Why labels matter", "An interviewer will trust a clear prototype boundary more than a broad claim. ‘The app records an approved local action, but does not reroute a real gateway’ is precise. ‘The AI autonomously fixes payment failures’ is not supported by this code."),
 ]),
 ("30 Limitations and Troubleshooting", [
  ("Important limitations", "The repository mixes a current payment domain with older building/water/revenue models and some paths still use the shared legacy Alert structure. The Streamlit UI does not uniformly call the API. Some investigation screen numbers and narratives are illustrative. The hosted Render setup is not verifiable from the repository snapshot. PostgreSQL migration is not complete, the Alembic revision is empty, and Compose runs SQLite rather than Postgres. The LLM and dense embedding path require local Ollama and configured models. Production authentication, tenant isolation, CORS policy, rate limiting, persistent hosting, and security review need additional work."),
  ("Common local issues", "Database connection error: check DATABASE_URL and whether the selected database file exists and is writable. Streamlit page error: read the first application traceback line and confirm imports/paths. API unavailable: inspect the terminal running Uvicorn, then request /health. Razorpay order error: check test credentials, key pair, network access, and server logs; do not expose the secret. Missing receipt: check whether the payment was actually captured and verified and whether payment/order/customer IDs match. CSV rejected: inspect detected headers, required fields, rejected-row reason, and size limit."),
  ("RAG/model issues", "If the reference index is empty, confirm text files exist in backend/data/documents and that the app has permission to read them. If Ollama is unavailable, the optional generation path should report unavailable and a fallback may respond. Check `/health` for listed models and chunk count. Do not infer that an LLM is running just because OLLAMA_MODEL has a configured name."),
  ("PostgreSQL issues", "A PostgreSQL URL needs a reachable server, correct database/user/password, and psycopg2. A successful connection does not import existing SQLite rows. Data migration is a separate operation that must be backed up, run, checked for row counts and constraints, and tested with the application. This repository snapshot does not prove that migration has been completed."),
 ]),
 ("31 Simple Demo Walkthrough", [
  ("A focused five-minute story", "1. Start with the merchant problem: a failure pattern is hard to diagnose from separate records. 2. Show Customer and add a small set of cafe items; explain the total. 3. If using the demo wallet, explicitly state the balance is simulated. If using Razorpay test mode, complete a test checkout and show server-confirmed receipt only after verification. 4. Open Merchant Payments to show the stored payment and source. 5. In Admin, show the payment lookup or a selected batch's status counts. 6. Explain one anomaly as a signal, not a fraud verdict. 7. Open AI Investigation and distinguish a database-backed payment lookup from the illustrative incident narrative. 8. Review evidence, record a decision, then show the saved workflow/audit result. 9. Finish by saying actions are local and do not reroute real payment traffic."),
  ("What to prepare", "Before presenting, open the working application, check the health route and database setting, verify your test keys remain private, and select one known payment or sample alert. Keep a note of which screens are dynamic and which contain illustrative figures. Avoid multiple incidents if one complete story is clearer."),
  ("Narration rule", "Say what the screen shows, where the value came from, and what the system did with it. If you do not know the source, do not guess. For example: ‘This metric comes from saved CAPTURED and FAILED rows in the configured SQL database; this nearby bank latency narrative is illustrative.’"),
 ]),
 ("32 Interview Explanations", [
  ("30-second explanation", "PayBridge is a payment-operations prototype I built to make payment records easier to review. It stores compatible payment data, calculates operational metrics, highlights unusual groups, and provides an investigation workflow that combines SQL facts with retrieved procedures. A human reviews and records the next step. The dataset and operational actions are synthetic or simulated, and it does not reroute live payment traffic."),
  ("One-minute explanation", "The app has a Streamlit interface and FastAPI backend. Payment records can enter from a synthetic dataset, compatible CSV, demo wallet, or Razorpay checkout after server-side verification. SQLAlchemy stores orders, transactions, import runs, workflows, approvals, and audit entries. A payment analytics engine computes counts, captured volume, and rates. The anomaly detector groups by gateway, method, and bank, then combines Isolation Forest scores with deterministic thresholds. For an incident workflow, LangGraph calls named SQL queries, analytics, and local TF-IDF retrieval over operating procedures. Evidence is checked before a recommendation is shown; a human decision can trigger a local action record. It is a prototype, not live payment orchestration."),
  ("Three points to emphasize", "Problem: payment failures need organized investigation. Engineering: data is validated and stored, then metrics and evidence are assembled by bounded services. Governance: AI can suggest, but an authorized human reviews; actions in this project remain local/simulated. These are stronger than claiming that the AI automatically fixes payments."),
  ("Questions to ask yourself", "Can you show one file that creates the metric? Can you explain the success-rate denominator? Can you identify which evidence is computed versus retrieved? Can you show where approval is persisted? Can you state exactly what does not happen to real payment routing? If yes, your explanation will be credible."),
 ]),
 ("33 Interview Questions and Short Answers", [
  ("Why use FastAPI?", "It provides typed request validation, dependency injection, HTTP routes, and generated OpenAPI docs. In PayBridge, it exposes health, login, payment analytics, CSV ingestion, investigation, decisions, and checkout endpoints."),
  ("Why SQLAlchemy?", "It maps Python model classes to database tables and manages sessions/queries. PayBridge uses it to store merchants, orders, transactions, workflows, decisions, and audit rows."),
  ("Why SQLite and PostgreSQL?", "SQLite lowers local setup friction. The configuration can accept PostgreSQL connection URLs, but the migration and hosted PostgreSQL state are not verified in this source snapshot."),
  ("What does the anomaly model detect?", "It scores aggregates of payment records grouped by gateway, method, and bank, using attempt and failure features. Rule thresholds make some signals more interpretable. It is not a trained fraud classifier and does not prove root cause."),
  ("What is RAG used for?", "It retrieves relevant sections from local operating procedures to give the investigation relevant context. Payment facts still come from the database and analytics. Retrieval is TF-IDF by default; no LlamaIndex is present in the reviewed PayBridge dependencies."),
  ("Why a human approval gate?", "The system should not act on an uncertain recommendation without review. PayBridge persists a pending decision and only runs its registered local action after approval. It does not switch a live gateway route."),
  ("How is payment success verified?", "The server validates the checkout signature, fetches provider state, matches order, amount, and currency, and requires captured status before storing a captured record."),
  ("What are the limitations?", "Synthetic records, some illustrative UI narratives, incomplete uniform UI/API separation, no live routing, no proven hosted database migration, an empty Alembic revision, and runtime LLM/deployment state that must be checked separately."),
 ]),
 ("34 Why These Technologies", [
  ("Python and FastAPI", "Python lets the prototype share logic across data processing, analytics, machine learning, and APIs. FastAPI provides typed HTTP endpoints and generated docs. It is appropriate for this prototype because the project needs a small service layer that can be explored through Swagger."),
  ("SQLAlchemy and SQL", "SQL tables are suitable for structured transaction rows and relationships. SQLAlchemy provides a Python model/session layer; explicit SQL queries are used for analytics because grouping and aggregation are naturally expressed in SQL. Numeric amounts use Decimal/Numeric-style handling to reduce rounding errors."),
  ("Pandas and scikit-learn", "Pandas is used for feature-table construction and data manipulation; scikit-learn provides the Isolation Forest implementation. The detector combines this statistical proposal with business rules so a reviewer can see threshold-based reasons."),
  ("LangGraph, TF-IDF, and Ollama", "LangGraph helps order investigation work and pass a shared state between steps. TF-IDF and cosine similarity keep default document retrieval local and lightweight. Ollama is an optional local model interface; its model must actually be installed and reachable before claiming inference occurred."),
  ("Streamlit and Docker", "Streamlit provides fast Python-based portal screens. Docker files package API and UI services consistently for local environments and CI image builds. Compose shares a SQLite database directory; it does not currently provide a Postgres container."),
 ]),
 ("35 Glossary", [
  ("Core data terms", "API: a defined way for software to request a service. Database: structured storage for records. Table: a group of rows with the same columns. Primary key: unique row ID. Foreign key: reference connecting records. ORM: a tool that maps database rows to code objects. Migration: a controlled change from one database schema version to another. ETL: extract, transform, load data from one representation/source to another."),
  ("Payment terms", "Order: a request for a customer to pay a specified amount. Payment: a provider or simulated transaction attempt. Captured: provider-confirmed funds collection state used by this app. Pending: outcome not final in the local record. GMV: captured payment volume, not profit. MDR: merchant discount fee concept; the prototype uses an illustrative calculation. Settlement: transfer/payout accounting separate from payment capture."),
  ("AI terms", "Anomaly: an unusual pattern that deserves review, not proof of fraud. Feature: a numeric input describing a group of records. Isolation Forest: an unsupervised method that scores unusual combinations. LLM: a language model that generates text. RAG: retrieval plus generation using selected source passages. Embedding: a vector representation of text. TF-IDF: a lexical weighting method. LangGraph: a library for representing stateful multi-step workflows. Node: one workflow step. State: the data passed across steps."),
  ("Governance terms", "Evidence: information that supports or challenges a claim. Human-in-the-loop: a person reviews before an important action. Approval: a recorded decision about an operational action, not a payment status. Audit log: an application record of actions and results. HMAC: a keyed hash used to verify message authenticity. Docker container: a packaged process environment. Synthetic data: generated data that resembles a domain but does not represent real customer transactions."),
 ]),
 ("36 Final Project Summary", [
  ("The whole project in one flow", "Payment → data → data quality → SQL database → analytics → anomaly signal → alert → LangGraph investigation → SQL and RAG evidence → recommendation → human review → local simulated action → audit record."),
  ("Closing explanation", "PayBridge takes payment transaction data, computes operational metrics, identifies unusual groups using ML and deterministic rules, investigates selected alerts using database evidence and retrieved procedures, presents a recommendation for human review, and records the decision. Razorpay checkout is verified server-side when configured. Some data and UI content are illustrative, and operational actions do not reroute live payments."),
  ("Source-of-truth note", "This guide was prepared from static inspection of the repository source, README, configuration examples, tests, and checked-in docs. Several older docs/audit files describe an apartment/water billing system and older file paths; those claims conflict with the present payment models and README. Source code was favored where paths and behavior could be confirmed. No test suite was run for this writing task, and the current Render configuration, database, live model availability, and a completed provider transaction were not verified from the repository."),
 ]),
]

def font(size, bold=False):
    p = Path(r"C:\Windows\Fonts") / ("arialbd.ttf" if bold else "arial.ttf")
    return ImageFont.truetype(str(p), size)

def make_flow(name, title, nodes, horizontal=False):
    W, H = (1500, 650) if horizontal else (1280, 1000)
    img = Image.new("RGB", (W,H), "white")
    d = ImageDraw.Draw(img)
    d.text((60,35), title, fill=f"#{NAVY}", font=font(36, True))
    if horizontal:
        gap=18; x0=50; y=210; boxw=(W-100-gap*(len(nodes)-1))//len(nodes); boxh=210
        for i,(head,sub) in enumerate(nodes):
            x=x0+i*(boxw+gap)
            d.rounded_rectangle((x,y,x+boxw,y+boxh),radius=22,fill=f"#{PALE}",outline=f"#{BLUE}",width=3)
            d.text((x+18,y+24),head,fill=f"#{NAVY}",font=font(22,True))
            lines=[]; words=sub.split(); cur=""
            for w in words:
                test=(cur+" "+w).strip()
                if d.textlength(test,font=font(17))>boxw-36: lines.append(cur);cur=w
                else:cur=test
            if cur:lines.append(cur)
            for j,l in enumerate(lines): d.text((x+18,y+68+j*24),l,fill=f"#{MUTED}",font=font(17))
            if i<len(nodes)-1:
                ax=x+boxw+3; ay=y+boxh//2
                d.line((ax,ay,ax+gap-8,ay),fill=f"#{TEAL}",width=5)
                d.polygon([(ax+gap-8,ay-9),(ax+gap,ay),(ax+gap-8,ay+9)],fill=f"#{TEAL}")
    else:
        boxw=1050; boxh=116; x=(W-boxw)//2; y0=120; gap=20
        for i,(head,sub) in enumerate(nodes):
            y=y0+i*(boxh+gap)
            d.rounded_rectangle((x,y,x+boxw,y+boxh),radius=20,fill=f"#{PALE}",outline=f"#{BLUE}",width=3)
            d.text((x+26,y+16),head,fill=f"#{NAVY}",font=font(24,True))
            d.text((x+26,y+56),sub,fill=f"#{MUTED}",font=font(18))
            if i<len(nodes)-1:
                cx=W//2; ya=y+boxh+2; yb=ya+gap-5
                d.line((cx,ya,cx,yb),fill=f"#{TEAL}",width=5)
                d.polygon([(cx-9,yb-4),(cx,yb+6),(cx+9,yb-4)],fill=f"#{TEAL}")
    path=BUILD/(name+".png"); img.save(path); return path

figs={
 "architecture":make_flow("architecture","PayBridge application layers",[
  ("Customer / Merchant / Admin","Streamlit portal screens and static landing page"),
  ("API and services","FastAPI routes, checkout, ingestion, investigation"),
  ("SQLAlchemy","Models, sessions, validation and persistence"),
  ("Payment data","Orders, transactions, import runs, workflows, audit"),
  ("Analytics and review","Metrics, anomaly signals, RAG evidence, human decision"),
 ]),
 "lifecycle":make_flow("lifecycle","One operational investigation path",[
  ("Payment records","Provider checkout or compatible imported CSV"),
  ("Validate and store","Normalize supported fields and record import lineage"),
  ("Measure","SQL metrics and grouped anomaly features"),
  ("Investigate","Named queries plus local policy retrieval"),
  ("Review and record","Human decision and local audit/action records"),
 ],horizontal=True),
 "checkout":make_flow("checkout","Razorpay Standard Checkout",[
  ("1 Create order","Server receives amount and returns provider order ID"),
  ("2 Checkout","Browser sends customer to Razorpay test/live checkout"),
  ("3 Verify","Server checks HMAC, provider order, amount, currency, captured state"),
  ("4 Store receipt","Captured payment is persisted; receipt reads that row"),
 ],horizontal=True),
 "langgraph":make_flow("langgraph","Investigation graph and approval continuation",[
  ("Intake + planner","Load alert; choose fixed investigation tools"),
  ("SQL + retrieval","Read payment facts and retrieve procedure chunks"),
  ("Analytics + validator","Calculate metrics and assess evidence sufficiency"),
  ("Recommendation + gate","Use optional Ollama/fallback; create pending approval"),
  ("Audit + continuation","Persist results; approved path calls local action executor"),
 ],horizontal=True),
 "rag":make_flow("rag","RAG in PayBridge",[
  ("Local SOP text","Files under backend/data/documents"),
  ("Section chunks","Split numbered sections; subdivide long passages"),
  ("TF-IDF index","Default lexical vector representation and cosine similarity"),
  ("Relevant context","Return top matching chunks with section citations"),
  ("LLM or fallback","Optional local Ollama; recommendation remains reviewable"),
 ],horizontal=True),
 "approval":make_flow("approval","Human decision boundary",[
  ("AI suggests","Evidence and recommendation are saved as a workflow"),
  ("Pending review","Approval row waits for an authorized decision"),
  ("Approve or reject","Decision and actor are saved; rejection runs no action"),
  ("Local action","Approved action writes an app record, not live routing"),
 ],horizontal=True),
}

doc=Document()
sec=doc.sections[0]
sec.top_margin=Inches(.72); sec.bottom_margin=Inches(.68); sec.left_margin=Inches(.82); sec.right_margin=Inches(.82)
styles=doc.styles
styles['Normal'].font.name='Arial'; styles['Normal'].font.size=Pt(10.2); styles['Normal'].font.color.rgb=RGBColor.from_string(NAVY)
styles['Normal'].paragraph_format.space_after=Pt(6); styles['Normal'].paragraph_format.line_spacing=1.12
for nm,size,col in [('Title',34,NAVY),('Subtitle',16,MUTED),('Heading 1',22,NAVY),('Heading 2',14,BLUE),('Heading 3',11,TEAL)]:
    st=styles[nm]; st.font.name='Arial'; st.font.size=Pt(size); st.font.bold=(nm!='Subtitle'); st.font.color.rgb=RGBColor.from_string(col)
    st.paragraph_format.keep_with_next=True
styles['Heading 1'].paragraph_format.space_before=Pt(2); styles['Heading 1'].paragraph_format.space_after=Pt(12)

def set_cell_shading(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); tcPr.append(shd)

def set_cell_margins(cell, top=90, start=110, bottom=90, end=110):
    tc=cell._tc; tcPr=tc.get_or_add_tcPr(); tcMar=tcPr.first_child_found_in('w:tcMar')
    if tcMar is None: tcMar=OxmlElement('w:tcMar'); tcPr.append(tcMar)
    for m,v in [('top',top),('start',start),('bottom',bottom),('end',end)]:
        node=tcMar.find(qn('w:'+m))
        if node is None: node=OxmlElement('w:'+m); tcMar.append(node)
        node.set(qn('w:w'),str(v)); node.set(qn('w:type'),'dxa')

def add_table(headers, rows, widths=None):
    t=doc.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'
    for j,h in enumerate(headers):
        c=t.rows[0].cells[j]; c.text=h; set_cell_shading(c,NAVY); set_cell_margins(c)
        for r in c.paragraphs[0].runs:r.font.bold=True;r.font.color.rgb=RGBColor(255,255,255);r.font.size=Pt(9)
    for i,row in enumerate(rows):
        cells=t.add_row().cells
        for j,val in enumerate(row):
            cells[j].text=str(val); set_cell_margins(cells[j]); cells[j].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if i%2==1:set_cell_shading(cells[j],PALE)
            for p in cells[j].paragraphs:
                for r in p.runs:r.font.size=Pt(8.3);r.font.color.rgb=RGBColor.from_string(NAVY)
    doc.add_paragraph()
    return t

def add_bullet(text):
    p=doc.add_paragraph(style='List Bullet');p.paragraph_format.space_after=Pt(3);p.add_run(text)

def add_code(text):
    for line in text.splitlines():
        p=doc.add_paragraph();p.paragraph_format.left_indent=Inches(.18);p.paragraph_format.space_after=Pt(1)
        r=p.add_run(line or ' ');r.font.name='Consolas';r.font.size=Pt(8.6);r.font.color.rgb=RGBColor.from_string('26354A')
        pPr=p._p.get_or_add_pPr();shd=OxmlElement('w:shd');shd.set(qn('w:fill'),'F1F4F8');pPr.append(shd)

def bookmark(paragraph, name, idnum):
    start=OxmlElement('w:bookmarkStart');start.set(qn('w:id'),str(idnum));start.set(qn('w:name'),name)
    end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(idnum))
    paragraph._p.insert(0,start);paragraph._p.append(end)

def hyperlink(paragraph, text, anchor):
    h=OxmlElement('w:hyperlink');h.set(qn('w:anchor'),anchor)
    r=OxmlElement('w:r');pr=OxmlElement('w:rPr');color=OxmlElement('w:color');color.set(qn('w:val'),BLUE);pr.append(color)
    u=OxmlElement('w:u');u.set(qn('w:val'),'single');pr.append(u);r.append(pr)
    tx=OxmlElement('w:t');tx.text=text;r.append(tx);h.append(r);paragraph._p.append(h)

# Cover
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(96)
r=p.add_run('PAYBRIDGE');r.bold=True;r.font.name='Arial';r.font.size=Pt(38);r.font.color.rgb=RGBColor.from_string(NAVY)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('End-to-End Project Guide');r.bold=True;r.font.size=Pt(23);r.font.color.rgb=RGBColor.from_string(BLUE)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('Beginner to Technical and Interview Ready');r.font.size=Pt(16);r.font.color.rgb=RGBColor.from_string(MUTED)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(24)
r=p.add_run('Payments AI-Powered FinOps and Payment Operations Platform');r.font.size=Pt(13);r.font.color.rgb=RGBColor.from_string(NAVY)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(50)
r=p.add_run('DEMO MODE  |  SYNTHETIC PAYMENT DATA  |  SIMULATED OPERATIONAL ACTIONS');r.bold=True;r.font.size=Pt(10);r.font.color.rgb=RGBColor.from_string(AMBER)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(98)
r=p.add_run('A practical guide to what the repository implements, how the parts connect, and what to explain honestly.');r.italic=True;r.font.size=Pt(11);r.font.color.rgb=RGBColor.from_string(MUTED)
doc.add_page_break()

# Guide orientation
doc.add_heading('How to Use This Guide',level=1)
doc.add_paragraph('Read the first chapters for the business story, then follow the customer-to-admin path. The later chapters explain code modules, data, API behavior, AI workflow, security, packaging, and interview language. Each technical chapter answers what a component does, why it exists, how it works, where it lives, and what to say about it.')
doc.add_paragraph('Evidence labels used throughout:',style='Heading 2')
add_table(['Label','Meaning'],[
 ('IMPLEMENTED','A source-code path exists for this behavior.'),('SIMULATED','The app models or records local demo behavior rather than acting on a real external operation.'),('DEMO ONLY','A seeded or illustrative screen/example used for demonstration.'),('SIMPLIFIED IMPLEMENTATION','A deliberately reduced prototype design.'),('NOT IMPLEMENTED','The repository does not currently perform the behavior.'),('NOT VERIFIED FROM REPOSITORY','Static source inspection cannot establish the runtime or deployment fact.')])
doc.add_paragraph('Important reading note: some older checked-in design/audit documents describe an apartment and water-billing project and refer to obsolete file paths. Those passages conflict with the current payment models and current README. This guide favors the source files that exist in the reviewed checkout and marks facts that cannot be established from source.')
doc.add_paragraph('The project uses a mixed transition state: payment-domain models are present alongside legacy billing models, and some investigation routes reuse the older Alert table. That is useful to know before an interview because it explains why not every page is a clean, payment-only workflow.')
doc.add_page_break()

# Static TOC with bookmarks
doc.add_heading('Contents',level=1)
doc.add_paragraph('Select a chapter title to jump to it. Page numbers are shown in the footer; chapter headings are also available in Word’s Navigation pane.')
for i,chapter in enumerate(chapters,1):
    title=chapter[0]
    p=doc.add_paragraph();p.paragraph_format.space_after=Pt(3)
    hyperlink(p,title,f'chapter_{i:02d}')
doc.add_page_break()

# Add chapters
for idx,(title,sections,*figkey) in enumerate(chapters,1):
    doc.add_page_break()
    h=doc.add_heading(title,level=1);bookmark(h,f'chapter_{idx:02d}',idx)
    doc.add_paragraph('Purpose: understand the component, its role in PayBridge, and the boundary between implemented and illustrative behavior.',style='Caption')
    for section,body in sections:
        doc.add_heading(section,level=2)
        if section in {'Route list','Business-to-code map','Status labels','Matrix','Core routes','Payment entities','One coherent story','Simplest explanation','Three points to emphasize','One-minute explanation'}:
            for line in body.splitlines():
                line=line.strip()
                if not line: continue
                if '—' in line or '→' in line or line.startswith(('GET ','POST ','Customer','Backend engineer','Data engineer','ML engineer','GenAI engineer','Problem:','Engineering:','Governance:')):
                    add_bullet(line)
                else: doc.add_paragraph(line)
        else:
            for para in body.split('\n'):
                if para.strip():doc.add_paragraph(para.strip())
    if figkey:
        doc.add_picture(str(figs[figkey[0]]),width=Inches(6.35))
        doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    if idx==10:
        add_table(['Method and path','Purpose','Important effect'],[
          ('GET /health','API/database readiness summary','Reads database; checks optional model/index.'),('POST /auth/login','Issue API access token','Validates demo or configured user credentials.'),('GET /alerts','List alert records','Reads Alert model; optional severity/status filters.'),('POST /alerts/{id}/investigate','Run evidence workflow','Creates workflow, approval, and audit data.'),('GET /workflows/{id}','Read investigation result','Returns saved recommendation and evidence.'),('POST /workflows/{id}/approve or /reject','Record operator decision','Approved path may write local action; no live routing.'),('GET /audit','Read audit events','Returns stored audit records.'),('GET /api/v1/payments/kpis','Payment KPI response','Deterministic aggregate queries.'),('POST /api/v1/ingestion/csv','Import CSV','Writes accepted records and ingestion lineage.'),('POST /api/create-order, /api/verify-payment','Razorpay checkout','Provider order and server-side payment verification.')])
    if idx==13:
        add_table(['Entity','Why it exists'],[
          ('merchants / customers','Business and payer identities for the payment example.'),('payment_orders','Order amount and lifecycle before/around payment.'),('payment_transactions','Payment method, outcome, amounts, errors and source.'),('payment_events / payment_attempts','Lifecycle events and retry attempts.'),('payment_ingestion_runs / records','CSV source lineage and rejected-row details.'),('workflows / approvals / action_records','Investigation state, decision, local action.'),('audit_logs','Workflow and human decision activity.')])
    if idx==28:
        add_table(['Feature','Status','What can be claimed'],[
          ('CSV import','IMPLEMENTED','Supported CSV schemas become stored rows with lineage.'),('Razorpay checkout','IMPLEMENTED, conditional','Provider order and server verification code; no live payment proven here.'),('Analytics','IMPLEMENTED','SQL-derived metrics with explicit denominator/window.'),('Anomaly detection','IMPLEMENTED, prototype','Isolation Forest proposal plus deterministic rules; broad accuracy unmeasured.'),('RAG','IMPLEMENTED, simplified','Local TF-IDF retrieval; citations; no guarantee of correctness.'),('Approval/action','IMPLEMENTED locally','Decision gate and local action record; no bank route change.'),('PostgreSQL migration','NOT VERIFIED / incomplete','Connection config exists; migration revision is empty.'),('Render setup','NOT VERIFIED FROM REPOSITORY','No Render manifest in the checked project tree.')])

# Footer page number
for section in doc.sections:
    f=section.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.CENTER
    run=f.add_run('PayBridge Project Guide  •  Page ');run.font.size=Pt(8);run.font.color.rgb=RGBColor.from_string(MUTED)
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)

# Set document metadata without personal data
doc.core_properties.title='PayBridge End-to-End Project Guide'
doc.core_properties.subject='Beginner-friendly technical and interview guide based on repository inspection'
doc.core_properties.author='PayBridge Project Documentation'
doc.save(OUT)
print(OUT)
