class StartupValidator:
    def __init__(self):
        pass

    def validate_boot(self, sequence, stats, health):
        # A fully successful boot requires all subsystems to start
        if stats.subsystems_failed > 0:
            health.mark_failure(f"{stats.subsystems_failed} subsystems failed to start.")
            return False

        if stats.subsystems_started != len(sequence):
            health.mark_failure("Not all subsystems completed startup.")
            return False

        health.mark_booted()
        return True
