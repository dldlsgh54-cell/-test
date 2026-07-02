# Documentary Project

다큐 롱폼 16:9와 다큐 숏츠 6개 9:16 제작용 템플릿입니다.

씬 블록은 `templates/scene_block.md` 형식을 기본으로 사용합니다.

중복 정리:
- `IMAGE=AUTO`, `BGM=AUTO`, `CAMERA=AUTO`, `TRANSITION=AUTO`, `COLOR=AUTO`, `SFX=AUTO`, `SUBTITLE=AUTO`는 GPT 판단 필드입니다.
- 실제 파일 입력은 앱의 이미지, BGM, 효과음 폴더를 우선 사용합니다.
- 씬 블록의 AUTO 값은 선택, 배치, 효과 지시로만 사용합니다.

프로젝트 구조:

```text
Project/
├─ project.was
├─ Assets/
│  ├─ 모든 이미지 파일
│  └─ Asset_Index.json
├─ BGM/
├─ Audio/
└─ Output/
```

자산 선택 규칙:
- `IMAGE=AUTO`: `Asset_Index.json`에서 `type=AI`, `usable=true`인 항목만 검색하고 대본과 가장 맞는 AI 이미지를 자동 선택합니다.
- `INFOGRAPHIC=희토류 공급망`: `Asset_Index.json`에서 `type=VS`, `usable=true`, `title=희토류 공급망`에 맞는 시각화 이미지를 삽입합니다.
- `AI`는 장면용 이미지입니다.
- `VS`는 인포그래픽, 도표, 지도, 공급망 그래픽처럼 정확한 정보 시각화 이미지입니다.
