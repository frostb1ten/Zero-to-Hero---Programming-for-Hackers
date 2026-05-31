# Day 1: Reading Other People's Code

## Why This Matters
Code review is the foundation of AppSec and bug bounty work.
You need to read code fast, trace data flow, and spot where
user input touches dangerous functions.

## The Code Review Mindset
1. **Where does user input enter?** (sources)
2. **Where does data do something dangerous?** (sinks)
3. **Does anything sanitize/validate between source and sink?**

If input reaches a sink without proper validation → vulnerability.

## Sources — Where User Data Enters
```python
# Web apps (Flask example)
request.args.get("id")       # URL parameters
request.form["username"]     # form data
request.headers["X-Token"]   # headers
request.cookies["session"]   # cookies
request.files["upload"]      # file uploads
request.get_json()["data"]   # JSON body

# CLI scripts
sys.argv[1]                  # command line args
input("Enter: ")             # user input
open(user_path).read()       # file contents

# Network
socket.recv(1024)            # raw socket data
```

## Sinks — Where Danger Lives
```python
# Command Injection
os.system(user_input)
subprocess.run(user_input, shell=True)
os.popen(cmd)

# SQL Injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
cursor.execute("SELECT * FROM users WHERE id = " + user_id)

# Path Traversal
open(f"/uploads/{filename}")
os.path.join("/var/data", user_path)

# Code Execution
eval(user_input)
exec(user_input)
__import__(module_name)

# Deserialization
pickle.loads(user_data)
yaml.load(user_data)  # without Loader=SafeLoader

# SSRF
requests.get(user_url)
urllib.request.urlopen(user_url)
```

## How to Read Code Systematically
```
Step 1: Identify the entry points
   - Routes in web apps (@app.route)
   - main() in scripts
   - Functions that accept external data

Step 2: Trace the data flow
   - Follow each input through the code
   - Note every transformation, validation, sanitization
   - Note every time it touches a sink

Step 3: Check the controls
   - Is there input validation? Is it sufficient?
   - Is there output encoding?
   - Are parameterized queries used?
   - Is authentication/authorization checked?

Step 4: Note the assumptions
   - What does the developer assume is safe?
   - Are those assumptions always true?
```

## Pattern Matching — What to grep For
```bash
# Command injection
grep -rn "os.system\|subprocess.*shell=True\|os.popen" .

# SQL injection
grep -rn "execute.*f\"\|execute.*+" .

# Code execution
grep -rn "eval(\|exec(\|__import__" .

# Deserialization
grep -rn "pickle.loads\|yaml.load\|json.loads" .

# Hardcoded secrets
grep -rn "password\s*=\|api_key\s*=\|secret\s*=" .

# Debug mode
grep -rn "debug\s*=\s*True\|DEBUG\s*=\s*True" .
```

## Reading Code You Don't Understand
1. Start at `main()` or the entry point
2. Read function names — they tell the story
3. Ignore implementation details on first pass
4. Focus on the **data flow**, not the logic
5. Draw it out: input → function → function → output
