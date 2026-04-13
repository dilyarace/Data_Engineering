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