# 📚 StudyHub (학습 시간 기록 및 통계 커뮤니티 플랫폼)

> **개인 학습 통계 시각화 및 동기부여를 위한 소셜 러닝 웹 서비스**  
> Django의 MTV 패턴 기반 풀스택 아키텍처로 개발되었으며, 대용량 데이터 조회 시의 쿼리 최적화(N+1 문제 해결)와 엄격한 인가(Authorization) 보안 설계를 적용한 프로젝트입니다.

---**Live Demo**: [https://studyhub-9r50.onrender.com](https://studyhub-9r50.onrender.com)

## 📌 1. 프로젝트 개요 (Overview)

* **개발 기간**: 2026.08
* **주요 목표**:
  * 매일의 학습 과목, 소요 시간, 회고 메모를 기록하고 주간/과목별 통계를 시각화
  * 타 학습자와의 공개 피드 공유 및 실시간 응원(좋아요) 인터랙션 제공
  * 공공/엔터프라이즈 시스템 기준의 **보안 무결성(접근 제어) 및 DB 조회 성능 최적화** 달성

---

## 🛠 2. 기술 스택 (Tech Stack)

* **Backend**: Python 3.13, Django 6.0
* **Frontend**: HTML5, Bootstrap 5, Chart.js (CDN)
* **Database**: SQLite3 (개발 및 로컬 검증)
* **VCS / Tools**: Git, GitHub, VS Code

---

## 🏛 3. 시스템 아키텍처 & DB 설계 (ERD)

### 🗄 Entity Relationship Diagram

```text
+------------------+         1 : 1         +------------------+
|   auth_user      |-----------------------|   UserProfile    |
| (Django Auth)    |                       | - bio (한줄 소개)|
+------------------+                       +------------------+
        |
        | 1 : N
        |
+------------------+         M : N         +------------------+
|   StudyRecord    |-----------------------|   auth_user      |
| - subject (과목) |                       | (Record Likes)   |
| - duration_min   |                       +------------------+
| - memo (회고)    |
| - is_public (공개)
| - created_at     |
+------------------+