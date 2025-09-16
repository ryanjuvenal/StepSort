# 📊 StepSort

**StepSort** é uma aplicação web desenvolvida em **Flask** que demonstra algoritmos de ordenação passo a passo.  
O sistema permite que o usuário insira números manualmente ou gere listas aleatórias, e visualize como os algoritmos **Bubble Sort** e **Selection Sort** organizam os dados.

---

## 🎯 Objetivo

- Fornecer uma ferramenta interativa e educacional para estudantes de programação.  
- Demonstrar visualmente o funcionamento dos algoritmos de ordenação.  
- Possibilitar testes simples via endpoint `/health` para verificar se a aplicação está ativa.

---

## 🛠️ Stack Utilizada

- **Linguagem:** Python 3.x  
- **Framework Web:** Flask  
- **Frontend:** HTML5, CSS3 e JavaScript  
- **Templates:** Jinja2  

---

## 📂 Estrutura Inicial do Projeto
```bash
StepSort/
├── static/          <- arquivos CSS
├── templates/
│   ├── index.html   <- Página inicial
│   └── sorted.html  <- Página com resultado da ordenação
├── main.py          <- Código principal Flask
└── README.md
```

---

## 🚀 Como Rodar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/StepSort.git
cd StepSort
```

### 2. Instalar dependências
```bash
pip install flask
```

### 3. Rodar o serviço Flask
```bash
python main.py
```

## A aplicação será executada em:
```bash
http://127.0.0.1:5000/
```

---

## 🧪 Testar endpoint /health

### Para verificar se o serviço está ativo, abra no navegador ou use curl:

```bash
http://127.0.0.1:5000/health	
```

### Resposta esperada
```bash
{"status": "ok"}
```

---

## 👥 Integrantes do Grupo

- **Ryan Juvenal Santos Oliveira**
- **Cesar Augusto Salles Marcondes**
- **doca**
- **deus gamer**
