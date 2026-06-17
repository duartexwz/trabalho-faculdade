(function initTheme() {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
})();
function toggleTheme() {
  const cur = document.documentElement.getAttribute('data-theme');
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  const icon = document.querySelector('.theme-toggle i');
  if (icon) icon.className = next === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}
window.toggleTheme = toggleTheme;
// ============ NAVBAR ============
function renderNavbar(active = '') {
  const user = API.user();
  const isAdmin = user && (user.acesso === 'admin' || user.acesso === 'administrador');
  const cartCount = getCart().length;
  return `
  <nav class="navbar navbar-expand-lg navbar-light bg-white fixed-top">
    <div class="container">
      <a class="navbar-brand" href="index.html">
        <i class="fas fa-graduation-cap me-2"></i>Tecno Brasília
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMain">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navMain">
        <ul class="navbar-nav ms-auto align-items-lg-center">
          <li class="nav-item"><a class="nav-link ${active==='home'?'active':''}" href="index.html">Home</a></li>
          <li class="nav-item"><a class="nav-link ${active==='sobre'?'active':''}" href="sobre.html">Sobre</a></li>
          <li class="nav-item"><a class="nav-link ${active==='cursos'?'active':''}" href="cursos.html">Cursos</a></li>
          <li class="nav-item"><a class="nav-link ${active==='contato'?'active':''}" href="contato.html">Contato</a></li>
          <li class="nav-item position-relative me-3">
            <a class="nav-link" href="matricula.html">
              <i class="fas fa-shopping-cart"></i>
              ${cartCount > 0 ? `<span class="cart-badge">${cartCount}</span>` : ''}
            </a>
          </li>
          ${user ? `
            ${isAdmin ? `<li class="nav-item"><a class="nav-link" href="admin.html">Admin</a></li>` : ''}
            <li class="nav-item"><a class="nav-link" href="#" onclick="logout();return false;">Sair</a></li>
          ` : `
            <li class="nav-item"><a class="nav-link btn btn-primary text-white px-3" href="login.html">Login</a></li>
          `}
          <li class="nav-item ms-2">
            <button class="theme-toggle" onclick="toggleTheme()" title="Alternar tema">
              <i class="fas ${document.documentElement.getAttribute('data-theme')==='dark'?'fa-sun':'fa-moon'}"></i>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>`;
}
function renderFooter() {
  return `
  <footer class="footer mt-5">
    <div class="container">
      <div class="row g-4">
        <div class="col-md-4">
          <h5><i class="fas fa-graduation-cap me-2"></i>Tecno Brasília</h5>
          <p>Formando profissionais de tecnologia em Brasília desde 2010.</p>
          <div class="social">
            <a href="#"><i class="fab fa-facebook"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-linkedin"></i></a>
            <a href="#"><i class="fab fa-youtube"></i></a>
          </div>
        </div>
        <div class="col-md-4">
          <h6>Navegação</h6>
          <ul class="list-unstyled">
            <li><a href="index.html">Home</a></li>
            <li><a href="sobre.html">Sobre</a></li>
            <li><a href="cursos.html">Cursos</a></li>
            <li><a href="contato.html">Contato</a></li>
          </ul>
        </div>
        <div class="col-md-4">
          <h6>Contato</h6>
          <p><i class="fas fa-map-marker-alt me-2"></i>SCS Qd. 02, Brasília-DF</p>
          <p><i class="fas fa-phone me-2"></i>(61) 3000-0000</p>
          <p><i class="fas fa-envelope me-2"></i>contato@tecnobrasilia.com</p>
        </div>
      </div>
      <hr class="my-4" style="border-color:#444">
      <p class="text-center mb-0">&copy; 2026 Escola Tecno Brasília. Todos os direitos reservados.</p>
    </div>
  </footer>`;
}
function mountLayout(active) {
  const nav = document.getElementById('navbar-mount');
  const foot = document.getElementById('footer-mount');
  if (nav) nav.innerHTML = renderNavbar(active);
  if (foot) foot.innerHTML = renderFooter();
}
window.mountLayout = mountLayout;

