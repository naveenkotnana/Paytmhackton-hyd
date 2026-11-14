import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const workspaceDir = 'D:/Deploy-OpsPilot-Razorpay-inspired-AI-FinOps-Platform';
const buildDir = path.join(workspaceDir, '.paybridge_interview_build');
const outputDir = path.join(workspaceDir, 'docs');
const finalPath = path.join(outputDir, 'PayBridge_Interview_Deck_Short.pptx');
const skillDir = 'C:/Users/nav/.codex/plugins/cache/openai-primary-runtime/presentations/26.1030.10813/skills/presentations';
const W = 1280, H = 720;
const C = {
  bg: '#F3F7FC', navy: '#10203D', body: '#536782', blue: '#315BFF', teal: '#008D75',
  amber: '#B66A00', white: '#FFFFFF', line: '#D6E0EF', paleBlue: '#E7EEFF',
  paleTeal: '#E3F5F0', paleAmber: '#FFF2D9', paleRed: '#FCE9E8', red: '#B7443E',
};

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}
function shape(slide, geometry, x, y, w, h, fill = 'none', stroke = 'none', sw = 0) {
  return slide.shapes.add({ geometry, position: { left: x, top: y, width: w, height: h }, fill,
    line: { style: 'solid', fill: stroke, width: sw } });
}
function text(slide, value, x, y, w, h, size, color = C.body, bold = false, align = 'left') {
  const s = shape(slide, 'textbox', x, y, w, h);
  s.text = value;
  s.text.style = { typeface: 'Arial', fontSize: size, color, bold, alignment: align,
    verticalAlignment: 'middle', wrap: true };
  return s;
}
function line(slide, x, y, w, h, color = C.line, thickness = 2) {
  return shape(slide, 'rect', x, y, w, h, color);
}
function base(title, number) {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  text(slide, title, 58, 42, 1150, 54, 34, C.navy, true);
  line(slide, 58, 108, 1164, 2);
  text(slide, `PAYBRIDGE  ·  INTERVIEW WALKTHROUGH`, 58, 682, 690, 16, 11, C.body, true);
  text(slide, String(number).padStart(2, '0'), 1174, 680, 48, 18, 12, C.body, true, 'right');
  return slide;
}
function card(slide, x, y, w, h, title, body, accent = C.blue, fill = C.white, titleSize = 21, bodySize = 17) {
  shape(slide, 'roundRect', x, y, w, h, fill, C.line, 1);
  shape(slide, 'rect', x, y, 7, h, accent);
  text(slide, title, x + 24, y + 18, w - 44, 34, titleSize, C.navy, true);
  text(slide, body, x + 24, y + 60, w - 46, h - 76, bodySize, C.body);
}
function pill(slide, label, x, y, w, fill, color) {
  shape(slide, 'roundRect', x, y, w, 30, fill);
  text(slide, label, x + 8, y + 1, w - 16, 26, 13, color, true, 'center');
}
function arrow(slide, x, y, color = C.blue) {
  text(slide, '→', x, y, 42, 40, 30, color, true, 'center');
}

const presentation = Presentation.create({ slideSize: { width: W, height: H } });

// 1. Cover: one sentence a candidate can say out loud.
{
  const s = presentation.slides.add();
  s.background.fill = C.bg;
  shape(s, 'rect', 0, 0, 16, H, C.blue);
  pill(s, 'PAYMENT OPERATIONS · AI ASSISTED', 72, 95, 302, C.paleBlue, C.blue);
  text(s, 'PayBridge', 72, 168, 720, 84, 64, C.navy, true);
  text(s, 'A simple way to understand payment issues', 74, 264, 760, 55, 32, C.blue, true);
  text(s, 'I built a prototype that brings payment records, operational analytics, and evidence-based investigation into one workflow.', 74, 352, 720, 102, 24, C.body);
  shape(s, 'roundRect', 870, 172, 300, 300, C.white, C.line, 1);
  text(s, 'PAYMENT', 915, 220, 210, 26, 14, C.body, true, 'center');
  text(s, '↓', 980, 256, 80, 52, 35, C.blue, true, 'center');
  text(s, 'EVIDENCE', 915, 322, 210, 30, 22, C.navy, true, 'center');
  text(s, '↓', 980, 357, 80, 52, 35, C.teal, true, 'center');
  text(s, 'DECISION', 915, 422, 210, 30, 22, C.navy, true, 'center');
  text(s, 'Interview overview · Kotnana NaveenKumar', 74, 642, 800, 24, 14, C.body);
  s.speakerNotes.text = 'Opening: PayBridge is my payment-operations prototype. It helps an operator move from payment records to evidence and a recorded human decision. The project uses synthetic data and some illustrative incident content; it is not a live bank-routing system. Sources: README.md; backend/app/api/main.py; backend/app/agent/workflow.py.';
}

