def call() {
	sh """
		flock /tmp/perfetto.lock plotting/plot_rt_app.py
	"""
}
