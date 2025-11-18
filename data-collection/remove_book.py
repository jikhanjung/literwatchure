#!/usr/bin/env python3
"""
특정 책의 인용구를 times.json에서 제거하는 스크립트
"""
import json

def remove_book_from_times(book_title):
    """times.json에서 특정 책의 인용구를 제거"""

    # times.json 읽기
    with open('../public/times.json', 'r', encoding='utf-8') as f:
        times_data = json.load(f)

    removed_count = 0

    # 각 시간대별로 처리
    for time_key in times_data:
        original_count = len(times_data[time_key])
        # 해당 책이 아닌 인용구만 유지
        times_data[time_key] = [
            quote for quote in times_data[time_key]
            if quote.get('title') != book_title
        ]
        removed_count += original_count - len(times_data[time_key])

    # 빈 시간대 제거
    times_data = {k: v for k, v in times_data.items() if v}

    # times.json 저장
    with open('../public/times.json', 'w', encoding='utf-8') as f:
        json.dump(times_data, f, ensure_ascii=False, indent=2)

    print(f"✅ '{book_title}' 제거 완료")
    print(f"   제거된 인용구 수: {removed_count}개")

    return removed_count

if __name__ == '__main__':
    remove_book_from_times("Email 101")
