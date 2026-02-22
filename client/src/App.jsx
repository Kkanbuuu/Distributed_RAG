import { useState, useRef, useEffect } from 'react'
import { sendQuery } from './api'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading) return

    setInput('')
    setError(null)
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setLoading(true)

    try {
      const data = await sendQuery(text)
      const answer = data.answer ?? '답변을 생성할 수 없습니다.'
      setMessages((prev) => [...prev, { role: 'assistant', content: answer }])
    } catch (err) {
      setError(err.message)
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `오류: ${err.message}`, isError: true },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1 className="logo">RAG Assistant</h1>
        <p className="tagline">문서 기반 질의응답</p>
      </header>

      <main className="main">
        {messages.length === 0 && (
          <div className="welcome">
            <p>질문을 입력하면 관련 문서를 검색한 뒤 답변을 생성합니다.</p>
            <p className="hint">예: 프로젝트 개요 알려줘, PostgreSQL 개념 설명해줘</p>
          </div>
        )}

        <div className="messages">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role} ${msg.isError ? 'error' : ''}`}>
              <div className="avatar">
                {msg.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="bubble">
                <div className="content">{msg.content}</div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="avatar">🤖</div>
              <div className="bubble loading">
                <span className="dot" />
                <span className="dot" />
                <span className="dot" />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {error && (
          <div className="toast error" role="alert">
            {error}
          </div>
        )}

        <form className="input-area" onSubmit={handleSubmit}>
          <textarea
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
            placeholder="메시지를 입력하세요..."
            rows={1}
            disabled={loading}
          />
          <button type="submit" className="send" disabled={loading || !input.trim()}>
            전송
          </button>
        </form>
      </main>
    </div>
  )
}

export default App
