# MVP - Sistema de Classificação de Avaliação de Carros

## Sobre o Projeto

Este projeto implementa um sistema completo de Machine Learning para classificação de avaliação de carros, utilizando o dataset **Car Evaluation** do UCI Machine Learning Repository.

### Dataset
- **Fonte**: UCI ML Repository (ID: 19)
- **Problema**: Classificação multiclasse
- **Classes**: unacc, acc, good, vgood
- **Atributos**: 6 features categóricas (buying, maint, doors, persons, lug_boot, safety)

## Estrutura do Projeto

```
MVPSP2/
├── car_evaluation_ml.ipynb          # Notebook Colab com pipeline ML completo
├── backend/
│   ├── app.py                        # API Flask
│   ├── model/
│   │   └── best_model.pkl           # Modelo treinado
│   ├── requirements.txt             # Dependências backend
│   └── test_model.py                # Testes PyTest
├── frontend/
│   ├── index.html                   # Interface web
│   ├── style.css                    # Estilos
│   └── script.js                    # Lógica frontend
├── data/                            # Dados auxiliares
├── docs/
│   └── SEGURANCA.md                 # Práticas de segurança
└── README.md                        # Este arquivo
```

## Execução do Projeto

### 1. Notebook de Machine Learning
Acesse o notebook no Google Colab:
- Link: [Será gerado após upload no GitHub]
- Executa do início ao fim sem erros
- Gera o modelo `best_model.pkl`

### 2. Aplicação Full Stack

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend:**
Abra `frontend/index.html` em um navegador ou use um servidor local.

**Testes:**
```bash
cd backend
pytest test_model.py -v
```

## Tecnologias Utilizadas

- **ML**: Python, Scikit-Learn, Pandas, NumPy
- **Backend**: Flask, Joblib
- **Frontend**: HTML5, CSS3, JavaScript
- **Testes**: PyTest
- **Notebook**: Google Colab

## Autores

Desenvolvido para o MVP da Sprint 2 - Pós-Graduação PUC-Rio
