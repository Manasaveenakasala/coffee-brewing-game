---
title: Coffee Brewing Mini-Game
emoji: ☕
colorFrom: orange
colorTo: brown
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
license: mit
short_description: Dial in the perfect brew parameters and become a master barista!
---

# ☕ Coffee Brewing Mini-Game

A fun interactive mini-game where you dial in coffee brewing parameters to score the perfect cup!

## 🎮 How to Play

1. **Choose a recipe** from the dropdown (Espresso, Cold Brew, French Press, Pour Over, Cappuccino, AeroPress)
2. **Adjust the 4 parameters** using the sliders:
   - 🌰 **Grind Size** — how finely the beans are ground (0 = powder, 100 = whole bean)
   - 🌡️ **Temperature** — water temperature in °C
   - 💨 **Pressure** — brewing pressure in bar
   - ⏱️ **Brew Time** — extraction time in seconds
3. **Hit ☕ Brew It!** to see your score and feedback
4. Unlock **7 achievements** as you improve!

## 🏆 Achievements

| Achievement | How to Unlock |
|---|---|
| 🥄 First Brew | Make your very first cup |
| 🏆 Perfect Shot | Score 100% on any brew |
| ☕ Espresso Pro | Perfect an Espresso (90%+) |
| 🧊 Cold Master | Master Cold Brew (85%+) |
| 🌍 World Barista | Attempt all 6 recipes |
| 🔥 On a Roll | Brew 5 times |
| 💎 High Scorer | Accumulate 800+ total points |

## 💡 Tips

- Use the **Hint** button to reveal the target parameters (costs –10 pts in spirit!)
- Each recipe has a **tolerance range** — you don't need to be pixel-perfect
- Check the **recipe info panel** for tips on each brew method

## 🛠️ Tech Stack

- [Gradio](https://gradio.app/) for the UI
- Pure Python — no external ML models needed
- Hosted on [Hugging Face Spaces](https://huggingface.co/spaces)

## 🚀 Local Development

```bash
git clone https://github.com/YOUR_USERNAME/coffee-brewing-game
cd coffee-brewing-game
pip install -r requirements.txt
python app.py
```

## 📁 Project Structure

```
coffee-brewing-game/
├── app.py            # Main Gradio application
├── requirements.txt  # Python dependencies
└── README.md         # This file (also the HF Space card)
```

---

Made with ☕ and Python
