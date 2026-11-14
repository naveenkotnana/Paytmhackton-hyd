import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
const { finalizePresentation } = await import(pathToFileURL('C:/Users/nav/.codex/plugins/cache/openai-primary-runtime/presentations/26.1030.10813/skills/presentations/container_tools/artifact_tool_utils.mjs').href);

const workspaceDir = 'D:/Deploy-OpsPilot-Razorpay-inspired-AI-FinOps-Platform';
const buildDir = path.join(workspaceDir, '.paybridge_deck_build');
const outputDir = path.join(workspaceDir, 'docs');
const finalPath = path.join(outputDir, 'PayBridge_Explanation_Deck.pptx');
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });

const W=1280,H=720;
const C={navy:'#0B1836',blue:'#315BFF',teal:'#07866D',muted:'#52627A',pale:'#F3F7FC',white:'#FFFFFF',line:'#D8E1EE',amber:'#A45A00',red:'#A83434',softBlue:'#E8EEFF'};
const FONT='Arial';
const p=Presentation.create({slideSize:{width:W,height:H}});

function shape(slide,geometry,name,x,y,w,h,fill='none',stroke='none',sw=0){
  return slide.shapes.add({geometry,name,position:{left:x,top:y,width:w,height:h},fill,
    line:{style:'solid',fill:stroke,width:sw}});
}
function txt(slide,text,x,y,w,h,size=24,color=C.navy,bold=false,align='left',name='text'){
  const s=shape(slide,'textbox',name,x,y,w,h);
  s.text=text;
  s.text.style={typeface:FONT,fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',wrap:'square',autoFit:'shrinkText',insets:{left:0,right:0,top:0,bottom:0}};
  return s;
}
function box(slide,x,y,w,h,title,body,accent=C.blue){
  shape(slide,'roundRect','content-card',x,y,w,h,C.white,C.line,1.2);
  shape(slide,'rect','accent-bar',x,y,7,h,accent,'none',0);
  txt(slide,title,x+22,y+18,w-42,34,21,C.navy,true);
  txt(slide,body,x+22,y+60,w-42,h-72,16,C.muted,false);
}
function numberRow(slide,n,title,body,x,y,w,accent=C.blue){
  shape(slide,'ellipse','step-number',x,y+4,32,32,accent,'none',0);
  txt(slide,String(n),x,y+3,32,32,15,C.white,true,'center');
  txt(slide,title,x+48,y,w-48,28,19,C.navy,true);
  txt(slide,body,x+48,y+29,w-50,44,15,C.muted,false);
}
function base(title,kicker='PAYBRIDGE PROJECT GUIDE'){
  const s=p.slides.add();s.background.fill=C.pale;
  txt(s,kicker,58,28,470,22,12,C.teal,true);
  txt(s,title,58,66,1164,52,33,C.navy,true);
  shape(s,'rect','title-rule',58,128,1164,2,C.line,'none',0);
  txt(s,'PAYBRIDGE  |  DEMO MODE · SYNTHETIC DATA · SIMULATED ACTIONS',58,682,950,18,10,C.muted,false);
  txt(s,String(p.slides.items.length).padStart(2,'0'),1160,680,62,20,11,C.muted,true,'right');
  return s;
}
function notes(slide,refs,text){slide.speakerNotes.text=`Presenter note: ${text}\nRepository references: ${refs.join('; ')}`;}

// 1 Cover
{
 const s=p.slides.add();s.background.fill=C.navy;
 shape(s,'rect','accent-block',0,0,18,H,C.teal,'none',0);
 txt(s,'PAYBRIDGE',74,118,1050,70,48,C.white,true);
 txt(s,'Payment operations, explained end to end',74,204,1020,58,31,'#AFC3FF',true);
 txt(s,'A simple technical walkthrough for a project interview',74,276,980,48,22,C.white,false);
 shape(s,'roundRect','scope-label',74,384,780,66,'#16294F','#315BFF',1.5);
 txt(s,'DEMO MODE  ·  SYNTHETIC PAYMENT DATA  ·  SIMULATED ACTIONS',98,398,735,38,16,'#DCE6FF',true);
 txt(s,'Customer → Merchant → Admin → Evidence → Human decision',74,520,1030,42,22,C.white,false);
 txt(s,'Built from the current repository structure and implementation',74,630,980,24,13,'#B7C5DE',false);
 notes(s,['README.md','frontend/views/','backend/app/api/','backend/app/agent/'],'Open with the payment-operations problem. State clearly that the dataset is synthetic and operational routing is not live.');
}
// 2 Project in one picture
{
 const s=base('PayBridge in one picture');
 const rows=[
  ['1','Capture or import','Checkout creates a provider order; CSV import accepts compatible payment rows.'],
  ['2','Store and validate','Structured rows and import history are saved in the configured SQL database.'],
  ['3','Measure and flag','SQL metrics and anomaly signals help find unusual payment groups.'],
  ['4','Investigate','LangGraph combines named SQL, analytics, and local procedure retrieval.'],
  ['5','Review and record','A human decision can trigger a local action record and audit entry.'],
 ];
 rows.forEach((r,i)=>numberRow(s,r[0],r[1],r[2],86,158+i*98,1080,i===4?C.teal:C.blue));
 notes(s,['backend/app/services/ingestion_payments.py','backend/app/analytics/payment_analytics.py','backend/app/ml/anomaly.py','backend/app/agent/workflow.py'],'Walk the audience from data entry to human decision. Emphasize that source data may be synthetic or imported and must be reviewed.');
}
// 3 Architecture
{
 const s=base('Architecture: one workflow across three layers');
 box(s,70,168,340,390,'Streamlit interface','Customer portal\nMerchant portal\nAdmin operations\n\nSome views read SQL directly; some use API helpers.',C.blue);
 box(s,470,168,340,390,'FastAPI services','Payment checkout\nCSV ingestion\nAnalytics APIs\nInvestigation and approvals\n\nStatic landing page is served here too.',C.teal);
 box(s,870,168,340,390,'Data and intelligence','SQLAlchemy models\nSQLite by default\nPayment analytics\nIsolation Forest + rules\nLangGraph + local RAG',C.amber);
 shape(s,'rightArrow','arrow1',411,328,58,42,C.blue,'none',0);
 shape(s,'rightArrow','arrow2',811,328,58,42,C.teal,'none',0);
 txt(s,'This is a prototype architecture; the UI is not uniformly separated from every backend path.',90,592,1100,38,18,C.muted,false,'center');
 notes(s,['frontend/dashboard.py','backend/app/api/main.py','backend/app/db/base.py','backend/app/models/payments.py'],'Describe the three layers. Mention the mixed direct-DB and API paths honestly.');
}
// 4 customer
{
 const s=base('Customer portal: choose items and pay');
 numberRow(s,1,'Choose menu items','Cart starts empty; the server calculates item totals.',78,170,520);
 numberRow(s,2,'Select a payment path','Simulated wallet credit or Razorpay checkout.',78,278,520,C.teal);
 numberRow(s,3,'Wait for the final result','Razorpay payment is not paid until server verification succeeds.',78,386,520,C.amber);
 box(s,680,175,520,350,'What is stored','Order and cart details\nPayment status and method\nPayment source label\nReceipt only for a matching captured row',C.blue);
 txt(s,'The INR 50,000 wallet is simulated credit. It is not a Razorpay balance.',680,556,520,54,16,C.amber,true);
 notes(s,['frontend/views/customer_portal.py','backend/app/services/cafe_menu.py','backend/app/services/demo_wallet.py','backend/app/api/checkout.py'],'Contrast wallet and Razorpay. Explain that a captured provider payment uses server-side confirmation before the receipt appears.');
}
// 5 merchant
{
 const s=base('Merchant portal: see this cafe’s stored payments');
 box(s,75,172,520,360,'Overview answers aggregate questions','Captured volume\nSuccessful count\nFailed count\nPending / authorized count\nStatus buttons open filtered rows',C.teal);
 box(s,685,172,520,360,'Payments answers record questions','Payment ID and order ID\nAmount and payment method\nBank and status\nFailure reason if one was saved\nSource distinguishes CSV, synthetic, wallet, or checkout',C.blue);
 txt(s,'Captured GMV means captured payment volume; it is not profit.',95,574,1110,40,21,C.navy,true,'center');
 notes(s,['frontend/views/merchant_portal.py','backend/app/models/payments.py'],'Show one filtered payment row and its source. Clarify that the merchant page reads stored transactions and that a missing failure reason is not guessed.');
}
// 6 admin
{
 const s=base('Admin portal: observe, investigate, decide');
 const items=[
  ['Overview','Counts and captured volume from stored payment rows; some incident cards are illustrative.'],
  ['Payments and imports','Browse ledger rows, uploaded batches, and rejected-row outcomes.'],
  ['Investigation','Look up a saved payment or inspect a selected incident workflow.'],
  ['Approvals and audit','Review a recommendation and inspect persisted decision activity.'],
 ];
 items.forEach((x,i)=>box(s,75+(i%2)*570,170+Math.floor(i/2)*208,530,170,x[0],x[1],i===3?C.teal:C.blue));
 txt(s,'Persona switching is navigation in the UI; it is not a secure identity system.',90,596,1100,30,16,C.amber,true,'center');
 notes(s,['frontend/views/admin_dashboard.py','frontend/views/ai_investigation_workspace.py','frontend/views/approvals.py'],'The database-backed payment lookup and the sample incident narrative are different experiences. Point out which one is live.');
}
// 7 ingestion
{
 const s=base('CSV ingestion: turn compatible rows into records');
 const steps=[['Read','Read CSV headers and row values'],['Map','Recognize common payment column aliases'],['Check','Validate required fields, amounts, dates, and IDs'],['Store','Save accepted rows to SQL and retain run lineage'],['Report','Keep rejected rows and reasons for review']];
 steps.forEach((x,i)=>box(s,58+i*240,215,218,280,x[0],x[1],i===4?C.teal:C.blue));
 txt(s,'An unrelated or arbitrary file is not reliably converted into a valid payment record.',82,542,1116,50,19,C.amber,true,'center');
 notes(s,['backend/app/services/ingestion_payments.py','backend/app/api/main.py','backend/app/models/payments.py'],'Explain that the CSV is an input, accepted data become database rows, and the import run stores counts and status.');
}
// 8 data model
{
 const s=base('Database: connect orders, payments, and decisions');
 const cells=[['Merchant','Customer'],['PaymentOrder','CafeOrderItems'],['PaymentTransaction','PaymentEvent'],['Workflow','Approval'],['ActionRecord','AuditLog']];
 cells.forEach((row,i)=>{
  const y=170+i*90;
  row.forEach((lab,j)=>{
   const x=235+j*440;shape(s,'roundRect','entity',x,y,360,58,j===0?C.softBlue:'#E8F5F1',j===0?C.blue:C.teal,1.4);
   txt(s,lab,x+12,y+8,336,40,19,C.navy,true,'center');
  });
  if(i<cells.length-1)shape(s,'line','relation',635,y+60,0,30,'none',C.muted,2);
 });
 txt(s,'SQLite is the default local store. PostgreSQL connectivity is configurable; migration is not verified.',120,638,1040,28,15,C.muted,false,'center');
 notes(s,['backend/app/models/payments.py','backend/app/models/ops.py','backend/app/db/base.py','backend/alembic/versions/3288d1cab678_initial_schema.py'],'Explain primary keys and related rows. State that the Alembic revision is empty and the current runtime creates tables from metadata.');
}
// 9 math
{
 const s=base('Analytics: explain the denominator');
 box(s,70,175,540,310,'Success rate','Captured ÷ (captured + failed) × 100\n\nExample: 80 captured and 20 failed\n80 ÷ 100 × 100 = 80%\n\nPending/authorized rows are excluded from this terminal-payment denominator.',C.blue);
 box(s,670,175,540,310,'Money metrics','Captured GMV = sum of captured amounts\n\nGMV is payment volume, not profit.\n\nProfit needs costs and other accounting inputs.',C.teal);
 txt(s,'Always say the time window, status set, and denominator used.',95,547,1100,52,22,C.navy,true,'center');
 notes(s,['backend/app/analytics/payment_analytics.py','backend/app/analytics/payment_queries.py'],'Use the simple 80/20 example and state pending rows are excluded from the success-rate formula in the KPI engine.');
}
// 10 anomaly
{
 const s=base('Anomaly detection: a signal to investigate');
 const xs=[90,370,650,930];
 const labs=[['Payment rows','status, method, bank, gateway'],['Group features','counts, failure rate, failed volume'],['Isolation Forest','scores unusual feature combinations'],['Rules','thresholds explain some signals']];
 labs.forEach((a,i)=>{
  shape(s,'roundRect','stage',xs[i],225,230,180,C.white,C.line,1.5);
  txt(s,a[0],xs[i]+18,248,194,38,20,C.navy,true,'center');
  txt(s,a[1],xs[i]+20,302,190,76,16,C.muted,false,'center');
  if(i<3)shape(s,'rightArrow','process-arrow',xs[i]+236,292,38,42,C.teal,'none',0);
 });
 txt(s,'A signal is not proof of fraud or proof of root cause.',140,500,1000,46,24,C.amber,true,'center');
 txt(s,'The prototype has no broad labeled benchmark establishing production precision or recall.',150,556,980,38,16,C.muted,false,'center');
 notes(s,['backend/app/ml/anomaly.py','backend/app/services/anomaly.py'],'Explain grouping and rule+model behavior. Clarify this is not an individual fraud classifier and broad accuracy has not been established.');
}
// 11 graph
{
 const s=base('LangGraph: ordered investigation steps');
 const labels=['Intake','Planner','SQL','RAG','Analytics','Evidence check','Recommend','Approval gate','Audit'];
 const x0=75,y0=180,ww=250,hh=68,gx=140,gy=26;
 labels.forEach((lab,i)=>{
  const row=Math.floor(i/3),col=i%3;const x=x0+col*(ww+gx),y=y0+row*(hh+gy);
  shape(s,'roundRect','graph-node',x,y,ww,hh,i===7?'#FFF2DC':C.white,i===7?C.amber:C.blue,1.5);
  txt(s,lab,x+10,y+10,ww-20,48,18,C.navy,true,'center');
 });
 box(s,900,434,300,125,'After approval','resume_after_approval calls a separate local action executor. It does not reroute live traffic.',C.teal);
 txt(s,'Nine nodes are wired in build_graph; the action executor is a separate post-approval continuation.',92,594,1095,42,16,C.muted,false,'center');
 notes(s,['backend/app/agent/workflow.py'],'Point out that the first graph contains nine wired nodes. The local action executor happens later, only after a saved approval.');
}
// 12 RAG
{
 const s=base('RAG: retrieve a procedure before generating');
 const steps=[['SOP text','Local .txt files'],['Chunks','Numbered sections; long sections split'],['Index','TF-IDF by default'],['Search','Cosine similarity returns top matches'],['Context','Citations are passed as untrusted reference text']];
 steps.forEach((x,i)=>box(s,58+i*240,210,218,270,x[0],x[1],i===4?C.teal:C.blue));
 txt(s,'No LlamaIndex dependency is present in the reviewed PayBridge source. Default RAG is lexical TF-IDF.',90,535,1100,52,18,C.amber,true,'center');
 notes(s,['backend/app/rag/store.py','backend/app/agent/tools/rag_tool.py','backend/data/documents/'],'Explain that RAG retrieves procedures while transaction facts come from SQL. Retrieval does not guarantee a correct answer.');
}
// 13 evidence
{
 const s=base('Evidence: separate facts from inference');
 box(s,75,174,340,325,'Database fact','Example: the saved row has status FAILED and error code GATEWAY_TIMEOUT.',C.blue);
 box(s,470,174,340,325,'Retrieved procedure','A local SOP section describes the escalation process for a specified timeout pattern.',C.teal);
 box(s,865,174,340,325,'Inference','The two sources may support a hypothesis. If a field or baseline is missing, say so.',C.amber);
 txt(s,'The validator checks evidence sufficiency and numeric grounding; it is not a full semantic proof.',105,550,1070,52,18,C.muted,false,'center');
 notes(s,['backend/app/agent/evidence.py','backend/app/agent/workflow.py'],'Use the fact/evidence/inference distinction. If the database does not contain a reason, the assistant should not invent one.');
}
// 14 approvals
{
 const s=base('Approvals: a human reviews the proposed action');
 const stages=[['Signal','An unusual payment group is flagged'],['Evidence','SQL, analytics, and procedures are reviewed'],['Decision','Authorized operator approves or rejects'],['Local record','Approved path writes an application action record']];
 stages.forEach((a,i)=>{
  const x=70+i*300;shape(s,'roundRect','approval-stage',x,228,255,230,i===2?'#FFF2DC':C.white,i===2?C.amber:C.line,1.5);
  txt(s,a[0],x+18,251,219,38,20,C.navy,true,'center');txt(s,a[1],x+22,305,211,100,16,C.muted,false,'center');
  if(i<3)shape(s,'rightArrow','arrow',x+258,320,40,40,C.teal,'none',0);
 });
 txt(s,'Approval does not change a customer payment’s status or route a real bank transaction.',90,525,1100,56,21,C.red,true,'center');
 notes(s,['backend/app/api/main.py','backend/app/agent/workflow.py','backend/app/agent/tools/action_tool.py'],'Approval prevents an unreviewed application action. In this code, the post-approval action is local rather than a live payment-routing change.');
}
// 15 Razorpay
{
 const s=base('Razorpay checkout: verify on the server');
 const steps=[['Create','FastAPI creates provider order'],['Pay','Razorpay Checkout completes a test attempt'],['Verify','Server checks signature and fetches captured state'],['Receipt','Only a matching captured database row is shown']];
 steps.forEach((a,i)=>{
  const x=70+i*300;shape(s,'roundRect','payment-stage',x,220,255,215,C.white,C.line,1.4);
  txt(s,a[0],x+12,242,231,36,20,C.navy,true,'center');txt(s,a[1],x+20,292,215,86,16,C.muted,false,'center');
  if(i<3)shape(s,'rightArrow','arrow',x+257,305,42,42,C.blue,'none',0);
 });
 txt(s,'Order created ≠ payment completed. Browser callback ≠ verified capture.',90,500,1100,48,22,C.amber,true,'center');
 txt(s,'The secret remains server-side. This guide does not include credentials.',130,558,1020,34,16,C.muted,false,'center');
 notes(s,['backend/app/api/checkout.py','frontend/views/customer_portal.py'],'Explain order creation, checkout, provider verification, and receipt gating. Do not expose the Razorpay secret.');
}
// 16 operations
{
 const s=base('Running, packaging, and deployment');
 box(s,70,168,350,360,'Local app','start-demo.ps1\nFastAPI: 127.0.0.1:8000\nSwagger: /docs\nStreamlit: 127.0.0.1:8501',C.blue);
 box(s,465,168,350,360,'Docker Compose','API + Streamlit services\nShared SQLite data volume\nOllama points to host\nNo Postgres service defined',C.teal);
 box(s,860,168,350,360,'Hosted deployment','User reports a Render deployment.\nRepository snapshot has no Render manifest.\nHosted database, persistence, and model are not verified here.',C.amber);
 txt(s,'The CI workflow builds both images and runs checks; this authoring pass did not run CI.',100,568,1080,44,17,C.muted,false,'center');
 notes(s,['start-demo.ps1','Dockerfile','frontend/Dockerfile','docker-compose.yml','.github/workflows/ci.yml'],'Separate local setup from hosted setup. The source tree does not establish the current Render service configuration.');
}
// 17 status and boundaries
{
 const s=base('What is working and what remains bounded');
 const left=[['Implemented','Payment models, CSV pipeline, deterministic analytics, API routes, anomaly code, investigation graph, verification code.'],['Conditional','Razorpay needs valid credentials/provider access; Ollama needs a reachable local model.'],['Simulated','Demo wallet balance and local operational action records.'],['Illustrative','Some incident-card narrative, latency figures, and recommendation text in the investigation UI.']];
 left.forEach((a,i)=>numberRow(s,i+1,a[0],a[1],80,162+i*108,1100,[C.blue,C.teal,C.amber,C.red][i]));
 notes(s,['README.md','backend/app/services/demo.py','backend/app/services/demo_wallet.py','frontend/views/ai_investigation_workspace.py'],'Use the labels to avoid overclaiming. The presence of code does not prove the current cloud service has the same configuration.');
}
// 18 demo story
{
 const s=base('A simple five-minute demo story');
 const items=[
  'Start with a merchant payment problem.',
  'Show one customer order and explain wallet versus provider checkout.',
  'Show the saved payment in the merchant ledger and identify its source.',
  'Show status counts and explain the success-rate denominator.',
  'Investigate one payment or one selected alert; label sample UI content.',
  'Review the evidence and record a human decision.',
  'Finish by stating that mitigation is local and does not reroute live payments.'
 ];
 items.forEach((t,i)=>numberRow(s,i+1,'',t,85,155+i*70,1090,i===6?C.teal:C.blue));
 notes(s,['frontend/views/customer_portal.py','frontend/views/merchant_portal.py','frontend/views/admin_dashboard.py','frontend/views/ai_investigation_workspace.py'],'Use one consistent example. Say which values are read from SQL and which are illustrative.');
}
// 19 interview pitch
{
 const s=base('Interview explanation you can say naturally');
 shape(s,'roundRect','pitch-box',90,175,1100,335,C.white,C.line,1.4);
 txt(s,'“PayBridge is a payment-operations prototype I built to help teams review payment data and investigate unusual failure patterns. It imports compatible records, stores them in SQL, calculates metrics, and uses an investigation workflow to combine database evidence with relevant procedures. An operator reviews the recommendation and records a decision. Some data and incident narratives are synthetic or illustrative, and the approved action is local; the project does not reroute live payment traffic.”',130,210,1020,270,24,C.navy,false,'center');
 txt(s,'Keep the business problem first. Then explain data, backend, analytics, investigation, and the safety boundary.',95,554,1090,56,18,C.teal,true,'center');
 notes(s,['README.md','backend/app/agent/workflow.py','backend/app/services/ingestion_payments.py'],'Invite the interviewer to pick one step and then trace it to the file and database record.');
}
// 20 close
{
 const s=base('The project in one sentence');
 txt(s,'Payment data → validation → SQL → analytics → anomaly signal → investigation → evidence → human review → audit',105,230,1070,125,30,C.navy,true,'center');
 shape(s,'roundRect','closing-label',220,420,840,70,C.navy,'none',0);
 txt(s,'A working prototype with clearly stated limits',245,433,790,42,22,C.white,true,'center');
 txt(s,'Demonstrate evidence. Explain the denominator. Do not claim live routing.',120,558,1040,38,19,C.muted,false,'center');
 notes(s,['README.md','docs/limitations.md'],'Close with the value proposition and the implementation boundary.');
}

// Render every slide for inspection and export a draft.
for (let i=0;i<p.slides.items.length;i++){
  const slide=p.slides.items[i];
  const png=await p.export({slide,format:'png',scale:1});
  await fs.writeFile(path.join(buildDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
const montage=await p.export({format:'webp',montage:true});
await fs.writeFile(path.join(buildDir,'montage.webp'),new Uint8Array(await montage.arrayBuffer()));
const candidatePath=path.join(buildDir,'candidate.pptx');
const blob=await PresentationFile.exportPptx(p);await blob.save(candidatePath);
const result=await finalizePresentation({
  explicitTotalSlideCount:20,
  requiredNativeTableOwnerSlides:[],
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable:'C:/Users/nav/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
  integrityValidatorPath:'C:/Users/nav/.codex/plugins/cache/openai-primary-runtime/presentations/26.1030.10813/skills/presentations/container_tools/inspect_presentation_package_integrity.py',
  layoutValidatorPath:'C:/Users/nav/.codex/plugins/cache/openai-primary-runtime/presentations/26.1030.10813/skills/presentations/container_tools/inspect_presentation_layout_geometry.py',
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],
  fontPolicy:{basis:'design',families:[FONT]},
  verifyArtifactToolImport:true,
  receiptPath:path.join(buildDir,'PayBridge_Explanation_Deck.validation.json'),
});
console.log(JSON.stringify({finalPath,slides:p.slides.items.length,result},null,2));
