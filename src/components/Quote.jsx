import './Quote.css'

function Quote({ quote }) {
  if (!quote) {
    return (
      <div className="quote no-quote">
        <p className="quote-text">
          이 시각에 해당하는 문장을 찾지 못했습니다.
        </p>
        <p className="quote-hint">
          잠시만 기다려주세요. 다음 분에 새로운 문장이 나타날 수 있습니다.
        </p>
      </div>
    )
  }

  return (
    <div className="quote">
      <div className="quote-mark opening">&ldquo;</div>
      <p className="quote-text">{quote.quote}</p>
      <div className="quote-mark closing">&rdquo;</div>

      <div className="quote-attribution">
        <p className="quote-title">{quote.title}</p>
        <p className="quote-author">by {quote.author}</p>
      </div>
    </div>
  )
}

export default Quote
