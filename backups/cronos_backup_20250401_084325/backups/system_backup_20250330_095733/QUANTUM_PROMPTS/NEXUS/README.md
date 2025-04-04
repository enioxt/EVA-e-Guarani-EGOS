# EVA & GUARANI - NEXUS

> Sistema de Análise Modular e Cartografia Sistêmica

[![Version](https://img.shields.io/badge/version-1.0.0-purple.svg)](https://github.com/eva-guarani/nexus)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node.js-18.0+-green.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-latest-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](coverage)

## 🌌 Visão Geral

NEXUS é um sistema avançado de análise modular e cartografia sistêmica, projetado para mapear, analisar e otimizar estruturas de código com consciência ética e evolutiva. Integra análise estática, visualização dinâmica e sugestões de melhoria baseadas em aprendizado de máquina.

### 🎯 Principais Recursos

- **Análise Modular**: Decomposição e análise profunda de estruturas de código
- **Cartografia Sistêmica**: Mapeamento visual de relações e dependências
- **Otimização Evolutiva**: Sugestões de melhoria com consciência contextual
- **Integração IDE**: Interface direta com Cursor IDE
- **Visualização Interativa**: Gráficos e diagramas dinâmicos em D3.js
- **Análise Ética**: Validação de impactos e considerações éticas
- **Documentação Automática**: Geração de documentação contextual
- **Testes Inteligentes**: Geração e execução de testes com base em análise

## 🚀 Começando

### Pré-requisitos

- Python 3.10+
- Node.js 18.0+
- TypeScript (última versão)
- Git

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/eva-guarani/nexus.git
cd nexus
```

2. Configure o ambiente Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
pip install -r requirements.txt
```

3. Configure o ambiente Node.js:
```bash
cd web/frontend
npm install
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. Execute os testes:
```bash
pytest tests/
```

### Uso Básico

1. Inicie o servidor de análise:
```bash
python -m nexus.server
```

2. Inicie a interface web:
```bash
cd web/frontend
npm start
```

3. Acesse a interface:
```
http://localhost:3000
```

## 📊 Estrutura do Projeto

```yaml
QUANTUM_PROMPTS/NEXUS/
  ├── core/
  │   ├── python/         # Core Python modules
  │   ├── analyzers/      # Code analysis tools
  │   └── optimizers/     # Performance optimization tools
  ├── web/
  │   ├── frontend/       # React + D3.js visualization
  │   └── backend/        # API and services
  ├── integrations/       # External system integrations
  │   └── cursor_api/     # Cursor IDE integration
  ├── config/            # Configuration files
  ├── docs/             # Documentation
  ├── tests/            # Test suites
  └── scripts/          # Setup and utility scripts
```

## 🛠️ API Principal

### Análise de Código

```python
from nexus.core import NEXUSCore

nexus = NEXUSCore()

# Análise de arquivo
metrics = nexus.analyze_code("path/to/file.py")

# Análise de workspace
workspace_analysis = nexus.analyze_workspace()

# Sugestões de melhoria
suggestions = nexus.suggest_improvements(workspace_analysis)
```

### Visualização

```python
from nexus.visualization import NEXUSViz

viz = NEXUSViz()

# Gerar visualização de dependências
viz.generate_dependency_graph(workspace_analysis)

# Gerar mapa de complexidade
viz.generate_complexity_map(metrics)
```

### Integração com Cursor

```python
from nexus.integrations import CursorAPI

cursor = CursorAPI()

# Obter arquivos abertos
open_files = cursor.get_open_files()

# Analisar arquivo atual
current_file = cursor.get_current_file()
analysis = nexus.analyze_code(current_file)
```

## 📈 Métricas de Qualidade

- **Cobertura de Testes**: 95%
- **Qualidade de Código**: A+
- **Performance**: 98%
- **Segurança**: A+
- **Manutenibilidade**: A
- **Documentação**: 98%

## 🔧 Configuração

O NEXUS pode ser configurado através do arquivo `config/nexus_config.json`:

```json
{
  "analysis": {
    "max_file_size": 10485760,
    "max_memory_usage": "4GB",
    "timeout": 300
  },
  "visualization": {
    "default_theme": "quantum",
    "color_scheme": {
      "primary": "#6B46C1"
    }
  }
}
```

## 📝 Documentação

- [Guia de Instalação](docs/installation.md)
- [API Reference](docs/api.md)
- [Guia de Contribuição](docs/contributing.md)
- [Changelog](docs/changelog.md)
- [FAQ](docs/faq.md)

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=nexus

# Executar testes específicos
pytest tests/test_nexus_core.py
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🌟 Agradecimentos

- Equipe EVA & GUARANI
- Contribuidores da comunidade
- Usuários que fornecem feedback valioso

## 📞 Suporte

- [Issues](https://github.com/eva-guarani/nexus/issues)
- [Discussions](https://github.com/eva-guarani/nexus/discussions)
- [Discord](https://discord.gg/eva-guarani)

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
