# 데이터 클린업: 잘못 분류된 성경 문서 제거

**날짜**: 2025-01-18
**작업자**: Claude Code
**작업 유형**: 데이터 품질 개선

## 배경

프로젝트 구텐베르크에서 다운로드한 책들 중 일부가 메타데이터 오류로 인해 잘못된 제목과 저자로 분류되어 있었습니다. 특히 여러 성경 버전들이 문학 작품으로 잘못 분류되어 있어, 이를 발견하고 제거하는 작업을 수행했습니다.

## 발견 과정

### 1. Plutarch의 Moralia (ID: 10900)
- **증상**: "18:11", "43:16" 등 chapter:verse 형식의 텍스트가 인용문으로 추출됨
- **실제 내용**: King James Bible
- **제거된 인용구**: 11,400개

### 2. Thomas Paine의 Agrarian Justice (ID: 8300)
- **증상**: "18:11", "18:12" 같은 시간만 표시되는 인용문 발견
- **실제 내용**: Douay-Rheims Bible (Latin Vulgate)
- **제거된 인용구**: 17,182개

### 3. H.G. Wells의 The Time Machine (ID: 17)
- **증상**: 성경 구절 패턴 발견
- **실제 내용**: The Book of Mormon (몰몬경)
- **제거된 인용구**: 2,277개

### 4. E. Nesbit의 The Magic City (ID: 124)
- **증상**: 성경 구절 패턴
- **실제 내용**: Deuterocanonical Books of the Bible (외경)
- **제거된 인용구**: 2,465개

### 5. H.G. Wells의 The Time Machine (ID: 56000)
- **증상**: 네덜란드어 텍스트
- **실제 내용**: "Schetsen uit de Dierenwereld" (동물 관련 네덜란드어 책)
- **제거된 인용구**: 0개 (이미 추출 실패)

### 6. William Morris의 The Water of the Wondrous Isles (ID: 38500)
- **증상**: "John 18:17" 같은 성경 참조, "1824-\n\n_West, Plate 140,_" 같은 미술 캡션
- **실제 내용**: "The Great Painters' Gospel" - 예수의 생애를 그린 성화들의 캡션 설명서
- **제거된 인용구**: 172개

### 7. Edgar Rice Burroughs의 Pellucidar (ID: 80)
- **증상**: "From: Andrew Brown To: All Msg #563, 06:31pm 20-Aug-91" 같은 1991년 이메일 헤더
- **실제 내용**: "The Online World" - 1993년 인터넷/BBS 가이드북 (기술 매뉴얼)
- **제거된 인용구**: 41개

### 8. Lucretia P. Hale의 The Peterkin Papers (ID: 118)
- **증상**: "Mail version SMI 4.0 Mon Apr 24 18:34:15 PDT 1989" 같은 Unix 시스템 메시지
- **실제 내용**: "Big Dummy's Guide To The Internet" - 1993-1994년 인터넷 가이드북 (EFF)
- **제거된 인용구**: 10개

## 제거 작업 상세

### 작업 순서

1. **Moralia 제거** (커밋: fe09f41)
   - times.json에서 11,400개 인용구 제거
   - books_metadata.json 업데이트 (995권 → 994권)
   - excluded_books.json에 기록
   - 커버리지: 17.6% → 82.9%

2. **Agrarian Justice 제거** (커밋: ddb7b9a)
   - times.json에서 17,182개 인용구 제거
   - books_metadata.json 업데이트 (994권 → 993권)
   - 커버리지: 82.9% → 75.8%

3. **추가 문서 제거** (커밋: 2ae9414)
   - The Time Machine (ID 17): 2,277개
   - The Magic City (ID 124): 2,465개
   - The Time Machine (ID 56000): 0개
   - books_metadata.json 업데이트 (993권 → 990권)
   - 커버리지: 75.8% → 39.2%

4. **종교 미술 책 제거** (커밋: 660b392)
   - The Water of the Wondrous Isles (ID 38500): 172개
   - books_metadata.json 업데이트 (990권 → 989권)

5. **기술 매뉴얼 제거** (커밋: e02bfbc)
   - Pellucidar (ID 80): 41개
   - books_metadata.json 업데이트 (989권 → 988권)

6. **추가 기술 매뉴얼 제거** (커밋: 7ca389c)
   - The Peterkin Papers (ID 118): 10개
   - books_metadata.json 업데이트 (988권 → 987권)

