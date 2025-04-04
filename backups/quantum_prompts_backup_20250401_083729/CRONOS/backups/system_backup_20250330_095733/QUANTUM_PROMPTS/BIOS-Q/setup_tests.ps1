# Script para configurar o ambiente e executar os testes do BIOS-Q
Write-Host "=== Configurando ambiente de testes do BIOS-Q ==="

# Verifica a versão do Python
Write-Host "`n=== Verificando versão do Python ==="
python --version

# Define o diretório do ambiente virtual
$VENV_DIR = "C:\Users\$env:USERNAME\AppData\Local\BIOS-Q\venv"

# Cria e ativa o ambiente virtual
Write-Host "`n=== Criando ambiente virtual em $VENV_DIR ==="
python -m venv $VENV_DIR
& "$VENV_DIR\Scripts\activate.ps1"

# Atualiza pip
Write-Host "`n=== Atualizando pip ==="
python -m pip install --upgrade pip

# Instala as dependências
Write-Host "`n=== Instalando dependências ==="
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov

# Executa os testes com cobertura
Write-Host "`n=== Executando testes com cobertura ==="
python -m pytest tests/ -v --cov=. --cov-report=html

# Exibe relatório de cobertura no terminal
Write-Host "`n=== Relatório de Cobertura ==="
python -m pytest tests/ --cov=. --cov-report=term-missing

Write-Host "`n=== Testes concluídos ==="
