import type { PlasmoMessaging } from "@plasmohq/messaging"
import { Storage } from "@plasmohq/storage"
import type { User } from "@supabase/supabase-js"
 
const handler: PlasmoMessaging.MessageHandler = async (req, res) => {
  const storage = new Storage()

  const user = await storage.get<User>("user")

  if (!user.id) {
    res.send({
      status: "error",
      message: "No user is logged in"
    })
    return
  }

  const message = await fetch(`http://localhost:8000/page/${user.id}`, 
    {
      headers: {
        "Content-Type": "application/json"
      },
      method: "POST",
      body: JSON.stringify(req.body)
    }
  )
 
  res.send({message})
}
 
export default handler