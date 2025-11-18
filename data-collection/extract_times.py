#!/usr/bin/env python3
"""
다운로드한 문학 작품에서 시간이 언급된 문장을 추출합니다.
"""

import os
import re
import json
from collections import defaultdict

# 숫자를 단어로 매핑
WORD_TO_NUM = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
    'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
    'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
    'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
    'twenty-one': 21, 'twenty-two': 22, 'twenty-three': 23, 'twenty-four': 24,
    'twenty-five': 25, 'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28,
    'twenty-nine': 29, 'thirty': 30, 'thirty-one': 31, 'thirty-two': 32,
    'thirty-three': 33, 'thirty-four': 34, 'thirty-five': 35, 'thirty-six': 36,
    'thirty-seven': 37, 'thirty-eight': 38, 'thirty-nine': 39, 'forty': 40,
    'forty-one': 41, 'forty-two': 42, 'forty-three': 43, 'forty-four': 44,
    'forty-five': 45, 'forty-six': 46, 'forty-seven': 47, 'forty-eight': 48,
    'forty-nine': 49, 'fifty': 50, 'fifty-one': 51, 'fifty-two': 52,
    'fifty-three': 53, 'fifty-four': 54, 'fifty-five': 55, 'fifty-six': 56,
    'fifty-seven': 57, 'fifty-eight': 58, 'fifty-nine': 59
}

def parse_time_to_24h(hour, minute, meridiem=None):
    """시간을 24시간 형식으로 변환합니다."""
    if meridiem and meridiem.upper() == 'PM' and hour != 12:
        hour += 12
    elif meridiem and meridiem.upper() == 'AM' and hour == 12:
        hour = 0
    return hour, minute