// 2. Problem and intended value.
{
  const s = base('The problem: payment issues take context to explain', 2);
  text(s, 'A merchant sees a payment fail. The team needs to answer three things quickly:', 72, 140, 1090, 40, 23, C.body);
  card(s, 72, 218, 330, 205, 'What happened?', 'Find the saved transaction and its status, method, source, and any recorded reason.', C.blue);
  card(s, 474, 218, 330, 205, 'Is it a pattern?', 'Compare outcomes across a group, such as UPI attempts by bank or gateway.', C.teal);
  card(s, 876, 218, 330, 205, 'What should we do?', 'Gather evidence, review a recommendation, and record who made the decision.', C.amber);
  text(s, 'PayBridge connects these steps in one prototype workflow.', 72, 482, 1090, 50, 27, C.navy, true);
  text(s, 'It supports investigation and operational review; it does not guarantee a cause or fix.', 72, 543, 1080, 36, 18, C.body);
  s.speakerNotes.text = 'Explain the real operational question: not just whether a payment failed, but whether many failures share a pattern and what evidence supports a response. A signal is not proof of fraud or provider fault. Sources: README.md; backend/app/services/payment_queries.py; backend/app/analytics/payment_analytics.py.';
}

// 3. Architecture and lifecycle.
{
  const s = base('One flow: screens, services, and payment data', 3);
  const xs = [72, 364, 656, 948];
  const titles = ['Streamlit UI', 'FastAPI', 'SQL database', 'Analysis + AI'];
  const bodies = [
    'Customer, Merchant, and Admin views',
    'Payment, import, analytics, and investigation endpoints',
    'Payments, import runs, approvals, and audit records',
    'Metrics, anomaly rules, SQL evidence, and retrieved procedures',
  ];
  const colors = [C.blue, C.teal, C.amber, C.blue];
  for (let i=0;i<4;i++) {
    card(s, xs[i], 214, 250, 190, titles[i], bodies[i], colors[i], C.white, 20, 17);
    if (i<3) arrow(s, xs[i]+252, 285, colors[i]);
  }
  pill(s, 'DEFAULT DATABASE: SQLITE', 72, 465, 248, C.paleBlue, C.blue);
  pill(s, 'POSTGRESQL CONFIGURABLE', 344, 465, 278, C.paleTeal, C.teal);
  text(s, 'The repository’s runtime database and deployment storage must be checked for each environment.', 72, 530, 1100, 46, 19, C.body);
  s.speakerNotes.text = 'Describe the architecture simply. Streamlit is the interface; FastAPI provides the service layer; SQL stores operational records; analytics and the AI workflow consume that evidence. SQLite is the configured default and PostgreSQL is supported by configuration, but don’t claim a production migration without verifying the deployed database. Sources: frontend/dashboard.py; backend/app/api/main.py; backend/app/core/config.py; backend/app/agent/workflow.py.';
}

// 4. Separate the personas.
{
  const s = base('Three portals, three jobs', 4);
  card(s, 72, 184, 350, 330, 'Customer', '• Builds a cafe order\n• Chooses a payment path\n• Sees the saved result and receipt', C.blue, C.white, 24, 20);
  card(s, 464, 184, 350, 330, 'Merchant', '• Reviews the merchant ledger\n• Filters captured, failed, and pending payments\n• Checks order and source details', C.teal, C.white, 24, 20);
  card(s, 856, 184, 350, 330, 'Admin', '• Reviews platform payments and metrics\n• Imports payment CSVs\n• Investigates issues and records decisions', C.amber, C.white, 24, 20);
  text(s, 'Same business story, viewed from the buyer, the merchant, and the operations team.', 72, 565, 1135, 38, 20, C.navy, true);
  s.speakerNotes.text = 'Walk through personas separately. Customer creates a cart and pays. Merchant sees the merchant-scoped transaction ledger. Admin handles platform operations, imports, investigations, and decisions. The displayed UI may contain illustrative elements; distinguish those from database-backed views. Sources: frontend/views/customer_portal.py; frontend/views/merchant_portal.py; frontend/views/admin_dashboard.py.';
}

