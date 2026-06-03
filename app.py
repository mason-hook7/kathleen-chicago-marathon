import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Kathleen — Chicago Marathon Plan",
    page_icon="🏃",
    layout="wide",
)
st.markdown(
    "<style>.block-container{padding-top:1rem;padding-bottom:0rem;}</style>",
    unsafe_allow_html=True,
)

# Interactive plan. Now also: a "Today" banner up top showing the
# current day's workout (with a one-tap Mark-done button), and the
# matching day highlighted on the calendar. Progress still saves in
# the browser (localStorage) across refreshes and future updates.
PLAN_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kathleen — Chicago Marathon Training Plan</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,900;1,9..144,500&family=Hanken+Grotesk:wght@400;500;600;800&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#f4efe6; --paper-2:#ece5d8; --ink:#1c1d1a; --ink-soft:#55564f; --line:#d8cfbe;
    --race:#cf4326; --long:#2f5d7c; --quality:#bd7314; --easy:#4a7c4e; --xt:#6f9c8c;
    --rest:#9a948a; --shake:#8a6cae; --travel:#a9824e; --done:#2f8f4e;
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  html{-webkit-text-size-adjust:100%;}
  body{
    background:
      radial-gradient(circle at 12% 8%, rgba(207,67,38,.06), transparent 38%),
      radial-gradient(circle at 88% 4%, rgba(47,93,124,.07), transparent 42%),
      var(--paper);
    color:var(--ink); font-family:'Hanken Grotesk',sans-serif; line-height:1.5;
    padding:clamp(14px,3.2vw,40px);
  }
  .wrap{max-width:1080px;margin:0 auto;}

  .mast{border-bottom:3px solid var(--ink);padding-bottom:20px;margin-bottom:0;}
  .kicker{font-size:12.5px;letter-spacing:.32em;text-transform:uppercase;font-weight:800;color:var(--race);margin-bottom:12px;}
  h1{font-family:'Fraunces',serif;font-weight:900;font-size:clamp(34px,7vw,68px);line-height:.92;letter-spacing:-.02em;margin-bottom:6px;}
  h1 em{font-style:italic;font-weight:500;color:var(--long);}
  .sub{font-family:'Fraunces',serif;font-style:italic;font-size:clamp(15px,2.2vw,20px);color:var(--ink-soft);font-weight:500;margin-top:8px;}

  /* ---------- Today banner ---------- */
  .today-banner{
    display:grid;grid-template-columns:auto 1fr auto;gap:20px;align-items:center;
    margin:20px 0 4px;padding:16px 20px;border-radius:14px;
    background:linear-gradient(120deg, #fbf7ee, #f0e7d6);
    border:2px solid var(--race);box-shadow:0 3px 0 rgba(207,67,38,.18);
  }
  .tb-left{display:flex;flex-direction:column;gap:4px;border-right:1px solid var(--line);padding-right:18px;}
  .tb-tag{font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;font-weight:800;color:var(--race);}
  .tb-date{font-family:'Fraunces',serif;font-weight:600;font-size:16px;line-height:1.05;}
  .tb-main{display:flex;flex-direction:column;gap:2px;}
  .tb-dist{font-family:'Fraunces',serif;font-weight:900;font-size:clamp(22px,3.4vw,30px);line-height:1;}
  .tb-label{font-size:13.5px;color:var(--ink-soft);}
  .tb-label b{color:var(--ink);font-weight:700;}
  .tb-action{display:flex;align-items:center;}
  .tb-btn{font-family:'Hanken Grotesk',sans-serif;font-weight:800;font-size:13px;letter-spacing:.02em;
    border:2px solid var(--done);background:var(--done);color:#fff;border-radius:30px;padding:11px 20px;cursor:pointer;white-space:nowrap;transition:all .15s;}
  .tb-btn:hover{filter:brightness(1.06);}
  .tb-btn.done{background:var(--paper);color:var(--done);}
  .tb-rest{font-size:13px;font-weight:700;color:var(--ink-soft);font-style:italic;white-space:nowrap;}
  @media(max-width:640px){
    .today-banner{grid-template-columns:1fr;gap:12px;}
    .tb-left{border-right:none;border-bottom:1px solid var(--line);padding-right:0;padding-bottom:10px;flex-direction:row;align-items:baseline;gap:10px;}
    .tb-action .tb-btn{width:100%;}
  }

  /* ---------- Sticky dashboard ---------- */
  .dash{
    position:sticky;top:0;z-index:20;margin:14px -4px 24px;padding:14px 18px;
    background:rgba(244,239,230,.94);backdrop-filter:blur(8px);
    border-bottom:2px solid var(--ink);
    display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:center;
  }
  .count{display:flex;flex-direction:column;align-items:flex-start;border-right:1px solid var(--line);padding-right:24px;}
  .count .big{font-family:'Fraunces',serif;font-weight:900;font-size:clamp(30px,5vw,46px);line-height:.9;color:var(--race);}
  .count .lab{font-size:10px;letter-spacing:.18em;text-transform:uppercase;font-weight:800;color:var(--ink-soft);margin-top:6px;}
  .count .date{font-size:11.5px;color:var(--ink-soft);font-weight:600;margin-top:2px;}
  .prog{display:flex;flex-direction:column;gap:8px;}
  .prog-top{display:flex;justify-content:space-between;align-items:baseline;}
  .prog-top .pct{font-family:'Fraunces',serif;font-weight:900;font-size:clamp(20px,3.2vw,28px);}
  .prog-top .cnt{font-size:12.5px;color:var(--ink-soft);font-weight:600;}
  .bar{height:14px;background:var(--paper-2);border:1px solid var(--line);border-radius:20px;overflow:hidden;}
  .bar-fill{height:100%;width:0%;background:linear-gradient(90deg,var(--long),var(--done));border-radius:20px;transition:width .35s ease;}
  .reset{align-self:flex-end;background:none;border:none;color:var(--ink-soft);font-family:'Hanken Grotesk',sans-serif;font-size:11px;font-weight:600;text-decoration:underline;cursor:pointer;padding:0;}
  .reset:hover{color:var(--race);}

  .stats{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--line);border:1px solid var(--line);margin:0 0 30px;border-radius:10px;overflow:hidden;}
  .stat{background:var(--paper);padding:14px 12px;}
  .stat .v{font-family:'Fraunces',serif;font-weight:900;font-size:clamp(20px,3.4vw,30px);line-height:1;}
  .stat .l{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);margin-top:6px;font-weight:600;}

  .panels{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:30px;}
  .panel{background:var(--paper-2);border:1px solid var(--line);border-radius:12px;padding:18px 20px;}
  .panel h3{font-family:'Fraunces',serif;font-size:18px;font-weight:600;margin-bottom:12px;display:flex;align-items:center;gap:9px;}
  .panel h3::before{content:"";width:9px;height:18px;background:var(--ink);border-radius:2px;}
  .pace-row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px dashed var(--line);font-size:14px;}
  .pace-row:last-child{border-bottom:none;}
  .pace-row b{font-weight:600;} .pace-row span{font-variant-numeric:tabular-nums;color:var(--ink-soft);font-weight:600;}
  .key{display:flex;flex-wrap:wrap;gap:8px 13px;}
  .chip{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:600;}
  .dot{width:13px;height:13px;border-radius:4px;flex:0 0 auto;}
  .hint{font-size:12.5px;color:var(--ink-soft);margin-top:12px;line-height:1.4;}

  .phase-head{font-family:'Fraunces',serif;font-weight:900;letter-spacing:-.01em;font-size:clamp(19px,2.8vw,25px);margin:30px 0 4px;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;}
  .phase-head small{font-family:'Hanken Grotesk',sans-serif;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft);font-weight:700;}
  .phase-rule{height:2px;background:var(--ink);opacity:.85;margin-bottom:16px;}

  .week{background:var(--paper);border:1px solid var(--line);border-radius:12px;margin-bottom:14px;overflow:hidden;}
  .week.down{background:repeating-linear-gradient(135deg,var(--paper),var(--paper) 11px,var(--paper-2) 11px,var(--paper-2) 22px);}
  .week.travelwk{background:repeating-linear-gradient(135deg,var(--paper),var(--paper) 11px,#efe2cf 11px,#efe2cf 22px);}
  .week.peak{border-color:var(--race);box-shadow:0 0 0 1px var(--race);}
  .week.raceweek{border-color:var(--race);box-shadow:0 2px 0 var(--race);}
  .wk-head{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px 16px;background:rgba(28,29,26,.04);border-bottom:1px solid var(--line);flex-wrap:wrap;}
  .wk-id{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;}
  .wk-n{font-family:'Fraunces',serif;font-weight:900;font-size:20px;}
  .wk-dates{font-size:13px;color:var(--ink-soft);font-weight:600;}
  .wk-tag{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:800;padding:3px 9px;border-radius:20px;color:#fff;}
  .tag-down{background:var(--rest);} .tag-peak{background:var(--race);} .tag-race{background:var(--race);}
  .tag-travel{background:var(--travel);} .tag-long{background:var(--long);} .tag-start{background:var(--easy);}
  .wk-meta{display:flex;align-items:center;gap:12px;}
  .wk-prog{font-size:12px;font-weight:700;color:var(--done);font-variant-numeric:tabular-nums;}
  .wk-total{font-size:13.5px;font-weight:700;font-variant-numeric:tabular-nums;}
  .wk-total b{font-family:'Fraunces',serif;font-size:17px;}

  .days{display:grid;grid-template-columns:repeat(7,1fr);}
  .day{position:relative;border-right:1px solid var(--line);padding:11px 11px 13px;min-height:112px;border-top:4px solid var(--rest);}
  .day:last-child{border-right:none;}
  .day.t-rest{border-top-color:var(--rest);} .day.t-easy{border-top-color:var(--easy);}
  .day.t-quality{border-top-color:var(--quality);} .day.t-long{border-top-color:var(--long);}
  .day.t-xt{border-top-color:var(--xt);} .day.t-shake{border-top-color:var(--shake);}
  .day.t-travel{border-top-color:var(--travel);background:repeating-linear-gradient(135deg,transparent,transparent 6px,rgba(169,130,78,.09) 6px,rgba(169,130,78,.09) 12px);}
  .day.t-race{border-top-color:var(--race);background:rgba(207,67,38,.07);}
  .day.tappable{cursor:pointer;-webkit-tap-highlight-color:transparent;transition:background .15s;}
  .day.tappable:hover{background:rgba(47,143,78,.06);}
  .day.done{background:rgba(47,143,78,.10);}
  .day.done:hover{background:rgba(47,143,78,.14);}
  .day.done .d-dist,.day.done .d-label{opacity:.55;}
  .day.done .d-name{color:var(--done);}
  .day.today{box-shadow:inset 0 0 0 2.5px var(--race);background:rgba(207,67,38,.06);}
  .day.today.done{background:rgba(47,143,78,.12);}
  .today-pill{position:absolute;top:8px;left:8px;background:var(--race);color:#fff;font-size:8.5px;letter-spacing:.14em;font-weight:800;padding:2px 6px;border-radius:10px;}
  .d-name{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);font-weight:700;}
  .day.today .d-name{margin-top:14px;}
  .d-dist{font-family:'Fraunces',serif;font-weight:900;font-size:19px;margin:3px 0 4px;line-height:1;}
  .d-dist.soft{color:var(--rest);font-weight:600;font-size:15px;font-style:italic;}
  .d-dist.race{color:var(--race);} .d-dist.travel{color:var(--travel);font-weight:600;font-size:14px;font-style:italic;}
  .d-label{font-size:11.5px;line-height:1.32;color:var(--ink-soft);}
  .d-label b{color:var(--ink);font-weight:700;}
  .check{position:absolute;top:9px;right:9px;width:20px;height:20px;border:2px solid var(--line);border-radius:50%;background:var(--paper);display:flex;align-items:center;justify-content:center;font-size:13px;color:#fff;line-height:1;}
  .day.done .check{background:var(--done);border-color:var(--done);}
  .check::after{content:"✓";opacity:0;font-weight:700;}
  .day.done .check::after{opacity:1;}

  .notes{margin-top:36px;border-top:3px solid var(--ink);padding-top:22px;}
  .notes h2{font-family:'Fraunces',serif;font-weight:900;font-size:25px;margin-bottom:16px;}
  .ngrid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .note{background:var(--paper-2);border:1px solid var(--line);border-left:4px solid var(--long);border-radius:0 10px 10px 0;padding:14px 18px;}
  .note h4{font-family:'Fraunces',serif;font-size:16px;font-weight:600;margin-bottom:6px;}
  .note p{font-size:13.5px;color:var(--ink-soft);}
  .note.heat{border-left-color:var(--quality);} .note.fuel{border-left-color:var(--easy);}
  .note.trip{border-left-color:var(--travel);} .note.strength{border-left-color:var(--shake);} .note.race{border-left-color:var(--race);}

  .foot{margin-top:24px;font-size:12px;color:var(--ink-soft);text-align:center;font-style:italic;font-family:'Fraunces',serif;}

  @media(max-width:760px){
    .panels{grid-template-columns:1fr;} .stats{grid-template-columns:repeat(2,1fr);} .ngrid{grid-template-columns:1fr;}
    .days{grid-template-columns:repeat(2,1fr);} .day{border-right:none;border-bottom:1px solid var(--line);min-height:auto;}
    .dash{grid-template-columns:1fr;gap:14px;} .count{border-right:none;border-bottom:1px solid var(--line);padding-right:0;padding-bottom:12px;}
  }
</style>
</head>
<body>
<div class="wrap">

  <header class="mast">
    <div class="kicker">Bank of America Chicago Marathon &middot; Sun Oct 11, 2026</div>
    <h1>Kathleen's <em>Road to 26.2</em></h1>
    <div class="sub">A 19-week build to a 4:15 finish. Tap any workout to mark it done.</div>
  </header>

  <div class="today-banner" id="today-banner">
    <div class="tb-left">
      <div class="tb-tag" id="tb-tag">Today</div>
      <div class="tb-date" id="tb-date">—</div>
    </div>
    <div class="tb-main">
      <div class="tb-dist" id="tb-dist">—</div>
      <div class="tb-label" id="tb-label"></div>
    </div>
    <div class="tb-action" id="tb-action"></div>
  </div>

  <div class="dash">
    <div class="count">
      <div class="big" id="cd-days">—</div>
      <div class="lab">days until Chicago</div>
      <div class="date">Race day &middot; Sun Oct 11, 2026 &middot; 7:20a</div>
    </div>
    <div class="prog">
      <div class="prog-top">
        <span class="pct" id="pg-pct">0%</span>
        <span class="cnt" id="pg-cnt">0 of 0 sessions done</span>
      </div>
      <div class="bar"><div class="bar-fill" id="pg-fill"></div></div>
      <button class="reset" id="reset-btn">Reset progress</button>
    </div>
  </div>

  <div class="stats">
    <div class="stat"><div class="v">19</div><div class="l">Weeks</div></div>
    <div class="stat"><div class="v">4&ndash;5&times;</div><div class="l">Runs / week</div></div>
    <div class="stat"><div class="v">41</div><div class="l">Peak miles</div></div>
    <div class="stat"><div class="v">22</div><div class="l">Longest run</div></div>
    <div class="stat"><div class="v">4:15</div><div class="l">Goal time</div></div>
  </div>

  <div class="panels">
    <div class="panel">
      <h3>Pace Guide</h3>
      <div class="pace-row"><b>Recovery / cross-train</b><span>easy effort</span></div>
      <div class="pace-row"><b>Easy / Long</b><span>10:30 &ndash; 11:15 /mi</span></div>
      <div class="pace-row"><b>Marathon pace (MP)</b><span>9:45 /mi</span></div>
      <div class="pace-row"><b>Tempo / Threshold</b><span>9:00 &ndash; 9:15 /mi</span></div>
      <div class="pace-row"><b>Strides</b><span>~8:00 /mi, 20s ea.</span></div>
    </div>
    <div class="panel">
      <h3>Day Key</h3>
      <div class="key">
        <span class="chip"><span class="dot" style="background:var(--rest)"></span>Rest / strength</span>
        <span class="chip"><span class="dot" style="background:var(--easy)"></span>Easy run</span>
        <span class="chip"><span class="dot" style="background:var(--quality)"></span>Quality / tempo</span>
        <span class="chip"><span class="dot" style="background:var(--long)"></span>Long run (Sat)</span>
        <span class="chip"><span class="dot" style="background:var(--xt)"></span>Cross-train (Sun)</span>
        <span class="chip"><span class="dot" style="background:var(--travel)"></span>Travel</span>
        <span class="chip"><span class="dot" style="background:var(--race)"></span>Race day</span>
      </div>
      <p class="hint">Core runs: <b style="color:var(--ink)">Tue (quality) &middot; Wed &middot; Thu (easy) &middot; Sat (long)</b>. Bigger weeks add an easy Monday. Fri = rest; Sun = cross-train. <b style="color:var(--done)">Tap a workout to check it off</b> — progress saves automatically on this device. Today's workout is outlined in red.</p>
    </div>
  </div>

  <div id="plan"></div>

  <div class="notes">
    <h2>Coaching Notes</h2>
    <div class="ngrid">
      <div class="note heat">
        <h4>Summer heat (Jun&ndash;Aug)</h4>
        <p>The build runs through NYC summer. Run early AM, hydrate hard, and on hot/humid days go by <b>effort, not pace</b> &mdash; heat can add 10&ndash;25 sec/mi.</p>
      </div>
      <div class="note trip">
        <h4>The trip (Jul 11&ndash;17)</h4>
        <p>Built in as a recovery break. Week 6 moves its long run to <b>Fri Jul 10</b> before you leave; Week 7 eases back with one easy run on return (Sat Jul 18).</p>
      </div>
      <div class="note fuel">
        <h4>Fuel &amp; the long run</h4>
        <p>From Week 8 on, treat long runs as rehearsals: a gel every ~30&ndash;40 min plus fluids, using the <b>exact products</b> she'll race with. Run the Week 16 twenty-two very easy.</p>
      </div>
      <div class="note strength">
        <h4>Cross-train &amp; strength</h4>
        <p>Sunday cross-train stays <b>low-impact</b> (bike, swim, elliptical, 40&ndash;60 min). Add 1&ndash;2 short strength sessions on rest days. Easy days stay <b>truly conversational</b>.</p>
      </div>
      <div class="note race">
        <h4>Race day &middot; Oct 11</h4>
        <p>7:20a wave start from Grant Park; flat, fast, likely 40s&ndash;50s&deg;F. Target even splits at <b>9:45/mi</b> &mdash; bank patience, not time.</p>
      </div>
    </div>
  </div>

  <div class="foot">Built around Kathleen's spring half-marathon base &middot; tap to track, and report back if a week feels off.</div>

</div>

<script>
const P = {
  base:{label:'Phase 1 · Base', note:'Build frequency & easy volume — no hard efforts yet'},
  thr :{label:'Phase 2 · Strength & Threshold', note:'Tempo work begins, then the trip recovery break'},
  bld :{label:'Phase 3 · Build', note:'Bigger long runs, longer quality sessions'},
  spec:{label:'Phase 4 · Marathon-Specific', note:'Goal-pace long runs — incl. the 20 & 22'},
  tap :{label:'Phase 5 · Taper & Race', note:'Cut volume, keep sharpness, arrive fresh'}
};
const CHECKABLE = ['easy','quality','long','shake','race','xt'];

const weeks = [
 {n:1, phase:'base', dates:'Jun 1 – Jun 7', total:17, badge:{t:'Start',c:'start'}, days:[
   ['Mon','easy','3','Easy <b>3</b>'],['Tue','easy','3','Easy <b>3</b> + 4 strides'],
   ['Wed','rest','Rest','Mobility / rest','soft'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','7','Easy long <b>7</b>'],['Sun','xt','XT','Cross-train 40m']]},
 {n:2, phase:'base', dates:'Jun 8 – Jun 14', total:19, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','easy','4','Easy <b>4</b> + strides'],
   ['Wed','easy','3','Easy <b>3</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','8','Easy long <b>8</b>'],['Sun','xt','XT','Cross-train 40m']]},
 {n:3, phase:'base', dates:'Jun 15 – Jun 21', total:22, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','easy','4','Easy <b>4</b> + strides'],
   ['Wed','easy','4','Easy <b>4</b>'],['Thu','easy','5','Easy <b>5</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','9','Easy long <b>9</b>'],['Sun','xt','XT','Cross-train 45m']]},
 {n:4, phase:'base', dates:'Jun 22 – Jun 28', total:17, down:true, badge:{t:'Cutback',c:'down'}, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','easy','4','Easy <b>4</b> + strides'],
   ['Wed','easy','3','Easy <b>3</b>'],['Thu','easy','3','Easy <b>3</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','7','Long <b>7</b> · cutback'],['Sun','xt','XT','Cross-train 40m']]},
 {n:5, phase:'thr', dates:'Jun 29 – Jul 5', total:23, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','quality','6','1.5 wu · <b>2.5mi tempo</b> · cd'],
   ['Wed','easy','4','Easy <b>4</b>'],['Thu','easy','3','Easy <b>3</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','10','Easy long <b>10</b>'],['Sun','xt','XT','Cross-train 45m']]},
 {n:6, phase:'thr', dates:'Jul 6 – Jul 12', total:23, travelwk:true, badge:{t:'Pre-trip',c:'travel'}, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','quality','6','1.5 wu · <b>3mi tempo</b> · cd'],
   ['Wed','easy','4','Easy <b>4</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','long','9','<b>Long 9</b> · before trip'],['Sat','travel','—','Trip — no run','travel'],['Sun','travel','—','Trip — no run','travel']]},
 {n:7, phase:'thr', dates:'Jul 13 – Jul 19', total:8, travelwk:true, badge:{t:'Travel week',c:'travel'}, days:[
   ['Mon','travel','—','Trip — no run','travel'],['Tue','travel','—','Trip — no run','travel'],
   ['Wed','travel','—','Trip — no run','travel'],['Thu','travel','—','Trip — no run','travel'],
   ['Fri','travel','—','Return — no run','travel'],['Sat','long','8','Easy re-entry <b>8</b>'],['Sun','xt','XT','Light cross-train']]},
 {n:8, phase:'thr', dates:'Jul 20 – Jul 26', total:25, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','quality','5','1 wu · <b>2mi tempo</b> · cd'],
   ['Wed','easy','4','Easy <b>4</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','12','Long <b>12</b>'],['Sun','xt','XT','Cross-train 45m']]},
 {n:9, phase:'bld', dates:'Jul 27 – Aug 2', total:31, days:[
   ['Mon','easy','4','Easy <b>4</b>'],['Tue','quality','6','1.5 wu · <b>4mi tempo</b> · cd'],
   ['Wed','easy','4','Easy <b>4</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','13','Long <b>13</b> · last 3 @ MP'],['Sun','xt','XT','Cross-train 50m']]},
 {n:10, phase:'bld', dates:'Aug 3 – Aug 9', total:35, days:[
   ['Mon','easy','4','Easy <b>4</b>'],['Tue','quality','7','2 wu · <b>2×2mi tempo</b> · cd'],
   ['Wed','easy','5','Easy <b>5</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','15','Long <b>15</b>'],['Sun','xt','XT','Cross-train 50m']]},
 {n:11, phase:'bld', dates:'Aug 10 – Aug 16', total:27, down:true, badge:{t:'Cutback',c:'down'}, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','quality','6','1.5 wu · <b>3mi tempo</b> · cd'],
   ['Wed','easy','4','Easy <b>4</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','13','Long <b>13</b> · cutback'],['Sun','xt','XT','Cross-train 45m']]},
 {n:12, phase:'spec', dates:'Aug 17 – Aug 23', total:37, days:[
   ['Mon','easy','4','Easy <b>4</b>'],['Tue','quality','7','1.5 wu · <b>5mi @ MP</b> · cd'],
   ['Wed','easy','5','Easy <b>5</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','17','Long <b>17</b> · last 5 @ MP'],['Sun','xt','XT','Cross-train 50m']]},
 {n:13, phase:'spec', dates:'Aug 24 – Aug 30', total:38, days:[
   ['Mon','easy','4','Easy <b>4</b>'],['Tue','quality','7','2 wu · <b>2×2.5mi tempo</b> · cd'],
   ['Wed','easy','5','Easy <b>5</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','18','Long <b>18</b> · last 6 @ MP'],['Sun','xt','XT','Cross-train 50m']]},
 {n:14, phase:'spec', dates:'Aug 31 – Sep 6', total:39, badge:{t:'First 20',c:'long'}, days:[
   ['Mon','easy','4','Easy <b>4</b>'],['Tue','quality','6','1.5 wu · <b>5mi @ MP</b> · cd'],
   ['Wed','easy','5','Easy <b>5</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','20','Long <b>20</b> · mid 8 @ MP'],['Sun','xt','XT','Cross-train 50m']]},
 {n:15, phase:'spec', dates:'Sep 7 – Sep 13', total:28, down:true, badge:{t:'Cutback',c:'down'}, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','quality','6','1.5 wu · <b>4mi tempo</b> · cd'],
   ['Wed','easy','4','Easy <b>4</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','14','Long <b>14</b> · last 4 @ MP'],['Sun','xt','XT','Cross-train 45m']]},
 {n:16, phase:'spec', dates:'Sep 14 – Sep 20', total:41, peak:true, badge:{t:'Peak · 22',c:'peak'}, days:[
   ['Mon','easy','4','Easy <b>4</b>'],['Tue','quality','6','1.5 wu · <b>4mi @ MP</b> · cd'],
   ['Wed','easy','5','Easy <b>5</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','22','Long <b>22</b> · easy, 8–10 @ MP'],['Sun','xt','XT','Cross-train 50m']]},
 {n:17, phase:'tap', dates:'Sep 21 – Sep 27', total:28, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','quality','6','1.5 wu · <b>4mi @ MP</b> · cd'],
   ['Wed','easy','4','Easy <b>4</b>'],['Thu','easy','4','Easy <b>4</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','14','Long <b>14</b> · last 3 @ MP'],['Sun','xt','XT','Cross-train 40m']]},
 {n:18, phase:'tap', dates:'Sep 28 – Oct 4', total:21, days:[
   ['Mon','rest','Rest','Strength / rest','soft'],['Tue','quality','5','1 wu · <b>3mi @ MP</b> · cd'],
   ['Wed','easy','3','Easy <b>3</b>'],['Thu','easy','3','Easy <b>3</b>'],
   ['Fri','rest','Rest','Full rest','soft'],['Sat','long','10','Long <b>10</b> · 2 @ MP'],['Sun','xt','XT','Light cross-train']]},
 {n:19, phase:'tap', dates:'Oct 5 – Oct 11', total:'35+', raceweek:true, badge:{t:'Race week',c:'race'}, days:[
   ['Mon','rest','Rest','Full rest','soft'],['Tue','easy','4','Easy <b>4</b> + 4 strides'],
   ['Wed','rest','Rest','Full rest','soft'],['Thu','easy','3','Easy <b>3</b> shakeout'],
   ['Fri','rest','Rest','Rest · hydrate · carb-load','soft'],['Sat','shake','2','Shakeout <b>2</b> + strides · gear'],
   ['Sun','race','26.2','<b>CHICAGO MARATHON</b> · 7:20a · 9:45/mi','race']]}
];

