from dataclasses import dataclass

@dataclass
class DiagnosticsStatistics:
    total_logs_processed: int = 0
    total_errors_logged: int = 0
    total_reports_generated: int = 0
    total_searches_performed: int = 0
