def call() {
	sh """
		tools/plot_rt_app.py > results.txt
	"""
}
