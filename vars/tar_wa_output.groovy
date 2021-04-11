def call() {
	sh """
		tar cJf wa_output.tar.xz wa_output
	"""
}
