<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Проект — YOMKO</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f8f6f3;min-height:100vh}
nav{background:#fff;padding:0 24px;height:60px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 8px rgba(0,0,0,0.06);position:sticky;top:0;z-index:100}
.nav-logo{font-size:18px;font-weight:800;color:#2c2c2c;letter-spacing:3px;text-decoration:none}
.nav-logo span{font-size:10px;color:#c4a35a;letter-spacing:2px;display:block;font-weight:400;text-transform:uppercase}
.nav-right{display:flex;align-items:center;gap:10px}
.btn{padding:8px 16px;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;border:none;text-decoration:none;display:inline-flex;align-items:center;gap:5px;transition:all .2s}
.btn-gold{background:#c4a35a;color:#fff}.btn-gold:hover{background:#b8923d}
.btn-outline{background:#fff;color:#555;border:1.5px solid #e5e7eb}.btn-outline:hover{border-color:#c4a35a;color:#c4a35a}
.btn-danger{background:#fee2e2;color:#dc2626;border:none}.btn-danger:hover{background:#fecaca}
.btn-sm{padding:5px 12px;font-size:12px}
.layout{display:grid;grid-template-columns:280px 1fr;min-height:calc(100vh - 60px)}
.sidebar{background:#fff;border-right:1px solid #f0ede8;padding:20px;overflow-y:auto}
.main{padding:24px;overflow-y:auto}
.proj-title{font-size:16px;font-weight:700;color:#2c2c2c;margin-bottom:4px}
.proj-client{font-size:13px;color:#888;margin-bottom:16px}
.progress-wrap{margin-bottom:20px}
.progress-bar{background:#f3f4f6;border-radius:10px;height:8px;margin-bottom:6px}
.progress-fill{background:linear-gradient(90deg,#c4a35a,#e8c97a);height:8px;border-radius:10px;transition:width .5s}
.progress-label{font-size:12px;color:#aaa;display:flex;justify-content:space-between}
.section-label{font-size:10px;font-weight:700;color:#c4a35a;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;margin-top:20px}
.stage-item{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;margin-bottom:4px;transition:background .2s}
.stage-item:hover{background:#faf9f7}
.stage-item input[type=checkbox]{accent-color:#c4a35a;width:16px;height:16px;cursor:pointer}
.stage-item label{font-size:13px;color:#555;cursor:pointer;flex:1}
.stage-item.done label{color:#aaa;text-decoration:line-through}
.sidebar-btn{width:100%;margin-bottom:6px;justify-content:flex-start;text-align:left}
.tabs{display:flex;gap:4px;margin-bottom:20px;flex-wrap:wrap}
.tab{padding:8px 16px;border-radius:8px;font-size:13px;font-weight:500;cursor:pointer;border:none;background:#f3f4f6;color:#666;transition:all .2s}
.tab.active{background:#c4a35a;color:#fff}
.tab-content{display:none}.tab-content.active{display:block}
.card{background:#fff;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.05);margin-bottom:16px}
.upload-area{border:2px dashed #e5e7eb;border-radius:10px;padding:24px;text-align:center;cursor:pointer;transition:all .2s;margin-bottom:16px}
.upload-area:hover{border-color:#c4a35a;background:#fffdf7}
.upload-area input{display:none}
.upload-icon{font-size:28px;margin-bottom:8px}
.upload-text{font-size:13px;color:#888}
.file-list{display:flex;flex-direction:column;gap:8px}
.file-item{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#fafafa;border-radius:8px;border:1px solid #f0f0f0}
.file-item-left{display:flex;align-items:center;gap:10px}
.file-icon{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px}
.icon-img{background:#dbeafe}.icon-pdf{background:#fee2e2}.icon-doc{background:#e0e7ff}.icon-file{background:#f3f4f6}
.file-name{font-size:13px;color:#2c2c2c;font-weight:500}
.file-size{font-size:11px;color:#aaa}
.rooms-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.room-card{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.05)}
.room-header{padding:12px 16px;background:#faf9f7;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #f0ede8}
.room-name{font-size:14px;font-weight:600;color:#2c2c2c}
.room-images{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:8px}
.room-images img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:6px;cursor:pointer;transition:opacity .2s}
.room-images img:hover{opacity:.85}
.room-upload{padding:8px 12px;border-top:1px solid #f0ede8}
.room-upload input{display:none}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:10px 12px;background:#faf9f7;color:#888;font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.5px;border-bottom:2px solid #f0ede8}
td{padding:10px 12px;border-bottom:1px solid #f9f9f9;color:#2c2c2c}
tr:hover td{background:#fdfcfb}
.total-row td{font-weight:700;background:#faf9f7;color:#2c2c2c}
.status-badge{padding:2px 8px;border-radius:10px;font-size:11px;font-weight:500}
.s-ordered{background:#d1fae5;color:#065f46}
.s-received{background:#dbeafe;color:#1e40af}
.s-installed{background:#e0e7ff;color:#3730a3}
.s-pending{background:#f3f4f6;color:#6b7280}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:1000;align-items:center;justify-content:center}
.modal.open{display:flex}
.modal-box{background:#fff;border-radius:16px;padding:28px;width:90%;max-width:520px;max-height:90vh;overflow-y:auto}
.modal-title{font-size:18px;font-weight:700;color:#2c2c2c;margin-bottom:20px}
.fg{margin-bottom:16px}
.fg label{display:block;font-size:13px;color:#555;margin-bottom:5px;font-weight:500}
.fg input,.fg textarea,.fg select{width:100%;padding:10px 13px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;outline:none;font-family:inherit}
.fg input:focus,.fg textarea:focus,.fg select:focus{border-color:#c4a35a}
.fg-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.link-box{background:#f8f6f3;border:1px solid #e5e7eb;border-radius:8px;padding:12px 16px;font-size:13px;color:#555;word-break:break-all;margin-bottom:16px}
.lightbox{display:none;position:fixed;inset:0;background:rgba(0,0,0,.9);z-index:2000;align-items:center;justify-content:center}
.lightbox.open{display:flex}
.lightbox img{max-width:90vw;max-height:85vh;border-radius:10px}
.viz-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;margin-top:16px}
.viz-item{background:#f9f7f4;border-radius:12px;overflow:hidden;text-align:center;padding-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,0.05)}
.viz-item img{width:100%;height:160px;object-fit:cover;cursor:pointer;display:block}
.viz-name{font-size:12px;color:#aaa;padding:8px 8px 4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
</style>
</head>
<body>

<nav>
  <a href="#" class="nav-logo">YOMKO<span>СТУДИЯ ДИЗАЙНА ИНТЕРЬЕРОВ</span></a>
  <div class="nav-right">
    <button onclick="openShareModal()" class="btn btn-outline">🔗 Поделиться</button>
    <button onclick="openEditModal()" class="btn btn-gold">✏️ Редактировать</button>
  </div>
</nav>

<div class="layout">

  <!-- SIDEBAR -->
  <div class="sidebar">
    <div class="proj-title" id="sideTitle">Мой проект</div>
    <div class="proj-client" id="sideClient">Клиент</div>

    <div class="progress-wrap">
      <div class="progress-bar">
        <div class="progress-fill" id="progressFill" style="width:0%"></div>
      </div>
      <div class="progress-label">
        <span>Прогресс</span>
        <span id="progressText">0%</span>
      </div>
    </div>

    <div class="section-label">Документы</div>
    <button onclick="switchTab('files',event)" class="btn btn-outline btn-sm sidebar-btn">📁 Договор</button>
    <button onclick="switchTab('viz',event)" class="btn btn-outline btn-sm sidebar-btn">🎨 Визуализация</button>
    <button onclick="switchTab('rooms',event)" class="btn btn-outline btn-sm sidebar-btn">📐 Планировочные решения</button>
    <button onclick="switchTab('materials',event)" class="btn btn-outline btn-sm sidebar-btn">📦 Материалы</button>
    <button onclick="switchTab('notes',event)" class="btn btn-outline btn-sm sidebar-btn">📝 Заметки</button>

    <div class="section-label">Этапы проекта</div>
    <div id="stagesList"></div>
    <button onclick="openStageModal()" class="btn btn-outline btn-sm" style="width:100%;margin-top:10px">+ Добавить этап</button>
  </div>

  <!-- MAIN -->
  <div class="main">
    <div class="tabs">
      <button class="tab active" onclick="switchTab('files',event)">📁 Договор</button>
      <button class="tab" onclick="switchTab('viz',event)">🎨 Визуализация</button>
      <button class="tab" onclick="switchTab('rooms',event)">📐 Планировка</button>
      <button class="tab" onclick="switchTab('materials',event)">📦 Материалы</button>
      <button class="tab" onclick="switchTab('notes',event)">📝 Заметки</button>
    </div>

    <!-- ДОГОВОР / ФАЙЛЫ -->
    <div id="tab-files" class="tab-content active">
      <div class="card">
        <div class="upload-area" onclick="document.getElementById('fileInput').click()">
          <input type="file" id="fileInput" multiple onchange="handleFiles(this.files)">
          <div class="upload-icon">📎</div>
          <div class="upload-text">Нажмите чтобы загрузить файлы<br><small>Любые форматы</small></div>
        </div>
        <div class="file-list" id="fileList"></div>
      </div>
    </div>

    <!-- ВИЗУАЛИЗАЦИЯ -->
    <div id="tab-viz" class="tab-content">
      <div class="card">
        <div class="upload-area" onclick="document.getElementById('vizInput').click()">
          <input type="file" id="vizInput" accept="image/*" multiple onchange="handleVizFiles(this.files)">
          <div class="upload-icon">🎨</div>
          <div class="upload-text">Нажмите чтобы загрузить изображения<br><small>JPG, PNG, WEBP</small></div>
        </div>
        <div class="viz-grid" id="vizGrid"></div>
      </div>
    </div>

    <!-- ПЛАНИРОВОЧНЫЕ РЕШЕНИЯ -->
    <div id="tab-rooms" class="tab-content">
      <div class="card">
        <div class="upload-area" onclick="document.getElementById('planInput').click()">
          <input type="file" id="planInput" accept="image/*,.pdf" multiple onchange="handlePlanFiles(this.files)">
          <div class="upload-icon">📐</div>
          <div class="upload-text">Нажмите чтобы загрузить планировки<br><small>JPG, PNG, PDF</small></div>
        </div>
        <div class="viz-grid" id="planGrid"></div>
      </div>
      <div style="display:flex;justify-content:flex-end;margin-bottom:16px">
        <button onclick="openRoomModal()" class="btn btn-gold">+ Добавить помещение</button>
      </div>
      <div class="rooms-grid" id="roomsGrid"></div>
    </div>

    <!-- МАТЕРИАЛЫ -->
    <div id="tab-materials" class="tab-content">
      <div style="display:flex;justify-content:flex-end;margin-bottom:16px">
        <button onclick="openMaterialModal()" class="btn btn-gold">+ Добавить материал</button>
      </div>
      <div class="card">
        <table>
          <thead>
            <tr>
              <th>Наименование</th>
              <th>Помещение</th>
              <th>Кол-во</th>
              <th>Цена</th>
              <th>Сумма</th>
              <th>Статус</th>
              <th></th>
            </tr>
          </thead>
          <tbody id="materialsBody"></tbody>
          <tfoot>
            <tr class="total-row">
              <td colspan="4">Итого</td>
              <td id="totalSum">0 ₽</td>
              <td colspan="2"></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- ЗАМЕТКИ -->
    <div id="tab-notes" class="tab-content">
      <div class="card">
        <div class="fg">
          <label>Заметки по проекту</label>
          <textarea id="notesArea" rows="12" placeholder="Введите заметки..." style="resize:vertical" oninput="saveNotes()"></textarea>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- МОДАЛКА: Редактировать -->
<div class="modal" id="editModal">
  <div class="modal-box">
    <div class="modal-title">✏️ Редактировать проект</div>
    <div class="fg"><label>Название</label><input id="editTitle" type="text"></div>
    <div class="fg"><label>Клиент</label><input id="editClient" type="text"></div>
    <div class="fg"><label>Адрес</label><input id="editAddress" type="text"></div>
    <div class="fg-row">
      <div class="fg"><label>Площадь (м²)</label><input id="editArea" type="number"></div>
      <div class="fg"><label>Бюджет (₽)</label><input id="editBudget" type="number"></div>
    </div>
    <div class="fg"><label>Описание</label><textarea id="editDesc" rows="3"></textarea></div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="closeModal('editModal')" class="btn btn-outline">Отмена</button>
      <button onclick="saveEdit()" class="btn btn-gold">Сохранить</button>
    </div>
  </div>
</div>

<!-- МОДАЛКА: Этап -->
<div class="modal" id="stageModal">
  <div class="modal-box">
    <div class="modal-title">➕ Новый этап</div>
    <div class="fg"><label>Название этапа</label><input id="stageName" type="text" placeholder="Например: Согласование планировки"></div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="closeModal('stageModal')" class="btn btn-outline">Отмена</button>
      <button onclick="addStage()" class="btn btn-gold">Добавить</button>
    </div>
  </div>
</div>

<!-- МОДАЛКА: Помещение -->
<div class="modal" id="roomModal">
  <div class="modal-box">
    <div class="modal-title">🛋 Новое помещение</div>
    <div class="fg"><label>Название</label><input id="roomName" type="text" placeholder="Например: Гостиная"></div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="closeModal('roomModal')" class="btn btn-outline">Отмена</button>
      <button onclick="addRoom()" class="btn btn-gold">Добавить</button>
    </div>
  </div>
</div>

<!-- МОДАЛКА: Материал -->
<div class="modal" id="materialModal">
  <div class="modal-box">
    <div class="modal-title">📦 Новый материал</div>
    <div class="fg"><label>Наименование</label><input id="matName" type="text" placeholder="Например: Паркет дуб"></div>
    <div class="fg"><label>Помещение</label><select id="matRoom"><option value="">— выберите —</option></select></div>
    <div class="fg-row">
      <div class="fg"><label>Количество</label><input id="matQty" type="number" min="1" value="1"></div>
      <div class="fg"><label>Цена за ед. (₽)</label><input id="matPrice" type="number" min="0" value="0"></div>
    </div>
    <div class="fg">
      <label>Статус</label>
      <select id="matStatus">
        <option value="pending">Ожидает</option>
        <option value="ordered">Заказан</option>
        <option value="received">Получен</option>
        <option value="installed">Установлен</option>
      </select>
    </div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="closeModal('materialModal')" class="btn btn-outline">Отмена</button>
      <button onclick="addMaterial()" class="btn btn-gold">Добавить</button>
    </div>
  </div>
</div>

<!-- МОДАЛКА: Поделиться -->
<div class="modal" id="shareModal">
  <div class="modal-box">
    <div class="modal-title">🔗 Ссылка для клиента</div>
    <div class="link-box" id="shareLink"></div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="closeModal('shareModal')" class="btn btn-outline">Закрыть</button>
      <button onclick="copyLink()" class="btn btn-gold">📋 Копировать</button>
    </div>
  </div>
</div>

<!-- ЛАЙТБОКС -->
<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <img id="lightboxImg" src="" alt="">
</div>

<script>
const projectId = 'demo';

let project = JSON.parse(localStorage.getItem('project_'+projectId) || 'null') || {
  title: 'Мой проект',
  client_name: 'Клиент',
  address: '',
  area: '',
  budget: '',
  description: ''
};

let stages    = JSON.parse(localStorage.getItem('stages_'+projectId)    || '[]');
let files     = JSON.parse(localStorage.getItem('files_'+projectId)     || '[]');
let rooms     = JSON.parse(localStorage.getItem('rooms_'+projectId)     || '[]');
let materials = JSON.parse(localStorage.getItem('materials_'+projectId) || '[]');
let vizImages = JSON.parse(localStorage.getItem('viz_'+projectId)       || '[]');
let planImages = JSON.parse(localStorage.getItem('plan_'+projectId)     || '[]');

function save(key, val){
  localStorage.setItem(key+'_'+projectId, JSON.stringify(val));
}

// ─── ТАБЫ ───────────────────────────────────────────
function switchTab(name, e){
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  if(e && e.target) e.target.classList.add('active');
}

// ─── МОДАЛКИ ────────────────────────────────────────
function openModal(id)  { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }
document.querySelectorAll('.modal').forEach(m => {
  m.addEventListener('click', e => { if(e.target === m) m.classList.remove('open'); });
});

// ─── РЕДАКТИРОВАНИЕ ─────────────────────────────────
function openEditModal(){
  document.getElementById('editTitle').value   = project.title;
  document.getElementById('editClient').value  = project.client_name;
  document.getElementById('editAddress').value = project.address;
  document.getElementById('editArea').value    = project.area;
  document.getElementById('editBudget').value  = project.budget;
  document.getElementById('editDesc').value    = project.description;
  openModal('editModal');
}
function saveEdit(){
  project.title       = document.getElementById('editTitle').value;
  project.client_name = document.getElementById('editClient').value;
  project.address     = document.getElementById('editAddress').value;
  project.area        = document.getElementById('editArea').value;
  project.budget      = document.getElementById('editBudget').value;
  project.description = document.getElementById('editDesc').value;
  document.getElementById('sideTitle').textContent  = project.title;
  document.getElementById('sideClient').textContent = project.client_name;
  save('project', project);
  closeModal('editModal');
}

// ─── ЭТАПЫ ──────────────────────────────────────────
function renderStages(){
  const list = document.getElementById('stagesList');
  list.innerHTML = '';
  stages.forEach((s,i) => {
    const div = document.createElement('div');
    div.className = 'stage-item' + (s.done ? ' done' : '');
    div.innerHTML = `
      <input type="checkbox" id="s${i}" ${s.done?'checked':''} onchange="toggleStage(${i})">
      <label for="s${i}">${s.name}</label>
      <button onclick="deleteStage(${i})" class="btn btn-danger btn-sm">✕</button>`;
    list.appendChild(div);
  });
  updateProgress();
}
function toggleStage(i){ stages[i].done=!stages[i].done; save('stages',stages); renderStages(); }
function deleteStage(i){ stages.splice(i,1); save('stages',stages); renderStages(); }
function openStageModal(){ document.getElementById('stageName').value=''; openModal('stageModal'); }
function addStage(){
  const name = document.getElementById('stageName').value.trim();
  if(!name) return;
  stages.push({name, done:false});
  save('stages',stages);
  renderStages();
  closeModal('stageModal');
}
function updateProgress(){
  const total = stages.length;
  const done  = stages.filter(s=>s.done).length;
  const pct   = total ? Math.round(done/total*100) : 0;
  document.getElementById('progressFill').style.width = pct+'%';
  document.getElementById('progressText').textContent = pct+'%';
}

// ─── ФАЙЛЫ ──────────────────────────────────────────
function handleFiles(fileList){
  Array.from(fileList).forEach(f => {
    const reader = new FileReader();
    reader.onload = e => {
      files.push({name:f.name, size:f.size, data:e.target.result, type:f.type});
      save('files',files);
      renderFiles();
    };
    reader.readAsDataURL(f);
  });
}
function renderFiles(){
  const list = document.getElementById('fileList');
  list.innerHTML = '';
  files.forEach((f,i) => {
    const ext = f.name.split('.').pop().toLowerCase();
    const icon      = ext==='pdf'?'📄':ext==='doc'||ext==='docx'?'📝':f.type.startsWith('image')?'🖼':'📎';
    const iconClass = ext==='pdf'?'icon-pdf':ext==='doc'||ext==='docx'?'icon-doc':f.type.startsWith('image')?'icon-img':'icon-file';
    const size = f.size>1024*1024 ? (f.size/1024/1024).toFixed(1)+' МБ' : (f.size/1024).toFixed(0)+' КБ';
    const div = document.createElement('div');
    div.className = 'file-item';
    div.innerHTML = `
      <div class="file-item-left">
        <div class="file-icon ${iconClass}">${icon}</div>
        <div><div class="file-name">${f.name}</div><div class="file-size">${size}</div></div>
      </div>
      <div style="display:flex;gap:8px">
        <a href="${f.data}" download="${f.name}" class="btn btn-outline btn-sm">⬇</a>
        <button onclick="deleteFile(${i})" class="btn btn-danger btn-sm">✕</button>
      </div>`;
    list.appendChild(div);
  });
}
function deleteFile(i){ files.splice(i,1); save('files',files); renderFiles(); }

// ─── ВИЗУАЛИЗАЦИЯ ───────────────────────────────────
function handleVizFiles(fileList){
  Array.from(fileList).forEach(f => {
    const reader = new FileReader();
    reader.onload = e => {
      vizImages.push({name:f.name, data:e.target.result});
      save('viz', vizImages);
      renderViz();
    };
    reader.readAsDataURL(f);
  });
}
function renderViz(){
  const grid = document.getElementById('vizGrid');
  grid.innerHTML = '';
  vizImages.forEach((img,i) => {
    const div = document.createElement('div');
    div.className = 'viz-item';
    div.innerHTML = `
      <img src="${img.data}" onclick="openLightbox('${img.data}')" alt="${img.name}">
      <div class="viz-name">${img.name}</div>
      <button onclick="deleteViz(${i})" class="btn btn-danger btn-sm" style="margin:6px 8px 0">✕ Удалить</button>`;
    grid.appendChild(div);
  });
}
function deleteViz(i){ vizImages.splice(i,1); save('viz',vizImages); renderViz(); }

// ─── ПЛАНИРОВКИ ─────────────────────────────────────
function handlePlanFiles(fileList){
  Array.from(fileList).forEach(f => {
    const reader = new FileReader();
    reader.onload = e => {
      planImages.push({name:f.name, data:e.target.result, type:f.type});
      save('plan', planImages);
      renderPlan();
    };
    reader.readAsDataURL(f);
  });
}
function renderPlan(){
  const grid = document.getElementById('planGrid');
  grid.innerHTML = '';
  planImages.forEach((img,i) => {
    const div = document.createElement('div');
    div.className = 'viz-item';
    if(img.type === 'application/pdf'){
      div.innerHTML = `
        <div style="height:160px;display:flex;align-items:center;justify-content:center;background:#fee2e2;font-size:40px">📄</div>
        <div class="viz-name">${img.name}</div>
        <div style="display:flex;gap:6px;margin:6px 8px 0">
          <a href="${img.data}" download="${img.name}" class="btn btn-outline btn-sm" style="flex:1">⬇ Скачать</a>
          <button onclick="deletePlan(${i})" class="btn btn-danger btn-sm">✕</button>
        </div>`;
    } else {
      div.innerHTML = `
        <img src="${img.data}" onclick="openLightbox('${img.data}')" alt="${img.name}">
        <div class="viz-name">${img.name}</div>
        <button onclick="deletePlan(${i})" class="btn btn-danger btn-sm" style="margin:6px 8px 0">✕ Удалить</button>`;
    }
    grid.appendChild(div);
  });
}
function deletePlan(i){ planImages.splice(i,1); save('plan',planImages); renderPlan(); }

// ─── ПОМЕЩЕНИЯ ──────────────────────────────────────
function openRoomModal(){ document.getElementById('roomName').value=''; openModal('roomModal'); }
function addRoom(){
  const name = document.getElementById('roomName').value.trim();
  if(!name) return;
  rooms.push({name, images:[]});
  save('rooms',rooms);
  renderRooms();
  updateMatRooms();
  closeModal('roomModal');
}
function deleteRoom(i){ rooms.splice(i,1); save('rooms',rooms); renderRooms(); updateMatRooms(); }
function renderRooms(){
  const grid = document.getElementById('roomsGrid');
  grid.innerHTML = '';
  rooms.forEach((r,i) => {
    const div = document.createElement('div');
    div.className = 'room-card';
    const imgs = (r.images||[]).map((src,j) =>
      `<img src="${src}" onclick="openLightbox('${src}')" alt="">`
    ).join('');
    div.innerHTML = `
      <div class="room-header">
        <span class="room-name">${r.name}</span>
        <button onclick="deleteRoom(${i})" class="btn btn-danger btn-sm">✕</button>
      </div>
      <div class="room-images">${imgs}</div>
      <div class="room-upload">
        <label class="btn btn-outline btn-sm" style="width:100%;justify-content:center;cursor:pointer">
          📷 Добавить фото
          <input type="file" accept="image/*" multiple onchange="addRoomImage(${i},this.files)">
        </label>
      </div>`;
    grid.appendChild(div);
  });
}
function addRoomImage(i, fileList){
  Array.from(fileList).forEach(f => {
    const reader = new FileReader();
    reader.onload = e => {
      rooms[i].images = rooms[i].images || [];
      rooms[i].images.push(e.target.result);
      save('rooms',rooms);
      renderRooms();
    };
    reader.readAsDataURL(f);
  });
}

// ─── МАТЕРИАЛЫ ──────────────────────────────────────
const statusLabels  = {pending:'Ожидает',ordered:'Заказан',received:'Получен',installed:'Установлен'};
const statusClasses = {pending:'s-pending',ordered:'s-ordered',received:'s-received',installed:'s-installed'};

function updateMatRooms(){
  const sel = document.getElementById('matRoom');
  sel.innerHTML = '<option value="">— выберите —</option>';
  rooms.forEach(r => {
    const opt = document.createElement('option');
    opt.value = r.name;
    opt.textContent = r.name;
    sel.appendChild(opt);
  });
}
function renderMaterials(){
  const tbody = document.getElementById('materialsBody');
  tbody.innerHTML = '';
  let total = 0;
  materials.forEach((m,i) => {
    const sum = m.qty * m.price;
    total += sum;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${m.name}</td>
      <td>${m.room||'—'}</td>
      <td>${m.qty}</td>
      <td>${Number(m.price).toLocaleString()} ₽</td>
      <td>${Number(sum).toLocaleString()} ₽</td>
      <td><span class="status-badge ${statusClasses[m.status]}">${statusLabels[m.status]}</span></td>
      <td><button onclick="deleteMaterial(${i})" class="btn btn-danger btn-sm">✕</button></td>`;
    tbody.appendChild(tr);
  });
  document.getElementById('totalSum').textContent = Number(total).toLocaleString()+' ₽';
}
function openMaterialModal(){ updateMatRooms(); openModal('materialModal'); }
function addMaterial(){
  const name = document.getElementById('matName').value.trim();
  if(!name) return;
  materials.push({
    name,
    room:   document.getElementById('matRoom').value,
    qty:    parseInt(document.getElementById('matQty').value)||1,
    price:  parseFloat(document.getElementById('matPrice').value)||0,
    status: document.getElementById('matStatus').value
  });
  save('materials',materials);
  renderMaterials();
  closeModal('materialModal');
}
function deleteMaterial(i){ materials.splice(i,1); save('materials',materials); renderMaterials(); }

// ─── ЗАМЕТКИ ────────────────────────────────────────
function saveNotes(){
  localStorage.setItem('notes_'+projectId, document.getElementById('notesArea').value);
}
function loadNotes(){
  document.getElementById('notesArea').value = localStorage.getItem('notes_'+projectId)||'';
}

// ─── ПОДЕЛИТЬСЯ ─────────────────────────────────────
function openShareModal(){
  document.getElementById('shareLink').textContent = window.location.href;
  openModal('shareModal');
}
function copyLink(){
  navigator.clipboard.writeText(window.location.href);
  alert('Ссылка скопирована!');
}

// ─── ЛАЙТБОКС ───────────────────────────────────────
function openLightbox(src){
  document.getElementById('lightboxImg').src = src;
  document.getElementById('lightbox').classList.add('open');
}
function closeLightbox(){
  document.getElementById('lightbox').classList.remove('open');
}

// ─── ИНИЦИАЛИЗАЦИЯ ──────────────────────────────────
document.getElementById('sideTitle').textContent  = project.title;
document.getElementById('sideClient').textContent = project.client_name;
renderStages();
renderFiles();
renderViz();
renderPlan();
renderRooms();
renderMaterials();
loadNotes();
</script>

</body>
</html>
