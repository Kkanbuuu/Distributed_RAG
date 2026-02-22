# RAG Client

React 기반 채팅 UI. 사용자 입력을 오케스트레이터 `/query` API로 보내고, 생성된 답변을 채팅 형태로 표시합니다.

## 로컬 개발

1. 의존성 설치 및 실행:

```bash
cd client
npm install
npm run dev
```

2. 브라우저에서 http://localhost:5173 접속.

3. 오케스트레이터가 **다른 포트**라면:

- `.env` 파일 생성 후 `VITE_ORCHESTRATOR_URL=http://localhost:8000` 설정  
  또는
- `vite.config.js`의 proxy `target`을 해당 주소로 변경.

기본값은 Vite 프록시 `/api` → `http://localhost:8000` 이므로, 오케스트레이터를 8000번에서 띄우면 별도 설정 없이 동작합니다.

## Docker Compose로 실행

프로젝트 루트에서:

```bash
docker compose up -d
```

클라이언트는 http://localhost:3000 (또는 compose에 설정한 포트)에서 접속합니다.

## 빌드

```bash
npm run build
```

산출물은 `dist/`에 생성됩니다.
