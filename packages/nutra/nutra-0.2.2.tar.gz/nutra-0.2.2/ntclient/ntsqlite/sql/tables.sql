-- ntsqlite, an sqlite3 database for nutratracker clients
-- Copyright (C) 2018-2022  Shane Jaroch <nutratracker@gmail.com>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.

CREATE TABLE version( id integer PRIMARY KEY AUTOINCREMENT, version text NOT NULL, created date NOT NULL, notes text
);

-- TODO: enforce FK constraint across two DBs?
--
---------------------------------
-- Equations
---------------------------------

CREATE TABLE bmr_eqs (
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL
);

CREATE TABLE bf_eqs (
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL
);

--
--------------------------------
-- Profiles table
--------------------------------

CREATE TABLE profiles (
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL UNIQUE,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  eula int DEFAULT 0,
  gender text,
  dob date,
  act_lvl int DEFAULT 2, -- [1, 2, 3, 4, 5]
  goal_wt real,
  goal_bf real,
  bmr_eq_id int DEFAULT 1,
  bf_eq_id int DEFAULT 1,
  FOREIGN KEY (bmr_eq_id) REFERENCES bmr_eqs (id) ON UPDATE CASCADE,
  FOREIGN KEY (bf_eq_id) REFERENCES bf_eqs (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Biometrics
--------------------------------

CREATE TABLE biometrics (
  -- TODO: support custom biometrics and sync?
  id integer PRIMARY KEY AUTOINCREMENT,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  name text NOT NULL UNIQUE,
  unit text
);

CREATE TABLE biometric_log (
  id integer PRIMARY KEY AUTOINCREMENT,
  profile_id int NOT NULL,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  date int DEFAULT (strftime ('%s', 'now')),
  tags text,
  notes text,
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE
);

CREATE TABLE bio_log_entry (
  log_id int NOT NULL,
  biometric_id int NOT NULL,
  value real NOT NULL,
  PRIMARY KEY (log_id, biometric_id),
  FOREIGN KEY (log_id) REFERENCES biometric_log (id) ON UPDATE CASCADE,
  FOREIGN KEY (biometric_id) REFERENCES biometrics (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Recipes
--------------------------------

CREATE TABLE recipes (
  id integer PRIMARY KEY AUTOINCREMENT,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  tagname text NOT NULL UNIQUE,
  name text NOT NULL UNIQUE
);

CREATE TABLE recipe_dat (
  recipe_id int NOT NULL,
  food_id int NOT NULL,
  grams real NOT NULL,
  notes text,
  PRIMARY KEY (recipe_id, food_id),
  FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Custom foods
--------------------------------

CREATE TABLE custom_foods (
  id integer PRIMARY KEY AUTOINCREMENT,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  tagname text NOT NULL UNIQUE,
  name text NOT NULL UNIQUE
);

CREATE TABLE cf_dat (
  cf_id int NOT NULL,
  nutr_id int NOT NULL, -- no FK constraining on usda :[
  nutr_val real NOT NULL,
  notes text,
  PRIMARY KEY (cf_id, nutr_id),
  FOREIGN KEY (cf_id) REFERENCES custom_foods (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Food (and recipe) logs
--------------------------------

CREATE TABLE meal_name (
  -- predefined, includes standard three, snacks, brunch, and 3 optional/extra meals
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL
);

CREATE TABLE food_log (
  id integer PRIMARY KEY AUTOINCREMENT,
  profile_id int NOT NULL,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  date int DEFAULT (strftime ('%s', 'now')),
  meal_id int NOT NULL,
  food_id int NOT NULL,
  msre_id int NOT NULL,
  amt real NOT NULL,
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE,
  FOREIGN KEY (meal_id) REFERENCES meal_name (id) ON UPDATE CASCADE
);

CREATE TABLE recipe_log (
  id integer PRIMARY KEY AUTOINCREMENT,
  profile_id int NOT NULL,
  created int DEFAULT (strftime ('%s', 'now')),
  updated int DEFAULT (strftime ('%s', 'now')),
  date int DEFAULT (strftime ('%s', 'now')),
  meal_id int NOT NULL,
  recipe_id int NOT NULL,
  grams real NOT NULL,
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE,
  FOREIGN KEY (meal_id) REFERENCES meal_name (id) ON UPDATE CASCADE,
  FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON UPDATE CASCADE
);

-- TODO: CREATE TABLE custom_food_log ( ... );
--
--------------------------------
-- Custom RDAs
--------------------------------

CREATE TABLE rda (
  profile_id int NOT NULL,
  nutr_id int NOT NULL,
  rda real NOT NULL,
  PRIMARY KEY (profile_id, nutr_id),
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE
);

--
--------------------------------
-- Food costs
--------------------------------

CREATE TABLE food_costs (
  food_id integer NOT NULL,
  profile_id integer NOT NULL,
  cost real NOT NULL,
  PRIMARY KEY (food_id, profile_id),
  FOREIGN KEY (profile_id) REFERENCES profiles (id) ON UPDATE CASCADE ON DELETE CASCADE
);

