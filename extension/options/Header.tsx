import type { User } from "@supabase/supabase-js"

import { Storage } from "@plasmohq/storage"
import { useStorage } from "@plasmohq/storage/hook"

export default function Header() {
  const [user, setUser] = useStorage<User>({
    key: "user",
    instance: new Storage()
  })

  return (
    <div className="absolute top-0 left-0 right-0 z-10 w-full px-6 flex justify-between items-center my-4 md:my-6 bg-background-primary text-text-primary">
      <a
        className="font-bold text-xl"
        href={`chrome-extension://${process.env.PLASMO_PUBLIC_CRX_ID}/options.html`}>
        SitDowns 😈
      </a>
      <div className="flex items-center">
        {user && (
          <a
            href={`chrome-extension://${process.env.PLASMO_PUBLIC_CRX_ID}/tabs/graph.html`}
            className="text-lg text-text-secondary mr-16">
            Graph
          </a>
        )}
        {user ? (
          <div className="text-lg text-text-secondary">
            {user.user_metadata.name}
          </div>
        ) : (
          <div></div>
        )}
      </div>
    </div>
  )
}