// 5. Data ingestion and quality.
{
  const s = base('CSV import: validate first, then store accepted rows', 5);
  const steps = [
    ['1', 'Choose CSV', 'Upload payment rows'],
    ['2', 'Map columns', 'Recognize supported names'],
    ['3', 'Validate', 'Check fields, dates, amounts, duplicates'],
    ['4', 'Save', 'Write accepted rows and run history'],
    ['5', 'Review', 'See counts, rejected rows, and ledger data'],
  ];
  const startX = 62, gap = 16, cw = 215;
  steps.forEach((st,i)=>{
    const x=startX+i*(cw+gap);
    shape(s,'ellipse',x+82,176,48,48,i===4?C.teal:C.blue);
    text(s,st[0],x+82,178,48,44,22,C.white,true,'center');
    text(s,st[1],x,246,cw,36,20,C.navy,true,'center');
    text(s,st[2],x+4,293,cw-8,104,17,C.body,false,'center');
    if(i<steps.length-1) arrow(s,x+cw-3,183,C.body);
  });
  shape(s,'roundRect',72,447,1134,111,C.paleAmber);
  text(s,'Important boundary',96,464,240,28,17,C.amber,true);
  text(s,'This structures supported payment CSVs. It does not turn arbitrary files into verified payments or connect automatically to every provider.',96,500,1065,42,18,C.navy);
  s.speakerNotes.text = 'Explain that ingestion is not magic parsing. The service maps recognized columns, normalizes fields, validates key values, deduplicates, saves accepted payment rows, and keeps an import run and rejection details. Only compatible CSVs are accepted; unrelated/unstructured files are not converted into trustworthy transactions. Sources: backend/app/services/ingestion_payments.py; backend/app/api/main.py.';
}

// 6. Analytics and anomaly signals.
{
  const s = base('Analytics counts outcomes; anomalies flag unusual patterns', 6);
  card(s, 72, 178, 516, 304, 'Payment analytics', 'Counts by status\nCaptured value (GMV)\nSuccess rate from captured + failed outcomes', C.blue, C.white, 24, 21);
  card(s, 692, 178, 516, 304, 'Anomaly signal', 'Groups outcomes by method, bank, or gateway\nApplies minimum-volume and failure-rate rules\nCreates a review target, not a fraud verdict', C.teal, C.white, 24, 21);
  shape(s,'roundRect',72,514,1136,72,C.paleBlue);
  text(s,'Success rate = captured ÷ (captured + failed) × 100%',98,531,1084,38,23,C.navy,true,'center');
  text(s,'Pending and authorized payments are excluded from this denominator.',72,607,1120,28,16,C.body,false,'center');
  s.speakerNotes.text = 'Give the simple math example: 80 captured and 20 failed gives 80/(80+20)=80% success. Pending/authorized are excluded. Captured GMV is transaction volume, not profit. Anomaly detection groups payments and applies rules; the repository’s threshold examples require a minimum attempt count. Do not state that every successful customer payment causes an anomaly. Sources: backend/app/analytics/payment_analytics.py; backend/app/ml/anomaly.py.';
}

// 7. AI investigation.
{
  const s = base('AI investigation combines facts, patterns, and procedures', 7);
  const cols = [
    ['Payment facts', 'Saved transaction records\nStatus, method, bank, gateway, errors', C.blue],
    ['Calculated patterns', 'SQL queries and metrics\nCounts, rates, and group comparisons', C.teal],
    ['Relevant guidance', 'RAG retrieves local procedure text\nText is context, not transaction truth', C.amber],
  ];
  cols.forEach((a,i)=>card(s,72+i*392,188,350,194,a[0],a[1],a[2],C.white,22,18));
  arrow(s,427,262,C.blue); arrow(s,819,262,C.teal);
  shape(s,'roundRect',192,442,896,104,C.paleBlue);
  text(s,'Evidence → explanation → suggested next step',220,459,840,34,26,C.navy,true,'center');
  text(s,'A human reviews the result. Unknown causes should stay unknown.',220,500,840,28,17,C.body,false,'center');
  s.speakerNotes.text = 'Explain RAG in one line: split local procedure documents into sections, retrieve relevant sections for a question, and pass them as context. SQL and metrics supply transaction evidence; RAG does not determine payment status. The code uses a local TF-IDF/cosine retrieval path by default, with optional Ollama support; do not claim a verified cloud LLM or LlamaIndex use for this repository. Some incident UI content remains hardcoded. Sources: backend/app/agent/workflow.py; backend/app/rag/store.py; backend/app/rag/ollama_client.py; frontend/views/ai_investigation_workspace.py.';
}

