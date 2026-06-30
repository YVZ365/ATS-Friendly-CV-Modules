# R4 — ATS Parser Alan Haritası

OpenCATS benzeri klasik ATS/CRM sistemlerinde CV parser'ların odaklandığı temel alanlar şunlardır:

## Çekirdek Alanlar
- `firstName`
- `lastName`
- `phone`
- `email`
- `address` / `city`
- `summary`
- `workHistory`
- `education`
- `skills`

## Format Gereksinimleri
- Tek sütun tercih edilir.
- İletişim bilgileri belge üst kısmında düz metin olmalıdır.
- Tarih aralıkları tutarlı yazılmalıdır (`2019-2023`, `Jan 2022 - Present` gibi).
- Skills bölümü düz liste veya kısa satırlar halinde verilmelidir.

## Haritalama Notu
Bu repo için `contact_info_extractor.py`, `experience_year_extractor.py` ve `section_strength_scorer.py` birlikte kullanıldığında parser'ın okuyacağı çekirdek alanların büyük kısmı ön-denetlenebilir.
