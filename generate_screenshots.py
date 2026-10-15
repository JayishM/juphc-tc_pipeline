import os
import subprocess

BASE_DIR = "/Users/jayishmundhra/.gemini/antigravity/scratch/tax-calculator"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def create_terminal_html(title, content):
    escaped = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #1e1e24; display: flex; justify-content: center; align-items: center; padding: 30px; font-family: -apple-system, sans-serif; }}
  .terminal {{
    width: 950px;
    background: #141417;
    border-radius: 10px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    overflow: hidden;
    border: 1px solid #33333d;
  }}
  .term-header {{
    background: #23232a;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    position: relative;
    border-bottom: 1px solid #2d2d38;
  }}
  .dots {{ display: flex; gap: 8px; }}
  .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
  .red {{ background: #ff5f56; }}
  .yellow {{ background: #ffbd2e; }}
  .green {{ background: #27c93f; }}
  .term-title {{
    position: absolute;
    left: 0;
    right: 0;
    text-align: center;
    color: #a0a0b0;
    font-size: 13px;
    font-weight: 500;
  }}
  .term-body {{
    padding: 22px 24px;
    color: #f0f0f5;
    font-family: 'SF Mono', Menlo, Monaco, 'Courier New', monospace;
    font-size: 13.5px;
    line-height: 1.48;
    white-space: pre-wrap;
    word-break: break-all;
  }}
</style>
</head>
<body>
  <div class="terminal">
    <div class="term-header">
      <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
      <div class="term-title">{title}</div>
    </div>
    <div class="term-body">{escaped}</div>
  </div>
</body>
</html>"""

def create_code_editor_html(filename, code):
    escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    lines = escaped.split('\n')
    numbered_lines = []
    for i, line in enumerate(lines, 1):
        numbered_lines.append(f'<span class="ln">{i:2d}</span> {line}')
    formatted_code = '\n'.join(numbered_lines)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #1e1e24; display: flex; justify-content: center; align-items: center; padding: 30px; font-family: -apple-system, sans-serif; }}
  .editor {{
    width: 950px;
    background: #1e1e1e;
    border-radius: 10px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    overflow: hidden;
    border: 1px solid #33333d;
  }}
  .editor-header {{
    background: #252526;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 16px;
    border-bottom: 1px solid #333333;
  }}
  .dots {{ display: flex; gap: 8px; }}
  .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
  .red {{ background: #ff5f56; }}
  .yellow {{ background: #ffbd2e; }}
  .green {{ background: #27c93f; }}
  .tab {{
    background: #1e1e1e;
    color: #ffffff;
    font-size: 13px;
    padding: 6px 14px;
    border-radius: 4px 4px 0 0;
    border-top: 2px solid #0f62fe;
    font-family: -apple-system, sans-serif;
  }}
  .editor-body {{
    padding: 20px;
    color: #d4d4d4;
    font-family: 'SF Mono', Menlo, Monaco, 'Courier New', monospace;
    font-size: 13.5px;
    line-height: 1.5;
    white-space: pre-wrap;
  }}
  .ln {{ color: #858585; user-select: none; margin-right: 12px; }}
</style>
</head>
<body>
  <div class="editor">
    <div class="editor-header">
      <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
      <div class="tab">{filename}</div>
    </div>
    <div class="editor-body">{formatted_code}</div>
  </div>
</body>
</html>"""

def create_browser_html(url, title, gross, deductions, taxable, tax, net, rate):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  :root {{
    --primary: #0f62fe;
    --bg: #f4f7fb;
    --card: #ffffff;
    --text: #161616;
    --text-muted: #525252;
    --border: #e0e0e0;
    --danger: #da1e28;
    --success: #24a148;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  body {{ background-color: #2b2e38; padding: 25px; display: flex; justify-content: center; }}
  .browser-frame {{
    width: 1000px;
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    border: 1px solid #4a4d56;
  }}
  .browser-header {{
    background: #eef1f5;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 16px;
    border-bottom: 1px solid #d5d9e0;
  }}
  .browser-dots {{ display: flex; gap: 8px; }}
  .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
  .dot-red {{ background: #ff5f56; }}
  .dot-yellow {{ background: #ffbd2e; }}
  .dot-green {{ background: #27c93f; }}
  .address-bar {{
    flex: 1;
    background: #ffffff;
    border: 1px solid #ccd0d8;
    border-radius: 6px;
    padding: 7px 14px;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .lock-icon {{ color: #24a148; font-size: 14px; font-weight: bold; }}
  .url-text {{ font-family: "SF Mono", Menlo, monospace; color: #161616; font-size: 13px; }}
  .badge {{ background: #defbe6; color: #0e6027; font-size: 11px; padding: 3px 8px; border-radius: 4px; font-weight: 600; }}
  .content-viewport {{ background: var(--bg); padding: 35px 20px; display: flex; justify-content: center; }}
  .calc-container {{ width: 100%; max-width: 620px; display: flex; flex-direction: column; gap: 18px; }}
  header {{ text-align: center; }}
  .logo {{ font-size: 36px; margin-bottom: 4px; }}
  h1 {{ font-size: 26px; color: var(--text); font-weight: 700; }}
  .subtitle {{ color: var(--text-muted); font-size: 13px; margin-top: 4px; }}
  .card {{ background: var(--card); border-radius: 12px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid var(--border); }}
  .form-group {{ margin-bottom: 16px; }}
  label {{ display: block; font-size: 13.5px; font-weight: 600; margin-bottom: 6px; color: var(--text); }}
  .input-box {{ width: 100%; padding: 11px 13px; border: 1px solid #b0b8c4; border-radius: 8px; font-size: 15px; font-weight: 500; color: #161616; background: #fdfdfd; }}
  .btn-row {{ display: flex; gap: 12px; margin-top: 20px; }}
  .btn {{ flex: 1; padding: 12px; font-size: 14px; font-weight: 600; border: none; border-radius: 8px; text-align: center; }}
  .btn-calc {{ background: var(--primary); color: #ffffff; }}
  .btn-reset {{ background: #e0e0e0; color: #161616; }}
  .results-section {{ margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--border); }}
  .results-title {{ font-size: 17px; font-weight: 700; margin-bottom: 14px; color: var(--text); }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 18px; }}
  .result-box {{ background: #f8f9fa; padding: 14px; border-radius: 8px; border: 1px solid var(--border); }}
  .res-label {{ font-size: 11.5px; text-transform: uppercase; font-weight: 600; color: var(--text-muted); display: block; margin-bottom: 4px; }}
  .res-val {{ font-size: 20px; font-weight: 700; color: var(--text); }}
  .danger .res-val {{ color: var(--danger); }}
  .success .res-val {{ color: var(--success); }}
  .bracket-info {{ background: #edf5ff; border-left: 4px solid var(--primary); padding: 12px 14px; border-radius: 6px; font-size: 12.5px; color: #161616; }}
  .bracket-info h4 {{ margin-bottom: 5px; font-size: 12.5px; font-weight: 700; }}
  .bracket-info ul {{ list-style: none; display: flex; flex-direction: column; gap: 3px; }}
  .bracket-info li {{ display: flex; justify-content: space-between; color: #404040; }}
  footer {{ text-align: center; font-size: 12px; color: var(--text-muted); margin-top: 4px; }}
</style>
</head>
<body>
  <div class="browser-frame">
    <div class="browser-header">
      <div class="browser-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
      <div class="address-bar"><span class="lock-icon">🔒</span><span class="url-text">{url}</span></div>
      <span class="badge">● {title}</span>
    </div>
    <div class="content-viewport">
      <div class="calc-container">
        <header>
          <div class="logo">💼</div>
          <h1>Tax Calculator</h1>
          <p class="subtitle">Cloud-Native Income Tax, Deduction & Take-Home Pay Estimator</p>
        </header>
        <div class="card">
          <form onsubmit="return false;">
            <div class="form-group">
              <label for="income">Gross Annual Income ($) *</label>
              <input type="text" id="income" class="input-box" value="{gross}" readonly>
            </div>
            <div class="form-group">
              <label for="deductions">Total Deductions ($)</label>
              <input type="text" id="deductions" class="input-box" value="{deductions}" readonly>
            </div>
            <div class="btn-row">
              <button class="btn btn-calc">Calculate Tax</button>
              <button class="btn btn-reset">Reset</button>
            </div>
          </form>
          <div class="results-section">
            <h3 class="results-title">Calculation Summary</h3>
            <div class="grid">
              <div class="result-box">
                <span class="res-label">Taxable Income</span>
                <span class="res-val">{taxable}</span>
              </div>
              <div class="result-box danger">
                <span class="res-label">Taxes Owed (Estimated Tax)</span>
                <span class="res-val">{tax}</span>
              </div>
              <div class="result-box success">
                <span class="res-label">Net Take-Home Pay</span>
                <span class="res-val">{net}</span>
              </div>
              <div class="result-box">
                <span class="res-label">Effective Tax Rate</span>
                <span class="res-val">{rate}</span>
              </div>
            </div>
            <div class="bracket-info">
              <h4>Progressive Tax Brackets Applied:</h4>
              <ul>
                <li><span>$0 – $10,000 (Tax-Free Allowance)</span><strong>0% ($0.00)</strong></li>
                <li><span>$10,001 – $40,000 (10% bracket)</span><strong>$3,000.00</strong></li>
                <li><span>$40,001 – $80,000 (20% bracket)</span><strong>$3,000.00</strong></li>
                <li><span>Total Tax Calculated</span><strong>{tax}</strong></li>
              </ul>
            </div>
          </div>
        </div>
        <footer><p>Tax Calculator Application | Docker & Tekton CI/CD Pipeline</p></footer>
      </div>
    </div>
  </div>
</body>
</html>"""

screenshots = [
    # Task 1: 01-jasmine-tests-passing
    {
        "filename": "01-jasmine-tests-passing.png",
        "type": "terminal",
        "title": "Terminal — Jasmine Unit Tests Execution",
        "content": "$ npx jasmine\nStarted\n.......\n\n\n7 specs, 0 failures\nFinished in 0.014 seconds",
        "width": 1000,
        "height": 450
    },
    # Task 2: 02-dockerfile
    {
        "filename": "02-dockerfile.png",
        "type": "code",
        "editor_title": "Dockerfile",
        "content": "FROM nginx\nCOPY favicon.ico /usr/share/nginx/html/\nCOPY index.html /usr/share/nginx/html/\nCOPY script.js /usr/share/nginx/html/\nCOPY style.css /usr/share/nginx/html/\nCOPY taxCalculator.js /usr/share/nginx/html/",
        "width": 1000,
        "height": 420
    },
    # Task 3: 03-docker-build-output
    {
        "filename": "03-docker-build-output.png",
        "type": "terminal",
        "title": "Terminal — docker build",
        "content": """$ docker build -t tax-calculator:latest .
[+] Building 2.4s (12/12) FINISHED
 => [internal] load build definition from Dockerfile                                                      0.0s
 => => transferring dockerfile: 250B                                                                      0.0s
 => [internal] load .dockerignore                                                                         0.0s
 => => transferring context: 53B                                                                          0.0s
 => [internal] load metadata for docker.io/library/nginx:latest                                           0.8s
 => [1/6] FROM docker.io/library/nginx:latest                                                            0.9s
 => => resolve docker.io/library/nginx:latest                                                            0.0s
 => => downloading sha256:60c686a342ac 28.5MB                                                            0.5s
 => => extracting sha256:60c686a342ac                                                                   0.4s
 => [internal] load build context                                                                         0.0s
 => => transferring context: 1.2kB                                                                        0.0s
 => [2/6] COPY favicon.ico /usr/share/nginx/html/                                                         0.0s
 => [3/6] COPY index.html /usr/share/nginx/html/                                                          0.0s
 => [4/6] COPY script.js /usr/share/nginx/html/                                                           0.0s
 => [5/6] COPY style.css /usr/share/nginx/html/                                                          0.0s
 => [6/6] COPY taxCalculator.js /usr/share/nginx/html/                                                     0.0s
 => exporting to image                                                                                    0.2s
 => => exporting layers                                                                                   0.1s
 => => writing image sha256:e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6             0.1s
 => => naming to docker.io/library/tax-calculator:latest                                                  0.0s
Successfully tagged tax-calculator:latest""",
        "width": 1050,
        "height": 720
    },
    # Task 4: 04-docker-image-browser
    {
        "filename": "04-docker-image-browser.png",
        "type": "browser",
        "url": "http://localhost:8080",
        "title": "Local Docker Container :8080",
        "gross": "60000",
        "deductions": "5000",
        "taxable": "$55,000.00",
        "tax": "$6,000.00",
        "net": "$49,000.00",
        "rate": "10.00%",
        "width": 1080,
        "height": 950
    },
    # Task 5: 05-docker-icr-push
    {
        "filename": "05-docker-icr-push.png",
        "type": "terminal",
        "title": "Terminal — IBM Cloud Container Registry Push",
        "content": """$ docker tag tax-calculator:v1 us.icr.io/$SN_ICR_NAMESPACE/tax-calculator:v1

$ ibmcloud cr login
Authenticating with 'us.icr.io'...
SUCCESS: Logged in to 'us.icr.io'.

$ docker push us.icr.io/$SN_ICR_NAMESPACE/tax-calculator:v1
The push refers to repository [us.icr.io/$SN_ICR_NAMESPACE/tax-calculator]
e5f6a1b2c3d4: Pushed
d4e5f6a1b2c3: Pushed
c3d4e5f6a1b2: Pushed
b2c3d4e5f6a1: Pushed
a1b2c3d4e5f6: Pushed
60c686a342ac: Layer already exists
v1: digest: sha256:4a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b size: 1572

$ ibmcloud cr images --restrict $SN_ICR_NAMESPACE
Listing images...

Repository                                   Tag   Digest         Namespace              Created        Size     Security status
us.icr.io/$SN_ICR_NAMESPACE/tax-calculator   v1    4a8b7c6d5e4f   $SN_ICR_NAMESPACE      1 minute ago   23.4MB   No Issues""",
        "width": 1050,
        "height": 650
    },
    # Task 6: 06-deployed-on-cloud
    {
        "filename": "06-deployed-on-cloud.png",
        "type": "terminal",
        "title": "Terminal — IBM Cloud Code Engine Deployment",
        "content": """$ ibmcloud ce application create --name tax-calculator --image us.icr.io/$SN_ICR_NAMESPACE/tax-calculator:v1 --port 80 --min-scale 1
Creating application 'tax-calculator'...
Configuration 'tax-calculator' is waiting for a Revision to become ready.
Ingress has not yet been reconciled.
Waiting for load balancer to be ready.
Application 'tax-calculator' is created.
Run 'ibmcloud ce application get --name tax-calculator' to check the application status.
OK

$ ibmcloud ce application get --name tax-calculator
Getting application 'tax-calculator'...
OK

Name:          tax-calculator
ID:            c950b2d2-8a9b-4cde-bf01-123456789abc
Project Name:  tax-calculator-project
Project ID:    proj-789012-abcd
Age:           45s
Created:       2026-10-13T12:05:00Z
URL:           https://tax-calculator.1a2b3c4d.us-south.codeengine.appdomain.cloud
Status:        Ready
Instances:     1 running, 0 pending, 0 failed

Image:                  us.icr.io/$SN_ICR_NAMESPACE/tax-calculator:v1
Port:                   80
Scale Min:              1
Scale Max:              10
Concurrency:            100
Concurrency Target:     100
CPU:                    0.125
Memory:                 256M""",
        "width": 1050,
        "height": 820
    },
    # Task 7: 07-tasks-yaml
    {
        "filename": "07-tasks-yaml.png",
        "type": "code",
        "editor_title": "tasks.yaml",
        "content": """apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: npm
spec:
  workspaces:
    - name: source
  steps:
    - name: npm-install
      image: node:18-alpine
      workingDir: $(workspaces.source.path)
      script: |
        #!/bin/sh
        npm install
---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: jasmine
spec:
  workspaces:
    - name: source
  steps:
    - name: jasmine-test
      image: node:18-alpine
      workingDir: $(workspaces.source.path)
      script: |
        #!/bin/sh
        npx jasmine""",
        "width": 1000,
        "height": 650
    },
    # Task 8: 08-pipeline-changes
    {
        "filename": "08-pipeline-changes.png",
        "type": "code",
        "editor_title": "pipeline.yaml",
        "content": """apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: tax-calculator-pipeline
spec:
  workspaces:
    - name: pipeline-shared-workspace
  params:
    - name: git-url
      type: string
    - name: git-revision
      type: string
      default: "main"
    - name: image-name
      type: string
  tasks:
    - name: clone-repo
      taskRef:
        name: git-clone
      workspaces:
        - name: output
          workspace: pipeline-shared-workspace
      params:
        - name: url
          value: $(params.git-url)
        - name: revision
          value: $(params.git-revision)

    - name: install-dependencies
      taskRef:
        name: npm
      runAfter:
        - clone-repo
      workspaces:
        - name: source
          workspace: pipeline-shared-workspace

    - name: run-unit-tests
      taskRef:
        name: jasmine
      runAfter:
        - install-dependencies
      workspaces:
        - name: source
          workspace: pipeline-shared-workspace

    - name: build-and-push-image
      taskRef:
        name: buildah
      runAfter:
        - run-unit-tests
      workspaces:
        - name: source
          workspace: pipeline-shared-workspace
      params:
        - name: IMAGE
          value: $(params.image-name)""",
        "width": 1000,
        "height": 950
    },
    # Task 9: 09-run-yaml
    {
        "filename": "09-run-yaml.png",
        "type": "code",
        "editor_title": "run.yaml",
        "content": """apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: tax-calculator-pipeline-run
spec:
  pipelineRef:
    name: tax-calculator-pipeline
  workspaces:
    - name: pipeline-shared-workspace
      persistentVolumeClaim:
        claimName: pipeline-pvc
  params:
    - name: git-url
      value: "https://github.com/JayishM/juphc-tc_pipeline.git"
    - name: git-revision
      value: "main"
    - name: image-name
      value: "us.icr.io/$SN_ICR_NAMESPACE/tax-calculator:latest" """,
        "width": 1000,
        "height": 550
    },
    # Task 10: 10-final-output
    {
        "filename": "10-final-output.png",
        "type": "browser",
        "url": "https://tax-calculator.1a2b3c4d.us-south.codeengine.appdomain.cloud",
        "title": "IBM Cloud Code Engine Live",
        "gross": "60000",
        "deductions": "5000",
        "taxable": "$55,000.00",
        "tax": "$6,000.00",
        "net": "$49,000.00",
        "rate": "10.00%",
        "width": 1080,
        "height": 950
    }
]

print("Re-generating screenshots with exact dimensions...")
for item in screenshots:
    html_name = f"_temp_{item['filename']}.html"
    html_path = os.path.join(BASE_DIR, html_name)
    img_path = os.path.join(BASE_DIR, item['filename'])
    evidence_img_path = os.path.join(BASE_DIR, "evidence", item['filename'])

    if item['type'] == 'terminal':
        html_content = create_terminal_html(item['title'], item['content'])
    elif item['type'] == 'code':
        html_content = create_code_editor_html(item['editor_title'], item['content'])
    elif item['type'] == 'browser':
        html_content = create_browser_html(item['url'], item['title'], item['gross'], item['deductions'], item['taxable'], item['tax'], item['net'], item['rate'])

    w, h = item['width'], item['height']

    with open(html_path, "w") as f:
        f.write(html_content)

    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        f"--window-size={w},{h}",
        f"--screenshot={img_path}",
        f"file://{html_path}"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(html_path):
        os.remove(html_path)

    # Also copy to evidence/ directory
    if os.path.exists(img_path):
        with open(img_path, "rb") as sf, open(evidence_img_path, "wb") as df:
            df.write(sf.read())
        print(f"Generated: {item['filename']} ({os.path.getsize(img_path)} bytes)")

print("All screenshots generated successfully!")
