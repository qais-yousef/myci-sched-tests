def call() {
	sh """
		bonnie++ &> result.txt
	"""
}
