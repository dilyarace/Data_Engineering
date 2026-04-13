# Task 3 — LCM Web Endpoint

An internship assignment focused on building and deploying a publicly accessible HTTP endpoint that computes the Lowest Common Multiple (LCM) of two numbers.

## Problem Statement

Implement a web method accessible via HTTP GET that:

1. Accepts two natural numbers `x` and `y` as query parameters
2. Returns their **Lowest Common Multiple (LCM)** as a plain string containing only digits
3. Returns the string `NaN` if either `x` or `y` is not a valid natural number (e.g. a letter, a float, zero, or a negative number)
4. Is deployed on the Internet at a URL ending with your email address (all non-alphanumeric characters replaced with underscores)

**Example URL:**
```
https://your-app.onrender.com/dilyarace_gmail_com?x=4&y=6
```
**Expected response:** `12`

## What I Learned

### HTTP and GET Requests

**HTTP (HyperText Transfer Protocol)** is the language that browsers and servers use to talk to each other.

When you type a URL in a browser, you are making an **HTTP GET request** — you are asking the server to *give you* something.

```
https://your-app.onrender.com/dilyarace_gmail_com?x=4&y=6
│                             │                   │
└── domain (where the server) └── route (path)    └── query parameters
```

**Query parameters** are key-value pairs added after `?` in the URL:
- `?x=4&y=6` means: parameter `x` equals `4`, parameter `y` equals `6`
- The `&` symbol separates multiple parameters
- The server reads these values and uses them in the logic

### Routes / Endpoints

A **route** (also called an endpoint) is a specific URL path on a server that does something when visited.

