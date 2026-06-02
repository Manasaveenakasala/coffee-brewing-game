import gradio as gr
import random
import json

# ── Game Data ────────────────────────────────────────────────────────────────

RECIPES = {
    "Espresso": {
        "description": "A concentrated shot of pure coffee intensity.",
        "emoji": "☕",
        "target": {"grind": 85, "temp": 93, "pressure": 9, "time": 27},
        "tolerance": {"grind": 5, "temp": 3, "pressure": 1, "time": 4},
        "tips": "Fine grind, high pressure, short extraction time.",
    },
    "Cold Brew": {
        "description": "Smooth and mellow, steeped slowly in cold water.",
        "emoji": "🧊",
        "target": {"grind": 20, "temp": 5, "pressure": 0, "time": 720},
        "tolerance": {"grind": 8, "temp": 5, "pressure": 0, "time": 120},
        "tips": "Very coarse grind, cold temperature, near-zero pressure, very long time.",
    },
    "French Press": {
        "description": "Rich and full-bodied with a heavy mouthfeel.",
        "emoji": "🫖",
        "target": {"grind": 30, "temp": 94, "pressure": 1, "time": 240},
        "tolerance": {"grind": 8, "temp": 4, "pressure": 1, "time": 30},
        "tips": "Coarse grind, near-boiling water, minimal pressure, 4-minute steep.",
    },
    "Pour Over": {
        "description": "Clean, bright, and nuanced — every note shines.",
        "emoji": "🌿",
        "target": {"grind": 55, "temp": 91, "pressure": 0, "time": 180},
        "tolerance": {"grind": 7, "temp": 4, "pressure": 0, "time": 25},
        "tips": "Medium grind, slightly cooler water, gravity-only, 3-minute pour.",
    },
    "Cappuccino": {
        "description": "Espresso crowned with velvety steamed milk foam.",
        "emoji": "🍵",
        "target": {"grind": 80, "temp": 93, "pressure": 9, "time": 25},
        "tolerance": {"grind": 6, "temp": 3, "pressure": 1, "time": 4},
        "tips": "Fine grind like espresso, but slightly shorter pull for milk balance.",
    },
    "AeroPress": {
        "description": "Versatile and forgiving — smooth with low acidity.",
        "emoji": "🔬",
        "target": {"grind": 60, "temp": 80, "pressure": 5, "time": 90},
        "tolerance": {"grind": 10, "temp": 5, "pressure": 2, "time": 20},
        "tips": "Medium-fine grind, lower temp than most, moderate pressure, quick brew.",
    },
}

FLAVOR_PROFILES = {
    "perfect": ["🏆 Barista-level perfection!", "☀️ A divine cup!", "🌟 World-class brew!"],
    "great":   ["😍 Really impressive!", "👏 Excellent technique!", "✨ Nearly perfect!"],
    "good":    ["😊 Solid brew!", "👍 Good job!", "☕ Enjoyable cup!"],
    "okay":    ["🤔 Decent attempt.", "📚 Keep practicing.", "💡 Getting there!"],
    "bad":     ["😬 Over/under extracted.", "🔧 Needs work.", "📖 Study the recipe!"],
}

ACHIEVEMENTS = {
    "first_brew":     ("🥄", "First Brew",     "Made your very first cup"),
    "perfect_shot":   ("🏆", "Perfect Shot",   "Scored 100% on a brew"),
    "espresso_pro":   ("☕", "Espresso Pro",   "Perfected an Espresso"),
    "cold_master":    ("🧊", "Cold Master",    "Mastered Cold Brew"),
    "all_recipes":    ("🌍", "World Barista",  "Attempted all 6 recipes"),
    "five_brews":     ("🔥", "On a Roll",      "Brewed 5 times"),
    "score_800":      ("💎", "High Scorer",    "Accumulated 800+ total points"),
}

# ── Scoring Logic ─────────────────────────────────────────────────────────────

def score_parameter(value, target, tolerance):
    diff = abs(value - target)
    if diff == 0:
        return 100
    if diff <= tolerance * 0.5:
        return 90
    if diff <= tolerance:
        return 75
    if diff <= tolerance * 1.5:
        return 50
    if diff <= tolerance * 2.5:
        return 25
    return 0

