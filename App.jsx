import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [targetRole, setTargetRole] = useState('AI/ML Engineer')
  const [userName, setUserName] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('dashboard')
  const [userXP, setUserXP] = useState(0)
  const [completedQuests, setCompletedQuests] = useState([])
  const [matchPercent, setMatchPercent] = useState(0)
  const [acquiredSkills, setAcquiredSkills] = useState([])
  const [showMCQ, setShowMCQ] = useState(null)
  const [mcqAnswers, setMcqAnswers] = useState({})
  const [mcqResult, setMcqResult] = useState(null)
  const [showProfile, setShowProfile] = useState(false)

  const roles = ['AI/ML Engineer','Data Scientist','Full Stack Developer','Frontend Developer','Backend Developer','DevOps Engineer']

  const handleUpload = async () => {
    setLoading(true); setError(null)
    const fd = new FormData()
    fd.append('target_role', targetRole)
    fd.append('user_name', userName)
    if(file) fd.append('file', file)
    try {
      const res = await axios.post('https://careerverse-backend-ntg4.onrender.com/analyze-resume', fd)
      setResult(res.data); setUserXP(res.data.xp.total); setMatchPercent(res.data.skill_gap.match)
      setCompletedQuests([]); setAcquiredSkills([])
    } catch(e) { setError('Backend not running. Start on port 8080.') }
    setLoading(false)
  }

  const openMCQ = (quest) => { setShowMCQ(quest); setMcqAnswers({}); setMcqResult(null) }
  const handleMCQAnswer = (qIndex, optionIndex) => setMcqAnswers(prev => ({...prev, [qIndex]: optionIndex}))

  const submitMCQ = () => {
    const mcq = showMCQ?.mcq || []
    let correct = 0; mcq.forEach((q, i) => { if(mcqAnswers[i] === q.answer) correct++ })
    setMcqResult({correct, total: mcq.length, passed: correct === mcq.length})
    if(correct === mcq.length) completeQuest(showMCQ.title, showMCQ.xp, showMCQ.skill)
  }

  const completeQuest = (title, xp, skill) => {
    if(!completedQuests.includes(title)) {
      setUserXP(p=>p+xp); setCompletedQuests(p=>[...p,title])
      if(skill) setAcquiredSkills(p=>[...p,skill])
      setMatchPercent(Math.min(100, matchPercent + Math.round(100 / (result?.total_quests || 5))))
    }
    setShowMCQ(null); setMcqResult(null)
  }

  const downloadCertificate = () => {
    const p = result?.profile || {}
    const today = new Date().toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'})
    const certId = 'CV-' + Math.random().toString(36).substring(2,10).toUpperCase()
    const w = window.open('','','width=1000,height=750')
    w.document.write(`<html><head><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Georgia','Times New Roman',serif;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#f0ebe3;padding:30px}.cert-outer{width:850px;padding:15px;background:linear-gradient(135deg,#c9a96e,#b8955e,#c9a96e);border-radius:5px;box-shadow:0 10px 40px rgba(0,0,0,0.15)}.cert-inner{background:#fffdfb;padding:55px 60px;text-align:center;position:relative;border:2px solid #d4b896}.cert-inner::before{content:'';position:absolute;top:12px;left:12px;right:12px;bottom:12px;border:1px solid #e8d5c0;pointer-events:none}.cert-logo{font-size:1.4rem;color:#8b6914;letter-spacing:4px;text-transform:uppercase;margin-bottom:8px}.cert-title{font-size:2.8rem;color:#2c1810;margin-bottom:5px;font-weight:bold}.cert-subtitle{font-size:1.1rem;color:#6b4423;margin-bottom:30px;font-style:italic}.cert-body{font-size:1.1rem;color:#4a3728;line-height:2;margin-bottom:20px}.cert-name{font-size:2.5rem;color:#1a1a1a;font-weight:bold;margin:20px 0;padding-bottom:12px;border-bottom:2px solid #c9a96e;display:inline-block;font-family:'Brush Script MT','Georgia',cursive}.cert-role{font-size:1.4rem;color:#8b6914;font-weight:bold;margin:15px 0;text-transform:uppercase;letter-spacing:2px}.cert-skills{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:20px 0}.cert-skill-tag{padding:6px 16px;background:#faf7f2;border:1px solid #d4b896;border-radius:20px;font-size:0.85rem;color:#4a3728}.cert-footer{display:flex;justify-content:space-between;margin-top:40px;padding-top:20px;border-top:1px solid #e8d5c0;font-size:0.85rem;color:#6b4423}.cert-seal{position:absolute;bottom:60px;right:70px;width:100px;height:100px;border:3px solid #8b0000;border-radius:50%;display:flex;align-items:center;justify-content:center;transform:rotate(-20deg);opacity:0.7}.cert-seal span{color:#8b0000;font-weight:bold;font-size:0.75rem;text-align:center;line-height:1.2}.cert-id{font-size:0.75rem;color:#999;margin-top:15px}</style></head><body><div class="cert-outer"><div class="cert-inner"><div class="cert-logo">🎓 CareerVerse AI</div><div class="cert-title">Certificate of Achievement</div><div class="cert-subtitle">This is proudly presented to</div><div class="cert-name">${result?.user_name||'Student'}</div><div class="cert-body"><p>For successfully demonstrating proficiency and completing</p><p>the comprehensive career development program in</p></div><div class="cert-role">${p.target_role||'Technology'}</div><div class="cert-body"><p>with a role match score of <strong>${matchPercent}%</strong></p></div><div class="cert-skills">${(p.skills||[]).slice(0,8).map(s=>`<span class="cert-skill-tag">${s}</span>`).join('')}</div><div class="cert-footer"><div><p><strong>Date of Issue:</strong> ${today}</p><p><strong>Certificate ID:</strong> ${certId}</p></div><div style="text-align:right"><p><strong>CareerVerse AI</strong></p><p>Intelligent Career Platform</p></div></div><div class="cert-seal"><span>CERTIFIED<br>PROFESSIONAL</span></div><div class="cert-id">Verify at: careerverse.ai/verify/${certId}</div></div></div></body></html>`)
    w.document.close(); setTimeout(()=>w.print(), 600)
  }

  const downloadRoadmap = () => {
    const r = result?.roadmap || []
    let h = '<html><head><style>body{font-family:sans-serif;padding:30px;background:#fafafa;color:#333}h1{color:#6366f1}h3{color:#8b5cf6}a{color:#6366f1;display:block;margin:5px 0}</style></head><body>'
    h += `<h1>🗺️ Roadmap - ${result?.profile?.target_role}</h1>`
    r.forEach(p=>{h+=`<h3>📅 ${p.phase}</h3>`; p.tasks.forEach(t=>{h+=`<p><strong>${t.skill}</strong> - ${t.project}</p>`; t.resources.forEach(r=>h+=`<a href="${r.url}">📖 ${r.name}</a>`)})})
    h+='</body></html>'; const w=window.open('','','width=800,height=600'); w.document.write(h); w.document.close(); setTimeout(()=>w.print(),500)
  }

  const p = result?.profile || {}
  const gap = result?.skill_gap || {found:[],missing:[],found_details:[],missing_details:[]}
  const quests = result?.quests || []
  const roadmap = result?.roadmap || []
  const jobs = result?.jobs || []
  const info = p?.role_info || {}
  const interviewRes = result?.interview_resources || []
  const displayMissing = (gap.missing || []).filter(s => !acquiredSkills.includes(s))
  const tabs = ['dashboard','skills','quests','roadmap','jobs','resources']

  return (
    <div className="app">
      {!result ? (
        <div className="landing"><div className="landing-card"><div className="logo-text">🎓 CareerVerse AI</div><p className="tagline">Your Intelligent Career Companion</p>
          <div className="input-group"><label>👤 Your Name</label><input type="text" placeholder="Enter your name" value={userName} onChange={e=>setUserName(e.target.value)} /></div>
          <div className="input-group"><label>📧 Your Email</label><input type="email" placeholder="Enter your email" /></div>
          <div className="input-group"><label>🎯 Target Role</label><select value={targetRole} onChange={e=>setTargetRole(e.target.value)}>{roles.map(r=><option key={r} value={r}>{r}</option>)}</select></div>
          <div className="upload-area"><input type="file" accept=".pdf" onChange={e=>setFile(e.target.files[0])} id="fi" hidden /><label htmlFor="fi" className="upload-label">{file ? `📄 ${file.name}` : '📁 Upload Resume PDF (Optional)'}</label><span className="opt-text">You can proceed without a resume</span></div>
          <button onClick={handleUpload} disabled={loading} className="launch-btn">{loading ? '⏳ Loading...' : '🚀 Start Your Journey'}</button>
          {error && <p className="error-text">{error}</p>}
        </div></div>
      ) : (
        <div className="main-container">
          <nav className="top-nav"><div className="nav-left"><span className="nav-logo">🎓 CareerVerse AI</span></div><div className="nav-tabs">{tabs.map(t=><button key={t} className={`nav-tab ${activeTab===t?'active':''}`} onClick={()=>setActiveTab(t)}>{t==='dashboard'?'📊':t==='skills'?'🎯':t==='quests'?'📜':t==='roadmap'?'🗺️':t==='jobs'?'💼':'📚'} {t.charAt(0).toUpperCase()+t.slice(1)}</button>)}</div>
          <div className="nav-profile" onClick={()=>setShowProfile(!showProfile)}><span className="profile-icon">🎓</span><span className="profile-name">{result.user_name}</span><span className="profile-arrow">▼</span>{showProfile&&<div className="profile-dropdown"><div className="pd-item"><strong>{result.user_name}</strong></div><div className="pd-item">📧 {result.user_email}</div><div className="pd-item">🎯 {p.target_role}</div><div className="pd-item">⭐ {result?.xp?.rank}</div><div className="pd-item">⚡ {userXP} XP</div><div className="pd-item">✅ {completedQuests.length}/{quests.length} Quests</div><div className="pd-item">🛠️ {p.skills?.length||0} Skills</div><div className="pd-item">📊 {matchPercent}%</div></div>}</div></nav>

          <div className="content">
            {showMCQ && (<div className="mcq-overlay"><div className="mcq-modal"><h3>📝 Test: {showMCQ.title}</h3><p className="mcq-sub">Answer all correctly to complete!</p>
              {mcqResult ? (<div className={`mcq-result ${mcqResult.passed?'passed':'failed'}`}><h2>{mcqResult.passed ? '🎉 Passed!' : '😔 Failed'}</h2><p>{mcqResult.correct}/{mcqResult.total}</p><button onClick={()=>setShowMCQ(null)} className="close-btn">Close</button></div>) : (
                <>{showMCQ.mcq?.map((q,qi)=>(<div key={qi} className="mcq-question"><p className="mcq-q-text"><strong>Q{qi+1}. {q.q}</strong></p>{q.options.map((opt,oi)=>(<label key={oi} className={`mcq-option ${mcqAnswers[qi]===oi?'selected':''}`}><input type="radio" name={`q${qi}`} checked={mcqAnswers[qi]===oi} onChange={()=>handleMCQAnswer(qi,oi)} />{opt}</label>))}</div>))}
                <button onClick={submitMCQ} className="submit-btn" disabled={Object.keys(mcqAnswers).length !== (showMCQ.mcq?.length||0)}>Submit</button><button onClick={()=>setShowMCQ(null)} className="cancel-btn">Cancel</button></>)}
            </div></div>)}

            <div className="main-area-full">
              {activeTab==='dashboard'&&(<div>
                <h1 className="page-title">Welcome, {result.user_name}! 👋</h1>
                <div className="grid-2">
                  <div className="card match-card"><h3>🎯 Role Match</h3><div className="match-circle-wrap"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="50" fill="none" stroke="#f0ebe3" strokeWidth="10"/><circle cx="60" cy="60" r="50" fill="none" stroke="#6366f1" strokeWidth="10" strokeDasharray={`${2*Math.PI*50}`} strokeDashoffset={`${2*Math.PI*50*(1-matchPercent/100)}`} transform="rotate(-90 60 60)" strokeLinecap="round"/></svg><span className="match-text">{matchPercent}%</span></div></div>
                  <div className="card info-card"><h3>💼 Role Details</h3><div className="info-row"><span>💰 Salary</span><strong>{info.salary||'N/A'}</strong></div><div className="info-row"><span>📈 Growth</span><strong>{info.growth||'N/A'}</strong></div><div className="info-row"><span>🏢 Recruiters</span><strong>{info.companies||'N/A'}</strong></div><div className="info-row"><span>📊 Market Rate</span><strong>{info.market_rate||'N/A'}</strong></div><div className="info-row"><span>🌍 Market Size</span><strong>{info.market_size||'N/A'}</strong></div><div className="info-row"><span>🔮 Future</span><strong>{info.future_scope||'N/A'}</strong></div></div>
                </div>
                <div className="card"><h3>⚡ Your Skills</h3><div className="skill-tags">{p.skills?.length>0 ? p.skills.map((s,i)=><span key={i} className="skill-tag">{s}</span>) : <p className="empty-text">Upload resume to see skills</p>}</div></div>
                <div className="card"><h3>📊 Progress</h3><div className="progress-bar"><div className="progress-fill" style={{width:`${matchPercent}%`}}>{matchPercent}%</div></div><p className="progress-msg">🎯 Complete quests to reach 80% and unlock your career certificate!</p></div>
                {matchPercent>=80&&<div className="card cert-card"><h3>🎓 Certificate Unlocked!</h3><button onClick={downloadCertificate} className="cert-btn">📜 Download Certificate</button></div>}
              </div>)}

              {activeTab==='skills'&&(<div>
                <h1 className="page-title">🎯 Skill Gap Analysis</h1>
                <div className="card"><div className="gap-bar"><div className="gap-fill" style={{width:`${matchPercent}%`}}>{matchPercent}% Match for {p.target_role}</div></div></div>
                <div className="grid-2">
                  <div className="card skills-card-green"><h3>✅ Skills You Have ({(gap.found||[]).length})</h3>{(gap.found_details||[]).map((s,i)=>(<div key={i} className="skill-item owned"><div className="skill-item-left"><span className="skill-icon-check">✓</span><div><strong>{s.skill}</strong><span className="skill-cat">{s.category}</span></div></div><p className="why-learn-mini">💡 {s.why_learn?.substring(0,100)}...</p><div className="skill-item-right"><span className="skill-info-badge">📊 {s.demand}</span><span className="skill-info-badge">💰 {s.salary_impact}</span></div></div>))}</div>
                  <div className="card skills-card-red"><h3>🎯 Skills To Learn ({displayMissing.length})</h3>{(gap.missing_details||[]).filter(s=>!acquiredSkills.includes(s.skill)).map((s,i)=>(<div key={i} className="skill-item missing"><div className="skill-item-top"><div className="skill-item-left"><span className="skill-icon-lock">🔒</span><div><strong>{s.skill}</strong><span className="skill-cat">{s.category}</span></div></div><span className={`difficulty-badge ${(s.difficulty||'').toLowerCase()}`}>{s.difficulty}</span></div><p className="why-learn">💡 {s.why_learn}</p><div className="skill-details-grid"><div className="skill-detail-item"><span>⏱️</span><strong>{s.time_to_learn}</strong></div><div className="skill-detail-item"><span>📊</span><strong>{s.demand}</strong></div><div className="skill-detail-item"><span>💰</span><strong>{s.salary_impact}</strong></div><div className="skill-detail-item"><span>📋</span><strong>{s.prerequisites}</strong></div></div>{s.courses?.length>0&&<div className="skill-courses-section"><span className="course-label">📖 Start Learning:</span><div className="course-links-row">{s.courses.map((c,j)=><a key={j} href={c.url} target="_blank" rel="noopener noreferrer" className="course-btn">▶ {c.name}</a>)}</div></div>}</div>))}{displayMissing.length===0&&<p className="empty-text">🎉 All skills acquired!</p>}</div>
                </div>
              </div>)}

              {activeTab==='quests'&&(<div><h1 className="page-title">📜 Quests ({completedQuests.length}/{quests.length})</h1><div className="quest-list">{quests.map((q,i)=>{const done=completedQuests.includes(q.title);return(<div key={i} className={`card quest-card ${done?'done':''}`}><div className="quest-top"><span>📚</span><div><h4>{q.title}</h4><p>{q.desc}</p></div></div>{q.courses?.length>0&&<div className="quest-courses"><strong>📖 Resources:</strong>{q.courses.map((c,j)=><a key={j} href={c.url} target="_blank" rel="noopener noreferrer" className="course-link">{c.name} ({c.type})</a>)}</div>}<div className="quest-bottom"><span>💰 +{q.xp}XP</span>{done?<span className="done-badge">✅ Done</span>:<button onClick={()=>openMCQ(q)} className="complete-btn">📝 Take Test</button>}</div></div>)})}</div></div>)}

              {activeTab==='roadmap'&&(<div><div className="page-header"><h1 className="page-title">🗺️ Roadmap</h1><button onClick={downloadRoadmap} className="download-btn">📥 PDF</button></div>{roadmap.map((phase,i)=>(<div key={i} className="card"><h3>📅 {phase.phase}</h3>{phase.tasks.map((task,j)=>(<div key={j} className="roadmap-task"><strong>{task.skill}</strong><p>🏆 {task.project}</p><div className="task-links">{task.resources.map((r,k)=><a key={k} href={r.url} target="_blank" rel="noopener noreferrer">📖 {r.name}</a>)}</div></div>))}</div>))}</div>)}

              {activeTab==='jobs'&&(<div><h1 className="page-title">💼 Opportunities</h1><div className="jobs-grid">{jobs.map((job,i)=>(<div key={i} className="card job-card"><span className="job-type">{job.type}</span><h3>{job.title}</h3><p>🏢 {job.company}</p><p>📍 {job.location}</p><a href={`https://linkedin.com/jobs/search?keywords=${encodeURIComponent(job.title)}`} target="_blank" className="apply-btn">Apply →</a></div>))}</div></div>)}

              {activeTab==='resources'&&(<div>
                <h1 className="page-title">📚 Interview Preparation Resources</h1>
                <p className="subtitle-text">Based on your resume skills and target role: <strong>{p.target_role}</strong></p>
                {interviewRes.length > 0 ? (
                  <div className="interview-resources-grid">
                    {interviewRes.map((r,i)=>(<a key={i} href={r.url} target="_blank" rel="noopener noreferrer" className="interview-res-card"><span className="ir-skill">{r.skill}</span><span className="ir-name">{r.name}</span><span className="ir-arrow">→</span></a>))}
                  </div>
                ) : (<p className="empty-text">Upload resume to see personalized interview resources for your skills!</p>)}
                <h2 style={{marginTop:30,marginBottom:15}}>📖 Learning Resources</h2>
                <div className="resources-grid">
                  <div className="card"><h3>🎤 Interview Preparation</h3>
                    <a href="https://www.youtube.com/watch?v=4djLQFi5gEI" target="_blank" className="res-link">▶️ Top 50 Interview Q&A (YouTube)</a>
                    <a href="https://www.interviewbit.com/python-interview-questions/" target="_blank" className="res-link">📌 Python Interview Questions</a>
                    <a href="https://github.com/donnemartin/system-design-primer" target="_blank" className="res-link">📌 System Design Primer</a>
                    <a href="https://www.themuse.com/advice/behavioral-interview-questions-answers-examples" target="_blank" className="res-link">📌 Behavioral Questions Guide</a>
                  </div>
                  <div className="card"><h3>🧮 Aptitude & Reasoning</h3>
                    <a href="https://www.youtube.com/watch?v=tnc9ojITRg4" target="_blank" className="res-link">▶️ Aptitude Full Course (YouTube)</a>
                    <a href="https://www.youtube.com/watch?v=0FjVSU3nJoA" target="_blank" className="res-link">▶️ Logical Reasoning Tricks (YouTube)</a>
                    <a href="https://www.indiabix.com/aptitude/questions-and-answers/" target="_blank" className="res-link">📌 IndiaBix Aptitude Practice</a>
                    <a href="https://www.geeksforgeeks.org/quantitative-aptitude/" target="_blank" className="res-link">📌 Quantitative Aptitude - GFG</a>
                  </div>
                  <div className="card"><h3>💻 DSA (Data Structures & Algorithms)</h3>
                    <a href="https://www.youtube.com/watch?v=RBSGKlAvoiM" target="_blank" className="res-link">▶️ DSA Full Course (freeCodeCamp)</a>
                    <a href="https://www.youtube.com/watch?v=8hly31xKli0" target="_blank" className="res-link">▶️ Algorithms Explained (YouTube)</a>
                    <a href="https://leetcode.com/problemset/all/" target="_blank" className="res-link">📌 LeetCode Practice Problems</a>
                    <a href="https://neetcode.io/practice" target="_blank" className="res-link">📌 NeetCode 150 Roadmap</a>
                  </div>
                  <div className="card"><h3>🗄️ SQL & Database</h3>
                    <a href="https://www.youtube.com/watch?v=HXV3zeQKqGY" target="_blank" className="res-link">▶️ SQL Full Course (freeCodeCamp)</a>
                    <a href="https://www.youtube.com/watch?v=7S_tz1z_5bA" target="_blank" className="res-link">▶️ MySQL Tutorial (Programming with Mosh)</a>
                    <a href="https://www.w3schools.com/sql/" target="_blank" className="res-link">📌 W3Schools SQL Tutorial</a>
                    <a href="https://leetcode.com/problemset/database/" target="_blank" className="res-link">📌 LeetCode SQL Problems</a>
                  </div>
                </div>
              </div>)}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
export default App
