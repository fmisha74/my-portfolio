import math
from flask import Flask, request, render_template_string

app = Flask(__name__)

# (value sent by the form, label shown in the dropdown)
OPERATIONS = [
    ("+", "+  Add"),
    ("-", "-  Subtract"),
    ("*", "*  Multiply"),
    ("/", "/  Divide"),
    ("%", "%  Modulus (remainder)"),
    ("**", "** Power"),
    ("//", "// Floor divide"),
    ("min", "Min of two numbers"),
    ("max", "Max of two numbers"),
    ("average", "Average of two numbers"),
    ("perct", "Percent (second % of first)"),
    ("sqrt", "Square root (first number)"),
    ("abs", "Absolute value (first number)"),
    ("int", "Whole number part (first number)"),
    ("factorial", "Factorial (first number)"),
    ("area", "Circle area (first = radius)"),
    ("sin", "Sin, degrees (first number)"),
    ("cos", "Cos, degrees (first number)"),
    ("tan", "Tan, degrees (first number)"),
    ("log", "Natural log (first number)"),
    ("log10", "Log base 10 (first number)"),
]

# These only use the first number, so the second box can be left empty
ONE_NUMBER_OPS = {"sqrt", "abs", "int", "factorial", "area",
                  "sin", "cos", "tan", "log", "log10"}


def calculate(num1, num2, op):
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        return num1 / num2
    elif op == "%":
        return num1 % num2
    elif op == "**":
        return num1 ** num2
    elif op == "//":
        return num1 // num2
    elif op == "sqrt":
        return math.sqrt(num1)
    elif op == "min":
        return min(num1, num2)
    elif op == "max":
        return max(num1, num2)
    elif op == "perct":
        return num1 / 100 * num2
    elif op == "area":
        return math.pi * num1 ** 2
    elif op == "average":
        return (num1 + num2) / 2
    elif op == "factorial":
        return math.factorial(int(num1))
    elif op == "int":
        return int(num1)
    elif op == "sin":
        return math.sin(math.radians(num1))
    elif op == "cos":
        return math.cos(math.radians(num1))
    elif op == "tan":
        return math.tan(math.radians(num1))
    elif op == "log":
        return math.log(num1)
    elif op == "log10":
        return math.log10(num1)
    elif op == "abs":
        return abs(num1)
    else:
        return None


PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Glam Calculator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Baloo+2:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px 16px;
      font-family: 'Baloo 2', 'Trebuchet MS', sans-serif;
      color: #fff;
      overflow-x: hidden;
      /* leopard-ish spots on hot pink */
      background-color: #ff2e93;
      background-image:
        radial-gradient(ellipse 14px 9px at 20px 22px, #5a0a35 55%, transparent 60%),
        radial-gradient(ellipse 10px 14px at 62px 58px, #5a0a35 55%, transparent 60%),
        radial-gradient(ellipse 16px 8px at 96px 20px, #5a0a35 55%, transparent 60%),
        radial-gradient(ellipse 9px 13px at 38px 92px, #5a0a35 55%, transparent 60%),
        radial-gradient(ellipse 13px 9px at 110px 88px, #5a0a35 55%, transparent 60%),
        radial-gradient(circle at 50% 0%, #ff7bc0, #ff2e93 60%);
      background-size: 130px 120px, 130px 120px, 130px 120px, 130px 120px, 130px 120px, 100% 100%;
    }

    /* twinkling sparkles */
    .sparkle {
      position: fixed;
      font-size: 26px;
      color: #fff;
      text-shadow: 0 0 8px #fff, 0 0 18px #ff9ad5;
      animation: twinkle 2.4s ease-in-out infinite;
      pointer-events: none;
    }
    .sparkle:nth-child(1)  { top: 6%;  left: 8%;  animation-delay: 0s; }
    .sparkle:nth-child(2)  { top: 14%; left: 86%; animation-delay: .5s; font-size: 34px; }
    .sparkle:nth-child(3)  { top: 40%; left: 4%;  animation-delay: 1s; }
    .sparkle:nth-child(4)  { top: 62%; left: 92%; animation-delay: 1.5s; }
    .sparkle:nth-child(5)  { top: 84%; left: 12%; animation-delay: .8s; font-size: 32px; }
    .sparkle:nth-child(6)  { top: 90%; left: 80%; animation-delay: 1.2s; }
    .sparkle:nth-child(7)  { top: 26%; left: 94%; animation-delay: 1.8s; font-size: 20px; }
    .sparkle:nth-child(8)  { top: 72%; left: 3%;  animation-delay: .3s; font-size: 20px; }
    @keyframes twinkle {
      0%, 100% { opacity: .25; transform: scale(.7) rotate(0deg); }
      50%      { opacity: 1;   transform: scale(1.2) rotate(20deg); }
    }

    .card {
      position: relative;
      width: 100%;
      max-width: 440px;
      padding: 28px 24px 22px;
      border-radius: 32px;
      background: linear-gradient(160deg, #2b0a3d 0%, #130420 100%);
      border: 4px solid #ffd1ec;
      box-shadow:
        0 0 0 6px #ff2e93,
        0 0 35px 8px rgba(255, 255, 255, .55),
        0 20px 40px rgba(60, 0, 40, .6);
    }

    h1 {
      margin: 0 0 4px;
      text-align: center;
      font-family: 'Pacifico', cursive;
      font-weight: 400;
      font-size: 42px;
      line-height: 1.1;
      color: #fff;
      text-shadow:
        0 0 6px #ff9ad5,
        0 0 16px #ff2e93,
        0 0 30px #ff2e93;
    }
    .tagline {
      text-align: center;
      margin: 0 0 18px;
      font-weight: 700;
      letter-spacing: 2px;
      font-size: 13px;
      text-transform: uppercase;
      color: #ffb3dd;
    }

    label {
      display: block;
      margin: 10px 0 2px 6px;
      font-weight: 800;
      font-size: 13px;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: #ff9ad5;
    }

    input, select {
      width: 100%;
      padding: 12px 16px;
      font-family: inherit;
      font-size: 18px;
      font-weight: 700;
      color: #4a0a2e;
      background: #fff0f8;
      border: 3px solid #ff79bd;
      border-radius: 999px;
      outline: none;
      transition: box-shadow .15s, border-color .15s;
    }
    input::placeholder { color: #c98aab; font-weight: 500; }
    input:focus, select:focus {
      border-color: #fff;
      box-shadow: 0 0 0 4px rgba(255, 46, 147, .6), 0 0 18px #ff79bd;
    }

    button {
      width: 100%;
      margin-top: 18px;
      padding: 14px;
      font-family: 'Pacifico', cursive;
      font-size: 24px;
      color: #fff;
      border: 3px solid #fff;
      border-radius: 999px;
      cursor: pointer;
      background: linear-gradient(180deg, #ff8fcb 0%, #ff2e93 50%, #d4106f 100%);
      box-shadow: 0 6px 0 #8f0a4a, 0 10px 20px rgba(255, 46, 147, .6),
                  inset 0 3px 6px rgba(255, 255, 255, .6);
      text-shadow: 0 2px 4px rgba(90, 0, 50, .7);
      transition: transform .08s, box-shadow .08s;
    }
    button:hover { filter: brightness(1.08); }
    button:active {
      transform: translateY(4px);
      box-shadow: 0 2px 0 #8f0a4a, 0 4px 10px rgba(255, 46, 147, .6),
                  inset 0 3px 6px rgba(255, 255, 255, .6);
    }

    .result {
      margin-top: 20px;
      padding: 16px;
      text-align: center;
      font-size: 22px;
      font-weight: 800;
      word-break: break-word;
      border-radius: 20px;
      color: #4a0a2e;
      background: linear-gradient(135deg, #fff 0%, #ffd1ec 50%, #fff 100%);
      border: 3px dashed #ff2e93;
      box-shadow: 0 0 22px rgba(255, 154, 213, .8);
    }

    .foot {
      margin: 16px 0 0;
      text-align: center;
      font-size: 13px;
      color: #d9a0c4;
    }
    /* dolls + layout */
    .stage {
      display: flex;
      flex-wrap: wrap;
      align-items: flex-end;
      justify-content: center;
      gap: 24px;
      width: 100%;
      max-width: 1000px;
    }
    .stage .card { width: auto; flex: 0 1 440px; order: 2; }
    .doll-wrap { flex: 0 0 auto; width: 180px; text-align: center; }
    .doll-wrap.left  { order: 1; }
    .doll-wrap.right { order: 3; }
    .doll {
      width: 100%;
      display: block;
      filter: drop-shadow(0 0 12px rgba(255, 255, 255, .6));
      animation: bob 3s ease-in-out infinite;
    }
    .doll-wrap.right .doll { animation-delay: 1.3s; }
    @keyframes bob {
      0%, 100% { transform: translateY(0); }
      50%      { transform: translateY(-10px); }
    }
    .bubble {
      position: relative;
      display: inline-block;
      margin-bottom: 14px;
      padding: 6px 14px;
      border-radius: 16px;
      background: #fff;
      color: #4a0a2e;
      font-weight: 800;
      font-size: 15px;
      box-shadow: 0 0 14px rgba(255, 255, 255, .7);
    }
    .bubble::after {
      content: "";
      position: absolute;
      left: 50%;
      bottom: -9px;
      margin-left: -9px;
      border: 9px solid transparent;
      border-bottom: 0;
      border-top-color: #fff;
    }
    /* small screens: dolls side by side above the card */
    @media (max-width: 860px) {
      .stage .card { flex-basis: 100%; order: 3; }
      .doll-wrap { width: 130px; }
    }
  </style>
</head>
<body>
  <span class="sparkle">&#10024;</span>
  <span class="sparkle">&#10022;</span>
  <span class="sparkle">&#10024;</span>
  <span class="sparkle">&#10022;</span>
  <span class="sparkle">&#10024;</span>
  <span class="sparkle">&#10022;</span>
  <span class="sparkle">&#10024;</span>
  <span class="sparkle">&#10022;</span>

  <div class="stage">

  <!-- LEFT DOLL: black hair, pink streak -->
  <div class="doll-wrap left">
    <div class="bubble">Slay, queen!</div>
    <svg class="doll" viewBox="0 0 160 320" role="img" aria-label="Doll with black hair and a pink streak">
      <path d="M28 78 C26 8 134 8 132 78 L142 205 C144 230 120 232 116 214 L112 130 L48 130 L44 214 C40 232 16 230 18 205 Z" fill="#1a0b1f"/>
      <path d="M36 70 C28 120 32 170 38 214 L47 214 C42 170 42 120 50 76 Z" fill="#ff2e93"/>
      <rect x="58" y="244" width="16" height="42" fill="#c98a5e"/>
      <rect x="86" y="244" width="16" height="42" fill="#c98a5e"/>
      <rect x="54" y="278" width="24" height="28" rx="7" fill="#ff2e93"/>
      <rect x="82" y="278" width="24" height="28" rx="7" fill="#ff2e93"/>
      <rect x="48" y="302" width="34" height="11" rx="5" fill="#fff"/>
      <rect x="78" y="302" width="34" height="11" rx="5" fill="#fff"/>
      <path d="M54 148 L34 204 L44 209 L62 160 Z" fill="#c98a5e"/>
      <path d="M106 148 L126 204 L116 209 L98 160 Z" fill="#c98a5e"/>
      <circle cx="39" cy="208" r="7" fill="#c98a5e"/>
      <circle cx="121" cy="208" r="7" fill="#c98a5e"/>
      <rect x="70" y="118" width="20" height="30" fill="#c98a5e"/>
      <rect x="52" y="188" width="56" height="22" fill="#c98a5e"/>
      <path d="M52 144 L108 144 L114 192 L46 192 Z" fill="#ff2e93"/>
      <path d="M52 144 L108 144 L106 156 L54 156 Z" fill="#ff79bd"/>
      <path d="M48 208 L112 208 L124 248 L36 248 Z" fill="#2b0a3d" stroke="#ff79bd" stroke-width="3"/>
      <ellipse cx="80" cy="78" rx="40" ry="46" fill="#c98a5e"/>
      <path d="M38 80 C34 22 126 22 122 80 C108 52 66 44 38 80 Z" fill="#1a0b1f"/>
      <ellipse cx="50" cy="102" rx="7" ry="4" fill="#ff79bd" opacity=".5"/>
      <ellipse cx="110" cy="102" rx="7" ry="4" fill="#ff79bd" opacity=".5"/>
      <ellipse cx="62" cy="86" rx="12" ry="8.5" fill="#fff"/>
      <circle cx="62" cy="86" r="6.5" fill="#5a2a8f"/>
      <circle cx="62" cy="86" r="3.2" fill="#12051a"/>
      <circle cx="64.5" cy="83.5" r="2" fill="#fff"/>
      <path d="M48 84 Q62 71 76 84" stroke="#ff2e93" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M48 85 Q62 75 76 85" stroke="#12051a" stroke-width="2.2" fill="none"/>
      <path d="M49 83 L44 79 M52 78 L48 73" stroke="#12051a" stroke-width="2" stroke-linecap="round"/>
      <ellipse cx="98" cy="86" rx="12" ry="8.5" fill="#fff"/>
      <circle cx="98" cy="86" r="6.5" fill="#5a2a8f"/>
      <circle cx="98" cy="86" r="3.2" fill="#12051a"/>
      <circle cx="100.5" cy="83.5" r="2" fill="#fff"/>
      <path d="M84 84 Q98 71 112 84" stroke="#ff2e93" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M84 85 Q98 75 112 85" stroke="#12051a" stroke-width="2.2" fill="none"/>
      <path d="M111 83 L116 79 M108 78 L112 73" stroke="#12051a" stroke-width="2" stroke-linecap="round"/>
      <path d="M50 68 Q62 61 74 67 M86 67 Q98 61 110 68" stroke="#12051a" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M80 92 Q77 100 81 100" stroke="#a8683f" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      <path d="M66 108 Q73 101 80 105 Q87 101 94 108 Q80 124 66 108 Z" fill="#ff2e93"/>
      <ellipse cx="76" cy="109" rx="5" ry="2" fill="#fff" opacity=".7"/>
      <circle cx="40" cy="94" r="6" fill="none" stroke="#ffd23f" stroke-width="2.5"/>
      <circle cx="120" cy="94" r="6" fill="none" stroke="#ffd23f" stroke-width="2.5"/>
    </svg>
  </div>

  <div class="card">
    <h1>Glam Calc</h1>
    <p class="tagline">&#128139; math, but make it fashion &#128139;</p>

    <form method="post">
      <label for="num1">First number</label>
      <input id="num1" name="num1" placeholder="e.g. 4" value="{{ num1 }}" required>

      <label for="num2">Second number</label>
      <input id="num2" name="num2" placeholder="skip for one-number moves" value="{{ num2 }}">

      <label for="operation">Pick your move</label>
      <select id="operation" name="operation">
        {% for value, label in operations %}
          <option value="{{ value }}" {% if value == selected %}selected{% endif %}>{{ label }}</option>
        {% endfor %}
      </select>

      <button type="submit">Calculate &#10084;</button>
    </form>

    {% if result %}
      <div class="result">&#10024; {{ result }} &#10024;</div>
    {% endif %}

    <p class="foot">Sin, cos &amp; tan use degrees.</p>
  </div>

  <!-- RIGHT DOLL: blonde bob, purple streak -->
  <div class="doll-wrap right">
    <div class="bubble">Do the math!</div>
    <svg class="doll" viewBox="0 0 160 320" role="img" aria-label="Doll with a blonde bob and a purple streak">
      <path d="M30 78 C28 8 132 8 130 78 L138 150 C128 162 108 156 104 140 L56 140 C52 156 32 162 22 150 Z" fill="#f4c542"/>
      <path d="M124 70 C132 100 130 130 126 154 L118 154 C122 128 120 100 112 76 Z" fill="#b57bff"/>
      <rect x="58" y="244" width="16" height="42" fill="#fbd3b5"/>
      <rect x="86" y="244" width="16" height="42" fill="#fbd3b5"/>
      <rect x="54" y="278" width="24" height="28" rx="7" fill="#12051a"/>
      <rect x="82" y="278" width="24" height="28" rx="7" fill="#12051a"/>
      <rect x="54" y="278" width="24" height="6" rx="3" fill="#ff2e93"/>
      <rect x="82" y="278" width="24" height="6" rx="3" fill="#ff2e93"/>
      <rect x="48" y="302" width="34" height="11" rx="5" fill="#ff79bd"/>
      <rect x="78" y="302" width="34" height="11" rx="5" fill="#ff79bd"/>
      <path d="M54 148 L34 204 L44 209 L62 160 Z" fill="#fbd3b5"/>
      <path d="M106 148 L126 204 L116 209 L98 160 Z" fill="#fbd3b5"/>
      <circle cx="39" cy="208" r="7" fill="#fbd3b5"/>
      <circle cx="121" cy="208" r="7" fill="#fbd3b5"/>
      <rect x="70" y="118" width="20" height="30" fill="#fbd3b5"/>
      <rect x="52" y="188" width="56" height="22" fill="#fbd3b5"/>
      <path d="M52 144 L108 144 L114 192 L46 192 Z" fill="#8f3bff"/>
      <path d="M52 144 L108 144 L106 156 L54 156 Z" fill="#b57bff"/>
      <path d="M48 208 L112 208 L124 248 L36 248 Z" fill="#ff2e93"/>
      <path d="M46 222 L114 222 L117 232 L43 232 Z" fill="#fff" opacity=".85"/>
      <ellipse cx="80" cy="78" rx="40" ry="46" fill="#fbd3b5"/>
      <path d="M36 82 C30 20 130 20 124 82 C118 60 90 44 66 52 C52 58 42 68 36 82 Z" fill="#f4c542"/>
      <polygon points="112,30 115,38 123,38 117,43 119,51 112,46 105,51 107,43 101,38 109,38" fill="#fff" stroke="#ff2e93" stroke-width="1.5"/>
      <ellipse cx="50" cy="102" rx="7" ry="4" fill="#ff79bd" opacity=".5"/>
      <ellipse cx="110" cy="102" rx="7" ry="4" fill="#ff79bd" opacity=".5"/>
      <ellipse cx="62" cy="86" rx="12" ry="8.5" fill="#fff"/>
      <circle cx="62" cy="86" r="6.5" fill="#12a8a8"/>
      <circle cx="62" cy="86" r="3.2" fill="#12051a"/>
      <circle cx="64.5" cy="83.5" r="2" fill="#fff"/>
      <path d="M48 84 Q62 71 76 84" stroke="#b57bff" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M48 85 Q62 75 76 85" stroke="#12051a" stroke-width="2.2" fill="none"/>
      <path d="M49 83 L44 79 M52 78 L48 73" stroke="#12051a" stroke-width="2" stroke-linecap="round"/>
      <ellipse cx="98" cy="86" rx="12" ry="8.5" fill="#fff"/>
      <circle cx="98" cy="86" r="6.5" fill="#12a8a8"/>
      <circle cx="98" cy="86" r="3.2" fill="#12051a"/>
      <circle cx="100.5" cy="83.5" r="2" fill="#fff"/>
      <path d="M84 84 Q98 71 112 84" stroke="#b57bff" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M84 85 Q98 75 112 85" stroke="#12051a" stroke-width="2.2" fill="none"/>
      <path d="M111 83 L116 79 M108 78 L112 73" stroke="#12051a" stroke-width="2" stroke-linecap="round"/>
      <path d="M50 68 Q62 61 74 67 M86 67 Q98 61 110 68" stroke="#9a6a1e" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M80 92 Q77 100 81 100" stroke="#d9a07c" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      <path d="M66 108 Q73 101 80 105 Q87 101 94 108 Q80 124 66 108 Z" fill="#ff4fa8"/>
      <ellipse cx="76" cy="109" rx="5" ry="2" fill="#fff" opacity=".7"/>
      <circle cx="40" cy="94" r="5" fill="#ffd23f"/>
      <circle cx="120" cy="94" r="5" fill="#ffd23f"/>
    </svg>
  </div>

  </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    num1_text = ""
    num2_text = ""
    selected = "+"

    if request.method == "POST":
        num1_text = request.form["num1"].strip()
        num2_text = request.form["num2"].strip()
        selected = request.form["operation"]

        try:
            num1 = float(num1_text)
            # One-number operations don't need the second box
            if num2_text == "" and selected in ONE_NUMBER_OPS:
                num2 = 0.0
            else:
                num2 = float(num2_text)

            answer = calculate(num1, num2, selected)
            if answer is None:
                result = "Operation is invalid."
            else:
                result = f"The answer is {answer}"
        except ZeroDivisionError:
            result = "You can't divide by zero."
        except OverflowError:
            result = "That number is too big to calculate."
        except ValueError:
            result = "Invalid input. Enter numbers only, and check that the number works for that operation (for example, no square root of a negative)."

    return render_template_string(
        PAGE,
        result=result,
        operations=OPERATIONS,
        num1=num1_text,
        num2=num2_text,
        selected=selected,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
