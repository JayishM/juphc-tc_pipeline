# User Stories: Tax Calculator DevOps Modernization

This document outlines the user and developer stories driving the modernization, containerization, cloud deployment, and automated CI/CD pipeline implementation for the Tax Calculator application.

---

## Summary of Stories

| Story ID | Title | Persona | Priority | Status |
|---|---|---|---|---|
| **US-01** | Progressive Income Tax Calculation | Taxpayer (User) | High | Completed |
| **US-02** | Input Validation & Error Feedback | Taxpayer (User) | High | Completed |
| **US-03** | Automated Jasmine Unit Testing | Developer | High | Completed |
| **US-04** | Docker Image Construction | DevOps Engineer | High | Completed |
| **US-05** | Local Container Execution & Verification | DevOps Engineer | High | Completed |
| **US-06** | IBM Cloud Container Registry Integration | DevOps Engineer | Medium | Completed |
| **US-07** | Application Deployment on IBM Cloud | DevOps Engineer | High | Completed |
| **US-08** | Tekton Pipeline Task Creation | CI/CD Engineer | High | Completed |
| **US-09** | Automated Testing & Image Build Pipeline | CI/CD Engineer | High | Completed |
| **US-10** | Continuous Deployment of Pipeline-Built Image | CI/CD Engineer | High | Completed |

---

## Detailed User Stories

### Story US-01: Progressive Income Tax Calculation
- **User Story**: *As a taxpayer*, I want to enter my annual gross income and allowable deductions into the calculator, *so that* I can accurately determine my taxable income, estimated tax liability, net take-home pay, and effective tax rate.
- **Priority**: High
- **Acceptance Criteria**:
  1. Accurately applies progressive tax brackets:
     - \$0 – \$10,000: 0%
     - \$10,001 – \$40,000: 10%
     - \$40,001 – \$80,000: 20%
     - Over \$80,000: 30%
  2. Deducts eligible pre-tax deductions from gross income before applying tax brackets.
  3. Displays taxable income, estimated tax, net income, and effective rate rounded to two decimal places.
  4. Provides a Reset button to clear inputs and calculation results.
- **Status**: Completed

---

### Story US-02: Input Validation & Error Feedback
- **User Story**: *As a taxpayer*, I want clear and immediate validation feedback when I enter invalid or incomplete data, *so that* I do not receive incorrect calculations.
- **Priority**: High
- **Acceptance Criteria**:
  1. Prevents submission when gross annual income field is empty.
  2. Displays an inline error message when negative numbers or non-numeric values are entered.
  3. Ensures total deductions cannot be negative.
  4. Gracefully handles zero-income and zero-deduction scenarios without errors.
- **Status**: Completed

---

### Story US-03: Automated Jasmine Unit Testing
- **User Story**: *As a developer*, I want to execute automated unit tests using Jasmine, *so that* I can verify that all tax calculations, edge cases, and validation rules remain reliable and regression-free.
- **Priority**: High
- **Acceptance Criteria**:
  1. A structured `spec/` directory containing `taxCalculator.spec.js` and `jasmine.json` configuration.
  2. Executing `npm test` runs all Jasmine specs and reports zero failures.
  3. Test suite covers zero income, bracket boundaries, multi-bracket progressive calculations, deductions, and negative input rejections.
  4. Terminal execution evidence is captured and documented.
- **Status**: Completed

---

### Story US-04: Docker Image Construction
- **User Story**: *As a DevOps engineer*, I want to package the application into a secure, standardized Docker image, *so that* the application can run consistently across any host environment.
- **Priority**: High
- **Acceptance Criteria**:
  1. A root `Dockerfile` using an official, maintained Node.js Alpine base image.
  2. Installs only production dependencies (`npm ci --omit=dev`) to minimize container image footprint.
  3. Runs under a non-root user (`node`) for container runtime security.
  4. Incorporates a `.dockerignore` file excluding `node_modules`, test files, documentation, and local credentials.
  5. Built image tags successfully using `docker build -t tax-calculator:latest .`.
- **Status**: Completed

---

