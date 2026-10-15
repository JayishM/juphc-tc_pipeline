# Epic: Modernize and Deploy the Tax Calculator Application Using DevOps

## 1. Project Objective and Business Value

The objective of this project is to transform a legacy static tax calculation utility into a cloud-native, production-ready web application backed by modern DevOps practices, containerization, and automated CI/CD pipelines.

### Business Value
- **Accuracy & Reliability**: Provides verified, error-free progressive tax calculation and deduction modeling for individual taxpayers, preventing costly financial calculation mistakes.
- **High Availability & Scalability**: Containerization with Docker and deployment on IBM Cloud ensures the application can scale seamlessly to meet surging user demand during peak tax seasons.
- **Rapid, Risk-Free Delivery**: Automated CI/CD pipelines using Tekton guarantee that every code change is validated through unit tests before container images are built and deployed, eliminating human deployment errors.
- **Maintainability & Portability**: Standardized container packaging ensures consistent behavior across developer workstations, automated test runners, and production cloud environments.

---

## 2. Scope of Modernization

### 2.1 Application Modernization
- Transform the static frontend into a full-stack, modular web application powered by Node.js and Express.
- Introduce an architectural separation of concerns:
  - **Core Business Logic**: Independent, pure JavaScript calculation module (`taxCalculator.js`) reusable across client and server runtimes.
  - **Application Server**: Express-based server (`server.js`) exposing a dedicated `/health` check endpoint for Kubernetes/container probes and an API calculation endpoint (`/api/calculate`).
  - **Modern User Experience**: Mobile-first, accessible, responsive interface featuring inline validation, instant tax bracket breakdown, and form reset capabilities.

### 2.2 Containerization Using Docker
- Author a production-grade multi-stage `Dockerfile` leveraging a secure Node.js Alpine base.
- Implement security best practices: running as a non-privileged `node` user, minimal layer footprints, proper `.dockerignore` filters, and explicit port exposure.
- Standardize local development workflows via container build, run, and local verification procedures.

### 2.3 Cloud Deployment on IBM Cloud
- Configure IBM Cloud Container Registry (ICR) for secure, private container image hosting.
- Deploy the containerized application on IBM Cloud Code Engine (serverless container platform) and Kubernetes/OpenShift targets with automatic TLS, health checks, and public HTTPS ingress.

### 2.4 Automated Unit Testing with Jasmine
- Implement comprehensive unit tests covering all tax brackets, edge cases (zero income, boundary values), deduction subtractions, and negative input validations.
- Integrate Jasmine test execution into the local developer lifecycle (`npm test`) and the CI/CD pipeline.

### 2.5 Automated CI/CD Using Tekton
- Implement declarative Tekton Task and Pipeline resources.
- Construct an end-to-end delivery pipeline orchestrating:
  1. Git repository cloning.
  2. Dependency installation (`npm install`).
  3. Automated unit testing (`jasmine`).
  4. Container image build and push (`buildah` / ICR).
  5. Automated continuous deployment (`ibmcloud ce application update` / Kubernetes rollout).

---

## 3. Acceptance Criteria

1. **Jasmine Unit Tests**: 100% of Jasmine test specs must execute and pass without failures.
2. **Container Image**: Docker image builds cleanly, includes no build-time development dependencies, runs as non-root user, and passes container health checks.
3. **Local Container Execution**: Application container runs locally, serving the UI and responding to `GET /health` with HTTP 200.
4. **Registry Integration**: Docker image tags adhere to semantic versioning / commit SHA conventions and push successfully to IBM Cloud Container Registry.
5. **Cloud Deployment**: Application deploys to IBM Cloud with an active public HTTPS endpoint and 100% healthy revision status.
6. **Pipeline Automation**: Tekton pipeline executes all stages sequentially; any failing test immediately terminates the pipeline and prevents image publishing or deployment.
7. **Traceability**: The deployed cloud application revision strictly references the exact container image tag produced by the pipeline run.

---

## 4. Definition of Done (DoD)

- [x] Application source code, tests, and configurations are committed to version control.
- [x] All 7 Jasmine unit test specifications pass locally and within pipeline containers.
- [x] Production `Dockerfile`, `.dockerignore`, and `.env.example` are created and verified.
- [x] Tekton Tasks (`npm`, `jasmine`, `build-and-push`, `deploy`) and Pipeline manifests are authored and syntactically validated.
- [x] Comprehensive documentation covering Docker workflows, IBM Cloud setup, and Tekton operations is published in `docs/`.
- [x] Concrete verification logs and evidence files are documented in `evidence/`.
- [x] Root `README.md` details all 10 grading criteria with mapping to project deliverables.
