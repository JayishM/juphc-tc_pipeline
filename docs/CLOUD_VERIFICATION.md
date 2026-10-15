# Cloud Verification Guide: Deploying Tax Calculator on IBM Cloud

This guide provides deployment and verification instructions for running the containerized Tax Calculator application on **IBM Cloud Code Engine** (serverless container runtime) as well as **IBM Cloud Kubernetes Service (IKS) / Red Hat OpenShift on IBM Cloud (ROKS)**.

---

## 1. Deployment Target Options & Cost Transparency

| Deployment Option | Ideal For | Prerequisites / Cost Profile |
|---|---|---|
| **Option A: IBM Cloud Code Engine (Recommended)** | Microservices & Web Apps | **Free Tier Available** (100,000 vCPU-seconds/mo free). Serverless scaling from 0 to N instances. No persistent cluster costs. |
| **Option B: IBM Cloud Kubernetes / OpenShift** | Enterprise CI/CD & Tekton In-Cluster Pipelines | Requires active Kubernetes/OpenShift cluster. Paid worker nodes. |

> [!NOTE]
> For standard student labs and DevOps assignment grading, **IBM Cloud Code Engine** is the preferred and evaluated platform because it runs directly from IBM Cloud Container Registry images with instant public HTTPS endpoints and zero idle infrastructure cost.

---

## 2. Configuration Parameters

Use the following parameters consistently:

```bash
export REGION="us-south"
export REGISTRY_HOST="us.icr.io"
export NAMESPACE="<YOUR_ICR_NAMESPACE>"
export PROJECT_NAME="tax-calculator-project"
export APP_NAME="tax-calculator"
export IMAGE_URL="${REGISTRY_HOST}/${NAMESPACE}/tax-calculator:v1"
```

---

## 3. Option A: Deployment on IBM Cloud Code Engine

### Step 1: Create or Select a Code Engine Project

```bash
# Create a Code Engine project in your targeted resource group
ibmcloud ce project create --name $PROJECT_NAME

# Target the newly created project
ibmcloud ce project select --name $PROJECT_NAME
```

### Step 2: Deploy the Application

Deploy the container image with port 3000 (or port 80 if using the Nginx variant), public ingress, and minimum scale 1:

```bash
ibmcloud ce application create \
  --name $APP_NAME \
  --image $IMAGE_URL \
  --port 3000 \
  --min-scale 1 \
  --max-scale 5 \
  --cpu 0.25 \
  --memory 0.5G \
  --env PORT=3000 \
  --env NODE_ENV=production
```

Expected output:
```text
Creating application 'tax-calculator'...
Configuration 'tax-calculator' is waiting for a Revision to become ready.
Ingress has not yet been reconciled.
Waiting for load balancer to be ready.
Application 'tax-calculator' is created.
Run 'ibmcloud ce application get --name tax-calculator' to check the application status.
OK
```

---

## 4. Option B: Kubernetes / OpenShift Deployment Manifests

If deploying to an existing Kubernetes or OpenShift cluster, apply the standard deployment and service manifests:

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tax-calculator
  labels:
    app: tax-calculator
spec:
  replicas: 2
  selector:
    matchLabels:
      app: tax-calculator
  template:
    metadata:
      labels:
        app: tax-calculator
    spec:
      containers:
        - name: tax-calculator
          image: us.icr.io/<YOUR_ICR_NAMESPACE>/tax-calculator:v1
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
          env:
            - name: PORT
              value: "3000"
            - name: NODE_ENV
              value: "production"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "250m"
              memory: "256Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: tax-calculator-service
spec:
  type: LoadBalancer
  selector:
    app: tax-calculator
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
```

Apply to cluster:
```bash
kubectl apply -f k8s-deployment.yaml
kubectl rollout status deployment/tax-calculator
```

---

## 5. Deployment Verification Checklist

### 5.1 Retrieve Public Endpoint & Application Status

For Code Engine:
```bash
ibmcloud ce application get --name $APP_NAME
```

Inspect output fields:
- **Status**: Must display `Ready`.
- **URL**: Note the public HTTPS URL (e.g. `https://tax-calculator.1a2b3c4d.us-south.codeengine.appdomain.cloud`).
- **Instances**: `1 running, 0 pending, 0 failed`.

### 5.2 Stream Application Logs

Inspect live container logs to verify clean startup:

```bash
ibmcloud ce application logs --name $APP_NAME
```

Expected log output:
```text
Tax Calculator server running on port 3000
Health check available at http://localhost:3000/health
```

### 5.3 Verify Public Health Check Endpoint

Query the `/health` endpoint over public HTTPS:

```bash
curl -i https://<PUBLIC_APP_URL>/health
```

Expected response:
```http
HTTP/2 200
content-type: application/json; charset=utf-8

{"status":"UP","service":"tax-calculator","version":"1.0.0","uptime":45.2,"timestamp":"..."}
```

### 5.4 Test Calculation via Public Endpoint

Verify backend calculation over the public URL:

```bash
curl -X POST https://<PUBLIC_APP_URL>/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"income": 100000, "deductions": 0}'
```

Expected response:
```json
{"grossIncome":100000,"deductions":0,"taxableIncome":100000,"tax":17000,"netIncome":83000,"effectiveRate":17}
```

### 5.5 Browser Verification
1. Navigate to `https://<PUBLIC_APP_URL>`.
2. Input **Gross Annual Income**: `$60,000`.
3. Input **Total Deductions**: `$5,000`.
4. Click **Calculate Tax**.
5. Confirm results:
   - Taxable Income: `$55,000.00`
   - Estimated Tax: `$6,000.00`
   - Net Take-Home Pay: `$49,000.00`
   - Effective Tax Rate: `10.00%`
6. Click **Reset** and confirm fields return to defaults.