// ---------- date helpers ----------
const START = new Date(2026, 5, 1);            // Mon, Jun 1, 2026 (local)
const RACE  = new Date(2026, 9, 11, 7, 20, 0); // Oct 11, 2026, 7:20a
function isoLocal(d){ return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }
function dateForCell(wn, i){ const d = new Date(2026,5,1); d.setDate(d.getDate() + (wn-1)*7 + i); return d; }

// ---------- persistence ----------
const STORE_KEY = 'kc-marathon-progress-v1';
function loadProgress(){ try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; } catch(e){ return {}; } }
function saveProgress(obj){ try { localStorage.setItem(STORE_KEY, JSON.stringify(obj)); } catch(e){} }
let progress = loadProgress();

// ---------- build calendar ----------
const plan = document.getElementById('plan');
const DATEMAP = {};
let lastPhase = null;
weeks.forEach(w=>{
  if(w.phase!==lastPhase){
    const ph = P[w.phase];
    const h = document.createElement('div'); h.className='phase-head';
    h.innerHTML = ph.label + ' <small>' + ph.note + '</small>';
    plan.appendChild(h);
    const r = document.createElement('div'); r.className='phase-rule'; plan.appendChild(r);
    lastPhase = w.phase;
  }
  const cls = ['week', w.down?'down':'', w.travelwk?'travelwk':'', w.peak?'peak':'', w.raceweek?'raceweek':''].join(' ').replace(/\s+/g,' ').trim();
  const tag = w.badge ? '<span class="wk-tag tag-'+w.badge.c+'">'+w.badge.t+'</span>' : '';

  const dayHTML = w.days.map((d,i)=>{
    const name=d[0], type=d[1], dist=d[2], label=d[3], distMod=d[4]||'';
    const checkable = CHECKABLE.indexOf(type) !== -1;
    const key = 'W'+w.n+'-'+name;
    const dISO = isoLocal(dateForCell(w.n, i));
    DATEMAP[dISO] = {wn:w.n, name:name, type:type, dist:dist, label:label, distMod:distMod, checkable:checkable, key:key, dateObj:dateForCell(w.n,i)};
    const isDone = checkable && progress[key]===true;
    return '<div class="day t-'+type+(checkable?' tappable':'')+(isDone?' done':'')+'"'
      + ' data-date="'+dISO+'" data-week="'+w.n+'"'
      + (checkable ? ' data-key="'+key+'"' : '') + '>'
      + (checkable ? '<span class="check"></span>' : '')
      + '<div class="d-name">'+name+'</div>'
      + '<div class="d-dist '+distMod+'">'+dist+'</div>'
      + '<div class="d-label">'+label+'</div>'
      + '</div>';
  }).join('');

  const el = document.createElement('div');
  el.className = cls;
  el.dataset.week = w.n;
  el.innerHTML =
    '<div class="wk-head">'
    + '<div class="wk-id"><span class="wk-n">Week '+w.n+'</span><span class="wk-dates">'+w.dates+'</span>'+tag+'</div>'
    + '<div class="wk-meta"><span class="wk-prog" data-wp="'+w.n+'"></span><span class="wk-total"><b>'+w.total+'</b> mi</span></div>'
    + '</div>'
    + '<div class="days">'+dayHTML+'</div>';
  plan.appendChild(el);
});