// 🔧 FIX: antes só chamava API.clearToken() e nunca tocava no carrinho.
// Por isso os itens continuavam no localStorage depois de sair.
// Agora usa API.logout(), que limpa sessão + carrinho ('cart').
function logout() {
  if (typeof API.logout === 'function') {
    API.logout();
  } else {
    API.clearToken();
    localStorage.removeItem('cart');
  }
  window.location.href = 'index.html';
}
window.logout = logout;

// ============ NOTIFICAÇÕES (toast) ============
// Substitui o alert() nativo por um cartão flutuante, no canto superior
// direito da tela, com ícone, cor e fechamento automático.
// Uso: showToast('Matrícula realizada com sucesso!', 'success');
//      showToast('Não foi possível concluir a matrícula.', 'error');
//      showToast('Aguarde, processando...', 'info', { autoClose: false });
(function setupToastContainer() {
  if (document.getElementById('toast-stack')) return;
  const el = document.createElement('div');
  el.id = 'toast-stack';
  el.setAttribute('aria-live', 'polite');
  el.style.cssText = `
    position: fixed; top: 90px; right: 20px; z-index: 2000;
    display: flex; flex-direction: column; gap: 12px;
    max-width: 380px; width: calc(100% - 40px);
  `;
  document.addEventListener('DOMContentLoaded', () => document.body.appendChild(el));
  if (document.body) document.body.appendChild(el);
})();

const TOAST_STYLES = {
  success: { bg: '#e9f7ef', border: '#28a745', color: '#1e7e34', icon: 'fa-circle-check' },
  error:   { bg: '#fdecea', border: '#dc3545', color: '#b02a37', icon: 'fa-circle-exclamation' },
  info:    { bg: '#e8f1fd', border: '#0d6efd', color: '#0a58ca', icon: 'fa-circle-info' },
  warning: { bg: '#fff8e6', border: '#ffc107', color: '#92720c', icon: 'fa-triangle-exclamation' }
};

function showToast(message, type = 'info', opts = {}) {
  const stack = document.getElementById('toast-stack');
  if (!stack) { console.warn('Toast container ausente:', message); return; }

  const style = TOAST_STYLES[type] || TOAST_STYLES.info;
  const autoClose = opts.autoClose !== false;
  const duration = opts.duration || 5000;

  const card = document.createElement('div');
  card.className = 'app-toast';
  card.style.cssText = `
    background: ${style.bg};
    border-left: 4px solid ${style.border};
    color: ${style.color};
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 0.92rem;
    line-height: 1.4;
    opacity: 0;
    transform: translateX(20px);
    transition: opacity .25s ease, transform .25s ease;
  `;
  card.innerHTML = `
    <i class="fas ${style.icon}" style="font-size:1.15rem; margin-top:2px;"></i>
    <div style="flex:1">${message}</div>
    <button type="button" aria-label="Fechar" style="
      background:none;border:none;color:${style.color};opacity:.6;
      cursor:pointer;font-size:1rem;line-height:1;padding:0 0 0 4px;
    ">&times;</button>
  `;

  const removeCard = () => {
    card.style.opacity = '0';
    card.style.transform = 'translateX(20px)';
    setTimeout(() => card.remove(), 200);
  };
  card.querySelector('button').addEventListener('click', removeCard);

  stack.appendChild(card);
  requestAnimationFrame(() => {
    card.style.opacity = '1';
    card.style.transform = 'translateX(0)';
  });

  if (autoClose) setTimeout(removeCard, duration);
  return { close: removeCard };
}
window.showToast = showToast;

