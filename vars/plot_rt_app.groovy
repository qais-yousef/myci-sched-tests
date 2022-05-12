def call() {
	sh """
		pflock /tmp/perfetto.lock lotting/plot_rt_app.py
	"""
}
