# 데이터 수집 스크립트

프로젝트 구텐베르크에서 문학 작품을 다운로드하고 시간이 언급된 문장을 추출합니다.

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

1. **도서 다운로드**
```bash
python download_books.py
```

2. **시간 문장 추출**
```bash
python extract_times.py
```

## 추출되는 시간 패턴

영어 패턴:
- 숫자 시각: "3:00", "4:15 PM", "10:30 am"
- 문자 시각: "three o'clock", "half past four", "quarter to nine"
- 구어체: "midnight", "noon", "morning", "evening"

## 출력

`../public/times.json` 파일에 다음 형식으로 저장됩니다:

```json
{
  "09:13": [
    {
      "quote": "At nine thirteen, the clock struck.",
      "title": "Example Book",
      "author": "Example Author"
    }
  ]
}
```
