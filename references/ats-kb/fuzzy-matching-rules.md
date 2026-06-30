# Fuzzy Matching Rules

ATS eşleştirme katmanında bazı varyasyonlar anlamlı kabul edilebilir:

## Kabul Edilebilir Varyasyonlar
- `React.js` ↔ `React`
- `machine learning` ↔ `ML`
- `artificial intelligence` ↔ `AI`
- `CI/CD` ↔ `CI CD`
- Noktalama / slash farkları (`Node.js`, `NodeJS`)

## Dikkat
- Kısa kısaltmalar bağlam dışı false positive üretebilir.
- Fuzzy eşleşme, **gerçek deneyim kanıtının yerine geçmez**; sadece varyasyon toleransı sağlar.

`fuzzy_keyword_matcher.py` bu kuralları normalize edilmiş substring, initialism ve sequence similarity sinyalleriyle uygular.
