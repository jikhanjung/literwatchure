import './Quote.css'

function Quote({ quote: quoteData }) {
  if (!quoteData) {
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

  const { quote, exactMatch, closestTime } = quoteData

  // 시간 표현을 찾아서 bold 처리하는 함수
  const highlightTime = (text) => {
    // 시간 관련 패턴들
    const timePatterns = [
      // 숫자:숫자 형식 (3:30, 15:45 등)
      /\b\d{1,2}:\d{2}(?:\s*(?:a\.?m\.?|p\.?m\.?|AM|PM|o'clock))?\b/gi,
      // o'clock 표현 (three o'clock, 3 o'clock 등)
      /\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2})\s+o'clock\b/gi,
      // half/quarter past/to (half past three, quarter to four 등)
      /\b(?:half|quarter)\s+(?:past|to)\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2})\b/gi,
      // 단순 시간 숫자 앞뒤 컨텍스트 (at three, at 3, by noon, until midnight 등)
      /\b(?:at|by|until|till|about|around|near|nearly)\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|noon|midnight|\d{1,2}(?:\s*(?:a\.?m\.?|p\.?m\.?|AM|PM))?)\b/gi,
      // 시간만 (one, two, three 등이 문맥상 시간일 때)
      /\b(?:noon|midnight|morning|evening|night|afternoon)\b/gi,
    ]

    let parts = [text]

    timePatterns.forEach(pattern => {
      const newParts = []
      parts.forEach(part => {
        if (typeof part === 'string') {
          const matches = [...part.matchAll(pattern)]
          if (matches.length > 0) {
            let lastIndex = 0
            matches.forEach(match => {
              // 매치 전 텍스트
              if (match.index > lastIndex) {
                newParts.push(part.substring(lastIndex, match.index))
              }
              // 매치된 시간 표현 (bold)
              newParts.push(<strong key={`${match.index}-${match[0]}`}>{match[0]}</strong>)
              lastIndex = match.index + match[0].length
            })
            // 남은 텍스트
            if (lastIndex < part.length) {
              newParts.push(part.substring(lastIndex))
            }
          } else {
            newParts.push(part)
          }
        } else {
          newParts.push(part)
        }
      })
      parts = newParts
    })

    return parts
  }

  return (
    <div className="quote">
      <div className="quote-mark opening">&ldquo;</div>
      <p className="quote-text">{highlightTime(quote.quote)}</p>
      <div className="quote-mark closing">&rdquo;</div>

      <div className="quote-attribution">
        <p className="quote-title">{quote.title}</p>
        <p className="quote-author">by {quote.author}</p>
        {!exactMatch && closestTime && (
          <p className="quote-time-note">
            (가장 가까운 시각: {closestTime})
          </p>
        )}
      </div>
    </div>
  )
}

export default Quote
