def call(target, workload, metrics='') {
	sh """
		flock /tmp/perfetto.lock plotting/plot_wa_results.py ${target} ${workload} ${metrics}
	"""
}
