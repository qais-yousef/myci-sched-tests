def call() {
	sh """
		plotting/plot_sysbench.py > results.txt
	"""
}
