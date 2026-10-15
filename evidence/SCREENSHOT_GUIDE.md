# Screenshot Guide: DevOps Assignment Evidence

This guide outlines exactly which screenshots to capture for submission, what commands to run to produce each view, and the key elements evaluators look for.

---

## Screenshot Checklist Overview

| # | Item to Capture | Required Command / URL | Key Elements to Show |
|---|---|---|---|
| **1** | Jasmine Tests Passing | `npm test` | "7 specs, 0 failures" |
| **2** | Docker Image Build | `docker build -t tax-calculator:latest .` | Steps executing & "Successfully built" |
| **3** | Local Container & Health Check | `docker ps` & `curl http://localhost:3000/health` | Container "Up", HTTP 200 `{"status":"UP"}` |
| **4** | Running Tax Calculator in Browser | Browser at `http://localhost:3000` | Populated inputs, calculation results displayed |
| **5** | IBM Cloud Container Registry Image | `ibmcloud cr images --restrict $SN_ICR_NAMESPACE` | Image repository URL, tag `v1`, "No Issues" status |
| **6** | IBM Cloud Code Engine Deployment | `ibmcloud ce app get --name tax-calculator` | Status: `Ready`, Public URL, 1 instance running |
| **7** | Tekton Pipeline Execution | `tkn pipeline start ... --showlog` | All tasks succeeded (exit code 0) |
| **8** | Updated Deployment with Pipeline Image | `ibmcloud ce app get --name tax-calculator` | Image tag `:latest`, 100% traffic to newest revision |

---

## Detailed Step-by-Step Screenshot Capture Instructions

### 1. Jasmine Unit Tests Passing
1. Open your terminal in the project root:
   ```bash
   npm test
   ```
2. Verify output displays:
   ```text
   Started
   .......
   7 specs, 0 failures
   Finished in 0.002 seconds
   ```
3. **Capture**: Screenshot of the full terminal window clearly showing the command `npm test` and the `7 specs, 0 failures` summary line.
4. **Save As**: `evidence/screenshot-01-jasmine-tests.png`

---

### 2. Docker Image Build
1. In your terminal, execute:
   ```bash
   docker build -t tax-calculator:latest .
   ```
2. Wait for the build steps to complete.
3. **Capture**: Terminal window showing the completed build steps ending in:
   ```text
   Successfully built <IMAGE_ID>
   Successfully tagged tax-calculator:latest
   ```
4. **Save As**: `evidence/screenshot-02-docker-build.png`

---

### 3. Local Container Running & Health Check
1. Start the container:
   ```bash
   docker run -d --name tax-calculator -p 3000:3000 tax-calculator:latest
   ```
2. Check running container status and verify health endpoint:
   ```bash
   docker ps
   curl -i http://localhost:3000/health
   ```
3. **Capture**: Terminal window showing both the `docker ps` output (confirming `tax-calculator` is `Up`) and the HTTP 200 response from `/health`.
4. **Save As**: `evidence/screenshot-03-container-health.png`

---

### 4. Running Tax Calculator in Browser
1. Open your web browser and navigate to:
   ```text
   http://localhost:3000
   ```
2. Enter test values:
   - **Gross Annual Income**: `60000`
   - **Total Deductions**: `5000`
3. Click **Calculate Tax**.
4. Confirm summary appears:
   - Taxable Income: `$55,000.00`
   - Estimated Tax: `$6,000.00`
   - Net Take-Home Pay: `$49,000.00`
   - Effective Tax Rate: `10.00%`
5. **Capture**: Browser window showing the calculator header, inputs, and the calculation results card.
6. **Save As**: `evidence/screenshot-04-browser-app.png`

---

### 5. IBM Cloud Container Registry Image
1. From IBM Cloud CLI or IBM Cloud Shell:
   ```bash
   ibmcloud cr images --restrict $SN_ICR_NAMESPACE
   ```
2. **Capture**: Terminal output displaying repository `us.icr.io/$SN_ICR_NAMESPACE/tax-calculator` with tag `v1` and security status `No Issues`.
3. **Save As**: `evidence/screenshot-05-icr-images.png`

---

### 6. IBM Cloud Application Deployed
1. Check Code Engine status:
   ```bash
   ibmcloud ce application get --name tax-calculator
   ```
2. Open the public URL in your browser and calculate tax.
3. **Capture**:
   - Terminal window showing `Status: Ready` and the public URL.
   - Browser showing the live app running on `*.codeengine.appdomain.cloud`.
4. **Save As**: `evidence/screenshot-06-cloud-deployment.png`

---

### 7. Tekton Pipeline Execution
1. Run the pipeline:
   ```bash
   tkn pipeline start tax-calculator-pipeline \
     -w name=pipeline-shared-workspace,claimName=pipeline-pvc \
     -p git-url="https://github.com/<YOUR-GITHUB-USERNAME>/tax-calculator.git" \
     -p git-revision="main" \
     -p image-name="us.icr.io/$SN_ICR_NAMESPACE/tax-calculator:latest" \
     --showlog
   ```
2. **Capture**: Terminal showing all tasks completing with checkmarks and final line:
   ```text
   STATUS: Succeeded (All tasks completed with exit code 0)
   ```
3. **Save As**: `evidence/screenshot-07-tekton-pipeline.png`

---

### 8. Updated Deployment with Pipeline Image
1. Query Code Engine application status:
   ```bash
   ibmcloud ce application get --name tax-calculator
   ```
2. Verify traffic points 100% to the latest revision with `image: us.icr.io/$SN_ICR_NAMESPACE/tax-calculator:latest`.
3. **Capture**: Terminal displaying the updated application status and latest revision routing.
4. **Save As**: `evidence/screenshot-08-pipeline-deployed.png`
