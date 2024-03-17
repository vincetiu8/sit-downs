import { useEffect, useState } from "react"

import "../style.css"

import type { User } from "@supabase/supabase-js"

import { sendToBackground } from "@plasmohq/messaging"
import { Storage } from "@plasmohq/storage"
import { useStorage } from "@plasmohq/storage/hook"

import Header from "./Header"
import SummaryCard from "./SummaryCard"

function OptionsIndex() {
  const [user, setUser] = useStorage<User>({
    key: "user",
    instance: new Storage()
  })

  const [myResults, setMyResults] = useState<any>({})
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const today: Date = new Date()
  const options: Intl.DateTimeFormatOptions = { month: "long", day: "numeric" }
  const formattedDate: string = today.toLocaleDateString("en-US", options)

  useEffect(() => {
    if (!user) {
      return
    }

    const loadData = async () => {
      const response = await sendToBackground({ name: "getRelevantToday" })
      setResults(response)
      const me = await sendToBackground({ name: "getMeToday" })
      setMyResults(me)
      setLoading(false)
    }
    loadData()
  }, [user])

  const filteredResults = results.filter((post) => {
    return (
      post.one_sentence_summary
        .toLowerCase()
        .includes(searchTerm.toLowerCase()) ||
      post.summary.toLowerCase().includes(searchTerm.toLowerCase())
    )
  })

  if (!user) {
    return (
      <div className="h-full min-h-screen w-full bg-background text-text-primary">
        <Header />
        <div className="container mx-auto max-w-screen-lg flex flex-col px-6 mt-24 mb-12">
          <div className="text-lg text-primary">{formattedDate}</div>
          <div className="text-4xl mt-2 mb-4">
            Hey there, welcome to SitDowns!
          </div>
          <div className="flex justify-center px-6 py-4 w-full border border-border-color rounded-full bg-background-light text-lg text-text-primary my-4 focus:outline-none">
            You're not logged in. Please log in to see your feed.
          </div>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="h-full min-h-screen w-full bg-background text-text-primary">
        <Header />
        <div className="container mx-auto max-w-screen-lg flex flex-col px-6 mt-24 mb-12">
          <div className="text-lg text-primary">{formattedDate}</div>
          <div className="text-4xl mt-2 mb-4">
            Hey {user.user_metadata.name}, here are today's sit downs!
          </div>
          <div className="flex justify-center animate-pulse px-6 py-4 w-full border border-border-color rounded-full bg-background-light text-lg text-text-primary my-4 focus:outline-none">
            Loading...
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full min-h-screen w-full bg-background text-text-primary">
      <Header />
      <div className="container mx-auto max-w-screen-lg flex flex-col px-6 mt-24 mb-12">
        <div className="text-lg text-primary">{formattedDate}</div>
        <div className="text-4xl mt-2 mb-4">
          Hey {user.user_metadata.name}, here are today's sit downs!
        </div>
        <input
          type="text"
          placeholder="Search your team's sit downs"
          className="px-6 py-4 w-full border border-border-color rounded-full bg-background-light text-lg text-text-primary my-4 focus:outline-none"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <SummaryCard
          person={
            myResults.one_sentence_summary_second_person
              ? myResults.one_sentence_summary_second_person.split(" ")[0]
              : myResults.one_sentence_summary.split(" ")[0]
          }
          action={
            myResults.one_sentence_summary_second_person
              ? myResults.one_sentence_summary_second_person
                  .split(" ")
                  .slice(1)
                  .join(" ")
              : myResults.one_sentence_summary.split(" ").slice(1).join(" ")
          }
          date={myResults.date}
          text={myResults.summary}
          links={myResults.links}
        />
        {filteredResults.map((post, index) => (
          <SummaryCard
            key={index}
            person={post.one_sentence_summary.split(" ")[0]}
            action={post.one_sentence_summary.split(" ").slice(1).join(" ")}
            date={post.date}
            text={post.summary}
            links={post.links}
          />
        ))}
      </div>
    </div>
  )
}

export default OptionsIndex
