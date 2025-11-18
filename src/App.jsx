import { useState, useEffect } from 'react'
import Clock from './components/Clock'
import Quote from './components/Quote'
import './App.css'

function App() {
  const [currentTime, setCurrentTime] = useState(new Date())
  const [timesData, setTimesData] = useState(null)
  const [currentQuote, setCurrentQuote] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // 시간 데이터 로드
  useEffect(() => {
    fetch('/times.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('시간 데이터를 불러올 수 없습니다.')
        }
        return response.json()
      })
      .then(data => {
        setTimesData(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  // 시계 업데이트 (매초)
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  // 현재 시각에 맞는 quote 선택
  useEffect(() => {
    if (!timesData) return

    const hours = currentTime.getHours()
    const minutes = currentTime.getMinutes()
    const timeKey = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`

    const quotes = timesData[timeKey]
    if (quotes && quotes.length > 0) {
      // 랜덤하게 하나 선택
      const randomQuote = quotes[Math.floor(Math.random() * quotes.length)]
      setCurrentQuote(randomQuote)
    } else {
      setCurrentQuote(null)
    }
  }, [currentTime, timesData])

  return (
    <div className="app">
      <header className="header">
        <h1>Literwatchure</h1>
        <p>문학 작품 속 시간으로 보는 현재</p>
      </header>

      <div className="content">
        <Clock time={currentTime} />

        {loading && <p className="loading">문학 작품을 불러오는 중...</p>}
        {error && <p className="error">{error}</p>}
        {!loading && !error && <Quote quote={currentQuote} />}
      </div>

      <footer style={{ opacity: 0.5, fontSize: '0.9rem', marginTop: 'auto' }}>
        <p>작품 출처: Project Gutenberg</p>
      </footer>
    </div>
  )
}

export default App
