# ✅ Checklist de Execução do MVP

## Status do Projeto

- [x] Estrutura do projeto criada
- [x] Backend Flask implementado
- [x] Frontend HTML/CSS/JS criado
- [x] Testes PyTest implementados
- [x] Notebook Jupyter completo
- [x] Documentação de segurança
- [x] Código commitado no GitHub
- [ ] **→ VOCÊ ESTÁ AQUI: Executar notebook no Colab**

---

## Próximos Passos (NA ORDEM)

### ⏳ PASSO 1: Executar Notebook no Google Colab
1. Acesse: https://colab.research.google.com/
2. File → Upload notebook → Selecione `car_evaluation_ml.ipynb`
3. Runtime → Run all (ou Ctrl+F9)
4. Aguarde ~5-10 min para completar
5. **IMPORTANTE**: Baixe o arquivo `best_model.pkl` gerado

### ⏳ PASSO 2: Mover Modelo para Backend
```bash
# Após baixar best_model.pkl
mv ~/Downloads/best_model.pkl backend/model/
```

### ⏳ PASSO 3: Instalar Dependências
```bash
cd backend
pip install -r requirements.txt
```

### ⏳ PASSO 4: Executar Testes
```bash
pytest test_model.py -v
```
**Resultado esperado**: Todos os 8 testes devem PASSAR ✓

### ⏳ PASSO 5: Iniciar Backend
```bash
python app.py
```
**Resultado esperado**: Servidor rodando em http://localhost:5000

### ⏳ PASSO 6: Testar Frontend
1. Abra novo terminal
2. `cd frontend`
3. Opção 1: Abra `index.html` direto no navegador
4. Opção 2: `python -m http.server 8000`
5. Preencha o formulário e teste predições

### ⏳ PASSO 7: Gravar Vídeo
**Máximo 3 minutos mostrando**:
- [ ] Notebook executado no Colab (mostrar células principais)
- [ ] Testes PyTest passando
- [ ] Backend rodando
- [ ] Frontend fazendo predições
- [ ] Diferentes casos de teste

### ⏳ PASSO 8: Validação Final
- [ ] README.md atualizado com link do repositório
- [ ] Vídeo hospedado (YouTube, Loom, etc)
- [ ] Link do vídeo no README
- [ ] Todos os arquivos no GitHub
- [ ] Repositório público

---

## Estrutura de Arquivos Esperada

```
MVPSP2/
├── car_evaluation_ml.ipynb          ✓ Criado
├── backend/
│   ├── app.py                        ✓ Criado
│   ├── test_model.py                 ✓ Criado
│   ├── requirements.txt              ✓ Criado
│   └── model/
│       └── best_model.pkl           ⚠️ PENDENTE (gerar no Colab)
├── frontend/
│   ├── index.html                    ✓ Criado
│   ├── style.css                     ✓ Criado
│   └── script.js                     ✓ Criado
├── docs/
│   └── SEGURANCA.md                  ✓ Criado
└── README.md                         ✓ Criado

```

---

## Troubleshooting

### Erro: "Modelo não encontrado"
→ Execute o notebook no Colab e baixe `best_model.pkl`

### Erro: "ModuleNotFoundError"
→ Execute `pip install -r requirements.txt`

### Erro: "CORS" no frontend
→ Backend deve estar rodando na porta 5000

### Testes falhando
→ Certifique-se de que `best_model.pkl` está em `backend/model/`

---

## Critérios de Avaliação (Checklist Final)

### Notebook (4 pts)
- [ ] Executa sem erros do início ao fim
- [ ] Segue etapas: carga, EDA, preprocessing, modelagem, otimização
- [ ] Blocos de texto explicam cada etapa
- [ ] Análise de resultados completa

### Aplicação Full Stack (3 pts)
- [ ] Backend carrega modelo corretamente
- [ ] Frontend permite entrada de dados
- [ ] Predição funciona e exibe resultado
- [ ] Teste PyTest passa e valida performance

### Código e Vídeo (3 pts)
- [ ] Código limpo e organizado
- [ ] Vídeo de 3 min mostra aplicação rodando
- [ ] Vídeo é claro e objetivo

**Total: 10 pontos**

---

## Contato de Suporte
Se tiver dúvidas, me chame novamente! 🚀
