const baseUrl = '/api/v1/users';
let currentEditId = null;

const sections = {
  create: el('createSection'),
  edit: el('editSection')
};

const inputs = {
  createName: el('name'),
  createEmail: el('email'),
  editName: el('edit-name'),
  editEmail: el('edit-email')
};

function el(id) { return document.getElementById(id); }

function setError(id, text='') {
    const node = el(id); if (node) node.textContent = text;
}

function clearCreateErrors() {
    ['err-name','err-email','err-global'].forEach(id => setError(id));
}


function clearEditErrors() {
    ['edit-err-name','edit-err-email','edit-err-global'].forEach(id => setError(id));
}

function clearErrors() { clearCreateErrors(); clearEditErrors(); }

function setStatus(text, kind='info') {
  const s = el('status');
  s.textContent = text;
  s.className = `msg ${kind}`;
  s.classList.remove('hidden');
  setTimeout(() => s.classList.add('hidden'), 3500);
}

function showCreateForm() {
  sections.create.classList.remove('hidden');
  sections.edit.classList.add('hidden');
  currentEditId = null;
  clearEditForm();
}

function showEditForm() {
  sections.create.classList.add('hidden');
  sections.edit.classList.remove('hidden');
}

function clearEditForm() {
  inputs.editName.value = '';
  inputs.editEmail.value = '';
  el('editTitle').textContent = 'Edit user';
}

async function fetchUsers() {
  clearErrors();
  try {
    const res = await fetch(baseUrl);
    if (!res.ok) {
      setStatus('Failed to load users: ' + res.status, 'warn');
      return;
    }
    const users = await res.json();
    renderUsers(users);
  } catch (e) {
    setStatus('Network error: ' + e.message, 'warn');
  }
}

function renderUsers(users) {
  const body = el('usersBody');
  body.innerHTML = '';

  if (!users || users.length === 0) {
    const emptyRow = document.createElement('tr');
    emptyRow.className = 'empty-row';
    const cell = document.createElement('td');
    cell.colSpan = 4;
    cell.textContent = 'No users available.';
    emptyRow.appendChild(cell);
    body.appendChild(emptyRow);
    return;
  }

  users.forEach(u => {
    const row = document.createElement('tr');

    const idCell = document.createElement('td');
    idCell.textContent = u.id;

    const nameCell = document.createElement('td');
    nameCell.textContent = u.name;

    const emailCell = document.createElement('td');
    emailCell.textContent = u.email;

    const actionCell = document.createElement('td');
    actionCell.className = 'actions';
    const viewBtn = document.createElement('button');
    viewBtn.textContent = 'View & Edit';
    viewBtn.onclick = () => viewUser(u.id);
    const delBtn = document.createElement('button');
    delBtn.textContent = 'Delete';
    delBtn.onclick = () => deleteUser(u.id);
    actionCell.appendChild(viewBtn);
    actionCell.appendChild(delBtn);

    row.appendChild(idCell);
    row.appendChild(nameCell);
    row.appendChild(emailCell);
    row.appendChild(actionCell);
    body.appendChild(row);
  });
}

async function viewUser(id) {
  clearErrors();
  try {
    const res = await fetch(`${baseUrl}/${id}`);
    if (res.status === 404) {
      setStatus('User not found', 'warn');
      return;
    }
    if (!res.ok) {
      setStatus('Error: ' + res.status, 'warn');
      return;
    }
    const u = await res.json();
    enterEditMode(u);
  } catch (e) {
    setStatus('Network error: ' + e.message, 'warn');
  }
}

function enterEditMode(user) {
  currentEditId = user.id;
  inputs.editName.value = user.name;
  inputs.editEmail.value = user.email;
  el('editTitle').textContent = `Edit user #${user.id}`;
  clearEditErrors();
  showEditForm();
}

async function createUser(name, email) {
  clearCreateErrors();
  try {
    const res = await fetch(baseUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email })
    });

    if (res.status === 201) {
      const created = await res.json();
      setStatus('Created user id ' + created.id, 'info');
      await fetchUsers();
      return created;
    }

    if (res.status === 400) {
      const payload = await res.json().catch(() => null);
      if (payload && payload.fields) {
        for (const [k, v] of Object.entries(payload.fields)) {
          setError(`err-${k}`, v);
        }
      } else {
        setStatus('Validation failed', 'warn');
      }
      return null;
    }

    setStatus('Create failed: ' + res.status, 'warn');
  } catch (e) {
    setStatus('Network error: ' + e.message, 'warn');
  }
}

async function deleteUser(id) {
  clearErrors();
  if (!confirm('Delete user ' + id + '?')) return;
  try {
    const res = await fetch(`${baseUrl}/${id}`, { method: 'DELETE' });
    if (res.status === 204) {
      setStatus('Deleted', 'info');
      if (currentEditId === id) {
        showCreateForm();
      }
      await fetchUsers();
      return;
    }
    if (res.status === 404) {
      setStatus('User not found', 'warn');
      if (currentEditId === id) {
        showCreateForm();
      }
      return;
    }
    setStatus('Delete failed: ' + res.status, 'warn');
  } catch (e) {
    setStatus('Network error: ' + e.message, 'warn');
  }
}

async function updateUser(id, name, email) {
  clearEditErrors();
  try {
    const res = await fetch(`${baseUrl}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email })
    });

    if (res.status === 200) {
      setStatus('User updated', 'info');
      showCreateForm();
      await fetchUsers();
      return;
    }
    if (res.status === 400) {
      const payload = await res.json().catch(() => null);
      if (payload && payload.fields) {
        for (const [k, v] of Object.entries(payload.fields)) {
          setError(`edit-err-${k}`, v);
        }
      } else {
        setStatus('Validation failed', 'warn');
      }
      return;
    }
    if (res.status === 404) {
      setStatus('User not found', 'warn');
      showCreateForm();
      return;
    }
    setStatus('Update failed: ' + res.status, 'warn');
  } catch (e) {
    setStatus('Network error: ' + e.message, 'warn');
  }
}

function onCreateSubmit(e) {
  e.preventDefault();
  const name = inputs.createName.value.trim();
  const email = inputs.createEmail.value.trim();
  createUser(name, email).then(created => {
    if (created) {
      inputs.createName.value = '';
      inputs.createEmail.value = '';
    }
  });
}

function onClear() {
  inputs.createName.value = '';
  inputs.createEmail.value = '';
  clearErrors();
}

function onEditSubmit(e) {
  e.preventDefault();
  if (currentEditId == null) {
    setStatus('No user selected for editing', 'warn');
    return;
  }
  const name = inputs.editName.value.trim();
  const email = inputs.editEmail.value.trim();
  updateUser(currentEditId, name, email);
}

function onCancelEdit() {
  showCreateForm();
  clearErrors();
}

el('createForm').addEventListener('submit', onCreateSubmit);
el('clearBtn').addEventListener('click', onClear);
el('editForm').addEventListener('submit', onEditSubmit);
el('cancelEditBtn').addEventListener('click', onCancelEdit);
el('refreshBtn').addEventListener('click', fetchUsers);

showCreateForm();

// initial load
fetchUsers();