// 8. Approval meaning and real boundary.
{
  const s = base('Approval means “review the proposed response”', 8);
  const labels = [
    ['Merchant reports a spike', C.blue],
    ['PayBridge gathers evidence', C.teal],
    ['Admin approves or rejects', C.amber],
    ['Decision is recorded', C.blue],
  ];
  labels.forEach((it,i)=>{
    const x=70+i*300;
    shape(s,'roundRect',x,200,256,112,C.white,C.line,1);
    shape(s,'rect',x,200,7,112,it[1]);
    text(s,it[0],x+20,220,220,72,19,C.navy,true,'center');
    if(i<3) arrow(s,x+260,238,it[1]);
  });
  shape(s,'roundRect',72,392,1135,156,C.paleAmber);
  text(s,'What approval changes',98,412,300,28,18,C.amber,true);
  text(s,'It records a human decision and audit activity.',98,450,500,34,21,C.navy,true);
  text(s,'What it does not change',660,412,340,28,18,C.red,true);
  text(s,'It does not make failed payments succeed or reroute live bank traffic.',660,450,500,62,19,C.navy);
  text(s,'This is the human-oversight step in the prototype.',72,584,1130,30,18,C.body,false,'center');
  s.speakerNotes.text = 'Use this real example: a merchant reports a UPI failure spike; PayBridge assembles evidence and suggests a temporary routing response; an admin reviews and approves or rejects it; the decision is recorded. In this repository the action is local/simulated and does not change provider routing. Sources: backend/app/api/main.py; backend/app/agent/workflow.py; backend/app/models/ops.py.';
}

// 9. Demo story + close.
{
  const s = base('A clear 3-minute demo and honest close', 9);
  const left = [
    'Show one customer order and payment result',
    'Find the saved transaction in Merchant Payments',
    'Import a compatible CSV and review accepted/rejected counts',
    'Show metrics, investigate evidence, record a decision',
  ];
  left.forEach((v,i)=>{
    shape(s,'ellipse',78,169+i*73,38,38,i===3?C.teal:C.blue);
    text(s,String(i+1),78,169+i*73,38,38,16,C.white,true,'center');
    text(s,v,132,169+i*73,635,44,19,C.navy,i===3);
  });
  shape(s,'roundRect',840,174,366,333,C.white,C.line,1);
  text(s,'My implementation',870,199,300,32,21,C.blue,true);
  text(s,'Streamlit UI\nFastAPI backend\nSQL payment records\nCSV validation and analytics\nLangGraph + local RAG workflow',870,246,300,183,20,C.navy);
  text(s,'Prototype limits',870,438,300,28,17,C.amber,true);
  text(s,'Synthetic and illustrative content remains; approval does not reroute real payments.',870,469,300,52,15,C.body);
  text(s,'“I built PayBridge to help payment teams move from a transaction record to evidence and a reviewed operational decision.”',72,566,1136,68,22,C.navy,true,'center');
  s.speakerNotes.text = 'Close by showing one consistent flow, not every feature. The project is deployed per the user report, but the repository inspection does not independently verify the live Render configuration, database persistence, provider transaction completion, or active Ollama model. Say what you personally built and what parts are illustrative. Sources: README.md; frontend/views/customer_portal.py; frontend/views/merchant_portal.py; frontend/views/admin_dashboard.py; backend/app/services/ingestion_payments.py; backend/app/agent/workflow.py.';
}

await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });
for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, '0')}`;
  await writeBlob(path.join(buildDir, `${stem}.png`), await presentation.export({ slide, format: 'png', scale: 1 }));
}
await writeBlob(path.join(buildDir, 'montage.webp'), await presentation.export({ format: 'webp', montage: true }));
const candidatePath = path.join(buildDir, 'candidate.pptx');
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const validationDir = path.join(buildDir, 'validation');
await fs.mkdir(validationDir, { recursive: true });
const result = await finalizePresentation({
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: 'C:/Users/nav/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
  integrityValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-bullet-geometry', '--validate-heading-fit'],
  expectedSlideSizeEmu: '12192000,6858000',
  requirements: { explicitTotalSlideCount: 9, requiredNativeTableOwnerSlides: [], requiredNativeChartOwnerSlides: [] },
  explicitTotalSlideCount: 9,
  fontPolicy: { basis: 'design', families: ['Arial'] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(validationDir, 'PayBridge_Interview_Deck_Short.validation.json'),
});
console.log(JSON.stringify(result, null, 2));
