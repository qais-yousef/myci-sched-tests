def call(condition=true, threads="") {
	if (condition) {
		sh """
			plotting/plot_pelt.py "${threads}"
		"""
	}
}
