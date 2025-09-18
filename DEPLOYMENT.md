# E-commerce Platform Deployment Guide

This document provides step-by-step instructions for deploying the e-commerce platform to a production environment.

## Prerequisites

- Ubuntu 22.04 LTS server
- Python 3.13+
- PostgreSQL 17+
- Redis
- Nginx
- Node.js 18+ (for frontend assets if needed)
- Domain name with DNS configured
- SSL certificate (Let's Encrypt recommended)

## Server Setup

### 1. System Updates

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential libpq-dev python3-dev python3-pip python3-venv nginx redis-server postgresql postgresql-contrib git ufw
```

### 2. Firewall Configuration

```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### 3. PostgreSQL Setup

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE ecommerce_prod;
CREATE USER ecommerce_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_prod TO ecommerce_user;
\c ecommerce_prod
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\q
```

### 4. Redis Setup

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

## Application Deployment

### 1. Create Deployment User

```bash
sudo adduser --system --group --shell /bin/bash deploy
sudo usermod -aG sudo deploy
```

### 2. Set Up Project Directory

```bash
sudo mkdir -p /opt/ecommerce
sudo chown -R deploy:deploy /opt/ecommerce
```

### 3. Clone Repository

```bash
sudo -u deploy git clone https://github.com/yourusername/project-nexus.git /opt/ecommerce
```

### 4. Create Virtual Environment

```bash
sudo -u deploy python3 -m venv /opt/ecommerce/venv
source /opt/ecommerce/venv/bin/activate
```

### 5. Install Dependencies

```bash
cd /opt/ecommerce
pip install --upgrade pip
pip install -r requirements/production.txt
```

### 6. Environment Variables

Create `.env` file in `/opt/ecommerce`:

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=.yourdomain.com,localhost,127.0.0.1

# Database
DB_NAME=ecommerce_prod
DB_USER=ecommerce_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
SERVER_EMAIL=your-email@example.com

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Admin
DJANGO_ADMIN_URL=admin/
```

### 7. Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Gunicorn Setup

### 1. Install Gunicorn

```bash
pip install gunicorn
```

### 2. Create Gunicorn Service

Create `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/opt/ecommerce
ExecStart=/opt/ecommerce/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/opt/ecommerce/ecommerce.sock ecommerce_backend.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Start and Enable Gunicorn

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## Nginx Configuration

### 1. Create Nginx Config

Create `/etc/nginx/sites-available/ecommerce`:

```nginx
upstream ecommerce {
    server unix:/opt/ecommerce/ecommerce.sock;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        return 301 https://$host$request_uri;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/letsencrypt;
    }
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_stapling on;
    ssl_stapling_verify on;

    access_log /var/log/nginx/ecommerce.access.log;
    error_log /var/log/nginx/ecommerce.error.log;

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://ecommerce;
    }

    location /static/ {
        alias /opt/ecommerce/static/;
        expires 30d;
        access_log off;
    }

    location /media/ {
        alias /opt/ecommerce/media/;
        expires 30d;
        access_log off;
    }
}
```

### 2. Enable the Site

```bash
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## SSL Certificate

Install Certbot and get SSL certificate:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Final Steps

1. Set up automatic certificate renewal:

    ```bash
    sudo systemctl enable certbot.timer
    sudo systemctl start certbot.timer
    ```

2. Verify services are running:

    ```bash
    sudo systemctl status gunicorn
    sudo systemctl status nginx
    ```

3. Verify your site is accessible at `https://yourdomain.com`

## CI/CD Integration

The GitHub Actions workflow will automatically deploy changes when pushing to the `main` branch. Ensure you've set up the following secrets in your GitHub repository:

- `SSH_PRIVATE_KEY`: Private key for server access
- `KNOWN_HOSTS`: Known hosts entry for your server
- `DEPLOY_USER`: Deployment username (e.g., `deploy`)
- `DEPLOY_HOST`: Server IP or hostname
- `DJANGO_SECRET_KEY`: Your Django secret key
- Other environment variables from your `.env` file

## Monitoring

1. Set up log rotation:

    ```bash
    sudo nano /etc/logrotate.d/ecommerce-logs
    ```

    Add the following:

    ```text
    /var/log/django/*.log {
        daily
        missingok
        rotate 14
        compress
        delaycompress
        notifempty
        create 0640 www-data adm
        sharedscripts
        postrotate
            systemctl reload gunicorn
        endscript
    }
    ```

2. Set up monitoring (optional but recommended):

- Uptime monitoring (e.g., UptimeRobot)
- Error tracking (Sentry)
- Performance monitoring (New Relic, Datadog)