// ---------- interactivity ----------
const allCells = Array.from(document.querySelectorAll('.day[data-key]'));
const TOTAL = allCells.length;

function toggleCell(cell){
  const key = cell.dataset.key;
  const nowDone = !cell.classList.contains('done');
  cell.classList.toggle('done', nowDone);
  if(nowDone){ progress[key] = true; } else { delete progress[key]; }
  saveProgress(progress);
  refreshStats();
  syncBanner();
}
allCells.forEach(cell=>{ cell.addEventListener('click', ()=>toggleCell(cell)); });

function refreshStats(){
  let done = 0;
  allCells.forEach(c=>{ if(c.classList.contains('done')) done++; });
  const pct = TOTAL ? Math.round(done/TOTAL*100) : 0;
  document.getElementById('pg-pct').textContent = pct + '%';
  document.getElementById('pg-cnt').textContent = done + ' of ' + TOTAL + ' sessions done';
  document.getElementById('pg-fill').style.width = pct + '%';
  document.querySelectorAll('.wk-prog').forEach(el=>{
    const wn = el.dataset.wp;
    const cells = allCells.filter(c=>c.dataset.week===wn);
    const d = cells.filter(c=>c.classList.contains('done')).length;
    el.textContent = cells.length ? (d+'/'+cells.length) : '';
  });
}

