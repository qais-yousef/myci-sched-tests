def call(target, workload) {
	sh """
		tools/plot_wa_results.py ${target} ${workload} > results.txt
	"""
}
