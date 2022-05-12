def call() {
	sh """
		flock /tmp/perfetto.lock plotting/plot_frequency.py
	"""
}
