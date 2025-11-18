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
  const [lastQuoteChangeTime, setLastQuoteChangeTime] = useState(null)
  const [currentTimeKey, setCurrentTimeKey] = useState(null)

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

  // 시간을 분 단위로 변환 (00:00 = 0, 23:59 = 1439)
  const timeToMinutes = (hours, minutes) => hours * 60 + minutes

  // 두 시간 사이의 최소 거리 계산 (원형으로)
  const getMinuteDistance = (time1, time2) => {
    const diff = Math.abs(time1 - time2)
    return Math.min(diff, 1440 - diff) // 1440분 = 24시간
  }

  // 가장 가까운 시간의 quote 찾기
  const findClosestQuote = (targetTimeKey) => {
    const availableTimes = Object.keys(timesData)
    if (availableTimes.length === 0) return null

    // 현재 시간에 정확히 매칭되는 quote가 있으면 반환
    if (timesData[targetTimeKey] && timesData[targetTimeKey].length > 0) {
      const randomQuote = timesData[targetTimeKey][Math.floor(Math.random() * timesData[targetTimeKey].length)]
      return { quote: randomQuote, exactMatch: true }
    }

    // 목표 시간을 분으로 변환
    const [targetHours, targetMinutes] = targetTimeKey.split(':').map(Number)
    const targetInMinutes = timeToMinutes(targetHours, targetMinutes)

    // 가장 가까운 시간 찾기
    let closestTime = null
    let minDistance = Infinity

    availableTimes.forEach(timeKey => {
      const [hours, minutes] = timeKey.split(':').map(Number)
      const timeInMinutes = timeToMinutes(hours, minutes)
      const distance = getMinuteDistance(targetInMinutes, timeInMinutes)

      if (distance < minDistance) {
        minDistance = distance
        closestTime = timeKey
      }
    })

    if (closestTime && timesData[closestTime].length > 0) {
      const randomQuote = timesData[closestTime][Math.floor(Math.random() * timesData[closestTime].length)]
      return { quote: randomQuote, exactMatch: false, closestTime }
    }

    return null
  }

  // 현재 시각에 맞는 quote 선택
  useEffect(() => {
    if (!timesData) return

    const hours = currentTime.getHours()
    const minutes = currentTime.getMinutes()
    const timeKey = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`

    const now = Date.now()
    const timeSinceLastChange = lastQuoteChangeTime ? now - lastQuoteChangeTime : Infinity

    // 분이 바뀌었거나, 마지막 변경으로부터 10초 이상 경과했을 때만 quote 변경
    const shouldChangeQuote =
      timeKey !== currentTimeKey || // 분이 바뀜
      timeSinceLastChange >= 10000 || // 10초 경과
      !currentQuote // 첫 로드

    if (shouldChangeQuote) {
      const result = findClosestQuote(timeKey)
      setCurrentQuote(result)
      setLastQuoteChangeTime(now)
      setCurrentTimeKey(timeKey)
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