// Banner inline (fixo dentro de um container da página, não flutuante).
// Útil para resultados de ações importantes, como "Matrícula concluída",
// que devem ficar visíveis até a pessoa decidir continuar.
// Uso: showInlineMessage('#resultado-matricula', 'Matrícula realizada!', 'success');
function showInlineMessage(containerSelector, message, type = 'info') {
  const container = typeof containerSelector === 'string'
    ? document.querySelector(containerSelector)
    : containerSelector;
  if (!container) { console.warn('Container de mensagem não encontrado:', containerSelector); return; }

  const style = TOAST_STYLES[type] || TOAST_STYLES.info;
  container.innerHTML = `
    <div style="
      background:${style.bg}; border:1px solid ${style.border}33;
      border-left: 4px solid ${style.border}; color:${style.color};
      border-radius: 10px; padding: 18px 20px; display:flex; gap:14px;
      align-items:flex-start;
    ">
      <i class="fas ${style.icon}" style="font-size:1.4rem; margin-top:2px;"></i>
      <div style="flex:1">${message}</div>
    </div>
  `;
  container.classList.remove('d-none');
}
window.showInlineMessage = showInlineMessage;

// ============ CARRINHO ============
function getCart() {
  try { return JSON.parse(localStorage.getItem('cart') || '[]'); } catch { return []; }
}
function saveCart(c) { localStorage.setItem('cart', JSON.stringify(c)); }
function addToCart(curso) {
  const cart = getCart();
  if (cart.find(c => c.id === curso.id)) {
    showToast('Esse curso já está no seu carrinho.', 'info'); return;
  }
  cart.push(curso);
  saveCart(cart);
  showToast(`<strong>${curso.curso}</strong> foi adicionado ao carrinho!`, 'success');
  mountLayout(document.body.dataset.page);
}
function removeFromCart(id) {
  saveCart(getCart().filter(c => c.id !== id));
  mountLayout(document.body.dataset.page);
}
window.getCart = getCart; window.addToCart = addToCart; window.removeFromCart = removeFromCart;
// ============ MÁSCARAS ============
function maskCPF(v) {
  return v.replace(/\D/g,'').slice(0,11)
    .replace(/(\d{3})(\d)/,'$1.$2')
    .replace(/(\d{3})(\d)/,'$1.$2')
    .replace(/(\d{3})(\d{1,2})$/,'$1-$2');
}
function maskTel(v) {
  return v.replace(/\D/g,'').slice(0,11)
    .replace(/^(\d{2})(\d)/,'($1) $2')
    .replace(/(\d{5})(\d)/,'$1-$2');
}
function maskCEP(v) {
  return v.replace(/\D/g,'').slice(0,8).replace(/(\d{5})(\d)/,'$1-$2');
}
function applyMasks(root = document) {
  root.querySelectorAll('[data-mask="cpf"]').forEach(i => i.addEventListener('input', e => e.target.value = maskCPF(e.target.value)));
  root.querySelectorAll('[data-mask="tel"]').forEach(i => i.addEventListener('input', e => e.target.value = maskTel(e.target.value)));
  root.querySelectorAll('[data-mask="cep"]').forEach(i => i.addEventListener('input', e => e.target.value = maskCEP(e.target.value)));
}
window.applyMasks = applyMasks;
// ============ VALIDAÇÃO ============
function setError(input, msg) {
  input.classList.add('is-invalid');
  let next = input.nextElementSibling;
  if (!next || !next.classList.contains('is-invalid-msg')) {
    next = document.createElement('div');
    next.className = 'is-invalid-msg';
    input.after(next);
  }
  next.textContent = msg;
  next.style.display = 'block';
}
function clearError(input) {
  input.classList.remove('is-invalid');
  const next = input.nextElementSibling;
  if (next && next.classList.contains('is-invalid-msg')) next.style.display = 'none';
}
function validateRequired(form) {
  let ok = true;
  form.querySelectorAll('[required]').forEach(i => {
    clearError(i);
    if (!i.value.trim()) { setError(i, 'Campo obrigatório'); ok = false; }
    else if (i.type === 'email' && !/^\S+@\S+\.\S+$/.test(i.value)) { setError(i, 'E-mail inválido'); ok = false; }
    else if (i.dataset.mask === 'cpf' && i.value.replace(/\D/g,'').length !== 11) { setError(i, 'CPF inválido'); ok = false; }
  });
  return ok;
}
window.validateRequired = validateRequired;
window.setError = setError; window.clearError = clearError;
// Format BRL
function brl(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}
window.brl = brl;