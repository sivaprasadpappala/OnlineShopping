I've generated a comprehensive README for the Online Shopping repository. However, I don't have write permissions to create the file directly in your repository. 

Here's the generated README content you can copy and paste into a new `README.md` file:

```markdown
# Online Shopping Application

A secure, containerized e-commerce web application built with Flask and SQLAlchemy that allows users to browse products, manage shopping carts, and place orders. The application includes integrated security scanning, CI/CD pipeline automation with Jenkins, and Kubernetes deployment orchestration.

### Stack
- **Language:** Python 3.11
- **Framework / runtime:** Flask 3.0.0 + Flask-SQLAlchemy 3.1.1
- **Notable libraries:** Flask-SQLAlchemy (ORM), Bandit (security scanning)
- **Database:** SQLite (development)
- **Containerization:** Docker (Alpine-based)
- **Orchestration:** Kubernetes
- **CI/CD:** Jenkins pipeline with security gates

## How it's organized

```
.
├── app.py                    # Flask application entry point, route handlers
├── models.py                 # SQLAlchemy ORM models (Product, Order)
├── config.py                 # Application configuration (DB URI, secrets)
├── db_init.py                # Database initialization with sample data
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container image definition (Alpine Linux)
├── Jenkinsfile               # CI/CD pipeline (build, scan, deploy)
├── sonar-project.properties  # SonarQube configuration for code quality
├── k8s/
│   ├── deployment.yaml       # Kubernetes Deployment manifest
│   └── service.yaml          # Kubernetes Service manifest
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Base layout template
│   ├── index.html            # Product listing page
│   ├── product.html          # Product detail page
│   ├── cart.html             # Shopping cart page
│   └── checkout.html         # Order confirmation page
└── static/                   # CSS, JavaScript, and static assets (optional)
```

**How it fits together:**

The application follows a traditional web application architecture. Requests enter through Flask routes in `app.py`, which render Jinja2 templates from the `templates/` directory. Product and Order data are persisted using SQLAlchemy ORM models defined in `models.py`. The shopping cart is stored in Flask sessions for stateless operation. When a user checks out, an Order record is persisted to the database and the session cart is cleared. The entire application runs on port 5000 and can be deployed as a Docker container or directly on Kubernetes via the Jenkins pipeline.

## How to run it

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Docker (optional, for containerization)
- Kubernetes cluster (optional, for orchestration)

### Local development

```bash
# Clone the repository
git clone https://github.com/sivaprasadpappala/OnlineShopping.git
cd OnlineShopping

# Install dependencies
pip install -r requirements.txt

# Initialize the database with sample products
python db_init.py

# Run the Flask development server
python app.py
```

The application will start on `http://0.0.0.0:5000`. Open your browser and navigate to `http://localhost:5000` to view the product listing.

### Docker

```bash
# Build the Docker image
docker build -t online-shop:latest .

# Run the container
docker run -p 5000:5000 online-shop:latest
```

The application will be accessible at `http://localhost:5000`.

### Kubernetes

The repository includes Kubernetes manifests for production deployment:

```bash
# Deploy to Kubernetes (assumes kubectl configured)
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check deployment status
kubectl rollout status deployment/online-shop
```

### CI/CD Pipeline (Jenkins)

The `Jenkinsfile` automates the entire deployment workflow:

1. **Checkout** — Clones the repository
2. **Install Dependencies** — Sets up Python virtual environment
3. **Bandit Security Scan** — Performs Python security analysis
4. **SonarQube Scan** — Runs code quality analysis
5. **SonarQube Quality Gate** — Enforces code quality standards
6. **Build Docker Image** — Creates and tags the container image
7. **Trivy Image Scan** — Scans image for critical vulnerabilities
8. **Push Image** — Pushes to Docker Hub (requires credentials)
9. **Deploy to Kubernetes** — Applies manifests and verifies rollout

**Required Jenkins Configuration:**
- Credentials: `dockerhub-creds` (Docker Hub username/password)
- SonarQube server configured as `sonarqube`
- `kubectl` and Docker installed on Jenkins agent
- Kubernetes configuration at `~/.kube/config`

## Key Features

- **Product Catalog** — Browse and view product details
- **Shopping Cart** — Add products with session-based persistence
- **Checkout** — Process orders and persist to database
- **Security Scanning** — Integrated Bandit and Trivy scanning in CI/CD
- **Code Quality** — SonarQube integration with quality gates
- **Containerization** — Alpine-based Docker image with non-root user
- **Orchestration** — Kubernetes deployment and service manifests
- **Non-Root Security** — Dockerfile runs application as unprivileged `appuser`

