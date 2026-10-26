-- SQLite schema. The app initializes these tables automatically.
CREATE TABLE IF NOT EXISTS players (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  country TEXT NOT NULL,
  role TEXT NOT NULL,
  batting_style TEXT,
  bowling_style TEXT,
  runs INTEGER NOT NULL DEFAULT 0 CHECK(runs >= 0),
  wickets INTEGER NOT NULL DEFAULT 0 CHECK(wickets >= 0),
  matches INTEGER NOT NULL DEFAULT 0 CHECK(matches >= 0),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_players_country ON players(country);
CREATE INDEX IF NOT EXISTS idx_players_runs ON players(runs DESC);

CREATE TABLE IF NOT EXISTS matches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT NOT NULL,
  team1 TEXT NOT NULL,
  team2 TEXT NOT NULL,
  venue TEXT,
  match_date TEXT,
  match_format TEXT,
  winner TEXT,
  victory_margin INTEGER,
  victory_type TEXT,
  home_team TEXT,
  away_team TEXT,
  toss_winner TEXT,
  toss_decision TEXT
);
CREATE TABLE IF NOT EXISTS venues (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  city TEXT,
  country TEXT,
  capacity INTEGER
);
CREATE TABLE IF NOT EXISTS series (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  host_country TEXT,
  match_type TEXT,
  start_date TEXT,
  planned_matches INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS player_innings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
  innings_number INTEGER NOT NULL CHECK(innings_number > 0),
  runs INTEGER NOT NULL DEFAULT 0 CHECK(runs >= 0),
  balls_faced INTEGER NOT NULL DEFAULT 0 CHECK(balls_faced >= 0),
  fours INTEGER NOT NULL DEFAULT 0 CHECK(fours >= 0),
  sixes INTEGER NOT NULL DEFAULT 0 CHECK(sixes >= 0),
  is_out INTEGER NOT NULL DEFAULT 1 CHECK(is_out IN (0, 1))
);
CREATE INDEX IF NOT EXISTS idx_player_innings_player ON player_innings(player_id);
CREATE INDEX IF NOT EXISTS idx_player_innings_match ON player_innings(match_id);

CREATE TABLE IF NOT EXISTS bowling_figures (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
  innings_number INTEGER NOT NULL CHECK(innings_number > 0),
  balls_bowled INTEGER NOT NULL DEFAULT 0 CHECK(balls_bowled >= 0),
  maidens INTEGER NOT NULL DEFAULT 0 CHECK(maidens >= 0),
  runs_conceded INTEGER NOT NULL DEFAULT 0 CHECK(runs_conceded >= 0),
  wickets INTEGER NOT NULL DEFAULT 0 CHECK(wickets >= 0),
  wides INTEGER NOT NULL DEFAULT 0 CHECK(wides >= 0),
  no_balls INTEGER NOT NULL DEFAULT 0 CHECK(no_balls >= 0)
);
CREATE INDEX IF NOT EXISTS idx_bowling_figures_player ON bowling_figures(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_figures_match ON bowling_figures(match_id);

CREATE TABLE IF NOT EXISTS partnerships (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
  innings_number INTEGER NOT NULL CHECK(innings_number > 0),
  wicket_number INTEGER NOT NULL CHECK(wicket_number > 0),
  player1_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  player2_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  runs INTEGER NOT NULL CHECK(runs >= 0)
);
CREATE INDEX IF NOT EXISTS idx_partnerships_match ON partnerships(match_id);