def brew_coffee(recipe_name, grind, temp, pressure, time_val, state):
    recipe = RECIPES[recipe_name]
    target = recipe["target"]
    tol    = recipe["tolerance"]

    scores = {
        "Grind Size":    score_parameter(grind,     target["grind"],    tol["grind"]),
        "Temperature":   score_parameter(temp,      target["temp"],     tol["temp"]),
        "Pressure":      score_parameter(pressure,  target["pressure"], tol["pressure"]),
        "Brew Time":     score_parameter(time_val,  target["time"],     tol["time"]),
    }

    overall = int(sum(scores.values()) / len(scores))

    if overall >= 95:  tier = "perfect"
    elif overall >= 80: tier = "great"
    elif overall >= 60: tier = "good"
    elif overall >= 40: tier = "okay"
    else:               tier = "bad"

    feedback = random.choice(FLAVOR_PROFILES[tier])

    # Update state
    state["brews"] += 1
    state["total_score"] += overall
    state["history"].append({"recipe": recipe_name, "score": overall})
    if recipe_name not in state["attempted"]:
        state["attempted"].add(recipe_name)

    # Check achievements
    new_achievements = []
    if state["brews"] == 1 and "first_brew" not in state["achievements"]:
        state["achievements"].add("first_brew"); new_achievements.append("first_brew")
    if overall == 100 and "perfect_shot" not in state["achievements"]:
        state["achievements"].add("perfect_shot"); new_achievements.append("perfect_shot")
    if recipe_name == "Espresso" and overall >= 90 and "espresso_pro" not in state["achievements"]:
        state["achievements"].add("espresso_pro"); new_achievements.append("espresso_pro")
    if recipe_name == "Cold Brew" and overall >= 85 and "cold_master" not in state["achievements"]:
        state["achievements"].add("cold_master"); new_achievements.append("cold_master")
    if len(state["attempted"]) == 6 and "all_recipes" not in state["achievements"]:
        state["achievements"].add("all_recipes"); new_achievements.append("all_recipes")
    if state["brews"] >= 5 and "five_brews" not in state["achievements"]:
        state["achievements"].add("five_brews"); new_achievements.append("five_brews")
    if state["total_score"] >= 800 and "score_800" not in state["achievements"]:
        state["achievements"].add("score_800"); new_achievements.append("score_800")

    # ── Build result markdown ────────────────────────────────────────────────
    result_md = f"""
## {recipe["emoji"]} Brewing {recipe_name}...

---

### 📊 Parameter Scores

| Parameter     | Your Value | Target | Score |
|---------------|-----------|--------|-------|
| Grind Size    | {grind}    | {target['grind']} | {'⭐' * (scores['Grind Size'] // 25)} {scores['Grind Size']}% |
| Temperature   | {temp}°C   | {target['temp']}°C | {'⭐' * (scores['Temperature'] // 25)} {scores['Temperature']}% |
| Pressure      | {pressure} bar | {target['pressure']} bar | {'⭐' * (scores['Pressure'] // 25)} {scores['Pressure']}% |
| Brew Time     | {time_val}s | {target['time']}s | {'⭐' * (scores['Brew Time'] // 25)} {scores['Brew Time']}% |

---

### 🎯 Overall Score: **{overall}%**

{feedback}

> 💡 **Pro tip:** {recipe['tips']}
"""

    if new_achievements:
        result_md += "\n### 🏅 Achievement Unlocked!\n"
        for a in new_achievements:
            icon, name, desc = ACHIEVEMENTS[a]
            result_md += f"**{icon} {name}** — {desc}\n\n"

    # ── Build stats markdown ─────────────────────────────────────────────────
    avg = state["total_score"] // max(state["brews"], 1)
    best = max((h["score"] for h in state["history"]), default=0)
    ach_md = ""
    for key, (icon, name, desc) in ACHIEVEMENTS.items():
        if key in state["achievements"]:
            ach_md += f"**{icon} {name}**  \n"
        else:
            ach_md += f"🔒 *{name}*  \n"

    stats_md = f"""
### 📈 Your Stats

| | |
|---|---|
| Total Brews | **{state['brews']}** |
| Average Score | **{avg}%** |
| Best Score | **{best}%** |
| Recipes Tried | **{len(state['attempted'])}/6** |

---

### 🏅 Achievements

{ach_md}
"""

    return result_md, stats_md, state


def update_recipe_info(recipe_name):
    r = RECIPES[recipe_name]
    t = r["target"]
    info = f"""
### {r['emoji']} {recipe_name}
*{r['description']}*

**Target Parameters:**
- 🌰 Grind Size: **{t['grind']}** (0=powder, 100=whole bean)
- 🌡️ Temperature: **{t['temp']}°C**
- 💨 Pressure: **{t['pressure']} bar**
- ⏱️ Brew Time: **{t['time']}s**

> 💡 {r['tips']}
"""
    return info


def get_hint(recipe_name):
    r = RECIPES[recipe_name]
    t = r["target"]
    return (
        t["grind"],
        t["temp"],
        t["pressure"],
        t["time"],
    )


