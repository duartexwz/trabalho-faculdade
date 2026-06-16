// js/api.js
// Ajuste a porta de acordo com o container da sua API
const BASE_URL = 'http://localhost:8000/docs'; 

const api = {
    // Busca todos os cursos
    async getCursos() {
        try {
            const response = await fetch(`${BASE_URL}/cursos`);
            if (!response.ok) throw new Error('Erro ao buscar cursos');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return [];
        }
    },

    // Autenticação genérica
    async login(credentials) {
        try {
            const response = await fetch(`${BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(credentials)
            });
            return await response.json();
        } catch (error) {
            console.error('Erro de Login:', error);
        }
    }
};