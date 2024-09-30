## Sobre 📝

**Popify** é um chatbot de música pop estadunidense 🎶. Ele foi desenvolvido para fornecer informações sobre artistas americanos do gênero pop, abrangendo os seguintes aspectos: biografias, músicas e álbuns.
## Tecnologias Utilizadas 👩‍💻

- **Linguagem**: Python
- **Framework**: FastAPI para criação de APIs rápidas e robustas
- **Bibliotecas**:
  - `llama_index`: Usado para criar e gerenciar índices de busca e recuperação de informações
  - `OpenAI`: Integração com o GPT-4o-mini para geração de respostas
  - **Dependências adicionais**:
    - `uvicorn`: Servidor ASGI para rodar a aplicação FastAPI
    - `python-dotenv`: Para gerenciar variáveis de ambiente

## Pré-requisitos 📍

Antes de iniciar, você precisará ter instalado em sua máquina:

- **Python 3.x**
- **Git** para clonar o repositório
- **Chave de API da OpenAI** (para acessar o modelo GPT)

### Configuração do Ambiente 🖱️

Crie um arquivo `.env` na raiz do projeto com a seguinte variável de ambiente:

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
```
### Parte visual 🎨
O fron-tend do sistema está disponível no repositório https://github.com/raianipontes/popify-frontend
