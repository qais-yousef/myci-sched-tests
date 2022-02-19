def call(target, workload) {
	sh """
		plotting/plot_wa_power.py ${target} ${workload} > power.txt
	"""
}
