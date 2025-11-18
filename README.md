# Literwatchure

문학 작품 속 시간을 통해 현재 시각을 보여주는 Literary Clock

## 소개

Literwatchure는 프로젝트 구텐베르크(Project Gutenberg)의 공개 문학 작품에서 시간이 언급된 문장을 추출하여, 현재 시각에 해당하는 문학적 표현을 보여주는 웹 애플리케이션입니다.

예를 들어, 현재 시각이 오후 3시라면 "The clock struck three o'clock, and I heard him walk to the door." (Wuthering Heights, Emily Brontë)와 같은 문장이 표시됩니다.

## 프로젝트 구조

```
literwatchure/
├── data-collection/          # 데이터 수집 스크립트 (Python)
│   ├── download_books.py     # 프로젝트 구텐베르크에서 책 다운로드
│   ├── extract_times.py      # 시간이 언급된 문장 추출
│   └── requirements.txt      # Python 의존성
├── src/                      # React 웹 앱
│   ├── components/
│   │   ├── Clock.jsx         # 시계 컴포넌트
│   │   └── Quote.jsx         # 문장 표시 컴포넌트
│   └── App.jsx
├── public/
│   └── times.json            # 추출된 시간별 문장 데이터
└── package.json
```

## 시작하기

### 필요 사항

- Node.js 18 이상
- Python 3.8 이상
- npm 또는 yarn

### 1. 데이터 수집 (선택사항)

프로젝트에는 이미 샘플 데이터가 포함되어 있습니다. 더 많은 문장을 수집하려면 아래 단계를 따르세요:

```bash
cd data-collection
pip install -r requirements.txt
python download_books.py      # 25개 이상의 고전 문학 작품 다운로드
python extract_times.py       # 시간 문장 추출 및 JSON 생성
```

이 과정은 약 5-10분 정도 소요됩니다.

### 2. 웹 앱 실행

```bash
npm install
npm run dev
```

브라우저에서 http://localhost:5173 을 열어 확인하세요.

### 3. 프로덕션 빌드

```bash
npm run build
npm run preview
```

## 기능

- **실시간 시계**: 현재 시각을 크게 표시
- **문학적 시간**: 현재 시각에 해당하는 문학 작품 속 문장 표시
- **작품 정보**: 문장이 나온 작품 제목과 저자 표시
- **자동 업데이트**: 매분마다 새로운 문장으로 자동 업데이트
- **반응형 디자인**: 모바일, 태블릿, 데스크톱 모두 지원
- **다크 모드**: 시스템 설정에 따라 자동 전환

## 수집되는 작품 목록

- Pride and Prejudice (Jane Austen)
- Frankenstein (Mary Shelley)
- The Adventures of Sherlock Holmes (Arthur Conan Doyle)
- Alice's Adventures in Wonderland (Lewis Carroll)
- Dracula (Bram Stoker)
- Jane Eyre (Charlotte Brontë)
- Wuthering Heights (Emily Brontë)
- Moby Dick (Herman Melville)
- A Tale of Two Cities (Charles Dickens)
- 그 외 20여 개의 고전 문학 작품

## 기술 스택

- **Frontend**: React 18 + Vite
- **Styling**: CSS3 (vanilla CSS)
- **Data Collection**: Python 3
- **Data Source**: Project Gutenberg

## 라이선스

이 프로젝트는 MIT 라이선스로 제공됩니다.
모든 문학 작품의 텍스트는 Project Gutenberg에서 제공되며 퍼블릭 도메인입니다.

## 기여

버그 리포트, 기능 제안, PR은 언제든 환영합니다!

## 크레딧

- 문학 작품 출처: [Project Gutenberg](https://www.gutenberg.org/)
- Literary Clock 아이디어에서 영감을 받았습니다
