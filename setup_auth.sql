-- 1. Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'member', 
    allowed_tools TEXT[] DEFAULT ARRAY['Dashboard'], 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Insert the Admin user (Password: admin123)
-- Uses ON CONFLICT to avoid errors if user already exists
INSERT INTO users (email, password_hash, role, allowed_tools)
VALUES (
    'admin@trikon.com', 
    '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 
    'admin', 
    ARRAY['Dashboard', 'Business Card', 'Welcome Aboard', 'ID Card', 'Settings']
)
ON CONFLICT (email) DO NOTHING;

-- 3. CRITICAL: Configure Permissions (Row Level Security)
-- This allows your Streamlit app (which uses the public key) to Read and Write to this table.

ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Allow the app to READ user data (for Login)
DROP POLICY IF EXISTS "Allow public read" ON users;
CREATE POLICY "Allow public read"
ON users FOR SELECT
TO anon
USING (true);

-- Allow the app to INSERT new users (for Admin Settings)
-- Note: In a real production app, you would restrict this further.
DROP POLICY IF EXISTS "Allow public insert" ON users;
CREATE POLICY "Allow public insert"
ON users FOR INSERT
TO anon
WITH CHECK (true);
