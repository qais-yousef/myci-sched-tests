def call(agenda) {
	sh """
		wa run ${agenda}
	"""
}
