def call(condition=true) {
	if (condition) {
		sh """
			flock /tmp/perfetto.lock plotting/plot_rq_pressure.py
		"""
	}
}
