'use strict';
(async function(){
  const body=document.getElementById('checksBody');const summary=document.getElementById('snapshotSummary');
  try{
    const response=await fetch('./status.json',{cache:'no-store'});if(!response.ok)throw new Error('Snapshot not available');
    const d=await response.json();body.replaceChildren();let configured=0;
    for(const item of d.checks){if(item.enabled)configured++;
      const tr=document.createElement('tr');
      const a=document.createElement('td');a.textContent=item.name;
      const b=document.createElement('td');b.textContent=item.state.replaceAll('_',' ').toUpperCase();b.className='state '+(item.state==='up'?'up':item.state==='down'?'down':'');
      const c=document.createElement('td');c.textContent=item.checked_at||'—';
      tr.append(a,b,c);body.append(tr);
    }
    summary.textContent=configured?`${configured} public check(s) configured.`:'No external checks enabled yet. This is normal before deployment.';
    document.getElementById('snapshotTime').textContent=d.generated_at?`Snapshot generated: ${d.generated_at}`:'No checks have run.';
  }catch(e){body.textContent='No readable status snapshot. Run the site build/status workflow.';summary.textContent='Snapshot unavailable — no status claims can be made.';}
})();
