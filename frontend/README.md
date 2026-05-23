# Frontend Vue.js - Gestão de TCCs

Este diretório contém o frontend Vue.js para o projeto de gestão de TCCs.

## Como usar

1. Instale as dependências:

```bash
cd frontend
npm install
```

2. Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

3. Abra o frontend no navegador em:

```text
http://127.0.0.1:5173
```

4. Garanta que o backend Django esteja rodando em:

```text
http://127.0.0.1:8000
```

## Funcionalidades

- Listagem de alunos, professores, cursos e departamentos
- Cadastro de TCCs com upload de arquivo PDF
- Atualização de status dos TCCs
- Dashboard de estatísticas com gráficos

## Observações

- O frontend consome os endpoints do backend Django REST Framework na base `http://127.0.0.1:8000/api`
- O upload de arquivo usa `FormData` para enviar o PDF corretamente
