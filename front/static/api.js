const API_BASE_URL = 'https://tecno-brasilia.fly.dev';

// =============================================
const API = {
  base: API_BASE_URL,

  // ====== GERENCIAMENTO DE SESSÃO ======
  token() { return localStorage.getItem('token'); },
  setToken(t) { localStorage.setItem('token', t); },
  user() { try { return JSON.parse(localStorage.getItem('user') || 'null'); } catch { return null; } },
  setUser(u) { localStorage.setItem('user', JSON.stringify(u)); },

  // Limpa apenas os dados de SESSÃO (token + usuário). Não toca no carrinho.
  clearToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  // ====== LOGOUT COMPLETO (use no botão "Sair") ======
  // Limpa a sessão e também o carrinho salvo no localStorage (chave 'cart',
  // confirmada no main.js). Sem isso, o carrinho continua "solto" no
  // navegador depois de sair, podendo até ser visto por outra pessoa que
  // use o mesmo computador.
  logout() {
    this.clearToken();
    localStorage.removeItem('cart');
  },

  // Decodifica o payload de um JWT (sem validar assinatura — só para
  // extrair claims como username/acesso/id para uso na UI).
  _decodeJWT(token) {
    try {
      const payload = token.split('.')[1];
      const json = decodeURIComponent(
        atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
          .split('')
          .map(c => '%' + c.charCodeAt(0).toString(16).padStart(2, '0'))
          .join('')
      );
      return JSON.parse(json);
    } catch {
      return null;
    }
  },

  // ====== AUXILIAR INTERNO (QUERY STRINGS) ======
  _buildPath(endpoint, params = {}) {
    const filtrados = Object.entries(params).filter(([_, v]) => v !== '' && v != null && v !== 'undefined');
    if (filtrados.length === 0) return endpoint;
    const qs = new URLSearchParams(filtrados);
    return `${endpoint}?${qs.toString()}`;
  },

  // ====== REQUISIÇÃO CENTRALIZADA ======
  async request(path, options = {}) {
    // 1. Clona e isola as configurações recebidas para não haver colisões de propriedades
    const fetchOptions = { ...options };

    // 2. Garante que herde os headers informados ou inicialize vazio
    fetchOptions.headers = { ...options.headers };

    // 3. Define Content-Type JSON apenas se houver corpo E se não for FormData/URLSearchParams
    if (
      !fetchOptions.headers['Content-Type'] &&
      fetchOptions.body &&
      !(fetchOptions.body instanceof FormData) &&
      !(fetchOptions.body instanceof URLSearchParams)
    ) {
      fetchOptions.headers['Content-Type'] = 'application/json';
    }

    // 4. Injeta dinamicamente o Token se ele existir no localStorage
    const tk = this.token();
    if (tk) fetchOptions.headers['Authorization'] = `Bearer ${tk}`;

    // 5. Executa a chamada real usando a estrutura limpa isolada
    const res = await fetch(`${this.base}${path}`, fetchOptions);
    const ct = res.headers.get('content-type') || '';
    const data = ct.includes('application/json') ? await res.json().catch(() => null) : await res.text();

    if (!res.ok) {
      const msg = (data && (data.detail?.[0]?.msg || data.detail || data.message)) || `Erro ${res.status}`;
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }

    return data;
  },

  // ====== LOGIN ======
  async login(username, password) {
    const body = new URLSearchParams();
    body.append('grant_type', 'password');
    body.append('username', username);
    body.append('password', password);

    const data = await this.request('/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body
    });

    if (data && data.access_token) {
      this.setToken(data.access_token);

      // 🔧 FIX PRINCIPAL:
      // A maioria dos backends OAuth2 (FastAPI) devolve só o token no /login/,
      // sem o objeto "user". Antes, isso deixava API.user() sempre `null`
      // mesmo logado — e qualquer checagem do tipo "if (!API.user()) -> pedir
      // cadastro" no carrinho disparava errado mesmo com você autenticado.
      if (data.user) {
        this.setUser(data.user);
      } else {
        // 🔧 FIX: em vez de chamar um endpoint que talvez não exista no seu
        // backend, extraímos os dados direto do token JWT que o /login/ já
        // devolve. Assim API.user() passa a retornar algo sempre que o
        // login der certo, sem depender de mais nenhuma rota.
        const claims = this._decodeJWT(data.access_token);
        if (claims) {
          this.setUser(claims);
        } else {
          console.warn('Não foi possível extrair os dados do usuário do token.');
        }
      }
    }
    return data;
  },

  // ====== CURSOS ======
  getCursos(params = {}) { return this.request(this._buildPath('/cursos/', params)); },
  createCurso(payload) { return this.request('/cursos/', { method: 'POST', body: JSON.stringify(payload) }); },
  updateCurso(id, payload) { return this.request(`/cursos/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }); },
  deleteCurso(id) { return this.request(`/cursos/${id}`, { method: 'DELETE' }); },

  // ====== ALUNOS ======
  getAlunos(params = {}) { return this.request(this._buildPath('/alunos/', params)); },
  createAluno(payload) { return this.request('/alunos/', { method: 'POST', body: JSON.stringify(payload) }); },
  updateAluno(id, payload) { return this.request(`/alunos/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }); },
  deleteAluno(id) { return this.request(`/alunos/${id}`, { method: 'DELETE' }); },

  // ====== MATRÍCULAS ======
  getMatriculas(params = {}) { return this.request(this._buildPath('/matriculas/', params)); },
  createMatricula(payload) { return this.request('/matriculas/', { method: 'POST', body: JSON.stringify(payload) }); },
};

window.API = API;