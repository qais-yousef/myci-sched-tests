def call(condition=true, threads="") {
	if (condition) {
		sh """
			flock /tmp/perfetto.lock plotting/plot_uclamp.py "${threads}"
		"""
	}
}
