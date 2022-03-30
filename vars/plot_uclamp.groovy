def call(condition=true, threads="") {
	if (condition) {
		sh """
			plotting/plot_uclamp.py "${threads}"
		"""
	}
}