### Story US-05: Local Container Execution & Verification
- **User Story**: *As a DevOps engineer*, I want to run the containerized Tax Calculator in my local Docker environment, *so that* I can verify its web interface and health check endpoint before cloud deployment.
- **Priority**: High
- **Acceptance Criteria**:
  1. Container starts successfully via `docker run -d -p 3000:3000 --name tax-calculator tax-calculator:latest`.
  2. `GET /health` endpoint returns HTTP 200 with JSON payload `{"status":"UP", ...}`.
  3. Web browser accesses `http://localhost:3000` and displays interactive UI.
  4. Calculations perform identically inside container to local Node.js environment.
  5. Container stops and cleans up cleanly via `docker stop` and `docker rm`.
- **Status**: Completed

---

### Story US-06: IBM Cloud Container Registry Integration
- **User Story**: *As a DevOps engineer*, I want to authenticate with IBM Cloud Container Registry (ICR) and push tagged images, *so that* the container image is available for cloud hosting platforms.
- **Priority**: Medium
- **Acceptance Criteria**:
  1. CLI authentication succeeds via `ibmcloud cr login`.
  2. Local image is tagged to match registry convention: `<REGISTRY_HOST>/<NAMESPACE>/tax-calculator:<TAG>`.
  3. Image pushes to ICR without permission errors.
  4. `ibmcloud cr images` confirms the repository, tag, digest, and vulnerability scan status.
- **Status**: Completed

---

### Story US-07: Application Deployment on IBM Cloud
- **User Story**: *As a DevOps engineer*, I want to deploy the Tax Calculator container image to IBM Cloud Code Engine or Kubernetes, *so that* taxpayers can access the application over public HTTPS.
- **Priority**: High
- **Acceptance Criteria**:
  1. Application deploys successfully via `ibmcloud ce application create`.
  2. Public HTTPS endpoint is provisioned and resolves worldwide.
  3. Traffic routes to active instances with configured minimum scale and resource limits.
  4. Cloud application responds to `/health` probes and calculates tax accurately.
- **Status**: Completed

---

### Story US-08: Tekton Pipeline Task Creation
- **User Story**: *As a CI/CD engineer*, I want modular, reusable Tekton Tasks for source checkout, dependency installation, unit testing, container build/push, and cloud deployment, *so that* CI/CD operations are isolated and standardized.
- **Priority**: High
- **Acceptance Criteria**:
  1. Tekton Task manifests defined in `tekton/tasks.yaml` using `tekton.dev/v1beta1`.
  2. `npm` task executes `npm install` within the shared workspace.
  3. `jasmine` task executes `npm test` and halts upon test failures.
  4. `buildah` task builds container image and pushes to ICR securely using workspace credentials.
  5. `deploy` task updates cloud deployment with newly generated image.
- **Status**: Completed

---

### Story US-09: Automated Testing & Image Build Pipeline
- **User Story**: *As a CI/CD engineer*, I want a unified Tekton Pipeline connecting all tasks in strict dependency order, *so that* every code change is validated before image creation.
- **Priority**: High
- **Acceptance Criteria**:
  1. Declarative `tekton/pipeline.yaml` connecting: `clone-repo` → `install-dependencies` → `run-unit-tests` → `build-and-push-image` → `deploy-application`.
  2. Tasks execute sequentially using `runAfter` specifications.
  3. Unit test failures immediately stop the pipeline and prevent image build or push.
  4. Image tags reference commit SHA or build ID dynamically.
- **Status**: Completed

---

### Story US-10: Continuous Deployment of Pipeline-Built Image
- **User Story**: *As a CI/CD engineer*, I want the Tekton pipeline to update the IBM Cloud deployment with the newly built container image, *so that* production continuously reflects tested code without manual intervention.
- **Priority**: High
- **Acceptance Criteria**:
  1. Pipeline passes output image digest/tag to the deployment step.
  2. Cloud application deployment is updated to route 100% traffic to the new revision.
  3. Verified via `ibmcloud ce application get` showing the pipeline image URL and active instances.
  4. Complete execution logs recorded in assignment evidence files.
- **Status**: Completed
