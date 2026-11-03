'use strict';
// A public catalogue of technologies, not a directory of internal service URLs.
const services = [
  ['Dashy','Core systems','Personal service dashboard'],
  ['Portainer','Core systems','Docker and Compose management'],
  ['Cloudflare Tunnel','Core systems','Remote application routing'],
  ['Tailscale','Core systems','Private device connectivity'],
  ['Code Server','Development','Browser-based coding workspace'],
  ['JupyterLab','Development','Research notebooks and prototypes'],
  ['Buffy Workbench','Development','Experiments, logs and artifacts'],
  ['Python','Development','Automation and ML programming'],
  ['Ollama / Gradio','AI & MLOps','Local-model demo components'],
  ['DVC','AI & MLOps','Dataset and experiment versioning'],
  ['Prefect','AI & MLOps','Research workflow orchestration'],
  ['MinIO','AI & MLOps','Object storage for research artifacts'],
  ['NVIDIA RTX 4060 Ti','AI & MLOps','Local GPU compute, 16 GB VRAM'],
  ['Grafana','Observability','Time-series dashboards'],
  ['Prometheus','Observability','Metrics collection and queries'],
  ['Loki','Observability','Central log storage'],
  ['Alloy','Observability','Telemetry collection'],
  ['Node Exporter','Observability','Linux system metrics'],
  ['cAdvisor','Observability','Container resource metrics'],
  ['Beszel','Observability','Host resource monitoring'],
  ['Dozzle','Observability','Live container log browser'],
  ['Uptime Kuma','Observability','Service availability checks'],
  ['Paperless-ngx','Data & storage','Document archive and search'],
  ['Paperless-GPT','Data & storage','AI-assisted document workflows'],
  ['Apache Tika','Data & storage','Text and metadata extraction'],
  ['Gotenberg','Data & storage','Document format conversion'],
  ['PostgreSQL','Data & storage','Relational application database'],
  ['MariaDB','Data & storage','Relational application database'],
  ['Valkey','Data & storage','In-memory data and queues'],
  ['pgAdmin','Data & storage','PostgreSQL management'],
  ['phpMyAdmin','Data & storage','MariaDB management'],
  ['Adminer / DBGate','Data & storage','Database query interfaces'],
  ['Home Assistant','Smart home','Locally hosted automation'],
  ['ESPHome','Smart home','Wireless sensor firmware'],
  ['ESP8266 + BME280','Smart home','DIY room temperature nodes'],
  ['Z-Wave JS UI','Smart home','Thermostat and controller integration'],
  ['n8n','Automation','Event-driven workflows'],
  ['ntfy','Automation','Notifications and system alerts']
];
const q = (selector) => document.querySelector(selector);
let activeCategory = 'All';
function renderServices(){
  const grid=q('#servicesGrid');if(!grid)return;
  const term=q('#serviceSearch').value.trim().toLowerCase();
  const visible=services.filter(([name,category,desc])=>(activeCategory==='All'||activeCategory===category)&&`${name} ${category} ${desc}`.toLowerCase().includes(term));
  grid.replaceChildren();
  visible.forEach(([name,category,desc])=>{
    const article=document.createElement('article');article.className='service-card';
    const meta=document.createElement('span');meta.textContent=category.toUpperCase();
    const heading=document.createElement('h4');heading.textContent=name;
    const info=document.createElement('p');info.textContent=desc;
    article.append(meta,heading,info);grid.append(article);
  });
  if(!visible.length){const p=document.createElement('p');p.className='empty-message';p.textContent='Nothing matches that search. Try a different tool or category.';grid.append(p);}
  q('#serviceCount').textContent=visible.length;
}
function initCatalog(){
  if(!q('#servicesGrid'))return;
  const filterArea=q('#categoryFilters');
  ['All',...new Set(services.map(s=>s[1]))].forEach(category=>{
    const b=document.createElement('button');b.type='button';b.textContent=category;
    b.classList.toggle('active',category==='All');
    b.setAttribute('aria-pressed',String(category==='All'));
    b.addEventListener('click',()=>{
      activeCategory=category;
      filterArea.querySelectorAll('button').forEach(x=>{const active=x===b;x.classList.toggle('active',active);x.setAttribute('aria-pressed',String(active));});
      renderServices();
    });
    filterArea.append(b);
  });
  q('#serviceSearch').addEventListener('input',renderServices);renderServices();
}
function initSimulator(){
  const target=q('#tempSliders');if(!target)return;
  const rooms=[{name:'Living room',weight:.2,value:69},{name:'My bedroom',weight:.4,value:71},{name:'Roommate’s bedroom',weight:.4,value:65}];
  rooms.forEach((room,i)=>{
    const wrap=document.createElement('div');wrap.className='room-control';
    const label=document.createElement('label');label.htmlFor=`room-${i}`;
    const left=document.createElement('span');left.textContent=`${room.name} · ${Math.round(room.weight*100)}%`;
    const readout=document.createElement('strong');readout.id=`room-${i}-label`;readout.textContent=`${room.value.toFixed(1)}°F`;
    label.append(left,readout);
    const slider=document.createElement('input');slider.id=`room-${i}`;slider.type='range';slider.min='60';slider.max='78';slider.step='0.5';slider.value=String(room.value);
    slider.addEventListener('input',()=>{room.value=Number(slider.value);readout.textContent=`${room.value.toFixed(1)}°F`;render();});
    wrap.append(label,slider);target.append(wrap);
  });
  function render(){
    const [living,bedroom,friend]=rooms.map(r=>r.value);
    const weighted=rooms.reduce((s,r)=>s+r.value*r.weight,0);
    q('#avgTemp').textContent=`${weighted.toFixed(1)}°F`;
    q('#formulaOutput').textContent=`0.2 × ${living.toFixed(1)} + 0.4 × ${bedroom.toFixed(1)} + 0.4 × ${friend.toFixed(1)}`;
    const outcome=q('#heatState'),setpoint=q('#requestedSetpoint'),explanation=q('#simExplanation');
    let verdict,requested,reason;
    if(bedroom>=72){
      verdict='REDUCE HEAT';requested=68;
      reason='The bedroom reached the 72°F comfort limit. The supervisor requests a lower setpoint, even if the weighted temperature is low.';
    } else if(weighted<68.5){
      verdict='REQUEST HEAT';requested=Math.max(68,Math.min(72,living+2));
      reason='The weighted temperature is below 68.5°F. The controller requests a higher thermostat setpoint, bounded to 68–72°F.';
    } else if(weighted>69.5){
      verdict='REDUCE HEAT';requested=68;
      reason='The weighted temperature is above 69.5°F. The controller requests the lower thermostat setpoint.';
    } else {
      verdict='HOLD SETPOINT';requested=null;
      reason='The weighted temperature is within the 68.5–69.5°F band. No new setpoint is requested in this example.';
    }
    outcome.textContent=verdict;outcome.classList.toggle('heat-request',verdict==='REQUEST HEAT');
    setpoint.textContent=requested===null?'No change':`${requested.toFixed(1)}°F`;
    explanation.textContent=reason;
  }
  render();
}
function initRepoLink(){
  const l=q('#githubSourceLink');if(!l)return;
  const url=(window.LAB_PUBLIC_CONFIG||{}).githubRepoUrl||'';
  try{const parsed=new URL(url);if(parsed.protocol==='https:'&&parsed.hostname==='github.com'&&parsed.pathname.split('/').filter(Boolean).length>=2){l.href=url;l.hidden=false;}}catch{/* Link is not yet configured. */}
}
function initMobileNav(){
  const toggle=q('#menuToggle'),nav=q('#mainNav');if(!toggle||!nav)return;
  toggle.addEventListener('click',()=>{const isOpen=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(isOpen));});
  nav.addEventListener('click',event=>{if(event.target.closest('a')){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');}});
}
document.addEventListener('DOMContentLoaded',()=>{initCatalog();initSimulator();initRepoLink();initMobileNav();});
