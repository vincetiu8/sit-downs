import type { Provider, User } from "@supabase/supabase-js"
import { useEffect, useState } from "react"

import { Storage } from "@plasmohq/storage"
import { useStorage } from "@plasmohq/storage/hook"

import "../style.css"

import { sendToBackground } from "@plasmohq/messaging"

import { supabase } from "~core/supabase"

function toTitleCase(str) {
  return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  })
}

const IndexPopup = () => {
  const [user, setUser] = useStorage<User>({
    key: "user",
    instance: new Storage()
  })

  useEffect(() => {
    async function init() {
      const { data, error } = await supabase.auth.getSession()

      if (error) {
        console.error(error)
        return
      }
      if (!!data.session) {
        setUser(data.session.user)
      }
    }

    init()
  }, [])

  const [signup, setSignup] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [name, setName] = useState("")

  const handleEmailLogin = async (email: string, password: string) => {
    try {
      const { error, data } = await supabase.auth.signInWithPassword({
        email,
        password
      })

      if (error) {
        alert("Error with auth: " + error.message)
      } else {
        setUser(data.user)
      }
    } catch (error) {
      console.log("error", error)
      alert(error.error_description || error)
    }
  }

  const handleEmailSignup = async (
    email: string,
    password: string,
    name: string
  ) => {
    try {
      const { error, data } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            name: toTitleCase(name)
          }
        }
      })

      if (error) {
        alert("Error with auth: " + error.message)
      } else {
        setUser(data.user)
      }
    } catch (error) {
      console.log("error", error)
      alert(error.error_description || error)
    }
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    setUser(null)
  }

  const [isOn, setIsOn] = useState(true)

  const goToDashboard = () => {
    window.open(
      `chrome-extension://${process.env.PLASMO_PUBLIC_CRX_ID}/options.html`
    )
  }

  return (
    <div className="p-4 bg-background flex flex-col text-text-primary w-64">
      <h2 className="text-xl font-bold text-center w-full">SitDowns 😈</h2>
      {user ? (
        <>
          <div className="flex items-center justify-center">
            <label className="w-full my-4 flex justify-center items-center cursor-pointer">
              <input
                type="checkbox"
                checked={isOn}
                onChange={() => setIsOn(!isOn)}
                className="sr-only peer"
              />
              <div className="relative w-11 h-6 bg-background-light rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary"></div>
            </label>
          </div>
          <button
            className="btn my-2 border-primary"
            onClick={() => goToDashboard()}>
            Dashboard
          </button>
          <button className="btn" onClick={() => handleLogout()}>
            Logout
          </button>
        </>
      ) : (
        <>
          {signup && (
            <>
              <label className="mt-2">Name</label>
              <input
                type="text"
                placeholder="Your Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="rounded-lg h-8 p-2 text-text-primary bg-background-light focus:outline-none"
              />
            </>
          )}

          <label className="mt-2">Email</label>
          <input
            type="text"
            placeholder="Your Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="rounded-lg h-8 p-2 text-text-primary bg-background-light focus:outline-none"
          />
          <label className="mt-2">Password</label>
          <input
            type="password"
            placeholder="Your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="rounded-lg h-8 p-2 text-text-primary bg-background-light focus:outline-none"
          />

          <button
            className="btn mt-4 mb-2 border-primary"
            onClick={(e) => {
              signup
                ? handleEmailSignup(email, password, name)
                : handleEmailLogin(email, password)
            }}>
            {signup ? "Sign up" : "Login"}
          </button>

          <button
            className="btn"
            onClick={(e) => {
              setSignup(!signup)
            }}>
            {signup ? "Login" : "Sign up"}
          </button>
        </>
      )}
    </div>
  )
}

export default IndexPopup
