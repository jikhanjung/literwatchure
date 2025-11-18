import './Clock.css'

function Clock({ time }) {
  const hours = String(time.getHours()).padStart(2, '0')
  const minutes = String(time.getMinutes()).padStart(2, '0')
  const seconds = String(time.getSeconds()).padStart(2, '0')

  return (
    <div className="clock">
      <div className="time-display">
        <span className="time-hours">{hours}</span>
        <span className="time-separator">:</span>
        <span className="time-minutes">{minutes}</span>
        <span className="time-separator seconds">:</span>
        <span className="time-seconds">{seconds}</span>
      </div>
    </div>
  )
}

export default Clock
