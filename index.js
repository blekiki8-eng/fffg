const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// проста база в пам’яті (потім замінимо на MongoDB)
let users = {};

// створення юзера
app.post("/user", (req, res) => {
  const { id } = req.body;

  if (!users[id]) {
    users[id] = {
      fc: 100,
      gc: 10,
      ref: 0
    };
  }

  res.json(users[id]);
});

// отримати юзера
app.get("/user/:id", (req, res) => {
  const user = users[req.params.id];
  res.json(user || null);
});

// гра
app.post("/fish", (req, res) => {
  const { id, bet, currency } = req.body;

  if (!users[id]) return res.json({ error: "no user" });

  let u = users[id];

  if (currency === "fc" && u.fc < bet) return res.json({ error: "no money" });
  if (currency === "gc" && u.gc < bet) return res.json({ error: "no money" });

  let win = Math.random() > 0.5;

  let result = win
    ? ["🐟 Карась", "🐠 Короп", "🦈 Щука"][Math.floor(Math.random() * 3)]
    : "🗑️ Сміття";

  if (currency === "fc") {
    u.fc -= bet;
    if (win) u.fc += bet * 1.5;
  } else {
    u.gc -= bet;
    if (win) u.gc += bet * 1.5;
  }

  res.json({
    win,
    result,
    fc: u.fc,
    gc: u.gc
  });
});

app.listen(3000, () => console.log("Server running"));
