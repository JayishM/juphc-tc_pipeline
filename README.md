# Final Project: Tax Calculator App

A cloud-native web application containerized with Docker, deployed on IBM Cloud, and automated using Tekton CI/CD pipelines.

---

## 📁 Project Structure

```text
tax-calculator/
├── 01-jasmine-tests-passing     # Task 1: Jasmine 7 specs passing terminal output
├── 02-dockerfile                 # Task 2: Required Dockerfile snippet for evaluation
├── 03-docker-build               # Task 3: Docker build terminal log
├── 04-docker-run                 # Task 4: Local Docker container deployment log
├── 05-tag-push-icr               # Task 5: Tag & push to IBM Cloud Container Registry log
├── 06-deploy-ibm-cloud           # Task 6: IBM Cloud Code Engine deployment log
├── 09-pipeline-run               # Task 9: Tekton pipeline execution log
├── 10-deploy-image               # Task 10: Updated deployment with pipeline image log
├── Dockerfile                    # Multi-file Nginx container definition
├── favicon.ico                   # Application favicon
├── index.html                    # Responsive Tax Calculator UI
├── package.json                  # NPM dependencies & test scripts
├── pipeline.yaml                 # Task 8: Tekton Pipeline definition
├── pvc.yaml                      # Tekton workspace PersistentVolumeClaim
├── script.js                     # UI interactivity & form handler
├── spec/
│   ├── support/
│   │   └── jasmine.json          # Jasmine test runner configuration
│   └── taxCalculator.spec.js     # 7 Jasmine unit tests (Task 1)
├── style.css                     # Modern UI styling
├── tasks.yaml                    # Task 7: Tekton Task definitions (npm & jasmine)
└── taxCalculator.js              # Business logic module
```

---

## 🎯 10-Point Grading Criteria & Corresponding Files

| Point | Requirement | File / Artifact in Repo |
|---|---|---|
| **1 pt** | Run unit tests using Jasmine (7 passed specs) | `01-jasmine-tests-passing`, `spec/taxCalculator.spec.js` |
| **1 pt** | Create the Dockerfile for local Docker container | `02-dockerfile`, `Dockerfile` |
| **1 pt** | Build the Docker image | `03-docker-build` |
| **1 pt** | Deploy and test in local Docker container | `04-docker-run`, `index.html` |
| **1 pt** | Tag and push to IBM Cloud Registry | `05-tag-push-icr` |
| **1 pt** | Deploy Tax Calculator on IBM Cloud | `06-deploy-ibm-cloud` |
| **1 pt** | Create Tekton Pipeline tasks (npm & jasmine) | `tasks.yaml` |
| **1 pt** | Extend Pipeline to call required tasks | `pipeline.yaml` |
| **1 pt** | Run the Tekton pipeline | `09-pipeline-run` |
| **1 pt** | Deploy the image built using pipeline | `10-deploy-image` |

---

## 🚀 How to Upload This Project to GitHub

Run these commands from your local terminal:

```bash
# 1. Navigate to the project folder
cd /Users/jayishmundhra/.gemini/antigravity/scratch/tax-calculator

# 2. Initialize git repository
git init -b main

# 3. Stage all files
git add .

# 4. Commit changes
git commit -m "Initial commit: Complete Tax Calculator DevOps final project"

# 5. Create a new PUBLIC repository on GitHub named "tax-calculator"
# Then link and push:
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/tax-calculator.git
git push -u origin main
```

---

## 🔗 Task 7 GitHub URL Format
Once pushed, your public URL for Task 7 will be:
```text
https://github.com/<YOUR-GITHUB-USERNAME>/tax-calculator/blob/main/tasks.yaml
```
