def call(target, workload) {
	sh """
		tools/plot_wa_power.py ${target} ${workload} > power.txt
	"""
}
