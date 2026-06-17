:

🚀 Sistema de Gestão de Cursos - Escola Tecno Brasília
Este projeto é uma aplicação web completa para gestão de cursos e matrículas, desenvolvida com FastAPI (Backend) e JavaScript/HTML/CSS (Frontend).

📋 Funcionalidades
Gestão de Usuários: Cadastro de alunos com autenticação segura.

Catálogo de Cursos: Listagem de cursos disponíveis com filtros por nome, categoria e nível.

Carrinho de Compras: Sistema de seleção de cursos para futura matrícula.

Autenticação: Sistema baseado em Token (JWT) para persistência de sessão e acesso restrito.

Design Responsivo: Interface moderna utilizando Bootstrap 5.

🛠 Tecnologias Utilizadas
Backend: FastAPI, SQLAlchemy, PostgreSQL, Pydantic.

Frontend: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5.

Segurança: Autenticação OAuth2 via JWT.

⚙️ Como Rodar o Projeto
1. Pré-requisitos
Python 3.10+ instalado.

Docker e Docker Compose (para subir o banco de dados PostgreSQL).

Navegador moderno.

2. Configurando o Backend
Navegue até a pasta do backend.

Crie um ambiente virtual e instale as dependências:

Bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
Suba o banco de dados:

Bash
docker-compose up -d
Execute a API:

Bash
uvicorn main:app --reload
3. Configurando o Frontend
O frontend é estático. Certifique-se de que a variável API_BASE_URL no arquivo /front/static/api.js esteja apontando para http://127.0.0.1:8000.

Abra o arquivo index.html em um servidor local (Live Server no VS Code) para evitar problemas de CORS e carregamento de módulos.

⚠️ Notas Importantes (Soluções de Erros)
Constraint Error: Caso ocorra UniqueViolation no acesso do usuário, verifique a tabela usuarios no banco de dados e garanta que a coluna acesso não possua uma restrição de unicidade (Unique Key) desnecessária.

Sessão: O sistema utiliza localStorage para manter o usuário logado. Certifique-se de limpar o cache do navegador se encontrar conflitos de autenticação após alterações no código.