def extract_time_patterns(text, title, author):
    """텍스트에서 시간 패턴을 추출합니다."""
    results = defaultdict(list)

    # 문장 단위로 분리
    sentences = re.split(r'[.!?]\s+', text)

    for sentence in sentences:
        # 너무 긴 문장은 스킵 (250자 제한)
        if len(sentence) > 250:
            continue

        # 패턴 1: "3:45" 또는 "3:45 PM" 형식
        pattern1 = re.finditer(
            r'\b(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)?\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern1:
            hour = int(match.group(1))
            minute = int(match.group(2))
            meridiem = match.group(3)

            if 0 <= hour <= 23 and 0 <= minute <= 59:
                hour, minute = parse_time_to_24h(hour, minute, meridiem)
                if 0 <= hour <= 23:
                    time_key = f"{hour:02d}:{minute:02d}"
                    results[time_key].append({
                        "quote": sentence.strip(),
                        "title": title,
                        "author": author
                    })

        # 패턴 2: "three o'clock" 형식
        pattern2 = re.finditer(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+o'?\s*clock\b",
            sentence,
            re.IGNORECASE
        )
        for match in pattern2:
            word = match.group(1).lower()
            hour = WORD_TO_NUM.get(word, 0)
            if 1 <= hour <= 12:
                time_key = f"{hour:02d}:00"
                results[time_key].append({
                    "quote": sentence.strip(),
                    "title": title,
                    "author": author
                })

        # 패턴 3: "half past three", "quarter past four" 등
        pattern3 = re.finditer(
            r'\b(half|quarter)\s+past\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern3:
            fraction = match.group(1).lower()
            word = match.group(2).lower()
            hour = WORD_TO_NUM.get(word, 0)
            minute = 30 if fraction == 'half' else 15

            if 1 <= hour <= 12:
                time_key = f"{hour:02d}:{minute:02d}"
                results[time_key].append({
                    "quote": sentence.strip(),
                    "title": title,
                    "author": author
                })

        # 패턴 4: "quarter to four" (4시 15분 전 = 3시 45분)
        pattern4 = re.finditer(
            r'\bquarter\s+to\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern4:
            word = match.group(1).lower()
            hour = WORD_TO_NUM.get(word, 0) - 1
            if hour < 1:
                hour = 12
            minute = 45

            if 1 <= hour <= 12:
                time_key = f"{hour:02d}:{minute:02d}"
                results[time_key].append({
                    "quote": sentence.strip(),
                    "title": title,
                    "author": author
                })

        # 패턴 5: "midnight" (00:00)
        if re.search(r'\bmidnight\b', sentence, re.IGNORECASE):
            results["00:00"].append({
                "quote": sentence.strip(),
                "title": title,
                "author": author
            })

        # 패턴 6: "noon" (12:00)
        if re.search(r'\bnoon\b', sentence, re.IGNORECASE):
            results["12:00"].append({
                "quote": sentence.strip(),
                "title": title,
                "author": author
            })

        # 패턴 7: "twenty minutes past three" - X minutes past Y
        pattern7 = re.finditer(
            r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine)\s+minutes?\s+past\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern7:
            minute_word = match.group(1).lower()
            hour_word = match.group(2).lower()
            minute = WORD_TO_NUM.get(minute_word, 0)
            hour = WORD_TO_NUM.get(hour_word, 0)

            if 1 <= hour <= 12 and 0 <= minute <= 59:
                time_key = f"{hour:02d}:{minute:02d}"
                results[time_key].append({
                    "quote": sentence.strip(),
                    "title": title,
                    "author": author
                })

        # 패턴 8: "X minutes to Y" - Y시 X분 전
        pattern8 = re.finditer(
            r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine)\s+minutes?\s+to\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern8:
            minute_word = match.group(1).lower()
            hour_word = match.group(2).lower()
            minute_before = WORD_TO_NUM.get(minute_word, 0)
            hour = WORD_TO_NUM.get(hour_word, 0)

            if 1 <= hour <= 12 and 1 <= minute_before <= 59:
                # X분 전 = 60 - X분
                minute = 60 - minute_before
                hour = hour - 1
                if hour < 1:
                    hour = 12
                time_key = f"{hour:02d}:{minute:02d}"
                results[time_key].append({
                    "quote": sentence.strip(),
                    "title": title,
                    "author": author
                })

        # 패턴 9: "five past nine" - X past Y (minutes 생략)
        pattern9 = re.finditer(
            r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-five|thirty|thirty-five|forty|forty-five|fifty|fifty-five)\s+past\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern9:
            minute_word = match.group(1).lower()
            hour_word = match.group(2).lower()
            minute = WORD_TO_NUM.get(minute_word, 0)
            hour = WORD_TO_NUM.get(hour_word, 0)

            if 1 <= hour <= 12 and 0 < minute <= 59:
                time_key = f"{hour:02d}:{minute:02d}"
                results[time_key].append({
                    "quote": sentence.strip(),
                    "title": title,
                    "author": author
                })

        # 패턴 10: "twenty to eight" - X to Y (minutes 생략)
        pattern10 = re.finditer(
            r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-five|thirty|thirty-five|forty|forty-five|fifty|fifty-five)\s+to\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern10:
            minute_word = match.group(1).lower()
            hour_word = match.group(2).lower()
            minute_before = WORD_TO_NUM.get(minute_word, 0)
            hour = WORD_TO_NUM.get(hour_word, 0)

            if 1 <= hour <= 12 and 1 <= minute_before <= 59:
                minute = 60 - minute_before
                hour = hour - 1
                if hour < 1:
                    hour = 12
                time_key = f"{hour:02d}:{minute:02d}"
                results[time_key].append({
                    "quote": sentence.strip(),
                    "title": title,
                    "author": author
                })

        # 패턴 11: "3 twenty", "four thirty" - 시간 + 분 (단어 조합)
        pattern11 = re.finditer(
            r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+(oh-)?(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine)\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern11:
            hour_word = match.group(1).lower()
            minute_word = match.group(3).lower()
            hour = WORD_TO_NUM.get(hour_word, 0)
            minute = WORD_TO_NUM.get(minute_word, 0)

            if 1 <= hour <= 12 and 0 <= minute <= 59:
                time_key = f"{hour:02d}:{minute:02d}"
                results[time_key].append({
                    "quote": sentence.strip(),
                    "title": title,
                    "author": author
                })

        # 패턴 12: 숫자로 된 "3 20", "4 30" 형식 (추가 검증 포함)
        pattern12 = re.finditer(
            r'\b(\d{1,2})\s+(\d{2})\b',
            sentence,
            re.IGNORECASE
        )
        for match in pattern12:
            hour = int(match.group(1))
            minute = int(match.group(2))

            # 시간 범위 체크: 문맥상 시간일 가능성이 높은 경우만
            if 1 <= hour <= 12 and 0 <= minute <= 59:
                # 주변 문맥에 시간 관련 단어가 있는지 확인
                context = sentence[max(0, match.start()-20):min(len(sentence), match.end()+20)]
                if re.search(r'\b(at|clock|time|hour|morning|afternoon|evening|night|am|pm|a\.m\.|p\.m\.)\b', context, re.IGNORECASE):
                    time_key = f"{hour:02d}:{minute:02d}"
                    results[time_key].append({
                        "quote": sentence.strip(),
                        "title": title,
                        "author": author
                    })

    return results

def process_books(books_dir="books", metadata_file="books_metadata.json"):
    """모든 책을 처리하고 시간 문장을 추출합니다."""
    # 메타데이터 로드
    with open(metadata_file, 'r', encoding='utf-8') as f:
        books_metadata = json.load(f)

    # 메타데이터를 ID로 매핑
    metadata_map = {book["id"]: book for book in books_metadata}

    all_times = defaultdict(list)
    processed_count = 0

    # 모든 텍스트 파일 처리
    for filename in os.listdir(books_dir):
        if not filename.endswith('.txt'):
            continue

        book_id = int(filename.replace('.txt', ''))
        filepath = os.path.join(books_dir, filename)

        # 메타데이터 가져오기
        metadata = metadata_map.get(book_id)
        if not metadata:
            print(f"⚠ No metadata for book ID {book_id}, skipping...")
            continue

        title = metadata["title"]
        author = metadata["author"]

        print(f"Processing: {title} by {author}...")

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()

            # 구텐베르크 헤더/푸터 제거 (일반적으로 *** START/END 사이에 본문)
            start_match = re.search(r'\*\*\* START OF (THIS|THE) PROJECT GUTENBERG', text, re.IGNORECASE)
            end_match = re.search(r'\*\*\* END OF (THIS|THE) PROJECT GUTENBERG', text, re.IGNORECASE)

            if start_match and end_match:
                text = text[start_match.end():end_match.start()]

            # 시간 패턴 추출
            time_results = extract_time_patterns(text, title, author)

            # 결과 합치기
            for time_key, quotes in time_results.items():
                all_times[time_key].extend(quotes)

            print(f"  ✓ Found {sum(len(q) for q in time_results.values())} time references")
            processed_count += 1

        except Exception as e:
            print(f"  ✗ Error processing {filename}: {str(e)}")

    return all_times, processed_count

def main():
    """메인 함수"""
    print("=" * 60)
    print("문학 작품에서 시간 문장 추출")
    print("=" * 60)
    print()

    # 책 처리
    all_times, processed_count = process_books()

    # 결과 저장
    output_file = "../public/times.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 딕셔너리를 일반 dict로 변환 (JSON 직렬화를 위해)
    output_data = dict(all_times)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 60)
    print(f"처리 완료:")
    print(f"  - 처리한 책: {processed_count}개")
    print(f"  - 추출한 시간: {len(output_data)}개")
    print(f"  - 총 문장 수: {sum(len(quotes) for quotes in output_data.values())}개")
    print(f"  - 저장 위치: {output_file}")
    print("=" * 60)

    # 통계 출력
    print("\n시간대별 문장 수 (상위 10개):")
    sorted_times = sorted(output_data.items(), key=lambda x: len(x[1]), reverse=True)
    for time_key, quotes in sorted_times[:10]:
        print(f"  {time_key}: {len(quotes)}개 문장")

if __name__ == "__main__":
    main()
