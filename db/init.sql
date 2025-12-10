CREATE TABLE IF NOT EXISTS account (
  user_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_name text UNIQUE NOT NULL,
  user_email text UNIQUE,
  user_password text NOT NULL,
  permission integer DEFAULT 0,
  signed_up_time timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS exam (
  id serial PRIMARY KEY,
  user_id uuid REFERENCES account(user_id),
  exam_id text NOT NULL,
  exam_name text NOT NULL,
  exam_score integer NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS task (
  task_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  description text,
  answer text,
  hint text,
  category text,
  difficulty text DEFAULT 'Easy',
  tags text[],
  points integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS traffic_log (
  id serial PRIMARY KEY,
  user_id uuid,
  path text,
  method text,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_exam_user ON exam(user_id);

CREATE TABLE IF NOT EXISTS solved_task (
  id serial PRIMARY KEY,
  user_id uuid REFERENCES account(user_id),
  task_id uuid REFERENCES task(task_id),
  points integer NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS solved_unique ON solved_task(user_id, task_id);