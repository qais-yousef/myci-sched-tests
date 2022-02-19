def call(target, workload) {
	sh """
		plotting/plot_wa_results.py ${target} ${workload} > results.txt
	"""
}
