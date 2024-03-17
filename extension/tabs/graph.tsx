import Header from "../options/Header"

import "../style.css"

export default function Graph() {
  return (
    <div className="h-full min-h-screen w-full bg-background text-text-primary">
      <Header />
      <div className="w-full flex flex-col px-6 mt-24 mb-12">
        <iframe
          src="https://atlas.nomic.ai/data/vincetiu8/sit-downs-pages/map"
          className="w-full h-[48rem] rounded-[2rem]"
        />
      </div>
    </div>
  )
}
