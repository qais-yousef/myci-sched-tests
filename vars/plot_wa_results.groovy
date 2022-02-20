def call(target, workload, metrics='') {
	sh """
		plotting/plot_wa_results.py ${target} ${workload} ${metrics}
	"""
}
