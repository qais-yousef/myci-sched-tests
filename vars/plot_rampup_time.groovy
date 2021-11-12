def call() {
	sh """
		tools/plot_rampup_time.py > results.txt
	"""
}
