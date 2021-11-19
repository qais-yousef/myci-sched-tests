def call() {
	sh """
		kill -TERM `cat perfetto.pid`
	"""
}