document.getElementById('reset-btn').addEventListener('click', ()=>{
  if(confirm('Clear all checked workouts? This cannot be undone.')){
    progress = {}; saveProgress(progress);
    allCells.forEach(c=>c.classList.remove('done'));
    refreshStats(); syncBanner();
  }
});

// ---------- today banner + highlight ----------
const RESTTEXT = { rest:'Rest day — recover well', travel:'Travel day — enjoy the trip' };
let todayInfo = null;

function initToday(){
  const todayISO = isoLocal(new Date());
  const startISO = isoLocal(START);
  const tagEl = document.getElementById('tb-tag');
  const dateEl = document.getElementById('tb-date');
  const distEl = document.getElementById('tb-dist');
  const labelEl = document.getElementById('tb-label');

  // highlight the matching calendar cell (any day type)
  const cell = document.querySelector('.day[data-date="'+todayISO+'"]');
  if(cell){
    cell.classList.add('today');
    cell.insertAdjacentHTML('afterbegin','<span class="today-pill">Today</span>');
  }

  if(todayISO < startISO){
    tagEl.textContent = 'Up next';
    dateEl.textContent = 'Plan starts Mon, Jun 1';
    distEl.textContent = 'Get ready';
    labelEl.innerHTML = 'First run: Easy <b>3</b> miles';
    document.getElementById('tb-action').innerHTML = '';
    return;
  }
  if(todayISO > '2026-10-11'){
    tagEl.textContent = 'Done';
    dateEl.textContent = 'Plan complete';
    distEl.textContent = '🎉 Congratulations';
    labelEl.innerHTML = 'You crossed the line in Chicago.';
    document.getElementById('tb-action').innerHTML = '';
    return;
  }

  todayInfo = DATEMAP[todayISO] || null;
  const now = new Date();
  dateEl.textContent = now.toLocaleDateString(undefined,{weekday:'long', month:'short', day:'numeric'});
  if(todayInfo){
    distEl.textContent = (todayInfo.dist === '—') ? (todayInfo.type==='travel'?'Travel':'Rest') : todayInfo.dist + (/^\d/.test(todayInfo.dist)?' mi':'');
    labelEl.innerHTML = todayInfo.label;
  }
  syncBanner();
}

