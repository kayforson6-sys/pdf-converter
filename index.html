const input = document.getElementById('pdf_files');
const fileList = document.getElementById('fileList');
const dropzone = document.getElementById('dropzone');
const form = document.getElementById('uploadForm');
const btn = document.getElementById('convertBtn');
const selectedCount = document.getElementById('selectedCount');
const maxFiles = btn ? parseInt(btn.dataset.maxFiles || '60', 10) : 60;

// Keep selected files when the user clicks again or drops more files.
// This makes the app feel like true multi-file upload, not a one-time file picker.
let selectedFiles = [];

function syncInputFiles(){
  if(!input) return;
  const dt = new DataTransfer();
  selectedFiles.forEach(file => dt.items.add(file));
  input.files = dt.files;
}

function addFiles(fileListObject){
  const incoming = Array.from(fileListObject || []).filter(file => file.name.toLowerCase().endsWith('.pdf'));
  let limitReached = false;
  incoming.forEach(file => {
    if(selectedFiles.length >= maxFiles){ limitReached = true; return; }
    const key = `${file.name}-${file.size}-${file.lastModified}`;
    const exists = selectedFiles.some(existing => `${existing.name}-${existing.size}-${existing.lastModified}` === key);
    if(!exists) selectedFiles.push(file);
  });
  syncInputFiles();
  renderFiles();
  if(limitReached){ alert(`Maximum ${maxFiles} PDF files allowed per conversion.`); }
}

function removeFile(index){
  selectedFiles.splice(index, 1);
  syncInputFiles();
  renderFiles();
}

function renderFiles(){
  if(!fileList) return;
  fileList.innerHTML = '';
  if(selectedCount) selectedCount.textContent = selectedFiles.length;
  if(btn) btn.disabled = selectedFiles.length === 0 || selectedFiles.length > maxFiles;
  if(selectedFiles.length === 0){
    fileList.innerHTML = '<div class="text-muted small">No PDF selected yet.</div>';
    return;
  }
  const summary = document.createElement('div');
  summary.className = selectedFiles.length >= maxFiles ? 'mb-2 text-warning small' : 'mb-2 text-info small';
  summary.textContent = `${selectedFiles.length} / ${maxFiles} PDF file(s) selected`;
  fileList.appendChild(summary);
  selectedFiles.forEach((file, index) => {
    const div = document.createElement('div');
    div.className = 'file-pill';
    div.innerHTML = `<span>${file.name}</span><span>${(file.size/1024).toFixed(1)} KB <button type="button" class="btn btn-sm btn-outline-light ms-2" onclick="removeFile(${index})">Remove</button></span>`;
    fileList.appendChild(div);
  });
}

if(input){
  input.addEventListener('change', e => addFiles(e.target.files));
}

if(dropzone){
  ['dragenter','dragover'].forEach(evt => dropzone.addEventListener(evt, e => {e.preventDefault(); dropzone.classList.add('dragover')}));
  ['dragleave','drop'].forEach(evt => dropzone.addEventListener(evt, e => {e.preventDefault(); dropzone.classList.remove('dragover')}));
  dropzone.addEventListener('drop', e => addFiles(e.dataTransfer.files));
}

if(form && btn){
  form.addEventListener('submit', e => {
    syncInputFiles();
    if(!input || input.files.length === 0){
      e.preventDefault();
      alert('Please select at least one PDF file.');
      return;
    }
    if(input.files.length > maxFiles){
      e.preventDefault();
      alert(`Maximum ${maxFiles} PDF files allowed per conversion.`);
      return;
    }
    btn.disabled = true;
    btn.innerText = `Processing ${input.files.length} PDF(s)...`;
  });
}

renderFiles();