def reset_game():
    return {
        "brews": 0,
        "total_score": 0,
        "history": [],
        "attempted": set(),
        "achievements": set(),
    }


# ── UI Layout ──────────────────────────────────────────────────────────────────

CSS = """
body, .gradio-container { font-family: 'Georgia', serif; }
.brew-btn { background: #3d1c02 !important; color: #f5e6c8 !important; font-size: 1.1em !important; }
.hint-btn { background: #7a4a1e !important; color: #f5e6c8 !important; }
.reset-btn { background: #5a1a1a !important; color: #f5e6c8 !important; }
footer { display: none !important; }
"""

with gr.Blocks(
    title="☕ Coffee Brewing Mini-Game",
    theme=gr.themes.Soft(
        primary_hue="orange",
        secondary_hue="brown",
        neutral_hue="stone",
        font=["Georgia", "serif"],
    ),
    css=CSS,
) as demo:

    # ── State ──────────────────────────────────────────────────────────────
    game_state = gr.State(reset_game())

    # ── Header ─────────────────────────────────────────────────────────────
    gr.Markdown(
        """
        # ☕ Coffee Brewing Mini-Game
        ### Master the art of coffee — dial in the perfect parameters and brew legendary cups!
        """
    )

    with gr.Row():
        # ── Left: Controls ─────────────────────────────────────────────────
        with gr.Column(scale=2):
            recipe_dd = gr.Dropdown(
                choices=list(RECIPES.keys()),
                value="Espresso",
                label="🫘 Choose Your Recipe",
            )

            recipe_info_md = gr.Markdown(update_recipe_info("Espresso"))

            gr.Markdown("### 🎛️ Dial In Your Parameters")

            grind_sl = gr.Slider(
                minimum=0, maximum=100, value=50, step=1,
                label="🌰 Grind Size  (0 = powder fine · 100 = whole bean coarse)",
            )
            temp_sl = gr.Slider(
                minimum=0, maximum=100, value=80, step=1,
                label="🌡️ Temperature (°C)",
            )
            pressure_sl = gr.Slider(
                minimum=0, maximum=15, value=5, step=1,
                label="💨 Pressure (bar)",
            )
            time_sl = gr.Slider(
                minimum=0, maximum=900, value=120, step=5,
                label="⏱️ Brew Time (seconds)",
            )

            with gr.Row():
                brew_btn  = gr.Button("☕ Brew It!", variant="primary", elem_classes=["brew-btn"])
                hint_btn  = gr.Button("💡 Hint (–10 pts)",  elem_classes=["hint-btn"])
                reset_btn = gr.Button("🔄 Reset Game",      elem_classes=["reset-btn"])

        # ── Right: Results & Stats ─────────────────────────────────────────
        with gr.Column(scale=3):
            result_md = gr.Markdown("### Your brew result will appear here after you hit **☕ Brew It!**")

            gr.Markdown("---")

            stats_md = gr.Markdown(
                """
                ### 📈 Your Stats
                Start brewing to see your stats!

                ### 🏅 Achievements
                🔒 *First Brew*
                🔒 *Perfect Shot*
                🔒 *Espresso Pro*
                🔒 *Cold Master*
                🔒 *World Barista*
                🔒 *On a Roll*
                🔒 *High Scorer*
                """
            )

    # ── Event Handlers ─────────────────────────────────────────────────────

    recipe_dd.change(
        fn=update_recipe_info,
        inputs=[recipe_dd],
        outputs=[recipe_info_md],
    )

    brew_btn.click(
        fn=brew_coffee,
        inputs=[recipe_dd, grind_sl, temp_sl, pressure_sl, time_sl, game_state],
        outputs=[result_md, stats_md, game_state],
    )

    hint_btn.click(
        fn=get_hint,
        inputs=[recipe_dd],
        outputs=[grind_sl, temp_sl, pressure_sl, time_sl],
    )

    reset_btn.click(
        fn=reset_game,
        inputs=[],
        outputs=[game_state],
    ).then(
        fn=lambda: (
            "### Game reset! Start a fresh brewing journey ☕",
            """
### 📈 Your Stats
Start brewing to see your stats!

### 🏅 Achievements
🔒 *First Brew*  
🔒 *Perfect Shot*  
🔒 *Espresso Pro*  
🔒 *Cold Master*  
🔒 *World Barista*  
🔒 *On a Roll*  
🔒 *High Scorer*  
""",
        ),
        inputs=[],
        outputs=[result_md, stats_md],
    )

    gr.Markdown(
        """
        ---
        *Built with ❤️ and Gradio · [View on GitHub](https://github.com)*
        """
    )

if __name__ == "__main__":
    demo.launch()
