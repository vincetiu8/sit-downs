const LinksCard = () => {
  const dummyLinks = [
    ["Plasmo", "https://www.plasmo.com"],
    ["Plasmo", "https://www.plasmo.com"],
    ["Plasmo", "https://www.plasmo.com"]
  ]

  return (
    <div className="border border-zinc-200 rounded-lg flex flex-col p-4 basis-8/12">
      <h2 className="text-xl text-center">Top Visited Websites</h2>
      {dummyLinks.map(([name, link]) => {
        return (
          <a
            href={link}
            className="hover:text-zinc-50"
            target="_blank"
            rel="noopener noreferrer">
            {name}{" "}
            <span className="text-sky-300 hover:text-sky-400">({link})</span>
          </a>
        )
      })}
    </div>
  )
}

export default LinksCard
