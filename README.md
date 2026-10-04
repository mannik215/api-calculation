## Security (DevSecOps)

| Этап | Инструмент | Тип анализа | Политика |
|---|---|---|---|
| Test | pytest | функциональные тесты | блокирует |
| Security - Semgrep | Semgrep CE | SAST, исходный код | блокирует |
| Security - Dependency Audit | pip-audit | SCA, CVE в зависимостях | блокирует |
| Security - Trivy Gate | Trivy | CVE в Docker image | HIGH/CRITICAL fixable → блокирует |
| Security - Trivy Report | Trivy | JSON-отчёт | артефакт |

Security pipeline:
Test → Semgrep → pip-audit → Version → Build → Trivy → Deploy → Verify