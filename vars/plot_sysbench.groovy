def call() {
	sh """
		tools/plot_sysbench.py > results.txt
	"""
}