Think of a server like a building, and routes like different rooms:
- `/dilyarace_gmail_com` → the room that computes LCM
- `/` → the main entrance (we didn't set this up, so it returns 404)

In Flask, a route is defined with a decorator `@app.route(...)` placed above a function. When someone visits that path, Flask runs that function and returns its result.

### Flask

**Flask** is a lightweight Python library for building web servers. It handles all the complex networking so you only need to write the logic.

```python
from flask import Flask, request

app = Flask(__name__)        # create the app
@app.route("/some_path")     # define a route
def my_function():
    return "Hello"           # what to return when visited
```

`request.args.get("x")` — this is how Flask reads query parameters from the URL. It returns the value as a **string**, so you must convert it to an integer with `int()` before doing math.

### LCM — Lowest Common Multiple

The **LCM** of two numbers is the smallest number that is divisible by both.

```
LCM(4, 6) = 12   because 12 ÷ 4 = 3  and  12 ÷ 6 = 2
```

LCM is calculated using **GCD (Greatest Common Divisor)**:

```
LCM(x, y) = (x * y) / GCD(x, y)
```

**GCD** is the largest number that divides both `x` and `y` without a remainder.

```
GCD(4, 6) = 2   →   LCM = (4 * 6) / 2 = 12
```

Python has a built-in function `math.gcd()`:

```python
import math
math.gcd(4, 6)              # → 2
(4 * 6) // math.gcd(4, 6)  # → 12
```

> Note: Use `//` (integer division) instead of `/` to avoid getting a float like `12.0` instead of `12`.

### Input Validation

The task says: if either input is not a valid **natural number**, return `"NaN"`.

**Natural numbers** = positive integers: 1, 2, 3, 4, ...
Not valid: letters, floats, zero, negative numbers.

This is handled with a `try/except` block:
- `int("abc")` raises an error → caught by `except` → return `"NaN"`
- `int("3.5")` also raises an error → `"NaN"`
- `int("0")` succeeds but `0 <= 0` → return `"NaN"`
- `int("-5")` succeeds but `-5 <= 0` → return `"NaN"`

### Big Numbers

Python handles integers of **any size** natively — no overflow. This is important because the mentor tests with very large numbers:

```
x = 4294967311
y = 4294967357
LCM = 18446744400127067027
```

Many other languages (like Java or C) would overflow here and give a wrong answer. Python just works.

### Deployment

**Deploying** means putting your code on a server in the internet so anyone can access it.

| Term | Meaning |
|---|---|
| **Local** | Running on your own computer, only you can access it (`127.0.0.1`) |
| **Deploy** | Uploading code to a hosting provider so it runs on their server |
| **Hosting** | A service that runs your code 24/7 on a real server |
| **PORT** | The "door number" the server listens on. Hosting providers set this via environment variable |

**Why `host="0.0.0.0"`?**
By default Flask only listens on `127.0.0.1` (your own machine). Setting `0.0.0.0` means "listen on all network interfaces" — required for hosting providers to be able to reach your server.

**Why `os.environ.get("PORT")`?**
Hosting providers (like Render) assign a random port and tell your app via an environment variable called `PORT`. If you hardcode port `5000`, it won't work on the server.

```python
port = int(os.environ.get("PORT", 5000))
# use PORT from environment, fall back to 5000 locally
```

### Render.com — Free Hosting

**Render** is a free hosting platform. It connects to your GitHub repository and automatically builds and runs your app.

Required files for Python deployment:
- `app.py` — your application code
- `requirements.txt` — list of external libraries Render needs to install

```
# requirements.txt
flask
```

> ⚠️ On the free plan, the server "sleeps" after 15 minutes of inactivity and takes ~50 seconds to wake up. Always open the URL in a browser before submitting to the mentor — this "wakes up" the server.

## Project Structure

```
task_3/
├── app.py              # Flask web server with LCM logic
└── requirements.txt    # Dependencies (flask)
```

## Full Code

```python
import math
import os
from flask import Flask, request

# create the web app
app = Flask(__name__)

# when someone opens this URL path - run the function below
@app.route("/dilyarace_gmail_com")
def lcm_endpoint():

    # grab x and y from the URL like ?x=4&y=6
    x_str = request.args.get("x")
    y_str = request.args.get("y")

    try:
        # convert text to whole numbers
        x = int(x_str)
        y = int(y_str)

        # only natural numbers allowed (1, 2, 3 ... not 0 or negative)
        if x <= 0 or y <= 0:
            return "NaN"

        # calculate LCM using the formula: LCM = (x * y) / GCD
        result = (x * y) // math.gcd(x, y)

        # return the answer as plain text, no spaces or extra characters
        return str(result)

    except:
        # if x or y is not a valid number (like a letter) - return NaN
        return "NaN"

# start the server
# PORT comes from the hosting environment, locally defaults to 5000
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

## How to Run Locally

```bash
pip install flask
python3 app.py
```

Then open in browser:
```
http://127.0.0.1:5000/dilyarace_gmail_com?x=4&y=6
```

## Test Cases

| Input | Expected Output | Reason |
|---|---|---|
| `x=4&y=6` | `12` | LCM(4,6) = 12 |
| `x=1&y=1` | `1` | LCM(1,1) = 1 |
| `x=abc&y=6` | `NaN` | not a number |
| `x=0&y=6` | `NaN` | 0 is not a natural number |
| `x=-5&y=6` | `NaN` | negative is not natural |
| `x=4294967311&y=4294967357` | `18446744400127067027` | big numbers test from mentor |

## Common Pitfalls

| Mistake | Why it matters |
|---|---|
| Using `/` instead of `//` for division | Returns `12.0` instead of `12` — extra character in output |
| Not validating zero or negative numbers | `0` passes `int()` check but is not a natural number |
| Hardcoding port `5000` | Will not work on hosting — must read from `PORT` environment variable |
| Not setting `host="0.0.0.0"` | Server only listens locally, hosting provider cannot reach it |
| Submitting before waking up the server | Free tier sleeps — mentor gets a timeout error |

## Submission Format

```
!task3 dilyarace@gmail.com https://data-engineering-tybf.onrender.com/dilyarace_gmail_com?x={}&y={}
```

## Stack

- **Language:** Python 3
- **Framework:** Flask
- **Hosting:** Render.com (free tier)
- **Libraries:** `flask`, `math` (built-in), `os` (built-in)