function syncBanner(){
  const a = document.getElementById('tb-action');
  if(!todayInfo){ a.innerHTML=''; return; }
  if(!todayInfo.checkable){
    a.innerHTML = '<span class="tb-rest">'+(RESTTEXT[todayInfo.type]||'Nothing to log')+'</span>';
    return;
  }
  const done = progress[todayInfo.key]===true;
  a.innerHTML = '<button class="tb-btn'+(done?' done':'')+'" id="tb-btn">'+(done?'✓ Done — undo':'Mark today done')+'</button>';
  document.getElementById('tb-btn').addEventListener('click', ()=>{
    const c = document.querySelector('.day[data-key="'+todayInfo.key+'"]');
    if(c) toggleCell(c);
  });
}

// ---------- countdown ----------
function updateCountdown(){
  const days = Math.max(0, Math.ceil((RACE - new Date()) / 86400000));
  document.getElementById('cd-days').textContent = days === 0 ? 'Today!' : days;
}

updateCountdown();
setInterval(updateCountdown, 60000);
refreshStats();
initToday();
</script>
</body>
</html>

"""

# height = how tall the scrollable plan frame is, in px. The Today
# banner + countdown + progress bar sit at the top. Nudge 760–960
# if the framing feels off on a given screen.
components.html(PLAN_HTML, height=900, scrolling=True)