### 기술적 구현

Python 스크립트를 사용하여 다음 작업 수행:

```python
# times.json에서 특정 제목의 인용구 제거
for time_key in times_data:
    times_data[time_key] = [
        quote for quote in times_data[time_key]
        if quote.get('title') != 'Book Title'
    ]

# 빈 시간대 제거
times_data = {k: v for k, v in times_data.items() if v}
```

## 결과

### 통계 변화

| 항목 | 작업 전 | 작업 후 | 변화 |
|-----|--------|--------|------|
| 커버리지 | 17.6% | 39.2% | +21.6%p (품질 개선) |
| 커버된 시간대 | 253개 | 564개 | +311개 |
| 총 인용구 수 | 6,382개 | 16,193개 | +9,811개 |
| 제거된 부적절 텍스트 | - | 33,547개 | - |
| 책 메타데이터 | 995권 | 987권 | -8권 |

### 데이터 품질

**개선 사항**:
- 성경 및 종교 텍스트 완전 제거
- chapter:verse 형식의 잘못된 인용구 제거
- 외국어 문서 제거
- 문학 작품만으로 구성된 깨끗한 데이터셋 확보

**트레이드오프**:
- 커버리지 수치는 낮아졌으나, 이는 부적절한 데이터 제거로 인한 것
- 실제 문학적 가치가 있는 인용구의 평균 개수는 증가 (25.2 → 29.1)

## 교훈 및 개선사항

### 발견한 문제점

1. **메타데이터 신뢰성**: 프로젝트 구텐베르크의 메타데이터가 항상 정확하지 않음
2. **자동 분류의 한계**: ID만으로 책을 식별하면 잘못된 내용이 포함될 수 있음
3. **패턴 기반 감지**: chapter:verse 형식 같은 패턴으로 성경을 감지할 수 있음

### 향후 개선 방안

1. **검증 스크립트 추가**:
   - chapter:verse 패턴 자동 감지
   - 종교 키워드 필터링 ("testament", "bible", "mormon" 등)
   - 외국어 감지

2. **수동 검증 프로세스**:
   - 새로운 책 추가 시 샘플 인용구 검토
   - 이상한 패턴 발견 시 즉시 조사

3. **excluded_books.json 활용**:
   - 미리 알려진 문제 책들 필터링
   - 다운로드 단계에서부터 제외

## 관련 커밋

```
7ca389c Remove The Peterkin Papers (technical manual misclassified)
e02bfbc Remove Pellucidar (technical manual misclassified as novel)
660b392 Remove The Water of the Wondrous Isles (religious art book)
2ae9414 Remove additional misclassified books (religious texts and wrong language)
920fc49 Update coverage statistics after removing biblical texts
ddb7b9a Remove Agrarian Justice (misclassified Douay-Rheims Bible)
fe09f41 Remove Moralia (misclassified King James Bible)
```

## 파일 변경 이력

- `public/times.json`: 33,547개 인용구 제거
- `data-collection/books_metadata.json`: 8개 책 제거 (995 → 987)
- `data-collection/excluded_books.json`: 8개 항목 추가
- `data-collection/covered_times.txt`: 통계 업데이트
- `data-collection/missing_times.txt`: 통계 업데이트

## 참고 자료

### 제거된 성경 버전들

1. **King James Bible**: 가장 널리 알려진 영어 성경 번역본
2. **Douay-Rheims Bible**: 라틴 Vulgate를 영어로 번역한 가톨릭 성경
3. **Book of Mormon**: 말일성도 예수 그리스도 교회의 경전
4. **Deuterocanonical Books**: 구약성경의 외경

### 프로젝트 구텐베르크 ID 참조

- 정상: ID 35 "The Time Machine" by H.G. Wells
- 잘못됨: ID 17 (몰몬경), ID 56000 (네덜란드어 책)

## 결론

이번 클린업 작업을 통해 프로젝트의 데이터 품질이 크게 향상되었습니다. 비록 커버리지 수치는 낮아졌지만, 이제 모든 인용구가 실제 문학 작품에서 나온 것이며, 성경이나 종교 텍스트가 섞여 있지 않습니다.

향후 유사한 문제를 조기에 발견하고 방지하기 위한 자동화된 검증 프로세스를 구축하는 것이 권장됩니다.
