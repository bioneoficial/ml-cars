# Práticas de Segurança Aplicáveis ao Projeto

## Contexto

Este documento reflete sobre como as boas práticas vistas na disciplina **Desenvolvimento de Software Seguro** podem ser aplicadas ao projeto de classificação de carros.

## 1. Segurança dos Dados

### 1.1 Anonimização de Dados

No contexto do dataset Car Evaluation:
- **Dataset atual**: Utiliza dados sintéticos e categóricos sem informações pessoais identificáveis (PII)
- **Cenário real**: Se o sistema fosse usado com dados reais de clientes/proprietários, seria necessário:
  - Remover identificadores diretos (CPF, placa, nome)
  - Aplicar técnicas de k-anonymity para dados demográficos
  - Pseudonimização de IDs de clientes
  - Agregação de dados sensíveis

### 1.2 Minimização de Dados

**Aplicado no projeto**:
- Coletamos apenas 6 atributos essenciais para classificação
- Não armazenamos histórico de predições (stateless API)
- Nenhum dado pessoal é requisitado

**Melhorias futuras**:
- Implementar retenção de dados com prazo definido
- Logs sem informações sensíveis

## 2. Segurança da API

### 2.1 Autenticação e Autorização

**Status atual**: API aberta (MVP)

**Recomendações para produção**:
```python
# Exemplo: JWT Authentication
from flask_jwt_extended import JWTManager, jwt_required

@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    # Apenas usuários autenticados podem fazer predições
    pass
```

### 2.2 Rate Limiting

**Implementação recomendada**:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict():
    # Previne abuso da API
    pass
```

### 2.3 Validação de Entrada

**Já implementado**:
- Validação de campos obrigatórios
- Validação de valores permitidos (white-list)
- Tratamento de exceções

**Código de validação atual**:
```python
required_fields = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
for field in required_fields:
    if field not in data:
        return jsonify({"error": f"Campo '{field}' é obrigatório"}), 400
```

## 3. Segurança do Modelo

### 3.1 Envenenamento de Dados (Data Poisoning)

**Riscos**:
- Dados maliciosos no treinamento podem comprometer o modelo
- No dataset UCI, isso é mitigado pela fonte confiável

**Proteções**:
- Validação de fontes de dados
- Análise de outliers antes do treinamento
- Versionamento de datasets

### 3.2 Ataques Adversariais

**Vulnerabilidade**:
- Inputs crafted para enganar o modelo

**Mitigações implementadas**:
```python
# Validação estrita de valores categóricos
expected_values = {
    "buying": ["vhigh", "high", "med", "low"],
    "safety": ["low", "med", "high"]
}
```

### 3.3 Model Inversion e Privacy

**Prevenção**:
- Não expor probabilidades detalhadas em produção sensível
- Limitar informações sobre arquitetura do modelo
- Não retornar dados de treinamento via API

## 4. Segurança de Dependências

### 4.1 Gestão de Versões

**Implementado**:
```txt
flask==3.0.0
scikit-learn==1.3.2
```

**Boas práticas**:
```bash
# Verificar vulnerabilidades
pip install safety
safety check

# Manter dependências atualizadas
pip list --outdated
```

### 4.2 Isolamento de Ambiente

**Recomendado**:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5. Segurança em Produção

### 5.1 Variáveis de Ambiente

**Implementação recomendada**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
```

### 5.2 HTTPS e CORS

**CORS configurado**:
```python
from flask_cors import CORS
CORS(app)  # Em produção, especificar origens permitidas
```

**Produção**:
```python
CORS(app, origins=["https://meudominio.com"])
```

### 5.3 Logs e Monitoramento

**Implementação segura**:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nunca logar dados sensíveis
logger.info(f"Predição realizada - Resultado: {prediction}")
# NÃO: logger.info(f"Dados do usuário: {user_data}")
```

## 6. Conformidade e Regulamentações

### 6.1 LGPD (Lei Geral de Proteção de Dados)

**Aplicabilidade**:
- Se coletar dados de brasileiros, aplicar LGPD
- Direitos: acesso, correção, exclusão, portabilidade

**Implementações necessárias**:
- Consentimento explícito
- Política de privacidade
- DPO (Data Protection Officer)
- Registro de processamento

### 6.2 Transparência do Modelo

**Explicabilidade**:
```python
# Usar SHAP ou LIME para explicar predições
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
```

## 7. Testes de Segurança

### 7.1 Testes Implementados

**PyTest** para validação de performance:
- Previne deploy de modelos degradados
- Garante qualidade mínima (accuracy > 85%)

### 7.2 Testes Adicionais Recomendados

```python
def test_sql_injection_protection():
    # Testar inputs maliciosos
    malicious_input = {"buying": "' OR '1'='1"}
    response = client.post('/predict', json=malicious_input)
    assert response.status_code == 400

def test_xss_protection():
    # Testar scripts maliciosos
    malicious_input = {"buying": "<script>alert('XSS')</script>"}
    response = client.post('/predict', json=malicious_input)
    assert response.status_code == 400
```

## 8. Backup e Recuperação

### 8.1 Versionamento de Modelos

```python
import joblib
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
joblib.dump(model, f'model_v{timestamp}.pkl')
```

### 8.2 Disaster Recovery

- Backup regular de modelos treinados
- Documentação de processo de re-treinamento
- Plano de rollback para versões anteriores

## Conclusão

Embora este seja um MVP educacional com dados sintéticos, a aplicação destas práticas de segurança é **essencial** em ambientes de produção. A segurança deve ser considerada desde o design, não como uma camada adicional posterior.

**Principais takeaways**:
1. ✅ Validar todas as entradas
2. ✅ Minimizar coleta de dados
3. ✅ Proteger credenciais e secrets
4. ✅ Manter dependências atualizadas
5. ✅ Implementar autenticação em produção
6. ✅ Monitorar e auditar acessos
7. ✅ Garantir conformidade legal (LGPD)
8. ✅ Documentar e versionar modelos
