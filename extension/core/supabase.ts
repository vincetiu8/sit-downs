import { createClient } from "@supabase/supabase-js"
 
import { Storage } from "@plasmohq/storage"
 
const storage = new Storage()

console.log(process.env.SUPABASE_URL)
 
export const supabase = createClient(
  process.env.PLASMO_PUBLIC_SUPABASE_URL,
  process.env.PLASMO_PUBLIC_SUPABASE_KEY,
  {
    auth: {
      storage,
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true
    }
  }
)
