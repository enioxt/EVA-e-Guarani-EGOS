#!/bin/bash
# EVA & GUARANI - Script de Implantação para DigitalOcean
# ✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
echo -e "✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧"
echo -e "Script de Implantação para DigitalOcean"
echo -e "${NC}"

# Verificar dependências
echo -e "${BLUE}Verificando dependências...${NC}"
command -v node >/dev/null 2>&1 || { echo -e "${RED}Node.js não encontrado! Por favor, instale o Node.js.${NC}"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo -e "${RED}NPM não encontrado! Por favor, instale o NPM.${NC}"; exit 1; }
command -v git >/dev/null 2>&1 || { echo -e "${RED}Git não encontrado! Por favor, instale o Git.${NC}"; exit 1; }
echo -e "${GREEN}✓ Todas as dependências estão instaladas.${NC}"

# Configurações
PROJECT_DIR="eva-guarani"
SLOP_SERVER_DIR="$PROJECT_DIR/slop-server"
WEB_CLIENT_DIR="$PROJECT_DIR/web-client"
LOGS_DIR="$PROJECT_DIR/logs"
PORT=3000

# Criar diretórios
echo -e "${BLUE}Criando estrutura de diretórios...${NC}"
mkdir -p $SLOP_SERVER_DIR
mkdir -p $WEB_CLIENT_DIR
mkdir -p $LOGS_DIR
echo -e "${GREEN}✓ Diretórios criados.${NC}"

# Copiar arquivos do servidor SLOP
echo -e "${BLUE}Configurando SLOP Server...${NC}"
cp -r ../slop_server.js $SLOP_SERVER_DIR/
cp -r ../slop_config.json $SLOP_SERVER_DIR/
cp -r ../package.json $SLOP_SERVER_DIR/
cp -r ../package-lock.json $SLOP_SERVER_DIR/

# Configurando diretório de logs
sed -i "s|C:\\\\Eva Guarani EGOS\\\\logs|$LOGS_DIR|g" $SLOP_SERVER_DIR/slop_config.json

# Instalar dependências do servidor
echo -e "${BLUE}Instalando dependências do servidor...${NC}"
cd $SLOP_SERVER_DIR
npm install
echo -e "${GREEN}✓ Dependências do servidor instaladas.${NC}"

# Copiar arquivos do cliente web
echo -e "${BLUE}Configurando cliente web...${NC}"
cd - > /dev/null
cp -r ../web_client/* $WEB_CLIENT_DIR/

# Criar arquivo de configuração do Nginx
echo -e "${BLUE}Configurando Nginx...${NC}"
cat > $PROJECT_DIR/nginx.conf << EOF
server {
    listen 80;
    server_name eva-guarani.example.com;

    # Servir a aplicação web
    location / {
        root $PWD/$WEB_CLIENT_DIR;
        index index.html;
        try_files \$uri \$uri/ =404;
    }

    # Proxy para a API
    location /api/ {
        proxy_pass http://localhost:$PORT/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
echo -e "${GREEN}✓ Configuração do Nginx criada.${NC}"

# Criar script de inicialização
echo -e "${BLUE}Criando scripts de inicialização...${NC}"
cat > $PROJECT_DIR/start.sh << EOF
#!/bin/bash
# Iniciar o SLOP Server
cd $PWD/$SLOP_SERVER_DIR
NODE_ENV=production nohup node slop_server.js > ../logs/slop_server.log 2>&1 &
echo "SLOP Server iniciado na porta $PORT"
echo "Para visualizar os logs: tail -f $PWD/$LOGS_DIR/slop_server.log"
EOF
chmod +x $PROJECT_DIR/start.sh

# Criar script systemd service
cat > $PROJECT_DIR/eva-guarani.service << EOF
[Unit]
Description=EVA & GUARANI SLOP Server
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$PWD/$SLOP_SERVER_DIR
ExecStart=$(which node) slop_server.js
Restart=on-failure
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF
echo -e "${GREEN}✓ Scripts de inicialização criados.${NC}"

# Instruções finais
echo -e "${YELLOW}==================================================${NC}"
echo -e "${YELLOW}Implantação concluída! Siga estas etapas finais:${NC}"
echo -e "${CYAN}1. Copie o arquivo $PROJECT_DIR/eva-guarani.service para /etc/systemd/system/${NC}"
echo -e "${CYAN}   sudo cp $PROJECT_DIR/eva-guarani.service /etc/systemd/system/${NC}"
echo -e "${CYAN}2. Habilite e inicie o serviço:${NC}"
echo -e "${CYAN}   sudo systemctl enable eva-guarani.service${NC}"
echo -e "${CYAN}   sudo systemctl start eva-guarani.service${NC}"
echo -e "${CYAN}3. Configure o Nginx:${NC}"
echo -e "${CYAN}   sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/eva-guarani${NC}"
echo -e "${CYAN}   sudo ln -s /etc/nginx/sites-available/eva-guarani /etc/nginx/sites-enabled/${NC}"
echo -e "${CYAN}   sudo systemctl restart nginx${NC}"
echo -e "${YELLOW}==================================================${NC}"
echo -e "${PURPLE}✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧${NC}"
